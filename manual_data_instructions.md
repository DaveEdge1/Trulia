# Manual Data Download Instructions

If the automated download script doesn't work, you can manually download the data from each source and place it in the appropriate directories.

## Directory Structure

```
Trulia/
├── data/
│   ├── parcels/
│   │   ├── coconino_parcels.geojson
│   │   ├── yavapai_parcels.geojson
│   │   ├── mohave_parcels.geojson
│   │   └── navajo_parcels.geojson
│   └── federal_land/
│       ├── national_forests.geojson
│       └── blm_land.geojson
```

## County Parcel Data

### Coconino County
1. Visit: https://data-coconinocounty.opendata.arcgis.com/
2. Search for "parcels"
3. Click on the Parcels dataset
4. Click "Download" and select "Shapefile" or "GeoJSON"
5. If you downloaded a shapefile (.shp):
   - Use QGIS or similar to convert to GeoJSON
   - Or use: `ogr2ogr -f GeoJSON coconino_parcels.geojson parcels.shp`
6. Save as `data/parcels/coconino_parcels.geojson`

### Yavapai County
1. Visit: https://data-yavgis.opendata.arcgis.com/
2. Search for "parcels"
3. Download the Parcels dataset
4. Convert to GeoJSON if needed
5. Save as `data/parcels/yavapai_parcels.geojson`

### Mohave County
1. Visit: https://az-mohave.opendata.arcgis.com/
2. Search for "parcels"
3. Download the Parcels dataset
4. Convert to GeoJSON if needed
5. Save as `data/parcels/mohave_parcels.geojson`

### Navajo County
1. Visit: https://open-data-ncaz.hub.arcgis.com/datasets/parcels-1
2. Click "Download"
3. Select "GeoJSON" or "Shapefile"
4. Save as `data/parcels/navajo_parcels.geojson`

## Federal Land Boundaries

### National Forest Boundaries
1. Visit: https://data.fs.usda.gov/geodata/edw/datasets.php
2. Search for "National Forest System"
3. Download "S_USA.AdministrativeForest"
4. Convert to GeoJSON:
   ```bash
   ogr2ogr -f GeoJSON national_forests.geojson S_USA.AdministrativeForest.shp
   ```
5. Optionally filter to Arizona only using QGIS or:
   ```bash
   ogr2ogr -f GeoJSON -where "STATE='AZ'" national_forests_az.geojson national_forests.geojson
   ```
6. Save as `data/federal_land/national_forests.geojson`

**Alternative**: Use ArcGIS Online
1. Visit: https://hub.arcgis.com/datasets/3451bcca1dbc45168ed0b3f54c6098d3_0
2. Download as GeoJSON
3. Save to `data/federal_land/national_forests.geojson`

### BLM Land Boundaries
1. Visit: https://gbp-blm-egis.hub.arcgis.com/pages/arizona
2. Search for "Surface Management Agency" or "Administrative Boundaries"
3. Filter to Arizona
4. Download as GeoJSON or Shapefile
5. Save as `data/federal_land/blm_land.geojson`

**Alternative using BLM National Surface Management Agency**:
1. Visit: https://navigator.blm.gov/
2. Search for Arizona BLM lands
3. Export the data
4. Save to `data/federal_land/blm_land.geojson`

## Converting Shapefiles to GeoJSON

If you have GDAL/OGR installed:
```bash
ogr2ogr -f GeoJSON output.geojson input.shp
```

If you have QGIS:
1. Open the shapefile in QGIS
2. Right-click the layer → Export → Save Features As
3. Select GeoJSON format
4. Save with the appropriate filename

If you have Python with GeoPandas:
```python
import geopandas as gpd
gdf = gpd.read_file('input.shp')
gdf.to_file('output.geojson', driver='GeoJSON')
```

## Verifying Your Data

Once you've downloaded and placed all files, run:
```bash
python -c "from pathlib import Path; print('Missing files:', [str(f) for f in [Path('data/parcels/coconino_parcels.geojson'), Path('data/parcels/yavapai_parcels.geojson'), Path('data/parcels/mohave_parcels.geojson'), Path('data/parcels/navajo_parcels.geojson'), Path('data/federal_land/national_forests.geojson'), Path('data/federal_land/blm_land.geojson')] if not f.exists()])"
```

All files should be present before running the analysis.
