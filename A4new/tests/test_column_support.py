"""Tests for the column support check.

The geometry tests use simple boxes and do not need IfcOpenShell.
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from column_support_check.src.geometry import Mesh
from column_support_check.src.support_check import (
    DIRECT_SUPPORT, NO_BEARING_ELEMENT, ON_BASE_SLAB,
    SUPPORTED_THROUGH_SLAB, UNSUPPORTED_SLAB, run_check,
)

BOX_FACES = [0, 2, 1, 0, 3, 2, 4, 5, 6, 4, 6, 7, 0, 1, 5, 0, 5, 4,
             1, 2, 6, 1, 6, 5, 2, 3, 7, 2, 7, 6, 3, 0, 4, 3, 4, 7]


def box(guid, ifc_type, x0, y0, z0, x1, y1, z1, predefined_type=""):
    corners = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
               (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    verts = [c for corner in corners for c in corner]
    return Mesh(guid, ifc_type, verts, BOX_FACES, name=guid, storey="S",
                predefined_type=predefined_type)


def column(guid, x, y, z0, z1, size=0.3):
    h = size / 2
    return box(guid, "IfcColumn", x - h, y - h, z0, x + h, y + h, z1)


class ColumnSupportTests(unittest.TestCase):
    """Two storeys: base slab at 0.0, floor slab from 3.00 to 3.25 m."""

    def setUp(self):
        self.base = box("BASE", "IfcSlab", -10, -10, -0.3, 30, 30, 0, "BASESLAB")
        self.floor = box("FLOOR", "IfcSlab", -10, -10, 3.0, 30, 30, 3.25, "FLOOR")
        self.wall = box("WALL", "IfcWall", 4.9, -10, 0, 5.1, 30, 3.0)
        self.beam = box("BEAM", "IfcBeam", 9.8, -10, 2.6, 10.2, 30, 3.0)
        self.ground_column = column("C_GROUND", 0, 0, 0, 3.0)

    def check(self, *columns):
        cols = [self.ground_column, *columns]
        result = run_check(cols, [self.base, self.floor],
                           cols + [self.wall, self.beam])
        json.dumps(result, allow_nan=False)          # must be valid JSON
        return {c["global_id"]: c for c in result["columns"]}, result

    def test_column_above_column_is_supported_through_slab(self):
        columns, _ = self.check(column("C", 0, 0, 3.25, 6))
        self.assertEqual(columns["C"]["result"], SUPPORTED_THROUGH_SLAB)
        self.assertEqual(columns["C"]["support_below_slab"][0]["global_id"], "C_GROUND")

    def test_column_above_wall_and_beam_are_supported(self):
        columns, _ = self.check(column("ON_WALL", 5, 2, 3.25, 6),
                                column("ON_BEAM", 10, 2, 3.25, 6))
        self.assertEqual(columns["ON_WALL"]["result"], SUPPORTED_THROUGH_SLAB)
        self.assertEqual(columns["ON_BEAM"]["result"], SUPPORTED_THROUGH_SLAB)

    def test_column_on_slab_with_nothing_below_is_flagged(self):
        columns, result = self.check(column("FREE", 15, 15, 3.25, 6))
        self.assertEqual(columns["FREE"]["result"], UNSUPPORTED_SLAB)
        self.assertIn("FREE", result["flagged_columns"])

    def test_offset_column_reports_nearest_support(self):
        columns, _ = self.check(column("NEAR", 5.45, 5, 3.25, 6))
        self.assertEqual(columns["NEAR"]["result"], UNSUPPORTED_SLAB)
        self.assertEqual(columns["NEAR"]["nearest_support"]["global_id"], "WALL")
        self.assertAlmostEqual(columns["NEAR"]["nearest_support"]["distance_from_column_centre_m"], 0.35)

    def test_column_on_wall_without_slab_is_direct(self):
        columns, _ = self.check(box("DIRECT", "IfcColumn", 4.9, 8, 3.0, 5.1, 8.2, 6))
        self.assertEqual(columns["DIRECT"]["result"], DIRECT_SUPPORT)

    def test_ground_column_on_base_slab(self):
        columns, _ = self.check()
        self.assertEqual(columns["C_GROUND"]["result"], ON_BASE_SLAB)

    def test_column_on_nothing(self):
        columns, _ = self.check(column("AIR", 50, 50, 3.25, 6))
        self.assertEqual(columns["AIR"]["result"], NO_BEARING_ELEMENT)

    def test_small_gap_counts_as_contact_but_large_gap_does_not(self):
        columns, _ = self.check(column("GAP_OK", 15, 15, 3.28, 6),
                                column("GAP_BIG", 20, 20, 3.5, 6))
        self.assertEqual(columns["GAP_OK"]["result"], UNSUPPORTED_SLAB)
        self.assertEqual(columns["GAP_BIG"]["result"], NO_BEARING_ELEMENT)

    def test_lowest_slab_typed_as_floor_counts_as_ground(self):
        # Like B308X: the ground slab is exported as FLOOR, not BASESLAB.
        ground = box("GROUND", "IfcSlab", -10, -10, -0.6, 30, 30, 0, "FLOOR")
        floor = box("FLOOR", "IfcSlab", -10, -10, 3.0, 30, 30, 3.25, "FLOOR")
        ground_col = column("G", 0, 0, 0, 3.0)
        upper_free = column("FREE", 15, 15, 3.25, 6)
        cols = [ground_col, upper_free]
        result = run_check(cols, [ground, floor], cols)
        columns = {c["global_id"]: c for c in result["columns"]}
        self.assertEqual(columns["G"]["result"], ON_BASE_SLAB)
        self.assertIn("lowest slab", columns["G"]["ground_slab_reason"])
        # The suspended floor slab is still checked as before.
        self.assertEqual(columns["FREE"]["result"], UNSUPPORTED_SLAB)

    def test_lowest_slab_rule_can_be_switched_off(self):
        from column_support_check.src.support_check import Parameters
        ground = box("GROUND", "IfcSlab", -10, -10, -0.6, 30, 30, 0, "FLOOR")
        cols = [column("G", 0, 0, 0, 3.0)]
        result = run_check(cols, [ground], cols,
                           Parameters(lowest_slab_is_ground=False))
        self.assertEqual(result["columns"][0]["result"], UNSUPPORTED_SLAB)

    def test_summary_counts(self):
        _, result = self.check(column("C", 0, 0, 3.25, 6),
                               column("FREE", 15, 15, 3.25, 6))
        counts = result["summary"]["result_counts"]
        self.assertEqual(counts[SUPPORTED_THROUGH_SLAB], 1)
        self.assertEqual(counts[UNSUPPORTED_SLAB], 1)
        self.assertEqual(counts[ON_BASE_SLAB], 1)
        self.assertEqual(result["summary"]["columns_needing_review"], 1)


class AnalyseWithIfcTests(unittest.TestCase):
    def test_model_without_columns_returns_empty_result(self):
        try:
            import ifcopenshell
        except ImportError:
            self.skipTest("IfcOpenShell is not installed")
        from column_support_check.src.main import analyse

        result = analyse(ifcopenshell.file(schema="IFC4"))
        json.dumps(result, allow_nan=False)
        self.assertEqual(result["summary"]["columns_total"], 0)
        self.assertEqual(result["flagged_columns"], [])


if __name__ == "__main__":
    unittest.main()
