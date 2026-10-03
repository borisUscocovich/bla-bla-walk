"""Render native geometry against the actual OpenLayers Basel basemap locally."""

import argparse
import json
import math
import shutil
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import (
    Resampling,
    calculate_default_transform,
    reproject,
    transform,
    transform_geom,
)

from bla_bla_walk.geometry_rasters import valid_cells

PALETTE = np.array(
    [
        [130, 130, 130],
        [232, 244, 244],
        [175, 214, 210],
        [111, 175, 173],
        [52, 132, 136],
        [22, 92, 108],
        [8, 60, 85],
    ],
    dtype="uint8",
)


def preview_raster(root: Path, tile: str, directory: Path) -> list[float]:
    """Reproject native relative-height evidence for display only, not calculation."""
    east, north = map(int, tile.split("-"))
    bounds = [east * 1000, north * 1000, (east + 1) * 1000, (north + 1) * 1000]
    s = np.load(root / "arrays" / f"{tile}-surface.npy", allow_pickle=False)
    t = np.load(root / "arrays" / f"{tile}-terrain.npy", allow_pickle=False)
    valid = valid_cells(s) & valid_cells(t)
    relative = s - t
    relative[~valid] = -9999
    src_transform = from_origin(bounds[0], bounds[3], 0.5, 0.5)
    dst_transform, width, height = calculate_default_transform(
        "EPSG:2056", "EPSG:3857", 2000, 2000, *bounds, resolution=2
    )
    warped = np.full((height, width), -9999, dtype="float32")
    reproject(
        relative,
        warped,
        src_transform=src_transform,
        src_crs="EPSG:2056",
        dst_transform=dst_transform,
        dst_crs="EPSG:3857",
        src_nodata=-9999,
        dst_nodata=-9999,
        resampling=Resampling.nearest,
    )
    colours = PALETTE[np.clip(np.digitize(warped, [0, 1, 3, 10, 30, 80]), 0, 6)]
    image = np.concatenate(
        (colours, np.where(valid_cells(warped), 255, 0).astype("uint8")[..., None]),
        axis=2,
    )
    with rasterio.open(
        directory / f"{tile}.png",
        "w",
        driver="PNG",
        count=4,
        dtype="uint8",
        width=width,
        height=height,
    ) as out:
        out.write(np.moveaxis(image, 2, 0))
    return [
        dst_transform.c,
        dst_transform.f + dst_transform.e * height,
        dst_transform.c + dst_transform.a * width,
        dst_transform.f,
    ]


def render_preview(root: Path, inventory: dict, directory: Path) -> dict:
    """Build a local review page with centre/boundary pixel-centre references."""
    directory.mkdir(parents=True, exist_ok=True)
    # Centre: the same location used by the T1 map. Boundary: pinned western vertex.
    x, y = transform("EPSG:4326", "EPSG:2056", [7.5886], [47.5596])
    boundary = inventory["boundary"]["geometry"]["coordinates"][0][0][0]
    references = [
        {"id": "centre", "point_epsg2056": [x[0], y[0]], "wgs84": [7.5886, 47.5596]},
        {"id": "boundary", "point_epsg2056": boundary[:2]},
    ]
    for ref in references:
        east, north = ref["point_epsg2056"]
        tile = f"{int(east // 1000)}-{int(north // 1000)}"
        ref["tile"] = tile
        ref["image_extent_3857"] = preview_raster(root, tile, directory)
        row = int(((int(north // 1000) + 1) * 1000 - north) / 0.5)
        col = int((east - int(east // 1000) * 1000) / 0.5)
        pixel = [
            int(east // 1000) * 1000 + (col + 0.5) * 0.5,
            (int(north // 1000) + 1) * 1000 - (row + 0.5) * 0.5,
        ]
        ref["native_pixel_row_column"] = [row, col]
        ref["point_to_native_centre_m"] = math.dist([east, north], pixel)
        xx, yy = transform(
            "EPSG:2056", "EPSG:3857", [east, pixel[0]], [north, pixel[1]]
        )
        ref["point_3857"] = [xx[0], yy[0]]
        ref["pixel_centre_3857"] = [xx[1], yy[1]]
        lon, lat = transform("EPSG:2056", "EPSG:4326", [east], [north])
        ref["wgs84"] = [lon[0], lat[0]]
    boundary_3857 = transform_geom(
        "EPSG:2056", "EPSG:3857", inventory["boundary"]["geometry"]
    )
    # Copy the existing checksum-pinned browser assets; no new browser dependency.
    shutil.copyfile(Path(".cache/browser-assets/ol.js"), directory / "ol.js")
    shutil.copyfile(Path(".cache/browser-assets/ol.css"), directory / "ol.css")
    payload = {"references": references, "boundary": boundary_3857}
    (directory / "alignment.json").write_text(json.dumps(payload, indent=2) + "\n")
    (directory / "index.html").write_text(_html(payload))
    return payload


def _html(payload):
    return (
        """<!doctype html><html lang="en"><meta charset="utf-8">
<title>T8 native geometry alignment</title><link rel="stylesheet" href="ol.css">
<style>body{font:16px sans-serif;margin:20px}section{display:inline-block;width:48%}
.map{height:620px}button{padding:8px}#status{white-space:pre-wrap}</style>
<h1>T8 geometry alignment</h1><p>Native surface minus terrain, display reprojected.
Grey: negative differences. Teal: increasing relative height. This is not shade.
© swisstopo · Basemap: Geodaten Kanton Basel-Stadt, CC BY 4.0.</p>
<button id="toggle">Toggle geometry overlay</button><p id="status"></p>
<section><h2>Centre</h2><div class="map" id="centre"></div></section>
<section><h2>Canton boundary</h2><div class="map" id="boundary"></div></section>
<script src="ol.js"></script><script>
const evidence = """
        + json.dumps(payload)
        + """;
window.maps = []; window.overlayLayers = []; window.loadedBasemapTiles = 0;
for (const ref of evidence.references) {
 const basemap = new ol.source.XYZ({
 url:'https://wmts.geo.bs.ch/mapcache/wmts/1.0.0/'+
 'VS_Vektorstadtplan_grau/default/3857/{z}/{y}/{x}.png',
 maxZoom:17,crossOrigin:'anonymous'});
 basemap.on('tileloadend',()=>{window.loadedBasemapTiles++});
 const overlay = new ol.layer.Image({opacity:0.6,
 source:new ol.source.ImageStatic({url:ref.tile+'.png',
 imageExtent:ref.image_extent_3857,projection:'EPSG:3857'})});
 window.overlayLayers.push(overlay);
 const point = new ol.Feature(new ol.geom.Point(ref.point_3857));
 const centre = new ol.Feature(new ol.geom.Point(ref.pixel_centre_3857));
 point.setStyle(new ol.style.Style({image:new ol.style.Circle({radius:9,
 stroke:new ol.style.Stroke({color:'#a00',width:2})})}));
 centre.setStyle(new ol.style.Style({image:new ol.style.Circle({radius:3,
 fill:new ol.style.Fill({color:'#000'})})}));
 const boundary = new ol.format.GeoJSON().readGeometry(evidence.boundary,
 {dataProjection:'EPSG:3857',featureProjection:'EPSG:3857'});
 const vector = new ol.layer.Vector({source:new ol.source.Vector({
 features:[new ol.Feature(boundary),point,centre]}),style:new ol.style.Style({
 stroke:new ol.style.Stroke({color:'#a00',width:2})})});
 const map = new ol.Map({target:ref.id,layers:[
 new ol.layer.Tile({source:basemap}),overlay,vector],
 view:new ol.View({center:ref.point_3857,zoom:17,maxZoom:19})});
 window.maps.push(map);
 document.getElementById('status').textContent += ref.id+': '+ref.tile+
 '; reference to native pixel centre '+
 ref.point_to_native_centre_m.toFixed(3)+' m\\n';
}
document.getElementById('toggle').onclick=()=>{window.overlayLayers.forEach(l=>l.setVisible(!l.getVisible()))};
</script></html>"""
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/geometry"))
    parser.add_argument("--output", type=Path, default=Path(".hack/t8/alignment"))
    args = parser.parse_args()
    render_preview(
        args.root, json.loads(Path("data/tile-inventory.json").read_text()), args.output
    )
    print(f"Alignment preview: {args.output / 'index.html'}")


if __name__ == "__main__":
    main()
