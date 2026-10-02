#!/usr/bin/env python3
"""Regenerate closed inert mockup, real solids, print poses and verification.
Requires numpy, trimesh and manifold3d; see requirements.txt. Units are mm.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection, Mesh, OpType

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mockup_params as P


def rounded(w, length, radius):
    return CrossSection.square((w-2*radius, length-2*radius), True).offset(radius, circular_segments=32)


def plate(w, length, z0, z1, radius=3):
    return rounded(w, length, radius).extrude(z1-z0).translate((0,0,z0))


def cylinder(radius, z0, z1, x=0, y=0, segments=48):
    return Manifold.cylinder(z1-z0,radius,radius,segments).translate((x,y,z0))


def build_tray():
    solid = plate(44,92,P.TRAY_BOTTOM_Z,P.TOP_Z,5)
    solid -= plate(38,84,P.FLOOR_Z,16,4)
    for x,y in P.SCREW_XY:
        solid += cylinder(P.BOSS_RADIUS,P.TRAY_BOTTOM_Z,P.LID_BOTTOM_Z,x,y)
    solid -= plate(40.4,88.4,P.LID_BOTTOM_Z,16,4.2)
    for x,y in P.SCREW_XY:
        solid -= cylinder(P.CLEARANCE_DIA/2,7,16,x,y)
    return solid


def build_lid():
    solid = plate(40,88,P.LID_BOTTOM_Z,P.TOP_Z,4)
    for x,y in P.SCREW_XY:
        solid -= cylinder(1.7,12,16,x,y)
        sink = Manifold.cylinder(1.3,1.7,3.0,48).translate((x,y,13.5))
        solid -= sink + cylinder(3,14.8,16,x,y)
    return solid


def build_base():
    solid = plate(40,36,P.BASE_BOTTOM_Z,P.BASE_TOP_Z,4)
    for x,y in P.SCREW_XY:
        solid -= cylinder(1.7,1,7,x,y)
        solid -= cylinder(P.NUT_POCKET_AF/math.sqrt(3),1,P.NUT_TOP_Z,x,y,6)
    return solid


def mesh_solid(vertices, faces):
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    mesh.fix_normals()
    if not mesh.is_watertight or mesh.volume <= 0:
        raise ValueError('Loft is not a closed positive-volume mesh')
    result = Manifold(Mesh(np.asarray(mesh.vertices,dtype=np.float32),
                           np.asarray(mesh.faces,dtype=np.uint32)))
    if str(result.status()) != 'Error.NoError':
        raise ValueError(f'Invalid loft: {result.status()}')
    return result


def loft(points, widths, thicknesses, front=-14.0, bevel=.35):
    vertices, faces = [], []
    for i,(x,z) in enumerate(points):
        delta = np.asarray(points[min(i+1,len(points)-1)])-points[max(0,i-1)]
        tangent = delta/np.linalg.norm(delta)
        normal = np.array((-tangent[1],tangent[0]))
        half, w = thicknesses[i]/2, widths[i]
        r = min(bevel, half*.35)
        section = ((-half+r,0),(half-r,0),(half,r),(half,w-r),
                   (half-r,w),(-half+r,w),(-half,w-r),(-half,r))
        for offset,y in section:
            q = np.array((x,z))+offset*normal
            vertices.append((q[0],front+y,q[1]))
        if i:
            for j in range(8):
                a,b,c,d=(i-1)*8+j,(i-1)*8+(j+1)%8,i*8+(j+1)%8,i*8+j
                faces.extend(((a,b,c),(a,c,d)))
    for base, reverse in ((0,True),((len(points)-1)*8,False)):
        for j in range(1,7):
            tri=(base,base+j,base+j+1)
            faces.append(tuple(reversed(tri)) if reverse else tri)
    return mesh_solid(vertices,faces)


def ellipse_point(profile, degrees):
    width, depth = P.PROFILES[profile]
    a,b = width/2+P.CUFF_CLEARANCE,depth/2+P.CUFF_CLEARANCE
    t=math.radians(degrees)
    inner=np.array((a*math.sin(t),-depth/2+b*math.cos(t)))
    normal=np.array((math.sin(t)/a,math.cos(t)/b))
    normal/=np.linalg.norm(normal)
    return inner+P.CUFF_THICKNESS/2*normal


def build_cuff(profile, side='right'):
    width,depth=P.PROFILES[profile]
    outer_x=width/2+P.CUFF_CLEARANCE+P.CUFF_THICKNESS/2
    # A quarter ellipse gives a bounded-radius neck, unlike a reversing Bezier.
    transition=[np.array((20+(outer_x-20)*math.sin(t),
                         -depth/2+(depth/2+7.2)*math.cos(t)))
                for t in np.linspace(0,math.pi/2,60)]
    points=transition+[ellipse_point(profile,t) for t in np.linspace(90,125,35)[1:]]
    distance=np.r_[0,np.cumsum([np.linalg.norm(b-a) for a,b in zip(points,points[1:])])]
    fraction=distance/distance[-1]
    widths=[12+16*math.sin(math.pi*f)**1.35 for f in fraction]
    blend=np.minimum(1,fraction*4)
    thicknesses=[2+t*t*(3-2*t) for t in blend]
    terminal=(points[-1]-points[-2]); terminal/=np.linalg.norm(terminal)
    points.append(points[-1]+.45*terminal)
    widths.append(11.3); thicknesses.append(2.3)
    prefix=[(x,7.2) for x in (8,10,12,14,16,17,18,19)]
    prefix_widths=[28,28,28,28,28,24,16,12]
    solid=loft(prefix+points,prefix_widths+widths,[2.0]*len(prefix)+thicknesses)
    theta=np.linspace(0,2*math.pi,48,endpoint=False)
    hole=CrossSection.hull_points([(1.7*math.cos(t),1.7*math.sin(t)) for t in theta]+[(0,2.45)])
    for y in (-9,9):
        solid-=hole.extrude(12).translate((12,y,5))
    return solid if side=='right' else solid.mirror((1,0,0))


def build_gauge(profile):
    points=[ellipse_point(profile,t) for t in np.linspace(-125,125,130)]
    solid=loft(points,[6.0]*len(points),[3.0]*len(points),front=-3)
    solid+=plate(40,6,0,3.4,1)
    return solid


def build_pad():
    # Full height1.4; the upper0.2mm pocket accommodates adhesive without extra stack.
    return plate(40,36,0,1.4,4)-plate(30,26,1.2,1.5,3)


def build_adhesive():
    return plate(30,26,1.2,1.4,3)


def build_ballast():
    solid=plate(37,83,P.BALLAST_BOTTOM_Z,P.BALLAST_BOTTOM_Z+P.BALLAST_THICKNESS,3.5)
    for x,y in P.SCREW_XY:
        solid-=cylinder(4.1,9,13,x,y)
    return solid


def hardware():
    result={}
    bottom=P.SCREW_HEAD_TOP_Z-P.SCREW_LENGTH_MM
    for index,(x,y) in enumerate(P.SCREW_XY,1):
        screw=cylinder(1.5,bottom,13.3,x,y)
        screw+=Manifold.cylinder(1.3,1.5,2.8,48).translate((x,y,13.3))
        nut=cylinder(P.NUT_AF/math.sqrt(3),P.NUT_TOP_Z-P.NUT_HEIGHT,P.NUT_TOP_Z,x,y,6)
        nut-=cylinder(1.55,2,5,x,y)
        result[f'screw_{index}']=screw
        result[f'nut_{index}']=nut
    return result


def wrist_solid(profile):
    width,depth=P.PROFILES[profile]
    return CrossSection.circle(1,128).scale((width/2,depth/2)).extrude(130).rotate((90,0,0)).translate((0,65,-depth/2))


def build_assembly(profile='average'):
    if profile not in P.PROFILES:
        raise ValueError(f'Unknown nominal profile {profile!r}')
    return {'tray':build_tray(), 'lid':build_lid(), 'base':build_base(),
            'cuff_right':build_cuff(profile), 'cuff_left':build_cuff(profile,'left'),
            'ballast':build_ballast(), 'dorsal_pad':build_pad(), 'adhesive':build_adhesive(), **hardware()}


def to_trimesh(solid):
    mesh=solid.to_mesh()
    return trimesh.Trimesh(np.asarray(mesh.vert_properties)[:,:3],np.asarray(mesh.tri_verts),process=True)


def verify_assembly(profile):
    solids=build_assembly(profile)
    errors=[]
    for name,solid in solids.items():
        mesh=to_trimesh(solid)
        if not mesh.is_watertight or not mesh.is_winding_consistent or mesh.volume<=0:
            errors.append(f'{name}: invalid closed solid')
        if len(mesh.split(only_watertight=False))!=1:
            errors.append(f'{name}: disconnected bodies')
    intersections={}
    names=list(solids)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            volume=abs((solids[a]^solids[b]).volume())
            if volume>0.002:
                intersections[f'{a}/{b}']=round(volume,6)
    if intersections:
        errors.append({'unintended_overlap_mm3':intersections})
    wrist=wrist_solid(profile)
    for name,solid in solids.items():
        volume=abs((solid^wrist).volume())
        if volume>0.002:
            errors.append(f'{name}: wrist intrusion {volume:.5f} mm3')
    vertices=to_trimesh(solids['cuff_right']).vertices
    lower=vertices[vertices[:,2]<-P.PROFILES[profile][1]/2]
    opening=float(2*lower[:,0].min())
    end=P.SCREW_HEAD_TOP_Z-P.SCREW_LENGTH_MM
    engagement=P.NUT_TOP_Z-max(end,P.NUT_TOP_Z-P.NUT_HEIGHT)
    # Bearing material must survive below every head and above every captured nut.
    for x,y in P.SCREW_XY:
        seat=cylinder(2.6,12.65,13.30,x,y)-cylinder(1.9,12.6,13.4,x,y)
        roof=cylinder(2.7,5.05,6.05,x,y)-cylinder(1.9,5,6.1,x,y)
        if (solids['lid']^seat).volume()<seat.volume()*.995:
            errors.append('missing lid head bearing material')
        if (solids['base']^roof).volume()<roof.volume()*.995:
            errors.append('missing captured-nut reaction roof')
    gauge=build_gauge(profile)
    if abs((gauge^wrist).volume())>0.002:
        errors.append('fit gauge intersects nominal wrist')
    return {'profile':profile,'errors':errors,'underside_opening_mm':round(opening,3),
            'required_total_spread_mm':round(max(0,P.PROFILES[profile][0]+1-opening),3),
            'nut_thread_overlap_mm':round(engagement,3),
            'screw_end_recess_mm':round(end-P.BASE_BOTTOM_Z,3),
            'ballast_capacity_steel_g':round(solids['ballast'].volume()*.00785,3),
            'method':'volumetric Boolean interference of modeled closed solids; simplified thread envelopes, no strength/comfort certification'}


def ballast_for_target(measured_empty_g, target_g):
    if not all(math.isfinite(v) and v>=0 for v in (measured_empty_g,target_g)):
        raise ValueError('Masses must be finite and nonnegative')
    capacity=build_ballast().volume()*.00785
    extra=target_g-measured_empty_g
    if extra < -1e-8 or extra > capacity+1e-8:
        raise ValueError(f'Target outside measured-empty .. empty+{capacity:.2f} g capacity')
    return {'additional_mass_g':extra,'maximum_insert_mass_g':capacity,
            'approx_full_outline_steel_thickness_mm':extra/capacity*P.BALLAST_THICKNESS}


def export_print(name, solid, material, rotation=0):
    mesh=to_trimesh(solid)
    transform=trimesh.transformations.rotation_matrix(math.radians(rotation),(1,0,0))
    mesh.apply_transform(transform)
    shift=-mesh.bounds[0]
    mesh.apply_translation(shift)
    transform[:3,3]+=shift
    path=HERE/'parts'/f'{name}.stl'
    mesh.export(path)
    loaded=trimesh.load(path,force='mesh')
    if not loaded.is_watertight or len(loaded.split(only_watertight=False))!=1:
        raise ValueError(f'{name}: STL round trip invalid')
    if loaded.area_faces.min()<=1e-9 or not loaded.is_winding_consistent:
        raise ValueError(f'{name}: degenerate triangle or reversed winding')
    return {'file':str(path.relative_to(HERE)),'material':material,
            'print_to_assembly':np.linalg.inv(transform).round(9).tolist(),
            'bounds_mm':loaded.bounds.round(6).tolist(),
            'solid_volume_mm3':round(loaded.volume,3),
            'solid_fill_mass_estimate_g':round(loaded.volume/1000*P.DENSITY_G_CM3[material],3),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def generate_all():
    for folder in ('parts','qa','reference','renders','plates'):
        (HERE/folder).mkdir(exist_ok=True)
    reports={p:verify_assembly(p) for p in P.PROFILES}
    if any(r['errors'] for r in reports.values()):
        raise ValueError(json.dumps(reports,indent=2))
    # Remove only named superseded exports, already archived before redesign.
    for pattern in ('body.stl','cuff_blade_*.stl','coupon_*.stl','cal_cube.stl'):
        for path in (HERE/'parts').glob(pattern):
            path.unlink()
    parts={}
    for name,solid,rotation in (('tray',build_tray(),0),('lid',build_lid(),0),('base',build_base(),180)):
        parts[name]=export_print(name,solid,'PETG',rotation)
    parts['dorsal_pad']=export_print('dorsal_pad',build_pad(),'TPU')
    parts['calibration_10mm']=export_print('calibration_10mm',Manifold.cube((10,10,10)),'PETG')
    for profile in P.PROFILES:
        for side in ('left','right'):
            name=f'cuff_{side}_{profile}'
            parts[name]=export_print(name,build_cuff(profile,side),'TPU',90)
        name=f'fit_gauge_{profile}'
        parts[name]=export_print(name,build_gauge(profile),'TPU',90)
    manifest={'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('generate.py','mockup_params.py')},
              'module_mm_xyz':list(P.MODULE_MM),'closed_height_above_skin_mm':P.TOP_Z,
              'nominal_wrist_profiles_mm':P.PROFILES,'parts':parts,'verification':reports,
              'physical_print_or_wear_trial':'NOT PERFORMED',
              'mass_note':'Solid-fill CAD estimates, not slicer or measured masses; weigh the entire assembly including hardware.'}
    (HERE/'qa'/'assembly.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for profile in P.PROFILES:
        assembly=build_assembly(profile)
        folder=HERE/'reference'/profile
        folder.mkdir(exist_ok=True)
        scene=trimesh.Scene()
        for name,solid in assembly.items():
            mesh=to_trimesh(solid)
            mesh.export(folder/f'{name}.stl')
            mesh.visual.face_colors=([55,65,76,255] if 'cuff' in name else [145,157,174,255])
            scene.add_geometry(mesh,geom_name=name)
        scene.apply_scale(.001)  # glTF defines metres; STL files retain mm.
        scene.export(HERE/'reference'/f'assembly-{profile}-VIEW-ONLY.glb')
    outline=build_ballast().slice(10.5).to_polygons()
    paths=[]
    for poly in outline:
        paths.append('M '+' L '.join(f'{x+22:.4f},{46-y:.4f}' for x,y in poly)+' Z')
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="44mm" height="92mm" viewBox="0 0 44 92">'
    svg+='<path d="'+' '.join(paths)+'" fill="none" stroke="black" stroke-width="0.15"/></svg>\n'
    (HERE/'reference'/'steel-insert-cut-outline-1to1.svg').write_text(svg)
    print(json.dumps(reports,indent=2))
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mass',nargs=2,type=float,metavar=('MEASURED_EMPTY_G','TARGET_G'))
    args=parser.parse_args()
    if args.mass is not None:
        print(json.dumps(ballast_for_target(*args.mass),indent=2))
    else:
        generate_all()


if __name__=='__main__':
    main()
