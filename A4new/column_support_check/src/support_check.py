"""Vertical load path logic: what does each column stand on?

For every column the check looks straight down from the column base:

1. If a column, wall, beam, footing or pile is directly under the base,
   the column has DIRECT_SUPPORT.
2. If the column stands on a slab, the check looks straight down from the
   underside of that slab, at the same points. If a supporting element is
   found there, the result is SUPPORTED_THROUGH_SLAB. Slabs stacked on
   slabs (e.g. topping on a structural slab) are followed downwards.
3. If nothing is under the slab, the result is UNSUPPORTED_SLAB: the column
   load is delivered as a point load into a slab with no element below.
   A ground slab is reported as ON_BASE_SLAB, since its load normally
   goes into the ground. A slab counts as a ground slab when its
   PredefinedType is BASESLAB, or (by default) when it is the lowest slab
   in the model.
4. If the column stands on nothing in the model: NO_BEARING_ELEMENT.

This is geometric screening of the model, not a structural verification.
Nothing here depends on IfcOpenShell.
"""

import math

from .geometry import base_sample_points

DIRECT_SUPPORT = "DIRECT_SUPPORT"
SUPPORTED_THROUGH_SLAB = "SUPPORTED_THROUGH_SLAB"
UNSUPPORTED_SLAB = "UNSUPPORTED_SLAB"
ON_BASE_SLAB = "ON_BASE_SLAB"
NO_BEARING_ELEMENT = "NO_BEARING_ELEMENT"
MISSING_GEOMETRY = "MISSING_GEOMETRY"

RESULT_ORDER = [
    UNSUPPORTED_SLAB,
    NO_BEARING_ELEMENT,
    ON_BASE_SLAB,
    SUPPORTED_THROUGH_SLAB,
    DIRECT_SUPPORT,
    MISSING_GEOMETRY,
]

NEEDS_REVIEW = {UNSUPPORTED_SLAB, NO_BEARING_ELEMENT, MISSING_GEOMETRY}


class Parameters:
    """Screening tolerances in metres."""

    def __init__(self, max_gap=0.05, below_eps=0.01, overlap=0.05,
                 max_slab_layers=3, search_radius=2.0,
                 lowest_slab_is_ground=True, ground_tolerance=0.10):
        # Largest gap between two surfaces still counted as contact.
        self.max_gap = max_gap
        # An element must reach at least this far below a level to count
        # as being underneath it.
        self.below_eps = below_eps
        # Allowed modelled overlap (clash) at a contact.
        self.overlap = overlap
        # How many stacked slabs to follow downwards.
        self.max_slab_layers = max_slab_layers
        # Radius for reporting the nearest support when none is found.
        self.search_radius = search_radius
        # Treat the lowest slab(s) in the model as ground-bearing, even when
        # PredefinedType is not BASESLAB (common in Revit exports).
        self.lowest_slab_is_ground = lowest_slab_is_ground
        # Slabs whose underside is within this distance of the lowest slab
        # underside count as "lowest".
        self.ground_tolerance = ground_tolerance

    def as_dict(self):
        return {
            "max_gap_m": self.max_gap,
            "below_eps_m": self.below_eps,
            "overlap_m": self.overlap,
            "max_slab_layers": self.max_slab_layers,
            "search_radius_m": self.search_radius,
            "lowest_slab_is_ground": self.lowest_slab_is_ground,
            "ground_tolerance_m": self.ground_tolerance,
        }


def _contacts(level, points, meshes, exclude, p):
    """Elements that are underneath ``level`` at any of ``points``.

    An element counts when the vertical line through a point passes
    through it, the element reaches below the level, and its top at that
    point is no more than ``max_gap`` below the level.

    Returns a list of dicts sorted with the highest contact first.
    """
    found = []
    for mesh in meshes:
        if mesh.guid in exclude:
            continue
        if mesh.max[2] < level - p.max_gap or mesh.min[2] >= level + p.below_eps:
            continue

        top = None
        bottom = None
        hit_points = 0
        for x, y in points:
            hits = mesh.vertical_hits(x, y)
            if hits.size == 0:
                continue
            if hits.min() >= level - p.below_eps:
                continue                      # not below the level
            if hits.max() < level - p.max_gap:
                continue                      # too far below: a gap
            below = hits[hits <= level + p.overlap]
            point_top = below.max() if below.size else level
            point_bottom = hits.min()
            hit_points += 1
            top = point_top if top is None else max(top, point_top)
            bottom = point_bottom if bottom is None else min(bottom, point_bottom)

        if hit_points:
            found.append({"mesh": mesh, "top": float(top),
                          "bottom": float(bottom), "points": hit_points})

    found.sort(key=lambda c: c["top"], reverse=True)
    return found


def _nearest_support(level, centre, supports, exclude, p):
    """Nearest support (XY bounding-box distance) spanning ``level``."""
    cx, cy = centre
    best = None
    for mesh in supports:
        if mesh.guid in exclude:
            continue
        if not (mesh.min[2] < level - p.below_eps
                and mesh.max[2] >= level - p.max_gap):
            continue
        dx = max(mesh.min[0] - cx, 0.0, cx - mesh.max[0])
        dy = max(mesh.min[1] - cy, 0.0, cy - mesh.max[1])
        distance = math.hypot(dx, dy)
        if distance <= p.search_radius and (best is None or distance < best[0]):
            best = (distance, mesh)
    if best is None:
        return None
    return {**_ref(best[1]), "distance_from_column_centre_m": round(best[0], 3)}


def _ref(mesh):
    return {"global_id": mesh.guid, "ifc_type": mesh.ifc_type,
            "name": mesh.name}


def _ground_reason(slab_mesh, ground_level, p):
    """Why a slab counts as ground-bearing, or None."""
    if slab_mesh.predefined_type.upper() == "BASESLAB":
        return "PredefinedType BASESLAB"
    if (p.lowest_slab_is_ground and ground_level is not None
            and slab_mesh.min[2] <= ground_level + p.ground_tolerance):
        return "lowest slab in the model (assumed on ground)"
    return None


def check_column(column, slabs, supports, p, ground_level=None):
    """Return a JSON-compatible result for one column."""
    points = base_sample_points(column)
    centre = points[0]
    base = float(column.min[2])
    exclude = {column.guid}

    result = {
        "global_id": column.guid,
        "name": column.name,
        "storey": column.storey,
        "base_elevation_m": round(base, 3),
        "base_centre_xy_m": [round(centre[0], 3), round(centre[1], 3)],
        "result": None,
        "lands_on": None,
        "slab_chain": [],
        "support_below_slab": [],
        "support_coverage": None,
        "nearest_support": None,
        "comment": "",
    }

    direct = _contacts(base, points, supports, exclude, p)
    if direct:
        result["result"] = DIRECT_SUPPORT
        result["lands_on"] = [_ref(c["mesh"]) for c in direct]
        result["support_coverage"] = f"{max(c['points'] for c in direct)}/{len(points)}"
        result["comment"] = "Column base is directly on a supporting element."
        return result

    slab_hits = _contacts(base, points, slabs, exclude, p)
    if not slab_hits:
        result["result"] = NO_BEARING_ELEMENT
        result["nearest_support"] = _nearest_support(base, centre, supports, exclude, p)
        result["comment"] = ("No element found under the column base. Check "
                             "foundations or whether the support is modelled.")
        return result

    slab = slab_hits[0]
    result["lands_on"] = [_ref(slab["mesh"])]
    chain = []
    used = set(exclude)

    for _ in range(p.max_slab_layers):
        chain.append(slab)
        used.add(slab["mesh"].guid)
        underside = slab["bottom"]

        below = _contacts(underside, points, supports, used, p)
        if below:
            result["result"] = SUPPORTED_THROUGH_SLAB
            result["support_below_slab"] = [_ref(c["mesh"]) for c in below]
            result["support_coverage"] = f"{max(c['points'] for c in below)}/{len(points)}"
            result["comment"] = "A supporting element is directly under the slab."
            break

        next_slabs = _contacts(underside, points, slabs, used, p)
        if not next_slabs:
            break
        slab = next_slabs[0]

    result["slab_chain"] = [
        {**_ref(s["mesh"]), "predefined_type": s["mesh"].predefined_type,
         "top_m": round(s["top"], 3), "underside_m": round(s["bottom"], 3)}
        for s in chain
    ]

    if result["result"] is None:
        underside = chain[-1]["bottom"]
        reasons = [r for r in (_ground_reason(s["mesh"], ground_level, p)
                               for s in chain) if r]
        if reasons:
            result["result"] = ON_BASE_SLAB
            result["ground_slab_reason"] = reasons[0]
            result["comment"] = ("Column stands on a ground slab ("
                                 + reasons[0] + "); load assumed to go into "
                                 "the ground.")
        else:
            result["result"] = UNSUPPORTED_SLAB
            result["nearest_support"] = _nearest_support(
                underside, centre, supports, used, p)
            result["comment"] = ("Column delivers a point load into a slab with "
                                 "no supporting element directly below.")
    return result


def run_check(columns, slabs, supports, p=None, missing_geometry=()):
    """Check all columns and build the JSON-compatible result."""
    p = p or Parameters()
    ground_level = min((float(s.min[2]) for s in slabs), default=None)
    results = [check_column(c, slabs, supports, p, ground_level)
               for c in columns]

    for element in missing_geometry:
        results.append({
            "global_id": element["global_id"],
            "name": element["name"],
            "storey": element["storey"],
            "result": MISSING_GEOMETRY,
            "comment": "No usable geometry; the column could not be checked.",
        })

    counts = {name: 0 for name in RESULT_ORDER}
    for r in results:
        counts[r["result"]] += 1

    order = {name: i for i, name in enumerate(RESULT_ORDER)}
    results.sort(key=lambda r: (order[r["result"]], r.get("storey") or "",
                                r.get("name") or ""))

    checked = len(results) - counts[MISSING_GEOMETRY]
    supported = counts[DIRECT_SUPPORT] + counts[SUPPORTED_THROUGH_SLAB]

    return {
        "summary": {
            "columns_total": len(results),
            "columns_checked": checked,
            "slabs_in_model": len(slabs),
            "supporting_elements_in_model": len(supports),
            "result_counts": counts,
            "columns_needing_review": sum(counts[k] for k in NEEDS_REVIEW),
            "share_with_vertical_support_percent": (
                round(supported / checked * 100, 1) if checked else None),
        },
        "flagged_columns": [r["global_id"] for r in results
                            if r["result"] in NEEDS_REVIEW],
        "columns": results,
    }
