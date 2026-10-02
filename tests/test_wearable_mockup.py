"""Actual exported-solid contracts; no comfort or physical-strength claim."""
import importlib.util
import json
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOCK = ROOT / 'prototype' / 'wearable-mockup'
sys.path.insert(0, str(MOCK))


def generator():
    spec = importlib.util.spec_from_file_location('wearable_generator', MOCK/'generate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WearableMechanicalContracts(unittest.TestCase):
    def test_complete_assembly_contract_exists(self):
        g = generator()
        self.assertTrue(hasattr(g, 'build_assembly'), 'complete assembly builder missing')
        self.assertTrue(hasattr(g, 'verify_assembly'), 'real assembly verifier missing')

    def test_export_manifest_contains_paired_cuffs_and_full_gauges(self):
        path = MOCK/'qa'/'assembly.json'
        self.assertTrue(path.exists(), 'new print/assembly transform manifest missing')
        if not path.exists():
            return
        data = json.loads(path.read_text())
        self.assertEqual(data['module_mm_xyz'], [44.0, 92.0, 6.6])
        self.assertAlmostEqual(data['closed_height_above_skin_mm'], 14.8)
        for profile in ('slim', 'average', 'large'):
            for side in ('left', 'right'):
                self.assertIn(f'cuff_{side}_{profile}', data['parts'])
            self.assertIn(f'fit_gauge_{profile}', data['parts'])

    def test_real_solid_assembly_and_hardware(self):
        g = generator()
        self.assertTrue(hasattr(g, 'verify_assembly'))
        if not hasattr(g, 'verify_assembly'):
            return
        for profile in ('slim', 'average', 'large'):
            report = g.verify_assembly(profile)
            self.assertEqual(report['errors'], [], (profile, report))
            self.assertGreaterEqual(report['nut_thread_overlap_mm'], 2.0)
            self.assertGreaterEqual(report['screw_end_recess_mm'], 0.25)
            self.assertGreater(report['underside_opening_mm'], 40)
            self.assertLess(report['underside_opening_mm'], 64)

    def test_mass_capacity_rejects_impossible_loads(self):
        g = generator()
        self.assertTrue(hasattr(g, 'ballast_for_target'))
        if hasattr(g, 'ballast_for_target'):
            with self.assertRaises(ValueError):
                g.ballast_for_target(45, 200)

    def test_exported_meshes_and_assembly_transforms(self):
        import numpy as np
        import trimesh
        import hashlib
        data=json.loads((MOCK/'qa/assembly.json').read_text())
        for name,record in data['parts'].items():
            path=MOCK/record['file']; mesh=trimesh.load(path,force='mesh')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),record['sha256'],name)
            self.assertTrue(mesh.is_watertight and mesh.is_winding_consistent,name)
            self.assertEqual(len(mesh.split(only_watertight=False)),1,name)
            self.assertGreater(mesh.area_faces.min(),1e-9,name)
            self.assertGreater(mesh.volume,0,name)
            self.assertAlmostEqual(mesh.bounds[0,2],0,delta=1e-5,msg=name)
            self.assertTrue(np.all(mesh.extents[:2]<204),name)
            mesh.apply_transform(np.array(record['print_to_assembly']))
            if name in ('tray','lid'):
                self.assertAlmostEqual(mesh.bounds[1,2],14.8,delta=1e-4,msg=name)
            if name.startswith('cuff_'):
                self.assertAlmostEqual(mesh.extents[1],28,delta=.05,msg=name)
                self.assertLess(max(abs(mesh.bounds[:,1])),15,name)
            if name.startswith('fit_gauge_'):
                self.assertGreater(mesh.extents[0],60,name)
                self.assertLess(mesh.extents[1],6.01,name)

    def test_mass_boundaries_are_not_safety_limits(self):
        g=generator(); self.assertEqual(g.ballast_for_target(45,45)['additional_mass_g'],0)
        for a,b in ((45,44),(float('nan'),80),(45,float('inf')),(-1,40)):
            with self.assertRaises(ValueError):
                g.ballast_for_target(a,b)

    def test_collision_verifier_rejects_a_displaced_lid(self):
        from unittest.mock import patch
        g=generator(); original=g.build_lid
        with patch.object(g,'build_lid',lambda: original().translate((0,0,-.6))):
            report=g.verify_assembly('average')
        self.assertTrue(report['errors'], 'negative-control collision was missed')

    def test_export_report_is_bound_to_current_source(self):
        import hashlib
        data=json.loads((MOCK/'qa/assembly.json').read_text())
        for name in ('generate.py','mockup_params.py'):
            self.assertEqual(data['source_sha256'][name],hashlib.sha256((MOCK/name).read_bytes()).hexdigest())
