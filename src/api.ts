import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import type { components } from './interfaces';
import snapshotSchema from './snapshot.schema.json';

export type MapSnapshot = components['schemas']['MapSnapshot'];
export type MapFeature = components['schemas']['MapFeature'];
export type MapLayer = components['schemas']['MapLayer'];

const ajv = new Ajv2020({ strict: false });
addFormats(ajv);
const isSnapshot = ajv.compile<MapSnapshot>(snapshotSchema);

/** Validate the API boundary using the schema generated from Python models. */
export function parseSnapshot(value: unknown): MapSnapshot {
  if (!isSnapshot(value)) {
    throw new Error('The map API returned data that does not match its contract.');
  }
  return value;
}

/** Fetch one snapshot with bounded waiting; callers show a visible failure. */
export async function loadSnapshot(): Promise<MapSnapshot> {
  const response = await fetch('/api/map', {
    signal: AbortSignal.timeout(10_000),
  });
  if (!response.ok) throw new Error('The map API is unavailable.');
  return parseSnapshot(await response.json());
}
