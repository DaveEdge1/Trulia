#!/usr/bin/env python3
"""
Arizona Federal Land Adjacent Parcel Finder

Finds parcels in Coconino, Yavapai, Mohave, and Navajo counties that:
1. Are greater than 9 acres
2. Share a boundary with National Forest or BLM land
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from data_downloader import DataDownloader
from spatial_analyzer import SpatialAnalyzer


def main():
    """Main execution function."""

    # Load environment variables
    load_dotenv()

    # Get configuration
    min_acres = float(os.getenv('MIN_PARCEL_SIZE_ACRES', 9))
    data_dir = os.getenv('DATA_DIR', './data')
    output_dir = os.getenv('OUTPUT_DIR', './output')

    print("=" * 70)
    print("ARIZONA FEDERAL LAND ADJACENT PARCEL FINDER")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Minimum parcel size: {min_acres} acres")
    print(f"  Counties: Coconino, Yavapai, Mohave, Navajo")
    print(f"  Federal land types: National Forest, BLM")
    print(f"  Data directory: {data_dir}")
    print(f"  Output directory: {output_dir}")
    print()

    # Step 1: Download data
    print("\nSTEP 1: Downloading Data")
    print("-" * 70)
    downloader = DataDownloader(data_dir=data_dir)

    try:
        download_results = downloader.download_all_data()
    except Exception as e:
        print(f"\n✗ Error during data download: {e}")
        print("\nYou may need to manually download the data from the sources listed")
        print("in README.md and place them in the data/ directory.")
        return 1

    # Step 2: Perform spatial analysis
    print("\n\nSTEP 2: Spatial Analysis")
    print("-" * 70)
    analyzer = SpatialAnalyzer(
        data_dir=data_dir,
        output_dir=output_dir,
        min_acres=min_acres
    )

    try:
        results = analyzer.analyze_all_counties()

        if results is not None and len(results) > 0:
            # Step 3: Save results
            print("\n\nSTEP 3: Saving Results")
            print("-" * 70)
            analyzer.save_results(results)

            print("\n" + "=" * 70)
            print("SUCCESS!")
            print("=" * 70)
            print(f"\nFound {len(results)} parcels meeting your criteria.")
            print(f"Results saved to: {output_dir}/")
            print("\nFiles created:")
            print(f"  - adjacent_parcels.geojson (for GIS software)")
            print(f"  - adjacent_parcels.csv (for spreadsheets)")
            print(f"  - summary_report.txt (summary statistics)")
            return 0
        else:
            print("\n" + "=" * 70)
            print("NO RESULTS FOUND")
            print("=" * 70)
            print("\nNo parcels matching your criteria were found.")
            print("This could mean:")
            print("  - The data downloads were incomplete")
            print("  - There are no parcels >= 9 acres adjacent to federal land")
            print("  - There was an issue with the spatial analysis")
            return 1

    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
