#!/usr/bin/env python3
"""
Script to find and test ArcGIS Feature Service URLs for county parcels.
"""
import requests
import json


def test_service_url(url, name):
    """Test if a service URL is valid and accessible."""
    try:
        response = requests.get(url + "?f=json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print(f"\n✓ {name} - VALID")
                print(f"  URL: {url}")
                print(f"  Name: {data.get('name', 'N/A')}")
                print(f"  Type: {data.get('type', 'N/A')}")
                print(f"  Geometry Type: {data.get('geometryType', 'N/A')}")
                if 'extent' in data:
                    print(f"  Has extent: Yes")
                return url
            else:
                print(f"\n✗ {name} - Error in response: {data.get('error', {}).get('message', 'Unknown error')}")
        else:
            print(f"\n✗ {name} - HTTP {response.status_code}")
    except Exception as e:
        print(f"\n✗ {name} - Exception: {e}")
    return None


def find_services():
    """Test potential service URLs for each county."""

    print("="*70)
    print("TESTING ARCGIS FEATURE SERVICE URLs")
    print("="*70)

    valid_urls = {}

    # Navajo County - from the earlier search, this looked promising
    print("\n--- NAVAJO COUNTY ---")
    navajo_candidates = [
        "https://services8.arcgis.com/Y0Ay9HAd1Q86bpaT/arcgis/rest/services/Parcels/FeatureServer/0",
        "https://services8.arcgis.com/Y0Ay9HAd1Q86bpaT/ArcGIS/rest/services/Parcels/FeatureServer/0",
    ]
    for url in navajo_candidates:
        result = test_service_url(url, "Navajo County")
        if result:
            valid_urls['Navajo'] = result
            break

    # Yavapai County - try to find based on item ID 85d44993495140b9853ed78494a1e087
    print("\n--- YAVAPAI COUNTY ---")
    yavapai_candidates = [
        "https://services.arcgis.com/LERPnCje40pJ7gWc/arcgis/rest/services/Parcels/FeatureServer/0",
        "https://services.arcgis.com/LERPnCje40pJ7gWc/ArcGIS/rest/services/Parcels_in_Yavapai_County/FeatureServer/0",
        "https://services1.arcgis.com/LERPnCje40pJ7gWc/arcgis/rest/services/Parcels/FeatureServer/0",
    ]
    for url in yavapai_candidates:
        result = test_service_url(url, "Yavapai County")
        if result:
            valid_urls['Yavapai'] = result
            break

    # Mohave County
    print("\n--- MOHAVE COUNTY ---")
    mohave_candidates = [
        "https://services.arcgis.com/QjAJSHNBNHnZPjvZ/arcgis/rest/services/Parcels/FeatureServer/0",
        "https://services1.arcgis.com/QjAJSHNBNHnZPjvZ/arcgis/rest/services/Parcels/FeatureServer/0",
    ]
    for url in mohave_candidates:
        result = test_service_url(url, "Mohave County")
        if result:
            valid_urls['Mohave'] = result
            break

    # Coconino County
    print("\n--- COCONINO COUNTY ---")
    coconino_candidates = [
        "https://services1.arcgis.com/R3V5h2FWI1HRYMxw/arcgis/rest/services/Parcels/FeatureServer/0",
        "https://services.arcgis.com/R3V5h2FWI1HRYMxw/arcgis/rest/services/Parcels/FeatureServer/0",
    ]
    for url in coconino_candidates:
        result = test_service_url(url, "Coconino County")
        if result:
            valid_urls['Coconino'] = result
            break

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    if valid_urls:
        print("\nValid URLs found:")
        for county, url in valid_urls.items():
            print(f"  {county}: {url}")
    else:
        print("\n✗ No valid URLs found automatically.")
        print("\nYou may need to manually visit each county's open data portal:")
        print("  Coconino: https://data-coconinocounty.opendata.arcgis.com/")
        print("  Yavapai: https://data-yavgis.opendata.arcgis.com/")
        print("  Mohave: https://az-mohave.opendata.arcgis.com/")
        print("  Navajo: https://open-data-ncaz.hub.arcgis.com/")
        print("\nLook for the Parcels dataset and click 'View API Resources' or 'API'")

    return valid_urls


if __name__ == '__main__':
    valid_urls = find_services()

    # Save to a file for reference
    if valid_urls:
        with open('valid_service_urls.json', 'w') as f:
            json.dump(valid_urls, f, indent=2)
        print(f"\n✓ Saved valid URLs to valid_service_urls.json")
