# Arizona Federal Land Adjacent Parcel Finder

Find parcels in Coconino, Yavapai, Mohave, and Navajo counties that border National Forest or BLM land and are greater than 9 acres.

## Features

- Downloads parcel data from county open data portals
- Downloads National Forest and BLM boundary data
- Performs spatial analysis to find parcels that share a boundary with federal land
- Filters parcels by minimum acreage
- Generates reports with parcel details

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure as needed

## Usage

### Automated Download and Analysis

Run the complete pipeline:
```bash
python main.py
```

This will:
1. Download parcel data from all 4 counties
2. Download National Forest and BLM boundary data
3. Perform spatial analysis
4. Generate reports

### Manual Data Download

If the automated download doesn't work, you can manually download the data:

1. Find the correct ArcGIS service URLs:
```bash
python find_service_urls.py
```

2. Or follow the manual download instructions in `manual_data_instructions.md`

### Running Analysis Only

If you've already downloaded the data and just want to run the analysis:
```bash
python spatial_analyzer.py
```

## Data Sources

### County Parcel Data
- Coconino County: https://data-coconinocounty.opendata.arcgis.com/
- Yavapai County: https://data-yavgis.opendata.arcgis.com/
- Mohave County: https://az-mohave.opendata.arcgis.com/
- Navajo County: https://open-data-ncaz.hub.arcgis.com/

### Federal Land Boundaries
- National Forest: USDA Forest Service FSGeodata Clearinghouse
- BLM Land: BLM Arizona Geospatial Hub

## Output

Results are saved to the `output/` directory:
- `adjacent_parcels.geojson` - GeoJSON file with matching parcels
- `adjacent_parcels.csv` - CSV file with parcel details
- `summary_report.txt` - Summary statistics

## License

MIT
