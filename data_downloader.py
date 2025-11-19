"""
Download parcel and federal land boundary data from open data portals.
"""
import os
import requests
import geopandas as gpd
from pathlib import Path
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import time


class DataDownloader:
    """Download GIS data from various sources."""

    def __init__(self, data_dir='./data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Create subdirectories
        self.parcels_dir = self.data_dir / 'parcels'
        self.federal_dir = self.data_dir / 'federal_land'
        self.parcels_dir.mkdir(exist_ok=True)
        self.federal_dir.mkdir(exist_ok=True)

        # Initialize anonymous GIS connection
        self.gis = GIS()

    def download_county_parcels(self, county_name, feature_service_url):
        """
        Download parcel data from county ArcGIS feature service.

        Args:
            county_name: Name of the county
            feature_service_url: URL to the ArcGIS feature service
        """
        output_file = self.parcels_dir / f'{county_name.lower()}_parcels.geojson'

        if output_file.exists():
            print(f"✓ {county_name} County parcels already downloaded")
            return output_file

        print(f"Downloading {county_name} County parcels...")

        try:
            # Create feature layer
            feature_layer = FeatureLayer(feature_service_url)

            # Query all features in chunks
            # Get total count first
            count_result = feature_layer.query(where="1=1", return_count_only=True)
            print(f"  Total parcels: {count_result}")

            # Download in chunks to avoid timeout
            chunk_size = 2000
            all_features = []

            for offset in range(0, count_result, chunk_size):
                print(f"  Downloading parcels {offset} to {offset + chunk_size}...")
                feature_set = feature_layer.query(
                    where="1=1",
                    out_fields="*",
                    return_geometry=True,
                    result_offset=offset,
                    result_record_count=chunk_size
                )
                all_features.extend(feature_set.features)
                time.sleep(1)  # Be nice to the server

            # Convert to GeoDataFrame
            gdf = gpd.GeoDataFrame.from_features([f.as_dict for f in all_features])

            # Ensure CRS is set
            if gdf.crs is None:
                gdf.set_crs(epsg=4326, inplace=True)

            # Save to GeoJSON
            gdf.to_file(output_file, driver='GeoJSON')
            print(f"✓ Saved {len(gdf)} parcels to {output_file}")

            return output_file

        except Exception as e:
            print(f"✗ Error downloading {county_name} County parcels: {e}")
            return None

    def download_all_county_parcels(self):
        """Download parcel data for all 4 Arizona counties."""

        # ArcGIS Feature Service URLs for each county
        # These need to be updated with actual service URLs from the open data portals
        county_services = {
            'Coconino': 'https://services1.arcgis.com/R3V5h2FWI1HRYMxw/arcgis/rest/services/Parcels/FeatureServer/0',
            'Yavapai': 'https://services.arcgis.com/LERPnCje40pJ7gWc/arcgis/rest/services/Parcels/FeatureServer/0',
            'Mohave': 'https://services.arcgis.com/QjAJSHNBNHnZPjvZ/arcgis/rest/services/Parcels/FeatureServer/0',
            'Navajo': 'https://services8.arcgis.com/Y0Ay9HAd1Q86bpaT/arcgis/rest/services/Parcels/FeatureServer/0'
        }

        results = {}
        for county, url in county_services.items():
            result = self.download_county_parcels(county, url)
            results[county] = result

        return results

    def download_national_forest_boundaries(self):
        """Download National Forest boundaries for Arizona."""
        output_file = self.federal_dir / 'national_forests.geojson'

        if output_file.exists():
            print("✓ National Forest boundaries already downloaded")
            return output_file

        print("Downloading National Forest boundaries...")

        try:
            # USFS National Forests feature service
            url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/National_Forest_System_Land/FeatureServer/0"
            feature_layer = FeatureLayer(url)

            # Query for Arizona forests only (or nationwide)
            # We'll get all and filter in analysis
            feature_set = feature_layer.query(
                where="1=1",
                out_fields="*",
                return_geometry=True
            )

            # Convert to GeoDataFrame
            gdf = gpd.GeoDataFrame.from_features([f.as_dict for f in feature_set.features])

            if gdf.crs is None:
                gdf.set_crs(epsg=4326, inplace=True)

            # Save to GeoJSON
            gdf.to_file(output_file, driver='GeoJSON')
            print(f"✓ Saved {len(gdf)} National Forest boundaries to {output_file}")

            return output_file

        except Exception as e:
            print(f"✗ Error downloading National Forest boundaries: {e}")
            return None

    def download_blm_boundaries(self):
        """Download BLM land boundaries for Arizona."""
        output_file = self.federal_dir / 'blm_land.geojson'

        if output_file.exists():
            print("✓ BLM land boundaries already downloaded")
            return output_file

        print("Downloading BLM land boundaries...")

        try:
            # BLM Surface Management Agency feature service
            url = "https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_without_Mask/MapServer/1"
            feature_layer = FeatureLayer(url)

            # Query for Arizona BLM land
            # Using state FIPS code or spatial filter
            feature_set = feature_layer.query(
                where="STATE='AZ'",
                out_fields="*",
                return_geometry=True
            )

            # Convert to GeoDataFrame
            gdf = gpd.GeoDataFrame.from_features([f.as_dict for f in feature_set.features])

            if gdf.crs is None:
                gdf.set_crs(epsg=4326, inplace=True)

            # Save to GeoJSON
            gdf.to_file(output_file, driver='GeoJSON')
            print(f"✓ Saved {len(gdf)} BLM land boundaries to {output_file}")

            return output_file

        except Exception as e:
            print(f"✗ Error downloading BLM boundaries: {e}")
            return None

    def download_all_data(self):
        """Download all required data."""
        print("=" * 60)
        print("DOWNLOADING DATA")
        print("=" * 60)

        # Download county parcels
        print("\n1. Downloading County Parcel Data")
        print("-" * 60)
        parcel_files = self.download_all_county_parcels()

        # Download federal land boundaries
        print("\n2. Downloading Federal Land Boundaries")
        print("-" * 60)
        forest_file = self.download_national_forest_boundaries()
        blm_file = self.download_blm_boundaries()

        return {
            'parcels': parcel_files,
            'forests': forest_file,
            'blm': blm_file
        }


if __name__ == '__main__':
    downloader = DataDownloader()
    results = downloader.download_all_data()
    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
