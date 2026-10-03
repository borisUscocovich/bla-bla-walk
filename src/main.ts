import 'ol/ol.css';
import './theme.css';
import { loadSnapshot, type MapFeature, type MapLayer } from './api';
import { createMap } from './map';

const app = document.querySelector<HTMLDivElement>('#app')!;
app.innerHTML = `
  <header>
    <div><p class="eyebrow">Bla Bla Walk</p><h1>Explore Basel</h1></div>
    <p>Map foundation · synthetic overlays</p>
  </header>
  <main>
    <aside aria-label="Map layers and feature information">
      <section>
        <h2>Layers</h2>
        <p class="notice">Fixture mode: invented locations and values. Not current conditions.</p>
        <p id="api-status" role="status">Loading fixture API…</p>
        <button id="reload" type="button">Reload layers</button>
        <div id="layers"></div>
      </section>
      <section aria-labelledby="features-title">
        <h2 id="features-title">Inspect a feature</h2>
        <p>Click a marker, or choose a sample below.</p>
        <div id="features"></div>
      </section>
      <section id="details" aria-label="Selected feature" aria-live="polite">
        <p>Select a sample to see its source and timestamps.</p>
      </section>
    </aside>
    <section class="map-panel" aria-label="Basel map">
      <div id="map" tabindex="0" role="region" aria-label="Interactive Basel map. Arrow keys pan; plus and minus zoom."></div>
      <p id="basemap-status" role="status">Loading Basel basemap…</p>
      <p class="map-note">Squares: sample sensors · Circles: sample fountains.<br>Shade, routes and calculation coverage are not connected yet.</p>
    </section>
  </main>`;

const status = document.querySelector<HTMLParagraphElement>('#api-status')!;
const layerControls = document.querySelector<HTMLDivElement>('#layers')!;
const featureList = document.querySelector<HTMLDivElement>('#features')!;
const details = document.querySelector<HTMLElement>('#details')!;
const reload = document.querySelector<HTMLButtonElement>('#reload')!;
const map = createMap(
  document.querySelector<HTMLElement>('#map')!,
  showFeature,
  (message) => {
    document.querySelector('#basemap-status')!.textContent = message;
  },
);

/** Render untrusted feature text as text nodes, including timestamps and gaps. */
function showFeature(feature: MapFeature) {
  details.replaceChildren();
  const title = document.createElement('h2');
  title.textContent = feature.label;
  details.append(title);
  const source = feature.provenance;
  const rows = [
    ['Data mode', source.fixture ? 'Synthetic fixture' : 'Provider data'],
    ['Availability', feature.availability],
    ['Value', feature.value == null ? 'Unknown / no value' : `${feature.value} ${feature.unit ?? ''}`],
    ['Meaning', feature.explanation],
    ['Drinking water', feature.drinking_water ?? 'Not applicable'],
    ['Provider', source.provider],
    ['Attribution', source.attribution],
    ['Licence', source.licence],
    ['Observed', formatTime(source.observed_at)],
    ['Retrieved', formatTime(source.retrieved_at)],
  ];
  const list = document.createElement('dl');
  rows.forEach(([label, value]) => {
    const term = document.createElement('dt');
    term.textContent = label;
    const description = document.createElement('dd');
    description.textContent = value;
    list.append(term, description);
  });
  details.append(list);
  if (source.source_url?.startsWith('https://')) {
    const link = document.createElement('a');
    link.href = source.source_url;
    link.textContent = 'Open source metadata';
    details.append(link);
  }
}

function formatTime(value: string | null | undefined): string {
  return value ? new Date(value).toLocaleString('en-GB', { timeZone: 'UTC' }) + ' UTC' : 'Unknown / not supplied';
}

function renderLayers(layers: MapLayer[]) {
  layerControls.replaceChildren();
  featureList.replaceChildren();
  layers.forEach((layer) => {
    const control = document.createElement('label');
    control.className = 'layer-control';
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = true;
    const text = document.createElement('span');
    const name = document.createElement('strong');
    name.textContent = layer.label;
    const summary = document.createElement('small');
    summary.textContent = `${layer.availability} · ${layer.explanation}`;
    text.append(name, summary);
    control.append(checkbox, text);
    layerControls.append(control);
    const group = document.createElement('div');
    group.className = 'feature-group';
    layer.features.forEach((feature) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = `${feature.label} · ${feature.availability}`;
      button.addEventListener('click', () => {
        showFeature(feature);
        map.focus(feature);
      });
      group.append(button);
    });
    checkbox.addEventListener('change', () => {
      map.setVisible(layer.id, checkbox.checked);
      group.hidden = !checkbox.checked;
      details.textContent = 'Select a visible sample to inspect its source.';
    });
    featureList.append(group);
  });
}

async function refresh() {
  reload.disabled = true;
  status.textContent = 'Loading fixture API…';
  try {
    const snapshot = await loadSnapshot();
    map.replaceLayers(snapshot.layers);
    renderLayers(snapshot.layers);
    details.textContent = 'Select a sample to see its source and timestamps.';
    status.textContent = `Fixture API connected · snapshot ${formatTime(snapshot.generated_at)}`;
  } catch {
    map.replaceLayers([]);
    layerControls.replaceChildren();
    featureList.replaceChildren();
    details.textContent = 'No overlay data available. The basemap can still be used.';
    status.textContent = 'Layers missing: API unavailable or invalid. Start the API, then reload layers.';
  } finally {
    reload.disabled = false;
  }
}

reload.addEventListener('click', () => void refresh());
void refresh();
