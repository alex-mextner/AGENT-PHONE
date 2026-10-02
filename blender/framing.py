"""Frame measured geometry, not a guessed camera distance."""
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view


def fit_scene_camera(built, margin=0.06):
    scene = bpy.context.scene
    bpy.context.view_layer.update()
    objects = list(built['objects'].values())
    excluded = {'Context Wall','Media Console','Desk','Studio floor'}
    objects += [o for o in built.get('context_objects',[]) if o.name not in excluded]
    objects += [o for o in scene.objects if o.type == 'FONT']
    points = [o.matrix_world @ Vector(c) for o in objects for c in o.bound_box]
    if built.get('human'):
        human = built['human']['object'].evaluated_get(bpy.context.evaluated_depsgraph_get())
        hand = [human.matrix_world @ v.co for v in human.data.vertices]
        points += [p for p in hand if -.07 < p.y < .29 and abs(p.x) < .105 and abs(p.z) < .10]
    camera = scene.camera
    for _ in range(24):
        bpy.context.view_layer.update()
        p = [world_to_camera_view(scene,camera,v) for v in points]
        if min(v.z for v in p) <= 0:
            raise ValueError('Cannot frame geometry behind camera')
        left,right,bottom,top = min(v.x for v in p),max(v.x for v in p),min(v.y for v in p),max(v.y for v in p)
        if left >= margin-.0005 and right <= 1-margin+.0005 and bottom >= margin-.0005 and top <= 1-margin+.0005:
            return
        rotation = camera.matrix_world.to_3x3()
        frame = camera.data.view_frame(scene=scene)
        width = max(v.x for v in frame)-min(v.x for v in frame)
        height = max(v.y for v in frame)-min(v.y for v in frame)
        distance = sum(v.z for v in p)/len(p)
        if camera.data.type != 'ORTHO':
            width *= distance/abs(frame[0].z)
            height *= distance/abs(frame[0].z)
        dx,dy = (left+right)/2-.5, (bottom+top)/2-.5
        camera.location += rotation @ Vector((dx*width,dy*height,0))
        factor = max((right-left)/(1-2*margin),(top-bottom)/(1-2*margin),1.0)
        if camera.data.type == 'ORTHO':
            camera.data.ortho_scale *= factor*1.002
        else:
            camera.location += rotation @ Vector((0,0,distance*(factor*1.002-1)))
    raise RuntimeError(f'Camera framing failed: {(left,right,bottom,top)}')
