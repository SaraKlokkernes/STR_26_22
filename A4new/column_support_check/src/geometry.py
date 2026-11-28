"""Pure geometry helpers for the column support check.

Nothing in this module depends on IfcOpenShell. Elements are passed as
triangulated meshes in global coordinates (metres), so the logic can be
tested with simple boxes.
"""

import numpy as np

EPS = 1e-9


class Mesh:
    """A triangulated element in global coordinates (metres)."""

    def __init__(self, guid, ifc_type, verts, faces, name="",
                 storey="", predefined_type="", load_bearing=None):
        self.guid = guid
        self.ifc_type = ifc_type
        self.name = name
        self.storey = storey
        self.predefined_type = predefined_type or ""
        # True, False or None (unknown)
        self.load_bearing = load_bearing

        vertices = np.asarray(verts, dtype=float).reshape(-1, 3)
        indices = np.asarray(faces, dtype=int).reshape(-1, 3)
        if len(vertices) == 0 or len(indices) == 0:
            raise ValueError(f"Element {guid} has no triangulated geometry.")

        self.vertices = vertices
        self.triangles = vertices[indices]          # (n, 3, 3)
        self.min = vertices.min(axis=0)
        self.max = vertices.max(axis=0)

        # Pre-compute the XY projection used by vertical_hits().
        a = self.triangles[:, 0, :2]
        b = self.triangles[:, 1, :2]
        c = self.triangles[:, 2, :2]
        self._a = a
        self._v0 = c - a
        self._v1 = b - a
        self._d00 = np.einsum("ij,ij->i", self._v0, self._v0)
        self._d01 = np.einsum("ij,ij->i", self._v0, self._v1)
        self._d11 = np.einsum("ij,ij->i", self._v1, self._v1)
        self._den = self._d00 * self._d11 - self._d01 * self._d01
        # Vertical faces have no XY area and are ignored.
        self._valid = np.abs(self._den) > EPS

    def covers_xy(self, x, y, margin=0.001):
        return (self.min[0] - margin <= x <= self.max[0] + margin
                and self.min[1] - margin <= y <= self.max[1] + margin)

    def vertical_hits(self, x, y):
        """Z values where a vertical line through (x, y) crosses the mesh.

        Returns a sorted numpy array (may be empty).
        """
        if not self.covers_xy(x, y):
            return np.empty(0)

        p = np.array([x, y]) - self._a
        d02 = np.einsum("ij,ij->i", self._v0, p)
        d12 = np.einsum("ij,ij->i", self._v1, p)

        with np.errstate(divide="ignore", invalid="ignore"):
            u = (self._d11 * d02 - self._d01 * d12) / self._den
            v = (self._d00 * d12 - self._d01 * d02) / self._den

        tol = 1e-7
        inside = (self._valid & (u >= -tol) & (v >= -tol)
                  & (u + v <= 1 + tol))
        if not inside.any():
            return np.empty(0)

        tri = self.triangles[inside]
        u = u[inside]
        v = v[inside]
        z = (tri[:, 0, 2]
             + u * (tri[:, 2, 2] - tri[:, 0, 2])
             + v * (tri[:, 1, 2] - tri[:, 0, 2]))
        return np.sort(z)


def base_sample_points(column, inset=0.5, base_band=0.01):
    """Sample points in the column's base footprint.

    Uses the vertices at the bottom of the column. Returns the centre plus
    four points halfway (``inset``) from the centre to the footprint edges,
    so a wall or beam under part of the column is still detected.
    """
    zmin = column.min[2]
    bottom = column.vertices[column.vertices[:, 2] <= zmin + base_band]
    if len(bottom) == 0:
        bottom = column.vertices

    xmin, ymin = bottom[:, 0].min(), bottom[:, 1].min()
    xmax, ymax = bottom[:, 0].max(), bottom[:, 1].max()
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    hx, hy = (xmax - xmin) / 2 * inset, (ymax - ymin) / 2 * inset

    return [(cx, cy), (cx - hx, cy), (cx + hx, cy),
            (cx, cy - hy), (cx, cy + hy)]
