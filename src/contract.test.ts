import { readFileSync } from 'node:fs';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { loadSnapshot, parseSnapshot } from './api';

const fixture = JSON.parse(readFileSync('.cache/fixture-snapshot.json', 'utf8'));

afterEach(() => vi.unstubAllGlobals());

describe('canonical Python snapshot in the browser', () => {
  it('accepts the exported fixture, preserving unknown and stale evidence', () => {
    const snapshot = parseSnapshot(fixture);
    expect(snapshot.layers).toHaveLength(2);
    expect(snapshot.layers[0].features[0].availability).toBe('stale');
    expect(snapshot.layers[0].features[1].value).toBeNull();
    expect(snapshot.layers[1].features[0].drinking_water).toBe('unknown');
    expect(snapshot.layers.flatMap((layer) => layer.features).every((feature) => feature.provenance.fixture)).toBe(true);
  });

  it.each([
    { generated_at: 'not-a-time', layers: [] },
    { ...fixture, layers: [{ ...fixture.layers[0], availability: 'safe' }] },
    { ...fixture, unexpected: true },
    { ...fixture, layers: [{ ...fixture.layers[0], features: [{ ...fixture.layers[0].features[0], geometry: { type: 'Point', coordinates: [181, 47] } }] }] },
  ])('rejects contract drift before rendering', (invalid) => {
    expect(() => parseSnapshot(invalid)).toThrow('contract');
  });

  it('round trips the API response through runtime validation', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify(fixture))));
    expect((await loadSnapshot()).layers).toHaveLength(2);
  });

  it('propagates API failure so the screen can show missing layers', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('', { status: 503 })));
    await expect(loadSnapshot()).rejects.toThrow('unavailable');
  });
});
