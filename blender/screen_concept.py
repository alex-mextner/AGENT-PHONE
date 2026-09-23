import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "blender" / "ui"
OUT = ROOT / "renders"
OUT.mkdir(parents=True, exist_ok=True)

# ---- scene helpers ----

def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for data in (bpy.data.materials, bpy.data.curves, bpy.data.meshes, bpy.data.cameras, bpy.data.lights):
        pass

def mat(name, color, metallic=0.0, rough=0.45, emission=None, strength=1.0):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Metallic"].default_value=metallic
    bs.inputs["Roughness"].default_value=rough
    if emission:
        bs.inputs["Emission Color"].default_value=(*emission,1)
        bs.inputs["Emission Strength"].default_value=strength
    return m

def rounded_box(name, loc, dims, material, bevel=0.003, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o=bpy.context.object; o.name=name
    o.dimensions=dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    b=o.modifiers.new("soft edges","BEVEL"); b.width=min(bevel,min(dims)/2.2); b.segments=5
    o.data.materials.append(material)
    return o

def cylinder(name, loc, radius, depth, material, axis='X'):
    rot=(0,math.pi/2,0) if axis=='X' else ((math.pi/2,0,0) if axis=='Y' else (0,0,0))
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; o.data.materials.append(material); return o

def look_at(obj, point):
    direction=Vector(point)-obj.location
    obj.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()

def image_material(name, path):
    m=bpy.data.materials.new(name); m.use_nodes=True
    nodes=m.node_tree.nodes; links=m.node_tree.links
    for n in list(nodes): nodes.remove(n)
    out=nodes.new("ShaderNodeOutputMaterial")
    em=nodes.new("ShaderNodeEmission")
    tex=nodes.new("ShaderNodeTexImage")
    tex.image=bpy.data.images.load(str(path), check_existing=True)
    tex.interpolation='Linear'
    links.new(tex.outputs["Color"],em.inputs["Color"])
    links.new(em.outputs["Emission"],out.inputs["Surface"])
    em.inputs["Strength"].default_value=1.3
    return m

def ui_plane(texture, parent, angle_rad):
    # Plane center follows the screen center around the same hinge pivot.
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0,0,0))
    p=bpy.context.object; p.name="Emissive UI"
    p.dimensions=(0.097,0.030,1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    p.location=(0,0.018,0.00372)
    p.data.materials.append(image_material("UI-"+texture, UI/f"{texture}.png"))
    p.parent=parent
    return p

def screen_module(texture, angle_deg=0, detached_z=0):
    metal=mat("Titanium",(0.08,0.095,0.115),0.85,0.22)
    glass=mat("Glass rim",(0.012,0.016,0.022),0.15,0.12)
    pivot=bpy.data.objects.new("Tilt pivot",None); bpy.context.collection.objects.link(pivot)
    pivot.location=(0,-0.018,0.034+detached_z)
    pivot.rotation_euler.x=math.radians(angle_deg)
    frame=rounded_box("Display module",(0,0.018,0),(0.104,0.038,0.0058),metal,0.004)
    frame.parent=pivot
    bezel=rounded_box("Borderless glass",(0,0.018,0.0030),(0.101,0.0342,0.0012),glass,0.004)
    bezel.parent=pivot
    ui_plane(texture,pivot,math.radians(angle_deg))
    return pivot

def create_wrist():
    skin=mat("Skin",(0.47,0.235,0.14),0.0,0.58)
    # Forearm along Y
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1, depth=0.19, location=(0,-0.025,0), rotation=(math.pi/2,0,0))
    arm=bpy.context.object; arm.name="Wrist and forearm"
    arm.scale=(0.035,0.028,1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    arm.data.materials.append(skin)
    # Hand mass
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=(0,0.105,-0.001))
    hand=bpy.context.object; hand.name="Hand"
    hand.scale=(0.041,0.062,0.027); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    hand.data.materials.append(skin)

def create_base_and_strap(exploded=False):
    dark=mat("Base",(0.035,0.042,0.052),0.45,0.30)
    wingmat=mat("Battery wings",(0.06,0.07,0.082),0.58,0.27)
    strapmat=mat("Soft strap",(0.018,0.021,0.026),0.0,0.82)
    carrier=mat("Carrier",(0.12,0.135,0.15),0.75,0.25)
    gold=mat("Contacts",(0.65,0.40,0.08),0.75,0.24)

    base_z=0.030
    rounded_box("Main battery base",(0,0,base_z),(0.070,0.034,0.005),dark,0.004)

    # Battery wings are ABOVE/BELOW the screen in top view, continuing into strap.
    for sign in (-1,1):
        y=sign*0.031
        rot_x=sign*math.radians(18)
        rounded_box(f"Battery wing {'top' if sign>0 else 'bottom'}",(0,y,0.026),(0.052,0.027,0.0058),wingmat,0.005,rot=(rot_x,0,0))
        sy=sign*0.064
        rounded_box(f"Soft strap {'top' if sign>0 else 'bottom'}",(0,sy,0.016),(0.027,0.048,0.0038),strapmat,0.003,rot=(sign*math.radians(24),0,0))

    zc=0.0334 + (0.010 if exploded else 0)
    rounded_box("Thin tilt carrier",(0,0,zc),(0.074,0.031,0.0014),carrier,0.002)

    # Two tiny recessed hinge barrels, not one giant hinge.
    for x in (-0.025,0.025):
        cylinder("Micro hinge", (x,-0.0174,0.0328),0.00125,0.018,carrier,'X')

    # Visible pogo contacts in exploded mechanism only.
    if exploded:
        for x in (-0.015,-0.005,0.005,0.015):
            cylinder("Pogo contact",(x,-0.006,0.041),0.0008,0.002,gold,'Z')

def setup_world():
    world=bpy.context.scene.world
    world.color=(0.008,0.010,0.014)
    world.use_nodes=True
    bg=world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value=(0.006,0.008,0.012,1)
    bg.inputs["Strength"].default_value=0.12

def add_lighting():
    def area(name,loc,energy,size,color):
        bpy.ops.object.light_add(type='AREA', location=loc)
        l=bpy.context.object; l.name=name; l.data.energy=energy; l.data.shape='DISK'; l.data.size=size; l.data.color=color
        look_at(l,(0,0,0.025))
    area("Key",(0.12,-0.11,0.17),2.6,0.12,(1.0,0.91,0.82))
    area("Fill",(-0.13,-0.02,0.10),1.1,0.10,(0.72,0.82,1.0))
    area("Rim",(0.02,0.16,0.14),1.8,0.09,(0.58,0.72,1.0))

def camera_for(kind):
    if kind=="side":
        loc=(0.14,-0.005,0.075); target=(0,0,0.030); lens=70
    elif kind=="exploded":
        loc=(0.125,-0.145,0.125); target=(0,0,0.045); lens=68
    else:
        loc=(0.135,-0.155,0.125); target=(0,0.008,0.028); lens=67
    bpy.ops.object.camera_add(location=loc)
    cam=bpy.context.object; cam.data.lens=lens
    look_at(cam,target)
    bpy.context.scene.camera=cam

def ground():
    m=mat("Ground",(0.022,0.025,0.032),0.0,0.62)
    rounded_box("Ground",(0,0,-0.037),(0.42,0.42,0.008),m,0.01)

def render_scene(name, texture="home", angle=14, side=False):
    clear(); setup_world(); add_lighting(); ground(); create_wrist(); create_base_and_strap(False)
    screen_module(texture, angle)
    camera_for("side" if side else "hero")
    scene=bpy.context.scene
    scene.render.engine='BLENDER_EEVEE'
    scene.render.resolution_x=1280; scene.render.resolution_y=800; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.film_transparent=False
    scene.render.filepath=str(OUT/f"{name}.png")
    scene.render.image_settings.color_mode='RGBA'
    scene.view_settings.look='AgX - Medium High Contrast'
    bpy.ops.render.render(write_still=True)

def render_exploded():
    clear(); setup_world(); add_lighting(); ground()
    create_base_and_strap(True)
    # Display floats above carrier; still uses compact hinge below.
    screen_module("home",0,detached_z=0.032)
    # add simple detached reserve-cell slab inside module zone
    battery=mat("Reserve cell",(0.23,0.31,0.34),0.25,0.35)
    rounded_box("Small reserve cell",(0,-0.005,0.057),(0.048,0.020,0.0024),battery,0.002)
    camera_for("exploded")
    scene=bpy.context.scene
    scene.render.engine='BLENDER_EEVEE'
    scene.render.resolution_x=1280; scene.render.resolution_y=800; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.filepath=str(OUT/"mechanism-exploded.png")
    scene.view_settings.look='AgX - Medium High Contrast'
    bpy.ops.render.render(write_still=True)

# Render all UI states on wrist.
render_scene("hero-home","home",18)
render_scene("tilted-chat","chat",42)
render_scene("marketplace","marketplace",24)
render_scene("split-chat-photos","split",20)
render_scene("remote-control","remote",20)
render_scene("blind-input","blind-input",12)
render_scene("side-profile","home",55,side=True)
render_exploded()

# Rebuild hero and save source blend.
clear(); setup_world(); add_lighting(); ground(); create_wrist(); create_base_and_strap(False); screen_module("home",18); camera_for("hero")
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"screen-concept.blend"))
print("Rendered:", OUT)
