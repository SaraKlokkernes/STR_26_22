
# ifc_reader.py

"""
IFC Reader - Vertical Load Path Checker

Phase 1:
- Read IFC models
- Identify structural elements
- Extract geometric information
- Convert coordinates to metres
- Identify building storeys
"""

import ifcopenshell
import ifcopenshell.geom

from ifcopenshell.util.unit import calculate_unit_scale
from ifcopenshell.util.element import get_container


# --------------------------------------------------
# 1. OPEN IFC MODEL
# --------------------------------------------------

def read_ifc(ifc_path):
    """
    Open an IFC model and return the model object.
    """

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

def extract_geometry(element, settings, unit_scale):
    """
    Extract global bounding box coordinates.

    Coordinates are converted to metres.
    """

    shape = ifcopenshell.geom.create_shape(
        settings,
        element
    )

    vertices = shape.geometry.verts

    if len(vertices) < 3:
        raise ValueError("No usable geometry found.")

    # Convert coordinates to metres
    x = [
        vertices[i] * unit_scale
        for i in range(0, len(vertices), 3)
    ]

    y = [
        vertices[i] * unit_scale
        for i in range(1, len(vertices), 3)
    ]

    z = [
        vertices[i] * unit_scale
        for i in range(2, len(vertices), 3)
    ]

    return {
        "Xmin": min(x),
        "Xmax": max(x),

        "Ymin": min(y),
        "Ymax": max(y),

        "Zmin": min(z),
        "Zmax": max(z)
    }


# --------------------------------------------------
# 4. IDENTIFY BUILDING STOREY
# --------------------------------------------------

def get_storey_name(element):
    """
    Find the spatial container of an element.
    """

    try:

        container = get_container(element)

        if container:

            if container.is_a("IfcBuildingStorey"):
                return container.Name or "Unnamed Storey"

            return container.Name or "Unknown Container"

    except Exception:
        pass

    return "Not assigned"


# --------------------------------------------------
# 5. EXTRACT STRUCTURAL ELEMENTS
# --------------------------------------------------

def extract_structural_elements(model):
    """
    Identify structural elements and extract
    their properties and geometry.
    """

    # IFC geometry settings
    settings = ifcopenshell.geom.settings()

    settings.set(
        settings.USE_WORLD_COORDS,
        True
    )

    # Convert project units to metres
    unit_scale = calculate_unit_scale(model)

    print(f"\nUnit scale to metres: {unit_scale}")

    elements = []
    processed_ids = set()

    # Loop through the structural categories
    for category, ifc_types in ELEMENT_TYPES.items():

        for ifc_type in ifc_types:

            for element in model.by_type(ifc_type):

                # Avoid duplicate elements
                global_id = element.GlobalId

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
                        settings,
                        unit_scale
                    )

                    geometry_status = "Available"

                except Exception as error:

                    bbox = {
                        "Xmin": None,
                        "Xmax": None,
                        "Ymin": None,
                        "Ymax": None,
                        "Zmin": None,
                        "Zmax": None
                    }

                    geometry_status = "Missing"

                    print(
                        f"Geometry error for "
                        f"{global_id}: {error}"
                    )

                # Store element information
                element_data = {

                    "GlobalId": global_id,

                    "Name": element.Name or "Unnamed",

                    "IFC_Type": element.is_a(),

                    "Category": category,

                    "PredefinedType": (
                        getattr(element, "PredefinedType", None)
                        or "Not defined"
                    ),

                    "Storey": get_storey_name(element),

                    "Geometry_Status": geometry_status,

                    **bbox

                }

                elements.append(element_data)

    return elements


# --------------------------------------------------
# 6. GENERATE ELEMENT SUMMARY
# --------------------------------------------------

def element_summary(elements):
    """
    Count the extracted structural elements.
    """

    summary = {

        "Total": len(elements),

        "Columns": 0,

        "Beams": 0,

        "Walls": 0,

        "Foundations": 0,

        "Geometry_Available": 0,

        "Geometry_Missing": 0

    }

    for element in elements:

        category = element["Category"]

        if category == "Column":
            summary["Columns"] += 1

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

