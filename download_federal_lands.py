#!/usr/bin/env python3
"""
Download just the federal land boundaries (National Forest and BLM).
This script downloads federal land data which is easier to access than county parcels.
"""
import requests
import json
from pathlib import Path


def download_geojson(url, output_file, description):
    """Download GeoJSON data from a URL."""
    print(f"\nDownloading {description}...")
    print(f"  URL: {url}")

    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            data = response.json()

            # Save to file
            with open(output_file, 'w') as f:
                json.dump(data, f)

            # Count features
            feature_count = len(data.get('features', []))
            print(f"  ✓ Downloaded {feature_count} features")
            print(f"  ✓ Saved to: {output_file}")
            return True
        else:
            print(f"  ✗ HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def download_from_arcgis_feature_service(service_url, output_file, description, where_clause="1=1"):
    """
    Download data from an ArcGIS Feature Service using the query endpoint.
    """
    print(f"\nDownloading {description}...")
    print(f"  Service: {service_url}")

    # Build query URL
    query_url = f"{service_url}/query"

    params = {
        'where': where_clause,
        'outFields': '*',
        'returnGeometry': 'true',
        'f': 'geojson',
        'resultRecordCount': 5000  # Max records per request
    }

    try:
        all_features = []
        offset = 0

        while True:
            params['resultOffset'] = offset
            print(f"  Fetching records {offset}...")

            response = requests.get(query_url, params=params, timeout=60)

            if response.status_code != 200:
                print(f"  ✗ HTTP {response.status_code}")
                break

            data = response.json()

            if 'features' not in data:
                print(f"  ✗ No features in response")
                break

            features = data['features']
            if not features:
                break  # No more records

            all_features.extend(features)
            offset += len(features)

            # Check if there are more records
            if len(features) < params['resultRecordCount']:
                break  # Got all records

        if all_features:
            # Create GeoJSON structure
            geojson = {
                'type': 'FeatureCollection',
                'features': all_features
            }

            # Save to file
            with open(output_file, 'w') as f:
                json.dump(geojson, f)

            print(f"  ✓ Downloaded {len(all_features)} features")
            print(f"  ✓ Saved to: {output_file}")
            return True
        else:
            print(f"  ✗ No features downloaded")
            return False

    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*70)
    print("DOWNLOADING FEDERAL LAND BOUNDARIES")
    print("="*70)

    # Create data directories
    data_dir = Path('./data')
    federal_dir = data_dir / 'federal_land'
    federal_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    # Download National Forest boundaries
    # Using USFS National Forest System Lands
    forest_url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Forest_System_Land/FeatureServer/0"
    forest_file = federal_dir / 'national_forests.geojson'

    if download_from_arcgis_feature_service(
        forest_url,
        forest_file,
        "National Forest boundaries (nationwide)",
        where_clause="1=1"
    ):
        results['National Forest'] = str(forest_file)

    # Download BLM Surface Management Agency data
    # This is a large dataset, so we'll filter to Arizona
    blm_url = "https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_without_Mask/MapServer/1"
    blm_file = federal_dir / 'blm_land.geojson'

    if download_from_arcgis_feature_service(
        blm_url,
        blm_file,
        "BLM land (Arizona only)",
        where_clause="STATE_CODE='AZ' AND ADMIN_ST='BLM'"
    ):
        results['BLM'] = str(blm_file)

    print("\n" + "="*70)
    print("DOWNLOAD SUMMARY")
    print("="*70)

    if results:
        print("\n✓ Successfully downloaded:")
        for land_type, file_path in results.items():
            print(f"  {land_type}: {file_path}")
        return True
    else:
        print("\n✗ No data was downloaded successfully")
        print("\nYou may need to manually download the data:")
        print("  National Forests: https://data.fs.usda.gov/geodata/")
        print("  BLM Land: https://gbp-blm-egis.hub.arcgis.com/pages/arizona")
        return False


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
