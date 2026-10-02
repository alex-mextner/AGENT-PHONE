"""Add explicit bundled U1/0.4 profiles to separate unsliced project copies.
The generic 220-mm plates stay printer-neutral. No printer connection is used.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import tempfile
import zipfile
import numpy as np
import trimesh

HERE=Path(__file__).resolve().parent
ORCA=os.environ.get('ORCA','/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer')
PROFILES=Path(os.environ.get('ORCA_PROFILES','/Applications/OrcaSlicer.app/Contents/Resources/profiles/Snapmaker'))


def mesh_signature(path):
    scene=trimesh.load(path,force='scene')
    values=[]
    for name in scene.graph.nodes_geometry:
        transform,geom=scene.graph[name]
        mesh=scene.geometry[geom].copy(); mesh.apply_transform(transform)
        values.append([*mesh.extents.tolist(),float(mesh.volume)])
    return np.array(sorted(values))


def main():
    out=HERE/'plates'/'snapmaker-u1'; out.mkdir(exist_ok=True)
    machine=PROFILES/'machine/Snapmaker U1 (0.4 nozzle).json'
    process=PROFILES/'process/0.20 Standard @Snapmaker U1 (0.4 nozzle).json'
    reports=[]
    for source in sorted((HERE/'plates').glob('*.3mf')):
        kind='PETG' if source.stem=='rigid-parts' else 'TPU 95A'
        filament=PROFILES/f'filament/Snapmaker {kind} @U1.json'
        if not all(p.is_file() for p in (machine,process,filament)):
            raise FileNotFoundError('Set ORCA_PROFILES to the bundled Snapmaker preset directory')
        target=out/source.name
        with tempfile.TemporaryDirectory(prefix='agent-phone-u1-') as temp:
            cmd=[ORCA,'--datadir',temp,'--allow-newer-file','--arrange','0','--orient','0',
                 '--load-settings',str(machine)+';'+str(process),'--load-filaments',str(filament),
                 '--export-3mf',target.name,'--outputdir',str(out),str(source)]
            result=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
            if result.returncode:
                raise RuntimeError(result.stdout+'\n'+result.stderr)
        with zipfile.ZipFile(target) as z:
            entries={n:z.read(n) for n in z.namelist()}
        if any(n.endswith('.gcode') for n in entries):
            raise RuntimeError('Delivery project unexpectedly contains executable printer G-code')
        key='Metadata/project_settings.config'
        config=json.loads(entries[key])
        config.update({'wall_loops':'4','sparse_infill_density':'95%','enable_support':'0'})
        entries[key]=(json.dumps(config,indent=2)+'\n').encode()
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for name,data in entries.items(): z.writestr(name,data)
        before,after=mesh_signature(source),mesh_signature(target)
        if before.shape!=after.shape or not np.allclose(before,after,rtol=1e-5,atol=.01):
            raise RuntimeError(f'{source.name}: profile export changed geometry or orientation')
        scene=trimesh.load(target,force='scene'); boxes=[]
        for node in scene.graph.nodes_geometry:
            transform,geom=scene.graph[node]
            mesh=scene.geometry[geom].copy(); mesh.apply_transform(transform)
            if np.min(mesh.bounds[0,:2]) < -.01 or np.max(mesh.bounds[1,:2]) > 270.6:
                raise RuntimeError('Configured project extends beyond U1 bed')
            boxes.append(mesh.bounds)
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                extent=np.minimum(a[1,:2],b[1,:2])-np.maximum(a[0,:2],b[0,:2])
                if np.all(extent>.01):
                    raise RuntimeError('Configured project has overlapping part footprints')
        reports.append({'file':str(target.relative_to(HERE)), 'material':kind,
            'machine':'Snapmaker U1 (0.4 nozzle)', 'layer_height_mm':.2,
            'walls':4,'infill_percent':95,'supports_enabled':False,
            'geometry_orientation_preserved':True,'part_count':len(boxes),
            'printer_job_sent':False,'contains_sliced_gcode':False,
            'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
            'preset_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (machine,process,filament)}})
        print('CONFIGURED_UNSLICED_PROJECT',target.name,flush=True)
    (HERE/'qa'/'configured-projects.json').write_text(json.dumps(reports,indent=2)+'\n')


if __name__=='__main__':
    main()
