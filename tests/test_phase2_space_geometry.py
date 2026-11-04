"""Exercise sample-space selection and polygon-hole placement behavior."""

import unittest

from shapely import geometry

# This pinned source uses a Shapely 1 alias removed in Shapely 2.
if not hasattr(geometry, "asPolygon"):
    geometry.asPolygon = geometry.Polygon

from spwkml import PolygonFillEnv


class SpaceGeometryTests(unittest.TestCase):
    def setUp(self):
        self.env = PolygonFillEnv()

    def test_p2_space_01_selecting_a_different_outline_changes_placement_validity(self):
        self.env.select_space(1)
        outside_l_shape = self.env.step(0, 0, 0)

        self.assertFalse(outside_l_shape["is_valid"])
        self.assertGreater(outside_l_shape["area_out_of_space"], 0)
        self.assertEqual(outside_l_shape["n_steps"], 1)
        self.assertEqual(outside_l_shape["n_patches"], 0)

        self.env.select_space(2)
        inside_square = self.env.step(0, 0, 0)

        self.assertTrue(inside_square["is_valid"])
        self.assertEqual(inside_square["area_out_of_space"], 0)
        self.assertEqual(inside_square["n_steps"], 1)
        self.assertEqual(inside_square["n_patches"], 1)

    def test_p2_space_02_hole_excludes_center_but_allows_placement_outside_hole(self):
        self.env.select_space(3)

        hole_placement = self.env.step(0, 0, 0)
        valid_placement = self.env.step(0, 7, 0)

        self.assertFalse(hole_placement["is_valid"])
        self.assertGreater(hole_placement["area_out_of_space"], 0)
        self.assertTrue(valid_placement["is_valid"])
        self.assertEqual(valid_placement["area_out_of_space"], 0)
        self.assertEqual(valid_placement["n_steps"], 2)
        self.assertEqual(valid_placement["n_patches"], 1)


if __name__ == "__main__":
    unittest.main()
