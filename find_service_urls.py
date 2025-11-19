#!/usr/bin/env python3
"""
Helper script to find the correct ArcGIS Feature Service URLs for county parcels.

This script helps identify the correct REST API endpoints for each county's
parcel data from their open data portals.
"""
from arcgis.gis import GIS
import requests


def find_coconino_parcels():
    """Find Coconino County parcel service URL."""
    print("=" * 70)
    print("COCONINO COUNTY")
    print("=" * 70)
    print("Portal: https://data-coconinocounty.opendata.arcgis.com/")

    # Try to connect to the portal
    try:
        gis = GIS("https://coconinocounty.maps.arcgis.com")
        print("✓ Connected to Coconino County portal")

        # Search for parcel datasets
        search_results = gis.content.search(query="parcels", item_type="Feature Layer")

        print(f"\nFound {len(search_results)} parcel-related items:")
        for idx, item in enumerate(search_results[:5], 1):
            print(f"\n{idx}. {item.title}")
            print(f"   Type: {item.type}")
            print(f"   Owner: {item.owner}")
            if hasattr(item, 'url'):
                print(f"   URL: {item.url}")

    except Exception as e:
        print(f"✗ Error: {e}")

    print("\nManual search:")
    print("Visit: https://data-coconinocounty.opendata.arcgis.com/")
    print("Search for 'parcels' and look for REST API endpoint")


def find_yavapai_parcels():
    """Find Yavapai County parcel service URL."""
    print("\n" + "=" * 70)
    print("YAVAPAI COUNTY")
    print("=" * 70)
    print("Portal: https://data-yavgis.opendata.arcgis.com/")

    try:
        gis = GIS("https://yavgis.maps.arcgis.com")
        print("✓ Connected to Yavapai County portal")

        search_results = gis.content.search(query="parcels", item_type="Feature Layer")

        print(f"\nFound {len(search_results)} parcel-related items:")
        for idx, item in enumerate(search_results[:5], 1):
            print(f"\n{idx}. {item.title}")
            print(f"   Type: {item.type}")
            print(f"   Owner: {item.owner}")
            if hasattr(item, 'url'):
                print(f"   URL: {item.url}")

    except Exception as e:
        print(f"✗ Error: {e}")

    print("\nManual search:")
    print("Visit: https://data-yavgis.opendata.arcgis.com/")


def find_mohave_parcels():
    """Find Mohave County parcel service URL."""
    print("\n" + "=" * 70)
    print("MOHAVE COUNTY")
    print("=" * 70)
    print("Portal: https://az-mohave.opendata.arcgis.com/")

    try:
        gis = GIS("https://mohave.maps.arcgis.com")
        print("✓ Connected to Mohave County portal")

        search_results = gis.content.search(query="parcels", item_type="Feature Layer")

        print(f"\nFound {len(search_results)} parcel-related items:")
        for idx, item in enumerate(search_results[:5], 1):
            print(f"\n{idx}. {item.title}")
            print(f"   Type: {item.type}")
            print(f"   Owner: {item.owner}")
            if hasattr(item, 'url'):
                print(f"   URL: {item.url}")

    except Exception as e:
        print(f"✗ Error: {e}")

    print("\nManual search:")
    print("Visit: https://az-mohave.opendata.arcgis.com/")


def find_navajo_parcels():
    """Find Navajo County parcel service URL."""
    print("\n" + "=" * 70)
    print("NAVAJO COUNTY")
    print("=" * 70)
    print("Portal: https://open-data-ncaz.hub.arcgis.com/")
    print("Direct dataset: https://open-data-ncaz.hub.arcgis.com/datasets/parcels-1")

    try:
        # Try direct URL from the search results
        test_url = "https://services8.arcgis.com/Y0Ay9HAd1Q86bpaT/arcgis/rest/services/Parcels/FeatureServer/0"
        response = requests.get(test_url + "?f=json")

        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Found Navajo County Parcels service!")
            print(f"   URL: {test_url}")
            print(f"   Name: {data.get('name', 'Unknown')}")
            print(f"   Type: {data.get('type', 'Unknown')}")
            print(f"   Geometry Type: {data.get('geometryType', 'Unknown')}")
        else:
            print(f"✗ Could not access {test_url}")

    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all county searches."""
    print("FINDING ARCGIS FEATURE SERVICE URLs FOR ARIZONA COUNTY PARCELS")
    print("=" * 70)
    print("\nThis script helps identify the correct REST API endpoints")
    print("for parcel data from each county's open data portal.\n")

    find_coconino_parcels()
    find_yavapai_parcels()
    find_mohave_parcels()
    find_navajo_parcels()

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Visit each county's open data portal")
    print("2. Search for 'parcels' or 'tax parcels'")
    print("3. Click on the dataset and look for 'API' or 'I want to use this'")
    print("4. Copy the Feature Service URL (ends with /FeatureServer/0)")
    print("5. Update the URLs in data_downloader.py")
    print("\nAlternatively, you can manually download the shapefiles from")
    print("each portal and place them in the data/parcels/ directory.")


if __name__ == '__main__':
    main()
