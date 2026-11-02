
# team_tool.py

"""
Vertical Load Transfer Checker

Checks whether IFC columns have geometrically
plausible support from columns, beams or walls below.

IMPORTANT:
This is a geometric check, not a structural
capacity verification.
"""

import ifcopenshell
import ifcopenshell.geom
from ifcopenshell.util.unit import calculate_unit_scale


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

DEFAULT_VERTICAL_TOLERANCE = 0.15  # metres
MIN_OVERLAP_RATIO = 0.50


# --------------------------------------------------
# CAPT_ELEM: CAPTURE STRUCTURAL ELEMENTS
# --------------------------------------------------

def CAPT_ELEM(model):
    """
    Extract columns, beams and walls from an IFC model.
    Return their GlobalId, name, type and global bounding box.
    All coordinates are converted to metres.
    """

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    # Convert IFC project units to metres
    unit_scale = calculate_unit_scale(model)

    element_types = [
        "IfcColumn",
        "IfcBeam",
        "IfcWall",
        "IfcWallStandardCase"
    ]

    elements = []
    processed_ids = set()

    for ifc_type in element_types:

        for element in model.by_type(ifc_type):

            # Avoid duplicate elements
            if element.GlobalId in processed_ids:
                continue

            processed_ids.add(element.GlobalId)

            try:
                shape = ifcopenshell.geom.create_shape(
                    settings, element
                )

                vertices = shape.geometry.verts

                if not vertices:
                    continue

                # Convert coordinates to metres
                x = [
                    v * unit_scale
                    for v in vertices[0::3]
                ]

                y = [
                    v * unit_scale
                    for v in vertices[1::3]
                ]

                z = [
                    v * unit_scale
                    for v in vertices[2::3]
                ]

                # Calculate global bounding box
                bbox = {
                    "xmin": min(x),
                    "xmax": max(x),
                    "ymin": min(y),
                    "ymax": max(y),
                    "zmin": min(z),
                    "zmax": max(z)
                }

                elements.append({
                    "GlobalId": element.GlobalId,
                    "Name": element.Name or "Unnamed",
                    "Type": ifc_type,
                    "BBox": bbox
                })

            except Exception as error:

                print(
                    f"Could not process "
                    f"{element.GlobalId}: {error}"
                )

    return elements


# --------------------------------------------------
# CONN_ELEM: FIND POTENTIAL SUPPORTS
# --------------------------------------------------

def CONN_ELEM(elements, vertical_tolerance):
    """
    Identify potential supporting elements below columns.

    A potential support must:
    - Be a column, beam or wall.
    - Have a top elevation close to the column bottom.
    - Have horizontal geometric overlap.
    """

    columns = [
        e for e in elements
        if e["Type"] == "IfcColumn"
    ]

    supports = [
        e for e in elements
        if e["Type"] in (
            "IfcColumn",
            "IfcBeam",
            "IfcWall",
            "IfcWallStandardCase"
        )
    ]

    relationships = []

    for column in columns:

        col_box = column["BBox"]
        candidates = []

        for support in supports:

            # An element cannot support itself
            if support["GlobalId"] == column["GlobalId"]:
                continue

            sup_box = support["BBox"]

            # Vertical distance between column bottom
            # and potential support top
            vertical_gap = col_box["zmin"] - sup_box["zmax"]

            if not (
                -vertical_tolerance
                <= vertical_gap
                <= vertical_tolerance
            ):
                continue

            # Calculate horizontal overlap
            overlap_x = max(
                0,
                min(col_box["xmax"], sup_box["xmax"])
                - max(col_box["xmin"], sup_box["xmin"])
            )

            overlap_y = max(
                0,
                min(col_box["ymax"], sup_box["ymax"])
                - max(col_box["ymin"], sup_box["ymin"])
            )

            overlap_area = overlap_x * overlap_y

            column_area = (
                (col_box["xmax"] - col_box["xmin"])
                * (col_box["ymax"] - col_box["ymin"])
            )

            overlap_ratio = (
                overlap_area / column_area
                if column_area > 0
                else 0
            )

            if overlap_area > 0:

                candidates.append({
                    "Support": support,
                    "VerticalGap": vertical_gap,
                    "OverlapArea": overlap_area,
                    "OverlapRatio": overlap_ratio
                })

        relationships.append({
            "Column": column,
            "Candidates": candidates
        })

    return relationships


# --------------------------------------------------
# CALC_OVERLAP: CALCULATE GEOMETRIC OVERLAP
# --------------------------------------------------

def CALC_OVERLAP(candidate):
    """
    Calculate and return geometric overlap information.
    """

    return {
        "overlap_area": candidate["OverlapArea"],
        "overlap_ratio": candidate["OverlapRatio"],
        "vertical_gap": candidate["VerticalGap"]
    }


# --------------------------------------------------
# CHEK_SUPPORT: CHECK SUPPORT
# --------------------------------------------------

def CHEK_SUPPORT(candidates, min_overlap_ratio):
    """
    Classify whether a column has a potential support.

    SUPPORTED:
    At least one candidate satisfies the overlap threshold.

    UNSUPPORTED:
    No potential support was found.

    REVIEW:
    Potential support exists but does not satisfy
    the defined overlap threshold.
    """

    if not candidates:
        return "UNSUPPORTED"

    for candidate in candidates:

        overlap = CALC_OVERLAP(candidate)

        if overlap["overlap_ratio"] >= min_overlap_ratio:
            return "SUPPORTED"

    return "REVIEW"


# --------------------------------------------------
# COMM_REPORT: COMMUNICATE RESULTS
# --------------------------------------------------

def COMM_REPORT(relationships, min_overlap_ratio):
    """
    Generate a structured report for each column.
    """

    results = []

    for relationship in relationships:

        column = relationship["Column"]
        candidates = relationship["Candidates"]

        status = CHEK_SUPPORT(
            candidates,
            min_overlap_ratio
        )

        if candidates:

            # Select candidate with greatest overlap
            best = max(
                candidates,
                key=lambda c: c["OverlapRatio"]
            )

            support = best["Support"]

            support_id = support["GlobalId"]
            support_name = support["Name"]
            support_type = support["Type"]

            overlap_ratio = round(
                best["OverlapRatio"] * 100, 1
            )

            vertical_gap = round(
                best["VerticalGap"], 3
            )

        else:

            support_id = None
            support_name = None
            support_type = None
            overlap_ratio = 0
            vertical_gap = None

        results.append({

            "Column_ID": column["GlobalId"],
            "Column_Name": column["Name"],

            "Support_ID": support_id,
            "Support_Name": support_name,
            "Support_Type": support_type,

            "Overlap_Percent": overlap_ratio,
            "Vertical_Gap_m": vertical_gap,

            "Status": status

        })

    return results


# --------------------------------------------------
# MAIN FUNCTION: ANALYSE
# --------------------------------------------------

def analyse(
    model,
    vertical_tolerance=DEFAULT_VERTICAL_TOLERANCE,
    min_overlap_ratio=MIN_OVERLAP_RATIO
):
    """
    Main callable function.

    This function can be imported into another
    Python script and used with any compatible IFC model.
    """

    if vertical_tolerance < 0:
        raise ValueError(
            "Vertical tolerance must be non-negative."
        )

    if not 0 <= min_overlap_ratio <= 1:
        raise ValueError(
            "Overlap ratio must be between 0 and 1."
        )

    # 1. Capture elements
    elements = CAPT_ELEM(model)

    # 2. Find potential supports
    relationships = CONN_ELEM(
        elements,
        vertical_tolerance
    )

    # 3. Check and communicate results
    results = COMM_REPORT(
        relationships,
        min_overlap_ratio
    )

    # 4. Summarise results
    report = {

        "Element_Count": len(elements),

        "Column_Count": len(relationships),

        "Supported": sum(
            r["Status"] == "SUPPORTED"
            for r in results
        ),

        "Unsupported": sum(
            r["Status"] == "UNSUPPORTED"
            for r in results
        ),

        "Review": sum(
            r["Status"] == "REVIEW"
            for r in results
        ),

        "Results": results

    }

    return report


