"""
Perform spatial analysis to find parcels adjacent to federal land.
"""
import geopandas as gpd
from pathlib import Path
import pandas as pd
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union


class SpatialAnalyzer:
    """Analyze parcels for adjacency to federal land."""

    def __init__(self, data_dir='./data', output_dir='./output', min_acres=9):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.min_acres = min_acres

        self.parcels_dir = self.data_dir / 'parcels'
        self.federal_dir = self.data_dir / 'federal_land'

    def load_parcels(self, county_name):
        """Load parcel data for a county (supports GeoJSON and Shapefile)."""
        # Try multiple file extensions
        extensions = ['.geojson', '.shp', '.gpkg']
        file_path = None

        for ext in extensions:
            test_path = self.parcels_dir / f'{county_name.lower()}_parcels{ext}'
            if test_path.exists():
                file_path = test_path
                break

        if not file_path:
            print(f"✗ Parcel file not found for {county_name} County")
            print(f"  Looked for: {county_name.lower()}_parcels.[geojson|shp|gpkg]")
            print(f"  In directory: {self.parcels_dir}")
            return None

        try:
            print(f"Loading {county_name} County parcels from {file_path.name}...")
            gdf = gpd.read_file(file_path)

            if len(gdf) == 0:
                print(f"  ✗ File is empty!")
                return None

            # Reproject to a projected CRS for accurate area calculations
            # Using NAD83 / Arizona Central (EPSG:26949) for Arizona
            if gdf.crs is None:
                print(f"  Warning: No CRS defined, assuming EPSG:4326")
                gdf.set_crs(epsg=4326, inplace=True)

            gdf = gdf.to_crs(epsg=26949)

            print(f"  ✓ Loaded {len(gdf)} parcels")
            return gdf

        except Exception as e:
            print(f"  ✗ Error loading {file_path}: {e}")
            return None

    def load_federal_land(self):
        """Load and combine National Forest and BLM boundaries (supports multiple formats)."""
        print("Loading federal land boundaries...")

        federal_boundaries = []

        # Load National Forests (try multiple formats)
        forest_file = None
        for ext in ['.geojson', '.shp', '.gpkg']:
            test_path = self.federal_dir / f'national_forests{ext}'
            if test_path.exists():
                forest_file = test_path
                break

        if forest_file:
            try:
                forests = gpd.read_file(forest_file)
                if forests.crs is None:
                    forests.set_crs(epsg=4326, inplace=True)
                forests = forests.to_crs(epsg=26949)
                forests['land_type'] = 'National Forest'
                federal_boundaries.append(forests)
                print(f"  ✓ Loaded {len(forests)} National Forest boundaries from {forest_file.name}")
            except Exception as e:
                print(f"  ✗ Error loading National Forest file: {e}")
        else:
            print(f"  ✗ National Forest file not found in {self.federal_dir}")

        # Load BLM land (try multiple formats)
        blm_file = None
        for ext in ['.geojson', '.shp', '.gpkg']:
            test_path = self.federal_dir / f'blm_land{ext}'
            if test_path.exists():
                blm_file = test_path
                break

        if blm_file:
            try:
                blm = gpd.read_file(blm_file)
                if blm.crs is None:
                    blm.set_crs(epsg=4326, inplace=True)
                blm = blm.to_crs(epsg=26949)
                blm['land_type'] = 'BLM'
                federal_boundaries.append(blm)
                print(f"  ✓ Loaded {len(blm)} BLM boundaries from {blm_file.name}")
            except Exception as e:
                print(f"  ✗ Error loading BLM file: {e}")
        else:
            print(f"  ✗ BLM file not found in {self.federal_dir}")

        if not federal_boundaries:
            print("✗ No federal land boundaries loaded!")
            print(f"\nPlease download federal land data and place in: {self.federal_dir}")
            print("See QUICK_START.md for download instructions")
            return None

        # Combine all federal land
        combined = gpd.GeoDataFrame(pd.concat(federal_boundaries, ignore_index=True))
        print(f"  ✓ Total federal land polygons: {len(combined)}")

        return combined

    def calculate_acreage(self, gdf):
        """Calculate acreage for each parcel."""
        # Area is in square meters (from EPSG:26949)
        # Convert to acres (1 acre = 4046.86 square meters)
        gdf['acres'] = gdf.geometry.area / 4046.86
        return gdf

    def filter_by_acreage(self, gdf, min_acres):
        """Filter parcels by minimum acreage."""
        filtered = gdf[gdf['acres'] >= min_acres].copy()
        print(f"  Filtered to {len(filtered)} parcels >= {min_acres} acres")
        return filtered

    def find_adjacent_parcels(self, parcels_gdf, federal_gdf):
        """
        Find parcels that share a boundary with federal land.

        This uses the 'touches' spatial predicate which is true if geometries
        share at least one boundary point but no interior points.
        """
        print(f"Finding parcels adjacent to federal land...")

        # Create spatial index for efficiency
        federal_sindex = federal_gdf.sindex

        adjacent_parcels = []
        adjacent_federal_types = []

        for idx, parcel in parcels_gdf.iterrows():
            # Find potential matches using spatial index
            possible_matches_idx = list(federal_sindex.intersection(parcel.geometry.bounds))
            possible_matches = federal_gdf.iloc[possible_matches_idx]

            # Check for actual boundary touching
            for fed_idx, federal in possible_matches.iterrows():
                if parcel.geometry.touches(federal.geometry):
                    adjacent_parcels.append(idx)
                    adjacent_federal_types.append(federal['land_type'])
                    break  # Found adjacent federal land, no need to check more

            # Progress indicator
            if (idx + 1) % 1000 == 0:
                print(f"  Checked {idx + 1}/{len(parcels_gdf)} parcels...")

        # Get unique adjacent parcel indices
        adjacent_indices = list(set(adjacent_parcels))
        result_gdf = parcels_gdf.loc[adjacent_indices].copy()

        # Add federal land type information
        federal_type_map = dict(zip(adjacent_parcels, adjacent_federal_types))
        result_gdf['adjacent_to'] = result_gdf.index.map(federal_type_map)

        print(f"  Found {len(result_gdf)} parcels adjacent to federal land")

        return result_gdf

    def analyze_county(self, county_name, federal_gdf):
        """Analyze parcels for a single county."""
        print(f"\nAnalyzing {county_name} County")
        print("-" * 60)

        # Load parcels
        parcels = self.load_parcels(county_name)
        if parcels is None:
            return None

        # Calculate acreage
        parcels = self.calculate_acreage(parcels)

        # Filter by minimum acreage
        large_parcels = self.filter_by_acreage(parcels, self.min_acres)

        if len(large_parcels) == 0:
            print(f"  No parcels >= {self.min_acres} acres found")
            return None

        # Find adjacent parcels
        adjacent = self.find_adjacent_parcels(large_parcels, federal_gdf)

        # Add county name
        adjacent['county'] = county_name

        return adjacent

    def analyze_all_counties(self):
        """Analyze all counties and combine results."""
        print("=" * 60)
        print("SPATIAL ANALYSIS")
        print("=" * 60)

        # Load federal land once (used for all counties)
        federal_gdf = self.load_federal_land()
        if federal_gdf is None:
            print("Cannot proceed without federal land boundaries!")
            return None

        counties = ['Coconino', 'Yavapai', 'Mohave', 'Navajo']
        all_results = []

        for county in counties:
            result = self.analyze_county(county, federal_gdf)
            if result is not None and len(result) > 0:
                all_results.append(result)

        if not all_results:
            print("\n✗ No adjacent parcels found in any county!")
            return None

        # Combine all results
        combined = gpd.GeoDataFrame(pd.concat(all_results, ignore_index=True))

        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Total parcels found: {len(combined)}")
        print(f"\nBreakdown by county:")
        print(combined['county'].value_counts())
        print(f"\nBreakdown by federal land type:")
        print(combined['adjacent_to'].value_counts())

        return combined

    def save_results(self, gdf):
        """Save results to various formats."""
        if gdf is None or len(gdf) == 0:
            print("No results to save!")
            return

        print("\n" + "=" * 60)
        print("SAVING RESULTS")
        print("=" * 60)

        # Save as GeoJSON (keep in projected CRS for now)
        geojson_file = self.output_dir / 'adjacent_parcels.geojson'
        gdf_wgs84 = gdf.to_crs(epsg=4326)  # Convert to WGS84 for web mapping
        gdf_wgs84.to_file(geojson_file, driver='GeoJSON')
        print(f"✓ Saved GeoJSON: {geojson_file}")

        # Save as CSV (without geometry for easy viewing)
        csv_file = self.output_dir / 'adjacent_parcels.csv'
        csv_data = gdf.drop(columns=['geometry'])
        csv_data.to_csv(csv_file, index=False)
        print(f"✓ Saved CSV: {csv_file}")

        # Save summary report
        summary_file = self.output_dir / 'summary_report.txt'
        with open(summary_file, 'w') as f:
            f.write("ARIZONA FEDERAL LAND ADJACENT PARCELS REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Analysis Date: {pd.Timestamp.now()}\n")
            f.write(f"Minimum Parcel Size: {self.min_acres} acres\n\n")
            f.write(f"Total Parcels Found: {len(gdf)}\n\n")
            f.write("Breakdown by County:\n")
            f.write("-" * 40 + "\n")
            f.write(str(gdf['county'].value_counts()) + "\n\n")
            f.write("Breakdown by Federal Land Type:\n")
            f.write("-" * 40 + "\n")
            f.write(str(gdf['adjacent_to'].value_counts()) + "\n\n")
            f.write(f"Total Acreage: {gdf['acres'].sum():.2f} acres\n")
            f.write(f"Average Parcel Size: {gdf['acres'].mean():.2f} acres\n")
            f.write(f"Median Parcel Size: {gdf['acres'].median():.2f} acres\n")
            f.write(f"Largest Parcel: {gdf['acres'].max():.2f} acres\n")
        print(f"✓ Saved summary report: {summary_file}")

        print("\nAll results saved to:", self.output_dir)


if __name__ == '__main__':
    analyzer = SpatialAnalyzer(min_acres=9)
    results = analyzer.analyze_all_counties()
    if results is not None:
        analyzer.save_results(results)
