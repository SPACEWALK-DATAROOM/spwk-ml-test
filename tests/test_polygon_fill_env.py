
import sys as _contract_sys
from pathlib import Path as _contract_Path

_contract_sys.path.insert(0, str(_contract_Path(__file__).resolve().parents[1] / 'tests/file50_python/pipeline'))

import unittest

from shapely import geometry

from loader import load
coords_to_polygon=load('spwkml/polygon_fill_test/polygon_fill_env.py',['coords_to_polygon'],'PolygonFillEnv',geometry=geometry)['coords_to_polygon']


class PolygonFillEnvironmentTests(unittest.TestCase):
    def setUp(self):
        if self._testMethodName == "test_coordinate_conversion_rejects_out_of_bounds_or_mismatched_points":
            return
        from spwkml import PolygonFillEnv
        self.env = PolygonFillEnv()

    def test_valid_placement_advances_counters_and_records_one_patch(self):
        result = self.env.step(0, 0, 0)

        self.assertTrue(result["is_valid"])
        self.assertEqual(result["n_steps"], 1)
        self.assertEqual(result["n_patches"], 1)
        self.assertEqual(self.env.n_steps, 1)
        self.assertEqual(self.env.n_patches, 1)
        self.assertEqual(result["area_out_of_space"], 0)
        self.assertEqual(result["area_intersect_patches"], 0)

    def test_overlapping_patch_is_rejected_but_counts_as_a_step(self):
        self.env.step(0, 0, 0)

        result = self.env.step(0, 0, 0)

        self.assertFalse(result["is_valid"])
        self.assertGreater(result["area_intersect_patches"], 12)
        self.assertEqual(result["area_out_of_space"], 0)
        self.assertEqual(result["n_steps"], 2)
        self.assertEqual(result["n_patches"], 1)

    def test_out_of_space_patch_is_rejected_without_adding_patch(self):
        result = self.env.step(10, 0, 0)

        self.assertFalse(result["is_valid"])
        self.assertGreater(result["area_out_of_space"], 0)
        self.assertEqual(result["area_intersect_patches"], 0)
        self.assertEqual(result["n_steps"], 1)
        self.assertEqual(result["n_patches"], 0)

    def test_select_space_resets_step_and_placement_state(self):
        self.env.step(0, 0, 0)

        self.env.select_space(1)

        self.assertEqual(self.env.n_steps, 0)
        self.assertEqual(self.env.n_patches, 0)

    def test_step_rejects_non_numeric_and_out_of_range_actions(self):
        invalid_actions = [
            (("0", 0, 0), TypeError),
            ((10.1, 0, 0), ValueError),
            ((0, -10.1, 0), ValueError),
            ((0, 0, 2), ValueError),
        ]

        for action, error in invalid_actions:
            with self.subTest(action=action):
                with self.assertRaises(error):
                    self.env.step(*action)
                self.assertEqual(self.env.n_steps, 0)
                self.assertEqual(self.env.n_patches, 0)

    def test_coordinate_conversion_rejects_out_of_bounds_or_mismatched_points(self):
        poly=coords_to_polygon(None, [-10,10,0],[-10,-10,10])
        self.assertEqual(poly.area,200)
        with self.assertRaisesRegex(ValueError, "Coordinates are wrong"):
            coords_to_polygon(None, [-11, 0, 0], [0, 1, -1])

        with self.assertRaisesRegex(ValueError, "Coordinates are wrong"):
            coords_to_polygon(None, [0, 1], [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
