#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: Get vertex coordinates (lon/lat) and centroid from a cell ID
Based on examples from bindings_examples/py/geom.py
"""

from dggal import *

# Initialize the application
app = Application(appGlobals=globals())
pydggal_setup(app)

def get_cell_vertices(dggrs, cell_id, refined=False, refinement_level=0):
    """
    Get all vertex coordinates (lon/lat) for a given cell ID

    Args:
        dggrs: DGGRS instance (e.g., ISEA3H())
        cell_id: Cell ID as string (e.g., 'A4-0-A')
        refined: If True, use refined vertices with densification. If False, return only actual cell vertices
        refinement_level: Edge refinement level (only used if refined=True). 0 = no refinement

    Returns:
        List of tuples containing (lon, lat) coordinates
    """
    # Convert cell ID to zone
    zone = dggrs.getZoneFromTextID(cell_id)

    if zone == nullZone:
        print(f"Error: Invalid cell ID '{cell_id}'")
        return None

    # Get WGS84 vertices (lon/lat coordinates)
    if refined:
        # Get refined vertices with densification (adds in-between points)
        vertices = dggrs.getZoneRefinedWGS84Vertices(zone, refinement_level)
    else:
        # Get only the actual cell vertices (no densification)
        vertices = dggrs.getZoneWGS84Vertices(zone)

    if not vertices:
        print(f"Error: Could not get vertices for cell ID '{cell_id}'")
        return None

    # Extract coordinates
    coords = []
    for i in range(vertices.count):
        lon = vertices[i].lon.value
        lat = vertices[i].lat.value
        coords.append((lon, lat))

    return coords

def get_cell_centroid(dggrs, cell_id):
    """
    Get the centroid (center point) coordinates (lon/lat) for a given cell ID

    Args:
        dggrs: DGGRS instance (e.g., ISEA3H())
        cell_id: Cell ID as string (e.g., 'A4-0-A')

    Returns:
        Tuple containing (lon, lat) coordinates of the centroid
    """
    # Convert cell ID to zone
    zone = dggrs.getZoneFromTextID(cell_id)

    if zone == nullZone:
        print(f"Error: Invalid cell ID '{cell_id}'")
        return None

    # Get WGS84 centroid (lon/lat coordinates)
    centroid = dggrs.getZoneWGS84Centroid(zone)

    return (centroid.lon.value, centroid.lat.value)

def print_cell_info(cell_id, vertices, centroid, refined=False):
    """Pretty print the vertices and centroid"""
    print(f"\nCell ID: {cell_id}")
    print(f"Number of vertices: {len(vertices)}")
    if refined:
        print("(Using refined vertices with densification)")
    else:
        print("(Using actual cell vertices only)")

    print("\n--- Centroid (Center Point) ---")
    print(f"  Lon: {centroid[0]:.6f}, Lat: {centroid[1]:.6f}")

    print("\n--- Vertex coordinates (lon, lat) ---")
    for i, (lon, lat) in enumerate(vertices):
        print(f"  Vertex {i}: ({lon:.6f}, {lat:.6f})")

if __name__ == "__main__":
    # Initialize DGGRS (using ISEA3H as example)
    dggrs = ISEA3H()

    # Example cell ID
    cell_id = 'A4-0-A'

    # Example 1: Get actual cell vertices only (no densification)
    print("\n--- Example 1: Actual cell vertices (no densification) ---")
    vertices = get_cell_vertices(dggrs, cell_id, refined=False)
    centroid = get_cell_centroid(dggrs, cell_id)

    if vertices and centroid:
        print_cell_info(cell_id, vertices, centroid, refined=False)

    # Example 2: Get refined vertices with densification
    print("\n\n" + "="*60)
    print("--- Example 2: Refined vertices (with densification) ---")
    vertices_refined = get_cell_vertices(dggrs, cell_id, refined=True, refinement_level=2)
    if vertices_refined:
        print(f"\nCell ID: {cell_id}")
        print(f"Number of refined vertices: {len(vertices_refined)}")
        print("(Using refined vertices with refinement_level=2)")
        print("\nFirst 10 refined vertices:")
        for i, (lon, lat) in enumerate(vertices_refined[:10]):
            print(f"  Vertex {i}: ({lon:.6f}, {lat:.6f})")
        if len(vertices_refined) > 10:
            print(f"  ... ({len(vertices_refined) - 10} more vertices)")

    # Example 3: Compare different cells
    print("\n\n" + "="*60)
    print("--- Example 3: Another cell ---")
    cell_id2 = 'A4-0-B'
    vertices2 = get_cell_vertices(dggrs, cell_id2, refined=False)
    centroid2 = get_cell_centroid(dggrs, cell_id2)
    if vertices2 and centroid2:
        print_cell_info(cell_id2, vertices2, centroid2, refined=False)
