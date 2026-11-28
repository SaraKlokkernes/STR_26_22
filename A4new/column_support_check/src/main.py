"""Column support check (vertical load path screening).

Group 22 - STR - Structures, Assignment A4.

``analyse(model)`` receives an opened IfcOpenShell model and returns a
JSON-compatible dictionary. For every IfcColumn it reports what the column
stands on, and flags columns that deliver a point load into a slab with no
supporting element directly below.

This is a geometric screening of the model. It is not a structural
verification and does not check capacity.
"""

from .geometry import Mesh
from .support_check import Parameters, run_check

# --------------------------------------------------------------------------
# Screening tolerances (metres). Review with the structural engineer.
# --------------------------------------------------------------------------
PARAMETERS = Parameters(
    max_gap=0.05,        # gap between surfaces still treated as contact
    below_eps=0.01,      # element must reach this far below a level
    overlap=0.05,        # allowed modelled overlap at a contact
    max_slab_layers=3,   # stacked slabs followed downwards
    search_radius=2.0,   # report nearest support within this radius
    lowest_slab_is_ground=True,  # lowest slab = on ground, even if FLOOR
    ground_tolerance=0.10,       # slabs within 0.10 m of the lowest count too
)

# Elements that can carry a column load downwards.
SUPPORT_TYPES = ["IfcColumn", "IfcWall", "IfcBeam", "IfcMember",
                 "IfcFooting", "IfcPile"]
SLAB_TYPES = ["IfcSlab"]


def _storey_name(element):
    try:
        from ifcopenshell.util.element import get_container

        container = get_container(element)
        if container is not None:
            return container.Name or ""
    except Exception:
        pass
    return ""


def _predefined_type(element):
    try:
        from ifcopenshell.util.element import get_predefined_type

        return get_predefined_type(element) or ""
    except Exception:
        return getattr(element, "PredefinedType", None) or ""


def _load_bearing(element):
    """Pset_*Common.LoadBearing as True, False or None (unknown)."""
    try:
        from ifcopenshell.util.element import get_psets

        psets = get_psets(element, psets_only=True)
    except Exception:
        return None
    for name, props in psets.items():
        if name.startswith("Pset_") and name.endswith("Common"):
            value = props.get("LoadBearing")
            if isinstance(value, bool):
                return value
    return None


def _elements(model, ifc_types):
    seen = {}
    for ifc_type in ifc_types:
        try:
            found = model.by_type(ifc_type)
        except RuntimeError:          # type not in this schema
            continue
        for element in found:
            seen.setdefault(element.GlobalId, element)
    return list(seen.values())


def _meshes(elements):
    """Triangulate elements in world coordinates (metres).

    Returns (meshes, missing) where ``missing`` lists elements without
    usable geometry.
    """
    if not elements:
        return [], []

    import ifcopenshell.geom

    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    meshes, missing = [], []
    for element in elements:
        info = {"global_id": element.GlobalId,
                "name": element.Name or "",
                "storey": _storey_name(element)}
        try:
            shape = ifcopenshell.geom.create_shape(settings, element)
            meshes.append(Mesh(
                guid=element.GlobalId,
                ifc_type=element.is_a(),
                verts=shape.geometry.verts,
                faces=shape.geometry.faces,
                name=info["name"],
                storey=info["storey"],
                predefined_type=_predefined_type(element),
                load_bearing=_load_bearing(element),
            ))
        except Exception:
            missing.append(info)
    return meshes, missing


def analyse(model):
    """Return the column support check for an opened IFC model."""
    columns, missing_columns = _meshes(_elements(model, ["IfcColumn"]))
    slabs, _ = _meshes(_elements(model, SLAB_TYPES))

    # Columns are both checked and possible supports for other columns.
    other_supports, _ = _meshes(
        _elements(model, [t for t in SUPPORT_TYPES if t != "IfcColumn"]))
    # Elements explicitly marked LoadBearing = False cannot carry a column.
    candidates = columns + other_supports
    supports = [m for m in candidates if m.load_bearing is not False]

    result = run_check(columns, slabs, supports, PARAMETERS, missing_columns)
    result["summary"]["supports_excluded_not_load_bearing"] = (
        len(candidates) - len(supports))
    result["summary"]["supports_with_unknown_load_bearing"] = sum(
        m.load_bearing is None for m in supports)
    result["parameters"] = PARAMETERS.as_dict()
    result["model_schema"] = model.schema
    result["note"] = ("Geometric screening of the IFC model. Not a structural "
                      "verification; flagged columns need engineering review.")
    return result
