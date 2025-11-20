# Quick Start Guide - Finding Parcels Bordering Federal Land

This guide will help you find parcels in Coconino, Yavapai, Mohave, and Navajo counties that border National Forest or BLM land.

## Step 1: Download County Parcel Data

Visit each county's open data portal and download the parcel shapefiles or GeoJSON files:

### Coconino County
1. Visit: https://data-coconinocounty.opendata.arcgis.com/
2. Search for "parcels"
3. Download the parcels dataset as **GeoJSON** or **Shapefile**
4. Save to: `data/parcels/coconino_parcels.geojson` (or .shp)

**Direct link to try**: https://data-coconinocounty.opendata.arcgis.com/search?q=parcels

### Yavapai County
1. Visit: https://data-yavgis.opendata.arcgis.com/
2. Search for "parcels"
3. Click on "Parcels in Yavapai County"
4. Click "Download" → Select "GeoJSON" or "Shapefile"
5. Save to: `data/parcels/yavapai_parcels.geojson` (or .shp)

**Direct link to try**: https://data-yavgis.opendata.arcgis.com/datasets/YavGIS::parcels-in-yavapai-county-1

### Mohave County
1. Visit: https://az-mohave.opendata.arcgis.com/
2. Search for "parcels"
3. Download the parcels dataset
4. Save to: `data/parcels/mohave_parcels.geojson` (or .shp)

**Direct link to try**: https://az-mohave.opendata.arcgis.com/search?q=parcels

### Navajo County
1. Visit: https://open-data-ncaz.hub.arcgis.com/
2. Search for "parcels" or use direct link below
3. Click "Download" → Select "GeoJSON" or "Shapefile"
4. Save to: `data/parcels/navajo_parcels.geojson` (or .shp)

**Direct link**: https://open-data-ncaz.hub.arcgis.com/datasets/parcels-1

## Step 2: Download Federal Land Boundaries

### National Forest Boundaries
**Option A - ArcGIS Hub (Easiest)**:
1. Visit: https://hub.arcgis.com/datasets/esri::usa-forest-service-proclaimed-forests/explore
2. Click "Download" → Select "GeoJSON"
3. Save to: `data/federal_land/national_forests.geojson`

**Option B - USDA Forest Service**:
1. Visit: https://data.fs.usda.gov/geodata/edw/datasets.php
2. Search for "Administrative Forest Boundaries"
3. Download and save to: `data/federal_land/national_forests.geojson`

### BLM Land Boundaries
1. Visit: https://gbp-blm-egis.hub.arcgis.com/pages/arizona
2. Search for "Surface Management Agency" or "Administrative Boundaries"
3. Filter to Arizona and BLM managed lands
4. Download as GeoJSON
5. Save to: `data/federal_land/blm_land.geojson`

**Alternative**: https://navigator.blm.gov/ (BLM Navigator - can export data)

## Step 3: Verify Your Data

Run this command to check if all files are present:

```bash
ls -lh data/parcels/
ls -lh data/federal_land/
```

You should have:
- `data/parcels/coconino_parcels.geojson` (or .shp)
- `data/parcels/yavapai_parcels.geojson` (or .shp)
- `data/parcels/mohave_parcels.geojson` (or .shp)
- `data/parcels/navajo_parcels.geojson` (or .shp)
- `data/federal_land/national_forests.geojson`
- `data/federal_land/blm_land.geojson`

## Step 4: Run the Analysis

Once you have all the data files:

```bash
python spatial_analyzer.py
```

This will:
1. Load all parcel data
2. Filter to parcels >= 9 acres
3. Find parcels that share a boundary with National Forest or BLM land
4. Generate reports in the `output/` directory

## Step 5: View Results

Results will be saved to:
- `output/adjacent_parcels.geojson` - Open in QGIS, ArcGIS, or online viewers
- `output/adjacent_parcels.csv` - Open in Excel or Google Sheets
- `output/summary_report.txt` - Text summary of findings

## Troubleshooting

**If you have Shapefiles instead of GeoJSON:**
The code will automatically detect and load shapefiles. Just make sure they're named correctly (e.g., `coconino_parcels.shp`).

**If downloads are very large:**
Some county parcel datasets can be several GB. Be patient during download and processing.

**If you can't find the parcels dataset:**
Try searching for "tax parcels", "assessor parcels", or "cadastral" on the county portals.

## Alternative: Use Web Mapping Tools

If you prefer a visual approach, you can:
1. Upload the county parcel GeoJSON to https://geojson.io
2. Upload the federal land boundaries
3. Visually identify parcels near the boundaries
4. Manually check acreage

However, the Python script is much faster for processing thousands of parcels!
