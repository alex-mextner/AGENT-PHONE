"""Evaluated-mesh intersection queries for the geometry regression tests.

Everything here works on the evaluated depsgraph (modifiers, parenting and
tilt applied), never on declared dimensions or analytic clearance numbers.
"""
import bmesh
import bpy
from mathutils.bvhtree import BVHTree


def _world_bmesh(obj):
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(evaluated.matrix_world)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    evaluated.to_mesh_clear()
    return bm


def bvh_of(objects):
    """One world-space BVH over the evaluated triangles of all given objects."""
    bm = bmesh.new()
    for obj in objects:
        part = _world_bmesh(obj)
        offset = len(bm.verts)
        for v in part.verts:
            bm.verts.new(v.co)
        bm.verts.ensure_lookup_table()
        for face in part.faces:
            bm.faces.new([bm.verts[offset + v.index] for v in face.verts])
        part.free()
    tree = BVHTree.FromBMesh(bm)
    bm.free()
    return tree


def overlap_count(a_objects, b_objects):
    """Number of intersecting triangle pairs between two object groups."""
    bpy.context.view_layer.update()
    return len(bvh_of(a_objects).overlap(bvh_of(b_objects)))


def _one_way_gap(a_objects, b_objects):
    tree = bvh_of(b_objects)
    best = float("inf")
    for obj in a_objects:
        part = _world_bmesh(obj)
        for v in part.verts:
            hit = tree.find_nearest(v.co)
            if hit[0] is not None:
                best = min(best, hit[3])
        part.free()
    return best


def min_gap(a_objects, b_objects):
    """Smallest vertex-to-surface distance between two groups, in metres.

    Checked in both directions so a sharp vertex of either group is seen.
    Raises if either group has no geometry (inf would pass any minimum).
    """
    bpy.context.view_layer.update()
    best = min(_one_way_gap(a_objects, b_objects), _one_way_gap(b_objects, a_objects))
    if best == float("inf"):
        raise ValueError("min_gap: empty geometry")
    return best
