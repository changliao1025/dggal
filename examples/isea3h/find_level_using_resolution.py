#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: Find the appropriate DGGRS level based on desired resolution (cell area)
"""

import sys
sys.path.insert(0, '../../bindings/py')

from dggal import *

# Initialize the application
app = Application(appGlobals=globals())
pydggal_setup(app)

def find_level_from_resolution(dggrs, resolution_m2):
    """
    Find the DGGRS level that best matches the desired resolution (cell area in square meters)

    Args:
        dggrs: DGGRS instance (e.g., ISEA3H())
        resolution_m2: Desired resolution in square meters

    Returns:
        int: The level that best matches the desired resolution
    """
    level = dggrs.getLevelFromRefZoneArea(resolution_m2)
    return level

def get_resolution_at_level(dggrs, level):
    """
    Get the reference zone area (resolution) at a specific level

    Args:
        dggrs: DGGRS instance (e.g., ISEA3H())
        level: The DGGRS level

    Returns:
        float: Area in square meters
    """
    area_m2 = dggrs.getRefZoneArea(level)
    return area_m2

def print_level_info(dggrs, level):
    """Print information about a specific level"""
    area_m2 = get_resolution_at_level(dggrs, level)
    area_km2 = area_m2 / 1_000_000
    num_zones = dggrs.countZones(level)

    print(f"\nLevel {level}:")
    print(f"  Reference zone area: {area_m2:,.2f} m² ({area_km2:,.2f} km²)")
    print(f"  Number of zones: {num_zones:,}")

    # Calculate approximate cell size (assuming square cells for simplicity)
    side_length_m = area_m2 ** 0.5
    side_length_km = side_length_m / 1000
    print(f"  Approximate cell size: {side_length_m:,.2f} m ({side_length_km:,.2f} km)")

def print_resolution_table(dggrs, max_level=15):
    """Print a table of resolutions for different levels"""
    print("\n" + "="*70)
    print("DGGRS Resolution Table")
    print("="*70)
    print(f"{'Level':<8} {'Area (m²)':<20} {'Area (km²)':<15} {'# Zones':<15}")
    print("-"*70)

    for level in range(max_level + 1):
        area_m2 = get_resolution_at_level(dggrs, level)
        area_km2 = area_m2 / 1_000_000
        num_zones = dggrs.countZones(level)
        print(f"{level:<8} {area_m2:<20,.2f} {area_km2:<15,.2f} {num_zones:<15,}")

if __name__ == "__main__":
    # Initialize DGGRS (using ISEA3H as example)
    dggrs = ISEA3H()

    print("DGGRS: ISEA3H")
    print("="*70)

    # Example 1: Find level for a specific resolution
    print("\n--- Example 1: Find level from desired resolution ---")

    # Desired resolution: 1000 km² (1,000,000,000 m²)
    desired_resolution_km2 = 1000
    desired_resolution_m2 = desired_resolution_km2 * 1_000_000

    level = find_level_from_resolution(dggrs, desired_resolution_m2)
    print(f"\nDesired resolution: {desired_resolution_km2:,} km² ({desired_resolution_m2:,} m²)")
    print(f"Best matching level: {level}")

    print_level_info(dggrs, level)

    # Example 2: Find level for different resolutions
    print("\n\n--- Example 2: Find levels for various resolutions ---")

    test_resolutions = [
        (10000, "10,000 km²"),      # Very coarse
        (1000, "1,000 km²"),        # Coarse
        (100, "100 km²"),           # Medium
        (10, "10 km²"),             # Fine
        (1, "1 km²"),               # Very fine
    ]

    for res_km2, label in test_resolutions:
        res_m2 = res_km2 * 1_000_000
        level = find_level_from_resolution(dggrs, res_m2)
        actual_area_m2 = get_resolution_at_level(dggrs, level)
        actual_area_km2 = actual_area_m2 / 1_000_000
        print(f"\n{label:15} -> Level {level:2} (actual: {actual_area_km2:,.2f} km²)")

    # Example 3: Show resolution table for multiple levels
    print("\n\n--- Example 3: Resolution table for levels 0-10 ---")
    print_resolution_table(dggrs, max_level=10)
