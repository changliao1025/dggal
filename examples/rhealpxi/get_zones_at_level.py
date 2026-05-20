#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: Get all zones at a given level
Based on examples from bindings_examples/py/list.py
"""

import sys
sys.path.insert(0, '../../bindings/py')

from dggal import *

# Initialize the application
app = Application(appGlobals=globals())
pydggal_setup(app)

def get_all_zones_at_level(dggrs, level, bbox=None):
    """
    Get all zones at a specific level

    Args:
        dggrs: DGGRS instance (e.g., ISEA3H())
        level: The DGGRS level
        bbox: Optional bounding box (GeoExtent). If None, returns all zones globally

    Returns:
        List of zone IDs as strings
    """
    if bbox is None:
        bbox = wholeWorld

    # Get zones from the DGGRS
    zones = dggrs.listZones(level, bbox)

    # Convert zones to text IDs
    zone_ids = []
    for z in zones:
        zone_id = dggrs.getZoneTextID(z)
        zone_ids.append(zone_id)

    return zone_ids

def get_zones_with_centroids(dggrs, level, bbox=None):
    """
    Get all zones at a specific level with their centroids

    Args:
        dggrs: DGGRS instance (e.g., ISEA3H())
        level: The DGGRS level
        bbox: Optional bounding box (GeoExtent). If None, returns all zones globally

    Returns:
        List of tuples: [(zone_id, (lon, lat)), ...]
    """
    if bbox is None:
        bbox = wholeWorld

    # Get zones from the DGGRS
    zones = dggrs.listZones(level, bbox)

    # Get zone IDs and centroids
    zones_with_centroids = []
    for z in zones:
        zone_id = dggrs.getZoneTextID(z)
        centroid = dggrs.getZoneWGS84Centroid(z)
        zones_with_centroids.append((zone_id, (centroid.lon, centroid.lat)))

    return zones_with_centroids

def get_zones_in_bbox(dggrs, level, min_lat, min_lon, max_lat, max_lon):
    """
    Get all zones at a specific level within a bounding box

    Args:
        dggrs: DGGRS instance (e.g., ISEA3H())
        level: The DGGRS level
        min_lat: Minimum latitude
        min_lon: Minimum longitude
        max_lat: Maximum latitude
        max_lon: Maximum longitude

    Returns:
        List of zone IDs as strings
    """
    # Create bounding box
    bbox = GeoExtent()
    bbox.ll = (min_lat, min_lon)
    bbox.ur = (max_lat, max_lon)

    return get_all_zones_at_level(dggrs, level, bbox)

def print_zones_summary(zone_ids, level):
    """Print a summary of zones"""
    print(f"\nLevel {level}: Found {len(zone_ids)} zones")
    if len(zone_ids) <= 20:
        print("\nZone IDs:")
        for zone_id in zone_ids:
            print(f"  {zone_id}")
    else:
        print("\nFirst 10 zone IDs:")
        for zone_id in zone_ids[:10]:
            print(f"  {zone_id}")
        print(f"  ... ({len(zone_ids) - 10} more zones)")

if __name__ == "__main__":
    # Initialize DGGRS (using rHEALPix as example)
    dggrs = rHEALPix()

    print("DGGRS: rHEALPix")
    print("="*70)

    # Example 1: Get all zones at level 0 (global)
    print("\n--- Example 1: Get all zones at level 0 ---")
    level = 0
    zones = get_all_zones_at_level(dggrs, level)
    print_zones_summary(zones, level)

    # Example 2: Get all zones at level 2
    print("\n\n--- Example 2: Get all zones at level 2 ---")
    level = 2
    zones = get_all_zones_at_level(dggrs, level)
    print_zones_summary(zones, level)

    # Example 3: Get zones within a bounding box
    print("\n\n--- Example 3: Get zones in bounding box (North America region) ---")
    level = 3
    # Bounding box: roughly North America (lat: 25-50, lon: -125 to -70)
    zones = get_zones_in_bbox(dggrs, level, 25, -125, 50, -70)
    print(f"\nLevel {level} zones in North America region: {len(zones)} zones")
    print("\nFirst 10 zones:")
    for zone_id in zones[:10]:
        print(f"  {zone_id}")

    # Example 4: Get zones with centroids
    print("\n\n--- Example 4: Get zones with centroids at level 1 ---")
    level = 1
    zones_with_centroids = get_zones_with_centroids(dggrs, level)
    print(f"\nLevel {level}: Found {len(zones_with_centroids)} zones")
    print("\nZones with centroids (lon, lat):")
    for zone_id, (lon, lat) in zones_with_centroids[:10]:
        print(f"  {zone_id}: ({lon.value:.6f}, {lat.value:.6f})")
    if len(zones_with_centroids) > 10:
        print(f"  ... ({len(zones_with_centroids) - 10} more zones)")

    # Example 5: Count zones at different levels
    print("\n\n--- Example 5: Zone counts at different levels ---")
    print(f"{'Level':<8} {'# Zones':<15}")
    print("-"*25)
    for lvl in range(0, 8):
        zones = get_all_zones_at_level(dggrs, lvl)
        print(f"{lvl:<8} {len(zones):<15,}")
