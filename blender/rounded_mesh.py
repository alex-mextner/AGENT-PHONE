"""True rounded planforms, independent of plate thickness (all units metres)."""
import bpy
from blender.design_geometry import rounded_outline


def rounded_plate(name, location, dimensions, mat, radius=0.005):
    width, length, height = dimensions
    outline = rounded_outline(width, length, radius)
    count = len(outline)
    vertices = [(x, y, z) for z in (-height/2, height/2) for x, y in outline]
    faces = [tuple(reversed(range(count))), tuple(range(count, 2*count))]
    faces += [(i, (i+1)%count, (i+1)%count+count, i+count) for i in range(count)]
    mesh = bpy.data.meshes.new(name+' Mesh')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(mat)
    for face in mesh.polygons:
        face.use_smooth = len(face.vertices) == 4
    edge = obj.modifiers.new('Soft edge', 'BEVEL')
    edge.width = min(0.00012, height/5)
    edge.segments = 3
    return obj


def rounded_surface(name, dimensions, mat, radius=0.0042):
    width, length = dimensions
    outline = rounded_outline(width, length, radius)
    mesh = bpy.data.meshes.new(name+' Mesh')
    mesh.from_pydata([(x,y,0) for x,y in outline], [], [tuple(range(len(outline)))])
    mesh.update()
    uv = mesh.uv_layers.new(name='UVMap')
    for loop in mesh.loops:
        x, y, _ = mesh.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = (x/width+0.5, y/length+0.5)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj
