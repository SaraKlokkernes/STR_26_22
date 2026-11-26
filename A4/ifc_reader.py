

# ifc_reader.py

"""
IFC Reader - Vertical Load Path Checker
Group 22 - STR - Structures

Phase 1: IFC Element Extraction

- Read IFC models
- Identify structural elements
- Extract global geometry in metres
- Identify building storeys
- Extract material and type information
- Extract load-bearing and construction status properties
- Calculate element centre coordinates

The extracted information is used for the subsequent
column alignment analysis.
"""

from pathlib import Path

import ifcopenshell
import ifcopenshell.geom

from ifcopenshell.util.element import (
    get_container,
    get_materials,
    get_psets,
    get_type
)


# --------------------------------------------------
# 1. OPEN IFC MODEL
# --------------------------------------------------

def read_ifc(ifc_path):
    """
    Open an IFC model and return the model object.
    """

    ifc_path = Path(ifc_path)

    if not ifc_path.is_file():
        raise FileNotFoundError(
            f"No IFC file found at {ifc_path}"
        )

    print("\nOpening IFC model...")

    model = ifcopenshell.open(str(ifc_path))

    print("IFC model successfully opened.")
    print(f"IFC schema: {model.schema}")

    return model


# --------------------------------------------------
# 2. DEFINE STRUCTURAL ELEMENT TYPES
# --------------------------------------------------

ELEMENT_TYPES = {
    "Column": ["IfcColumn"],
    "Beam": ["IfcBeam"],
    "Wall": ["IfcWall"],
    "Foundation": ["IfcFooting", "IfcPile"]
}


# --------------------------------------------------
# 3. EXTRACT ELEMENT GEOMETRY
# --------------------------------------------------

def extract_geometry(element, settings):
    """
    Extract global bounding box coordinates,
    centre coordinates and height.

    IfcOpenShell geometry is returned in metres
    when convert-back-units is disabled.
    """

    shape = ifcopenshell.geom.create_shape(
        settings,
        element
    )

    vertices = shape.geometry.verts

    if len(vertices) < 3:
        raise ValueError("No usable geometry found.")

    # Extract global X, Y and Z coordinates
    x = vertices[0::3]
    y = vertices[1::3]
    z = vertices[2::3]

    # Calculate bounding box
    xmin = min(x)
    xmax = max(x)

    ymin = min(y)
    ymax = max(y)

    zmin = min(z)
    zmax = max(z)

    # Calculate bounding box centre
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    z_center = (zmin + zmax) / 2

    return {
        "Xmin": xmin,
        "Xmax": xmax,

        "Ymin": ymin,
        "Ymax": ymax,

        "Zmin": zmin,
        "Zmax": zmax,

        "X_center": x_center,
        "Y_center": y_center,
        "Z_center": z_center,

        "Height": zmax - zmin
    }


# --------------------------------------------------
# 4. IDENTIFY BUILDING STOREY
# --------------------------------------------------

def get_storey_name(element):
    """
    Find the building storey of an IFC element.
    """

    try:
        storey = get_container(
            element,
            ifc_class="IfcBuildingStorey"
        )

        if storey:
            return storey.Name or "Unnamed Storey"

    except Exception as error:
        print(f"Storey extraction error: {error}")

    return "Not assigned"


# --------------------------------------------------
# 5. EXTRACT MATERIAL INFORMATION
# --------------------------------------------------

def get_material_name(element):
    """
    Extract assigned IFC material names.

    Material information may be inherited
    from the element type.
    """

    try:
        materials = get_materials(
            element,
            should_inherit=True
        )

        names = []

        for material in materials:
            name = getattr(material, "Name", None)

            if name and name not in names:
                names.append(name)

        if names:
            return "; ".join(names)

    except Exception as error:
        print(f"Material extraction error: {error}")

    return "Unknown"


# --------------------------------------------------
# 6. EXTRACT ELEMENT TYPE
# --------------------------------------------------

def get_type_name(element):
    """
    Extract the assigned IFC element type name.
    """

    try:
        element_type = get_type(element)

        if element_type:
            return element_type.Name or "Unnamed Type"

    except Exception as error:
        print(f"Type extraction error: {error}")

    return "Unknown"


# --------------------------------------------------
# 7. EXTRACT PROPERTY SETS
# --------------------------------------------------

def get_element_properties(element):
    """
    Extract property sets from the element
    and its assigned type.
    """

    try:
        return get_psets(
            element,
            psets_only=True,
            should_inherit=True
        )

    except Exception as error:
        print(f"Property extraction error: {error}")

        return {}


def find_property(psets, property_names, preferred_pset=None):
    """
    Find a property by name.

    The standard IFC property set is checked first.
    Other property sets are used as a fallback.

    Conflicting fallback values are not accepted.
    """

    names = {
        name.casefold()
        for name in property_names
    }

    if preferred_pset:
        properties = psets.get(preferred_pset, {})

        for key, value in properties.items():
            if key.casefold() in names:
                if value is not None and value != "":
                    return value

    matches = []

    for properties in psets.values():
        for key, value in properties.items():

            if key.casefold() in names:
                if value is not None and value != "":
                    matches.append(value)

    if matches:
        first = matches[0]

        if all(value == first for value in matches):
            return first

    return None


# --------------------------------------------------
# 8. IDENTIFY LOAD-BEARING ELEMENTS
# --------------------------------------------------

def get_load_bearing(psets, preferred_pset):
    """
    Identify whether the element is load-bearing.

    Missing information is reported as Unknown,
    rather than assuming that an element is structural.
    """

    value = find_property(
        psets,
        ["LoadBearing", "Load Bearing"],
        preferred_pset
    )

    if value is True:
        return "True"

    if value is False:
        return "False"

    if value is not None:
        text = str(value).strip().lower()

        if text in ["true", "yes", "1"]:
            return "True"

        if text in ["false", "no", "0"]:
            return "False"

    return "Unknown"


# --------------------------------------------------
# 9. EXTRACT CONSTRUCTION STATUS
# --------------------------------------------------

def get_construction_status(psets, preferred_pset):
    """
    Extract information describing whether
    an element is new, existing or demolished.

    Actual property names depend on the IFC model.
    """

    value = find_property(
        psets,
        [
            "Status",
            "ConstructionStatus",
            "Construction Status",
            "RenovationStatus",
            "Phase Created"
        ],
        preferred_pset
    )

    if value is not None:
        return str(value)

    return "Unknown"


# --------------------------------------------------
# 10. EXTRACT STRUCTURAL ELEMENTS
# --------------------------------------------------

def extract_structural_elements(model):
    """
    Identify structural elements and extract
    their properties and geometry.
    """

    # IFC geometry settings
    settings = ifcopenshell.geom.settings()

    # Use global model coordinates
    settings.set("use-world-coords", True)

    # Keep geometry coordinates in metres
    settings.set("convert-back-units", False)

    print("\nGeometry coordinates are in metres.")

    elements = []
    processed_ids = set()

    # Loop through all structural categories
    for category, ifc_types in ELEMENT_TYPES.items():

        for ifc_type in ifc_types:

            for element in model.by_type(ifc_type):

                global_id = element.GlobalId

                # Avoid duplicate elements
                if global_id in processed_ids:
                    continue

                processed_ids.add(global_id)

                print(
                    f"Processing {category}: "
                    f"{element.Name or global_id}"
                )

                # Extract geometry
                try:
                    bbox = extract_geometry(
                        element,
                        settings
                    )

                    geometry_status = "Available"

                except Exception as error:

                    bbox = {
                        "Xmin": None,
                        "Xmax": None,

                        "Ymin": None,
                        "Ymax": None,

                        "Zmin": None,
                        "Zmax": None,

                        "X_center": None,
                        "Y_center": None,
                        "Z_center": None,

                        "Height": None
                    }

                    geometry_status = "Missing"

                    print(
                        f"Geometry error for "
                        f"{global_id}: {error}"
                    )

                # Extract properties
                psets = get_element_properties(element)

                preferred_pset = {
                    "Column": "Pset_ColumnCommon",
                    "Beam": "Pset_BeamCommon",
                    "Wall": "Pset_WallCommon",
                    "Foundation": (
                        f"Pset_{ifc_type[3:]}Common"
                    )
                }.get(category)

                # Store element information
                element_data = {

                    "GlobalId": global_id,

                    "Name": element.Name or "Unnamed",

                    "IFC_Type": element.is_a(),

                    "Category": category,

                    "PredefinedType": (
                        getattr(
                            element,
                            "PredefinedType",
                            None
                        )
                        or "Not defined"
                    ),

                    "Type_Name": get_type_name(element),

                    "Storey": get_storey_name(element),

                    "Material": get_material_name(element),

                    "LoadBearing": get_load_bearing(
                        psets,
                        preferred_pset
                    ),

                    "Construction_Status":
                        get_construction_status(
                            psets,
                            preferred_pset
                        ),

                    "Geometry_Status": geometry_status,

                    **bbox

                }

                elements.append(element_data)

    return elements


# --------------------------------------------------
# 11. GENERATE ELEMENT SUMMARY
# --------------------------------------------------

def element_summary(elements):
    """
    Count the extracted structural elements
    and assess information availability.
    """

    summary = {

        "Total": len(elements),

        "Columns": 0,
        "Beams": 0,
        "Walls": 0,
        "Foundations": 0,

        "Geometry_Available": 0,
        "Geometry_Missing": 0,

        "Columns_Material_Unknown": 0,
        "Columns_LoadBearing_Unknown": 0,
        "Columns_Status_Unknown": 0

    }

    for element in elements:

        category = element["Category"]

        if category == "Column":

            summary["Columns"] += 1

            if element["Material"] == "Unknown":
                summary["Columns_Material_Unknown"] += 1

            if element["LoadBearing"] == "Unknown":
                summary["Columns_LoadBearing_Unknown"] += 1

            if element["Construction_Status"] == "Unknown":
                summary["Columns_Status_Unknown"] += 1

        elif category == "Beam":

            summary["Beams"] += 1

        elif category == "Wall":

            summary["Walls"] += 1

        elif category == "Foundation":

            summary["Foundations"] += 1

        if element["Geometry_Status"] == "Available":

            summary["Geometry_Available"] += 1

        else:

            summary["Geometry_Missing"] += 1

    return summary

