#!/usr/bin/env python3
"""
Search ArcGIS portals for parcel datasets and get their service URLs.
"""
from arcgis.gis import GIS
import time


def search_portal(portal_url, portal_name):
    """Search an ArcGIS portal for parcel data."""
    print(f"\n{'='*70}")
    print(f"Searching: {portal_name}")
    print(f"Portal: {portal_url}")
    print('='*70)

    try:
        # Connect anonymously
        gis = GIS(portal_url)
        print(f"✓ Connected to {portal_name}")

        # Search for parcels
        search_queries = ['parcels', 'tax parcels', 'parcel']

        for query in search_queries:
            print(f"\nSearching for '{query}'...")
            results = gis.content.search(
                query=query,
                item_type="Feature Layer",
                max_items=10
            )

            if results:
                print(f"Found {len(results)} items:")
                for idx, item in enumerate(results, 1):
                    print(f"\n  {idx}. {item.title}")
                    print(f"     ID: {item.id}")
                    print(f"     Type: {item.type}")
                    print(f"     Owner: {item.owner}")

                    # Try to get the URL
                    if hasattr(item, 'url') and item.url:
                        print(f"     URL: {item.url}")
                        # Check if this looks like the main parcel layer
                        if 'parcel' in item.title.lower() and 'county' in item.title.lower():
                            print(f"     >>> LIKELY MATCH <<<")
                            return item.url

                    # Try to get layers
                    try:
                        if hasattr(item, 'layers'):
                            layers = item.layers
                            if layers:
                                print(f"     Layers: {len(layers)}")
                                for layer in layers[:3]:
                                    print(f"       - {layer.properties.name} ({layer.url})")
                                # Return the first layer URL
                                if layers[0].url:
                                    return layers[0].url
                    except Exception as e:
                        print(f"     (Could not access layers: {e})")

                # If we found results for this query, use the first one
                if results and hasattr(results[0], 'url'):
                    return results[0].url
                elif results:
                    try:
                        return results[0].layers[0].url
                    except:
                        pass

            time.sleep(1)  # Be polite

        print(f"\n✗ No parcel datasets found for {portal_name}")
        return None

    except Exception as e:
        print(f"\n✗ Error searching {portal_name}: {e}")
        return None


def main():
    """Search all county portals."""
    portals = {
        'Coconino County': 'https://coconinocounty.maps.arcgis.com',
        'Yavapai County': 'https://yavgis.maps.arcgis.com',
        'Mohave County': 'https://mohave.maps.arcgis.com',
        'Navajo County': 'https://ncaz.maps.arcgis.com'
    }

    found_urls = {}

    for county, portal in portals.items():
        url = search_portal(portal, county)
        if url:
            found_urls[county] = url
            print(f"\n✓✓✓ Found URL for {county}: {url}")

    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)

    if found_urls:
        print("\nFound URLs:")
        for county, url in found_urls.items():
            print(f"\n{county}:")
            print(f"  {url}")

        # Write to a file
        with open('found_service_urls.txt', 'w') as f:
            f.write("ArcGIS Feature Service URLs for Arizona County Parcels\n")
            f.write("="*70 + "\n\n")
            for county, url in found_urls.items():
                f.write(f"{county}:\n  {url}\n\n")
        print(f"\n✓ Saved URLs to found_service_urls.txt")
    else:
        print("\n✗ No URLs found automatically.")
        print("\nManual search required. Visit these portals:")
        for county, portal in portals.items():
            print(f"  {county}: {portal}")


if __name__ == '__main__':
    main()
