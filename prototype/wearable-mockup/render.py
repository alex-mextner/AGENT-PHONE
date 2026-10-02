"""Blender renders of the ACTUAL exported print assembly, not beauty-model proxies.
Run Blender --background --python-exit-code 1 --python this_file.py.
"""
from pathlib import Path
import math
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent


def material(name,color,metallic=0,roughness=.45):
    m=bpy.data.materials.new(name); m.use_nodes=True
    node=m.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value=(*color,1)
    node.inputs['Metallic'].default_value=metallic
    node.inputs['Roughness'].default_value=roughness
    return m


def aim(obj,point):
    obj.rotation_euler=(Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()


def light(name,location,power,size,target):
    bpy.ops.object.light_add(type='AREA',location=location)
    obj=bpy.context.object; obj.name=name; obj.data.energy=power
    obj.data.shape='DISK'; obj.data.size=size; aim(obj,target)


def build(view):
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    rigid=material('Rigid PETG',(.29,.34,.40),.1)
    tpu=material('TPU open cuff',(.055,.065,.075),0,.72)
    steel=material('Recessed M3 hardware',(.38,.43,.48),.8,.25)
    ballast=material('Optional four-hole steel insert',(.20,.35,.37),.6)
    for path in sorted((HERE/'reference'/'average').glob('*.stl')):
        name=path.stem
        if name=='ballast' and view!='exploded':
            continue
        bpy.ops.wm.stl_import(filepath=str(path),global_scale=.001)
        obj=bpy.context.object; obj.name=name
        mat=tpu if 'cuff' in name or name=='dorsal_pad' else steel if name.startswith(('nut','screw')) else ballast if name=='ballast' else rigid
        obj.data.materials.clear(); obj.data.materials.append(mat)
        if view=='exploded':
            obj.location.z+=.034 if name.startswith('screw') else .029 if name=='lid' else .018 if name=='ballast' else .009 if name=='tray' else 0
    if view=='wrist-fit':
        skin=material('Nominal wrist gauge, not anatomy',(.52,.56,.60),0,.8)
        bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=1,depth=.15,
            rotation=(math.pi/2,0,0),location=(0,0,-.021))
        obj=bpy.context.object; obj.name='Nominal 58 x 42 mm wrist'
        obj.scale=(.029,.021,1); obj.data.materials.append(skin)
    target=(0,0,-.010 if view!='exploded' else .002)
    camera={'closed':(.14,-.18,.115),'underside':(.12,-.17,-.11),
            'exploded':(.16,-.19,.15),'wrist-fit':(.13,-.20,.075)}[view]
    bpy.ops.object.camera_add(location=camera)
    cam=bpy.context.object; cam.data.type='ORTHO'; cam.data.ortho_scale=.17
    aim(cam,target); bpy.context.scene.camera=cam
    cam.data.clip_start=.001; cam.data.clip_end=10
    light('Key',(.12,-.10,.20),9,.18,target)
    light('Fill',(-.16,.02,.06),5,.20,target)
    light('Underside fill',(.02,-.10,-.16),5,.16,target)
    light('Rim',(.08,.18,.17),7,.15,target)
    scene=bpy.context.scene
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.23,.25,.28,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value=.7
    scene.render.engine='CYCLES'; scene.cycles.samples=48; scene.cycles.use_denoising=True
    scene.render.resolution_x=1600; scene.render.resolution_y=1200
    scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'
    scene.view_settings.view_transform='AgX'
    scene.view_settings.look='AgX - Medium High Contrast'
    scene.unit_settings.system='METRIC'; scene.unit_settings.length_unit='MILLIMETERS'
    scene.render.filepath=str(HERE/'renders'/f'{view}.png')
    bpy.ops.render.render(write_still=True)
    print('CAD_RENDER',view,flush=True)


for view in ('closed','underside','exploded','wrist-fit'):
    build(view)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'renders'/'wearable-mockup.blend'),compress=True)
