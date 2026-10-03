import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';

// Verify T2's arithmetic and acceptance examples. T5 owns the production evaluator.
const scenarioPath = new URL('../data/scenarios.json', import.meta.url);
const fixture = JSON.parse(readFileSync(scenarioPath, 'utf8'));
const rules = fixture.rules;
const criteria = ['shade', 'duration', 'water'];
const clamp = (value) => Math.max(0, Math.min(1, value));
const finite = (value) => typeof value === 'number' && Number.isFinite(value);

function expandRoutes(example) {
  return fixture.base_routes.map((base) => {
    const patch = example.route_patches[base.id] ?? {};
    return { ...base, ...patch, water: { ...base.water, ...patch.water } };
  });
}

function accessStatus(route) {
  const lengths = ['distance_metres', 'shaded_metres', 'unshaded_metres', 'unknown_metres'];
  if (lengths.some((name) => !finite(route[name]) || route[name] < 0)
      || route.distance_metres === 0
      || !finite(route.planned_stop_minutes) || route.planned_stop_minutes < 0
      || Math.abs(route.shaded_metres + route.unshaded_metres + route.unknown_metres
        - route.distance_metres) > rules.arithmetic_tolerance) return 'invalid_data';
  if (route.access_state === 'confirmed_blocked') return 'blocked';
  if (route.access_state !== 'checked_open') return 'needs_verification';
  if (route.inside_calculation_coverage !== true) return 'unsupported';
  return 'eligible';
}

function waterEvidence(route) {
  const water = route.water;
  const fresh = finite(water.age_hours) && water.age_hours >= 0
    && water.age_hours <= rules.water_evidence_max_age_hours;
  if (!fresh || water.evidence_complete !== true) return { complete: false, benefit: 0 };
  if (water.state === 'fresh_absent') return { complete: true, benefit: 0 };
  const flags = ['drinking', 'accessible', 'operational'];
  if (water.state !== 'fresh_available'
      || flags.some((name) => typeof water[name] !== 'boolean')
      || !finite(water.extra_distance_metres) || water.extra_distance_metres < 0
      || water.extra_distance_included !== true) return { complete: false, benefit: 0 };
  const qualifies = flags.every((name) => water[name])
    && water.extra_distance_metres <= rules.water_max_extra_distance_metres;
  return { complete: true, benefit: qualifies ? 1 : 0 };
}

function routeMetrics(route, baseline) {
  const walkingMinutes = route.distance_metres / rules.walking_speed_m_per_s / 60;
  const durationMinutes = walkingMinutes + route.planned_stop_minutes;
  const shadeCurrent = route.shade_state === 'current'
    && route.shade_time_matches_request === true
    && route.shade_geometry_matches_request === true;
  const water = waterEvidence(route);
  const [minimumMinutes, maximumMinutes] = rules.duration_benefit_range_minutes;
  return {
    walking_minutes: walkingMinutes,
    duration_minutes: durationMinutes,
    shade_fraction: route.shaded_metres / route.distance_metres,
    unshaded_fraction: route.unshaded_metres / route.distance_metres,
    unknown_fraction: route.unknown_metres / route.distance_metres,
    known_shade_fraction: (route.shaded_metres + route.unshaded_metres) / route.distance_metres,
    shade_complete: shadeCurrent && (route.shaded_metres + route.unshaded_metres)
      / route.distance_metres + rules.arithmetic_tolerance >= rules.minimum_known_shade_fraction,
    water_complete: water.complete,
    benefits: {
      shade: shadeCurrent ? route.shaded_metres / route.distance_metres : 0,
      duration: clamp(1 - (durationMinutes - minimumMinutes) / (maximumMinutes - minimumMinutes)),
      water: water.benefit
    },
    extra_metres: Math.max(0, route.distance_metres - baseline.distance_metres),
    extra_minutes: Math.max(0, durationMinutes - baseline.duration_minutes),
    extra_distance_fraction: Math.max(0, route.distance_metres / baseline.distance_metres - 1)
  };
}

function evaluate(example) {
  const routes = expandRoutes(example);
  const weights = example.weights ?? rules.default_weights;
  const result = { status: null, winner: null, route_statuses: {}, scores: {}, metrics: {}, contributions: {} };
  for (const route of routes) result.route_statuses[route.id] = accessStatus(route);
  const candidates = routes.filter((route) => result.route_statuses[route.id] === 'eligible');
  if (Object.keys(weights).length !== criteria.length
      || criteria.some((name) => !finite(weights[name]) || weights[name] < 0)) {
    result.status = 'invalid_preferences';
    return result;
  }
  if (!candidates.length) {
    result.status = 'no_eligible_routes';
    return result;
  }
  const shortest = candidates.reduce((a, b) => {
    if (a.distance_metres !== b.distance_metres) return a.distance_metres < b.distance_metres ? a : b;
    return a.planned_stop_minutes <= b.planned_stop_minutes ? a : b;
  });
  const baseline = { ...shortest, duration_minutes: shortest.distance_metres / rules.walking_speed_m_per_s / 60 + shortest.planned_stop_minutes };
  for (const route of candidates) {
    const metrics = routeMetrics(route, baseline);
    result.metrics[route.id] = metrics;
    if (metrics.extra_distance_fraction > rules.max_extra_distance_fraction + rules.arithmetic_tolerance
        || metrics.extra_minutes > rules.max_extra_duration_minutes + rules.arithmetic_tolerance) {
      result.route_statuses[route.id] = 'detour_limit';
    }
  }
  const eligible = candidates.filter((route) => result.route_statuses[route.id] === 'eligible');
  const sum = criteria.reduce((total, name) => total + weights[name], 0);
  if (!finite(sum)) {
    result.status = 'invalid_preferences';
    return result;
  }
  for (const route of eligible) {
    result.contributions[route.id] = {};
    result.scores[route.id] = 0;
    for (const name of criteria) {
      const contribution = sum === 0 ? 0 : weights[name] / sum * result.metrics[route.id].benefits[name];
      result.contributions[route.id][name] = contribution;
      result.scores[route.id] += contribution;
    }
  }
  if (!eligible.length) result.status = 'no_eligible_routes';
  else if (sum === 0) result.status = 'no_preferences';
  else if (eligible.some((route) => (weights.shade > 0 && !result.metrics[route.id].shade_complete)
      || (weights.water > 0 && !result.metrics[route.id].water_complete))) result.status = 'insufficient_evidence';
  else {
    const highest = Math.max(...Object.values(result.scores));
    const winners = eligible.filter((route) => highest - result.scores[route.id] <= rules.tie_tolerance);
    result.status = winners.length > 1 ? 'tie' : 'recommended';
    if (winners.length === 1) result.winner = winners[0].id;
  }
  return result;
}

function checkNumbers(actual, expected, label) {
  for (const [key, value] of Object.entries(expected)) {
    if (value !== null && typeof value === 'object') checkNumbers(actual[key], value, label + '.' + key);
    else assert.ok(finite(actual[key]) && Math.abs(actual[key] - value) <= rules.arithmetic_tolerance,
      label + '.' + key + ': expected ' + value + ', got ' + actual[key]);
  }
}

assert.equal(fixture.format_version, 1);
assert.ok(rules.walking_speed_m_per_s > 0);
assert.ok(rules.duration_benefit_range_minutes[1] > rules.duration_benefit_range_minutes[0]);
assert.deepEqual(rules.shade_benefit_range_fraction, [0, 1]);
assert.deepEqual(rules.water_benefit_range, [0, 1]);
assert.ok(rules.minimum_known_shade_fraction >= 0 && rules.minimum_known_shade_fraction <= 1);
assert.equal(new Set(fixture.cases.map((example) => example.id)).size, fixture.cases.length);
for (const example of fixture.cases) {
  assert.equal(example.evidence, 'synthetic');
  const actual = evaluate(example);
  const expected = example.expected;
  assert.equal(actual.status, expected.status, example.id + ' status');
  assert.equal(actual.winner, expected.winner, example.id + ' winner');
  assert.deepEqual(actual.route_statuses, expected.route_statuses, example.id + ' eligibility');
  assert.deepEqual(Object.keys(actual.scores).sort(), Object.keys(expected.scores).sort(), example.id + ' scored routes');
  checkNumbers(actual.scores, expected.scores, example.id + '.scores');
  if (expected.metrics) checkNumbers(actual.metrics, expected.metrics, example.id + '.metrics');
  if (expected.contributions) checkNumbers(actual.contributions, expected.contributions, example.id + '.contributions');
  if (expected.detour) checkNumbers(actual.metrics, expected.detour, example.id + '.detour');
  fixture.base_routes.reverse();
  const reversed = evaluate(example);
  fixture.base_routes.reverse();
  assert.equal(reversed.status, actual.status, example.id + ' route order status');
  assert.equal(reversed.winner, actual.winner, example.id + ' route order winner');
  assert.deepEqual(reversed.route_statuses, actual.route_statuses, example.id + ' route order eligibility');
  assert.deepEqual(reversed.scores, actual.scores, example.id + ' route order scores');
}
const formatted = JSON.stringify(fixture, null, 2) + '\n';
if (process.argv.includes('--format')) writeFileSync(scenarioPath, formatted);
else assert.equal(readFileSync(scenarioPath, 'utf8').replaceAll('\r\n', '\n'), formatted, 'JSON formatting; run with --format');
console.log('T2: ' + fixture.cases.length + ' acceptance examples passed; JSON formatting checked.');
