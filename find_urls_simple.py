#!/usr/bin/env python3
"""
Simple script to find ArcGIS Feature Service URLs using REST API calls.
"""
import requests
import json


def find_hub_datasets(hub_url, search_term):
    """Search an ArcGIS Hub for datasets."""
    # ArcGIS Hub uses a specific API endpoint
    api_url = f"{hub_url}/api/v3/datasets"
    params = {
        'filter[searchTerms]': search_term,
        'page[size]': 10
    }

    try:
        print(f"  Searching {hub_url} for '{search_term}'...")
        response = requests.get(api_url, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            datasets = data.get('data', [])
            print(f"  Found {len(datasets)} datasets")

            for dataset in datasets:
                attrs = dataset.get('attributes', {})
                title = attrs.get('name', 'Untitled')
                print(f"\n    - {title}")

                # Look for the service URL
                if 'url' in attrs:
                    url = attrs['url']
                    if 'FeatureServer' in url or 'MapServer' in url:
                        print(f"      Service URL: {url}")
                        return url

        else:
            print(f"  HTTP {response.status_code}")

    except Exception as e:
        print(f"  Error: {e}")

    return None


def search_arcgis_rest(base_url):
    """Try to query ArcGIS REST services directly."""
    try:
        response = requests.get(base_url + "?f=json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'services' in data:
                print(f"\n  Found services at {base_url}")
                for service in data['services']:
                    name = service.get('name', '')
                    service_type = service.get('type', '')
                    if 'parcel' in name.lower():
                        service_url = f"{base_url}/{name}/{service_type}"
                        print(f"    Parcel service: {service_url}")
                        return service_url
    except:
        pass
    return None


def main():
    print("="*70)
    print("FINDING PARCEL SERVICE URLs")
    print("="*70)

    found_urls = {}

    # Try each county's open data hub
    counties = {
        'Navajo': 'https://open-data-ncaz.hub.arcgis.com',
        'Coconino': 'https://data-coconinocounty.opendata.arcgis.com',
        'Yavapai': 'https://data-yavgis.opendata.arcgis.com',
        'Mohave': 'https://az-mohave.opendata.arcgis.com'
    }

    for county, hub_url in counties.items():
        print(f"\n{county} County:")
        print("-" * 70)
        url = find_hub_datasets(hub_url, 'parcels')
        if url:
            found_urls[county] = url

    # Also try some known service endpoint patterns
    print("\n" + "="*70)
    print("TESTING KNOWN SERVICE PATTERNS")
    print("="*70)

    # Known service bases from earlier research
    known_patterns = {
        'Navajo': [
            "https://services8.arcgis.com/Y0Ay9HAd1Q86bpaT/arcgis/rest/services/Parcels/FeatureServer/0",
        ],
        'Yavapai': [
            "https://services.arcgis.com/LERPnCje40pJ7gWc/arcgis/rest/services/Parcels_in_Yavapai_County/FeatureServer/0",
        ],
        'Coconino': [
            "https://services1.arcgis.com/R3V5h2FWI1HRYMxw/arcgis/rest/services/Parcels_View/FeatureServer/0",
        ],
        'Mohave': [
            "https://services.arcgis.com/QjAJSHNBNHnZPjvZ/arcgis/rest/services/Tax_Parcels/FeatureServer/0",
        ]
    }

    for county, urls in known_patterns.items():
        if county in found_urls:
            continue  # Already found via Hub API

        print(f"\n{county} County:")
        for url in urls:
            try:
                response = requests.get(url + "?f=json", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'error' not in data and 'name' in data:
                        print(f"  ✓ Valid: {url}")
                        print(f"    Name: {data.get('name')}")
                        print(f"    Type: {data.get('type')}")
                        found_urls[county] = url
                        break
                    else:
                        print(f"  ✗ Invalid: {url}")
                else:
                    print(f"  ✗ HTTP {response.status_code}: {url}")
            except Exception as e:
                print(f"  ✗ Error: {url} - {e}")

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    if found_urls:
        print("\nFound URLs:\n")
        for county, url in found_urls.items():
            print(f"{county} County:")
            print(f"  {url}\n")

        # Save to file
        with open('service_urls.json', 'w') as f:
            json.dump(found_urls, f, indent=2)
        print("✓ Saved to service_urls.json")

        # Generate Python code
        print("\nCode for data_downloader.py:")
        print("-" * 70)
        print("county_services = {")
        for county, url in found_urls.items():
            print(f"    '{county}': '{url}',")
        print("}")

    else:
        print("\n✗ No URLs found automatically")
        print("\nManual steps:")
        print("1. Visit each county's open data portal")
        print("2. Search for 'parcels'")
        print("3. Click on the dataset")
        print("4. Look for 'API' or 'View API Resources'")
        print("5. Copy the FeatureServer URL")

    return found_urls


if __name__ == '__main__':
    found = main()
