const {
  Feature,
  Map,
  View
} = window.ol;
const {
  GeoJSON
} = window.ol.format;
const {
  Tile: TileLayer,
  Vector: VectorLayer
} = window.ol.layer;
const {
  fromLonLat,
  transformExtent
} = window.ol.proj;
const {
  Vector: VectorSource,
  XYZ
} = window.ol.source;
const {
  Circle: CircleStyle,
  Fill,
  RegularShape,
  Stroke,
  Style
} = window.ol.style;

// Official 3857 matrix set uses standard XYZ coordinates.
const configResponse = await fetch('/config/basemap.json');
if (!configResponse.ok) throw new Error('Basemap configuration unavailable.');
const basemapConfig = await configResponse.json();
const offline = new URLSearchParams(location.search).get('mode') === 'offline';
const BASEMAP_URL = offline ? '/tiles/{z}/{x}/{y}.png' : basemapConfig.url;
const BASEMAP_EXTENT = basemapConfig.bounds_wgs84;
const BASEL_CENTRE = [7.5886, 47.5596];

/** Build the real basemap; fixture layers can be replaced independently. */
export function createMap(
  target,
  onSelect,
  onBasemapStatus,
) {
  const source = new XYZ({
    url: BASEMAP_URL,
    maxZoom: basemapConfig.max_zoom,
    minZoom: basemapConfig.min_zoom,
    crossOrigin: 'anonymous',
    wrapX: false,
    attributions: '<a href="https://api.geo.bs.ch/stac/v1/collections/VSBS">Geodaten Kanton Basel-Stadt</a> · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>',
  });
  let hadTileError = false;
  source.on('tileloadend', () => {
    if (!hadTileError) onBasemapStatus(offline ? 'Basel basemap loaded · downloaded offline map' : 'Basel basemap loaded · live tile service');
  });
  source.on('tileloaderror', () => {
    hadTileError = true;
    onBasemapStatus(offline ? 'Offline basemap partly unavailable: tiles not downloaded or outside saved coverage.' : 'Basemap partly unavailable. Check your connection and reload.');
  });
  const map = new Map({
    target,
    layers: [
      new TileLayer({
        source,
        extent: transformExtent(BASEMAP_EXTENT, 'EPSG:4326', 'EPSG:3857'),
      }),
    ],
    view: new View({
      center: fromLonLat(BASEL_CENTRE),
      zoom: 14,
      minZoom: basemapConfig.min_zoom,
      maxZoom: basemapConfig.max_zoom,
      extent: offline ? transformExtent(BASEMAP_EXTENT, 'EPSG:4326', 'EPSG:3857') : undefined,
      constrainOnlyCenter: true,
    }),
  });
  const layers = new globalThis.Map();
  map.getControls().forEach((control) => {
    if (control instanceof window.ol.control.Attribution) {
      control.setCollapsible(false);
    }
  });
  const features = new globalThis.Map();
  map.on('singleclick', (event) => {
    map.forEachFeatureAtPixel(event.pixel, (feature) => {
      const selected = features.get(String(feature.getId()));
      if (selected) onSelect(selected);
      return true;
    });
  });

  function replaceLayers(snapshotLayers) {
    layers.forEach((layer) => map.removeLayer(layer));
    layers.clear();
    features.clear();
    const theme = getComputedStyle(document.documentElement);
    snapshotLayers.forEach((layer) => {
      const fill = new Fill({
        color: theme.getPropertyValue(`--${layer.kind}-color`).trim(),
      });
      const stroke = new Stroke({
        color: theme.getPropertyValue('--marker-outline').trim(),
        width: Number(theme.getPropertyValue('--marker-stroke')),
      });
      const radius = Number(theme.getPropertyValue('--marker-radius'));
      const image =
        layer.kind === 'observation' ?
        new RegularShape({
          points: 4,
          radius,
          angle: Math.PI / 4,
          fill,
          stroke
        }) :
        new CircleStyle({
          radius,
          fill,
          stroke
        });
      const vector = new VectorLayer({
        source: new VectorSource({
          features: layer.features.map((feature) => {
            features.set(feature.id, feature);
            const geometry = new GeoJSON().readGeometry(feature.geometry, {
              dataProjection: 'EPSG:4326',
              featureProjection: 'EPSG:3857',
            });
            const marker = new Feature({
              geometry
            });
            marker.setId(feature.id);
            return marker;
          }),
        }),
        style: new Style({
          image,
          stroke,
          fill
        }),
      });
      layers.set(layer.id, vector);
      map.addLayer(vector);
    });
  }

  return {
    replaceLayers,
    setVisible: (id, visible) => layers.get(id)?.setVisible(visible),
    focus: (feature) => {
      const geometry = new GeoJSON().readGeometry(feature.geometry, {
        dataProjection: 'EPSG:4326',
        featureProjection: 'EPSG:3857',
      });
      map.getView().fit(geometry, {
        maxZoom: 16,
        duration: 0,
        padding: Array(4).fill(Number(getComputedStyle(document.documentElement).getPropertyValue("--map-focus-padding")))
      });
    },
  };
}
