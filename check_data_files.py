#!/usr/bin/env python3
"""
Check which data files are present and their status.
"""
from pathlib import Path
import os


def check_files():
    """Check for presence of required data files."""
    print("="*70)
    print("DATA FILES CHECK")
    print("="*70)

    data_dir = Path('./data')
    parcels_dir = data_dir / 'parcels'
    federal_dir = data_dir / 'federal_land'

    # Create directories if they don't exist
    parcels_dir.mkdir(parents=True, exist_ok=True)
    federal_dir.mkdir(parents=True, exist_ok=True)

    # Check county parcel files
    print("\nCOUNTY PARCEL FILES:")
    print("-" * 70)

    counties = ['coconino', 'yavapai', 'mohave', 'navajo']
    parcel_status = {}

    for county in counties:
        found = False
        for ext in ['.geojson', '.shp', '.gpkg']:
            file_path = parcels_dir / f'{county}_parcels{ext}'
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  ✓ {county.capitalize()} County: {file_path.name} ({size_mb:.1f} MB)")
                parcel_status[county] = True
                found = True
                break

        if not found:
            print(f"  ✗ {county.capitalize()} County: NOT FOUND")
            parcel_status[county] = False

    # Check federal land files
    print("\nFEDERAL LAND FILES:")
    print("-" * 70)

    federal_status = {}

    # Check National Forest
    forest_found = False
    for ext in ['.geojson', '.shp', '.gpkg']:
        file_path = federal_dir / f'national_forests{ext}'
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"  ✓ National Forests: {file_path.name} ({size_mb:.1f} MB)")
            federal_status['forests'] = True
            forest_found = True
            break

    if not forest_found:
        print(f"  ✗ National Forests: NOT FOUND")
        federal_status['forests'] = False

    # Check BLM
    blm_found = False
    for ext in ['.geojson', '.shp', '.gpkg']:
        file_path = federal_dir / f'blm_land{ext}'
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"  ✓ BLM Land: {file_path.name} ({size_mb:.1f} MB)")
            federal_status['blm'] = True
            blm_found = True
            break

    if not blm_found:
        print(f"  ✗ BLM Land: NOT FOUND")
        federal_status['blm'] = False

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    parcel_count = sum(parcel_status.values())
    federal_count = sum(federal_status.values())

    print(f"\nCounty Parcels: {parcel_count}/4 counties")
    print(f"Federal Land: {federal_count}/2 datasets")

    if parcel_count == 4 and federal_count == 2:
        print("\n✓✓✓ ALL DATA FILES PRESENT ✓✓✓")
        print("\nYou can now run: python spatial_analyzer.py")
        return True
    else:
        print("\n✗ Some data files are missing")
        print("\nNext steps:")
        if parcel_count < 4:
            print("  1. Download county parcel data (see QUICK_START.md)")
        if federal_count < 2:
            print("  2. Download federal land boundaries (see QUICK_START.md)")
        print("  3. Run this script again to verify")
        return False


if __name__ == '__main__':
    import sys
    success = check_files()
    sys.exit(0 if success else 1)
