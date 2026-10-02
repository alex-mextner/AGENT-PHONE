"""Reproducible inert size-study meshes. STL coordinates are millimetres."""
import csv
import math
from pathlib import Path
import struct
from blender.design_geometry import DISPLAY_OUTER_MM, rounded_outline


def prism(outline, height):
    if not math.isfinite(height) or height <= 0:
        raise ValueError('height must be positive and finite')
    n = len(outline)
    vertices = [(x,y,z) for z in (0.0,height) for x,y in outline]
    cx = sum(p[0] for p in outline)/n
    cy = sum(p[1] for p in outline)/n
    vertices += [(cx,cy,0.0), (cx,cy,height)]
    faces = []
    for i in range(n):
        j = (i+1)%n
        faces += [(i,j,j+n), (i,j+n,i+n), (2*n,j,i), (2*n+1,i+n,j+n)]
    return vertices, faces


def dummy_mesh(height=6.6):
    long, short, _ = DISPLAY_OUTER_MM
    outline = rounded_outline(long, short, 5.0)
    return prism([(x+long/2,y+short/2) for x,y in outline], height)


def triangle_normal(vertices, face):
    a,b,c = (vertices[i] for i in face)
    u = [b[i]-a[i] for i in range(3)]
    v = [c[i]-a[i] for i in range(3)]
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def triangle_area(vertices, face):
    return math.sqrt(sum(x*x for x in triangle_normal(vertices,face)))/2


def write_stl(path, mesh):
    vertices, faces = mesh
    with Path(path).open('wb') as file:
        file.write(b'AGENT inert size dummy; units mm; not a validated wearable'.ljust(80,b' '))
        file.write(struct.pack('<I',len(faces)))
        for face in faces:
            normal = triangle_normal(vertices,face)
            length = math.sqrt(sum(v*v for v in normal))
            normal = tuple(v/length for v in normal)
            coords = tuple(v for i in face for v in vertices[i])
            file.write(struct.pack('<12fH', *normal, *coords, 0))


def generate_kit(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for height in (6.6,10.0,14.0):
        write_stl(folder/f'dummy-92x44x{height:g}mm.stl', dummy_mesh(height))
    write_stl(folder/'calibration-10mm.stl', prism([(0,0),(10,0),(10,10),(0,10)],10))
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="150mm" height="100mm" viewBox="0 0 150 100">
<rect x="8" y="8" width="92" height="44" rx="5" fill="none" stroke="black" stroke-width="0.3"/>
<text x="8" y="60" font-size="4">AGENT module footprint 92 x 44 mm</text>
<rect x="8" y="70" width="10" height="10" fill="none" stroke="black" stroke-width="0.3"/>
<text x="23" y="77" font-size="3.5">Verify this square is 10 x 10 mm. Print at 100%.</text>
<text x="8" y="92" font-size="3">Inert fit study only. Cuff and total height are additional.</text></svg>'''
    (folder/'template-1to1.svg').write_text(svg+'\n')
    with (folder/'wear-diary.csv').open('w',newline='') as file:
        csv.writer(file).writerow(['date','participant_code','configuration','wrist_width_mm',
            'wrist_thickness_mm','module_height_mm','total_height_above_skin_mm','total_mass_g',
            'mass_distribution','wear_minutes','task','clothing','snags','opposite_hand_uses',
            'task_errors','comfort_0_to_10','movement_restriction_0_to_10','removal_reason',
            'phone_access_category','notes'])
    return folder


if __name__ == '__main__':
    print(generate_kit(Path(__file__).resolve().parents[1]/'prototype'/'fit-kit'))
