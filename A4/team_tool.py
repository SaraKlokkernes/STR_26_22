
# team_tool.py

"""
Vertical Load Path Checker
Group 22 - STR - Structures

Phase 2: Column Classification
Phase 3: Vertical Load Path Analysis

This module analyses the spatial relationship
between new glulam columns and existing
load-bearing columns.

The analysis is a geometric screening tool
and does not verify structural capacity.
"""

import math


# --------------------------------------------------
# 1. ANALYSIS SETTINGS
# --------------------------------------------------

# Maximum horizontal centre-to-centre offset
# Preliminary screening tolerance: 150 mm
ALIGNMENT_TOLERANCE = 0.15

# Maximum vertical gap between columns
# Allows for intermediate floor structures
MAX_VERTICAL_GAP = 0.50

# Small vertical overlap allowed in the model
VERTICAL_OVERLAP_TOLERANCE = 0.05

# Material keywords
GLULAM_KEYWORDS = [
    "glulam",
    "glued laminated",
    "limtrae",
    "limtræ",
    "brettschichtholz",
    "gl24",
    "gl28",
    "gl30",
    "gl32"
]

# Construction status values
NEW_STATUS = [
    "new",
    "ny",
    "nyt"
]

EXISTING_STATUS = [
    "existing",
    "eksisterende"
]


# --------------------------------------------------
# 2. CLASSIFY COLUMNS
# --------------------------------------------------

def classify_columns(elements):
    """
    Separate columns into:

    - New glulam columns
    - Existing load-bearing columns
    - Unclassified columns
    - Other columns
    """

    new_columns = []
    existing_columns = []
    unclassified_columns = []
    other_columns = []

    for element in elements:

        if element["Category"] != "Column":
            continue

        material = str(
            element.get("Material", "Unknown")
        ).lower()

        status = str(
            element.get(
                "Construction_Status",
                "Unknown"
            )
        ).strip().lower()

        load_bearing = str(
            element.get("LoadBearing", "Unknown")
        ).strip().lower()

        is_glulam = any(
            keyword in material
            for keyword in GLULAM_KEYWORDS
        )

        is_new = status in NEW_STATUS
        is_existing = status in EXISTING_STATUS

        # Identify new glulam columns
        if is_new and is_glulam:

            new_columns.append(element)

        # Identify existing load-bearing columns
        elif is_existing and load_bearing == "true":

            existing_columns.append(element)

        # Columns with insufficient information
        elif (
            status not in NEW_STATUS + EXISTING_STATUS
            or (
                is_new
                and material.strip() in ["unknown", ""]
            )
            or (
                is_existing
                and load_bearing not in ["true", "false"]
            )
        ):

            unclassified_columns.append(element)

        # Columns outside the scope of the analysis
        else:

            other_columns.append(element)

    return (
        new_columns,
        existing_columns,
        unclassified_columns,
        other_columns
    )


# --------------------------------------------------
# 3. CHECK GEOMETRY AVAILABILITY
# --------------------------------------------------

def has_valid_geometry(column):
    """
    Check whether the coordinates required
    for the analysis are available.
    """

    required_coordinates = [
        "X_center",
        "Y_center",
        "Zmin",
        "Zmax"
    ]

    if column.get("Geometry_Status") != "Available":
        return False

    for coordinate in required_coordinates:

        value = column.get(coordinate)

        if not isinstance(value, (int, float)):
            return False

        if not math.isfinite(value):
            return False

    return column["Zmax"] > column["Zmin"]


# --------------------------------------------------
# 4. CHECK VERTICAL RELATIONSHIP
# --------------------------------------------------

def calculate_vertical_gap(
    new_column,
    existing_column
):
    """
    Calculate the vertical distance between
    the bottom of the new column and the top
    of the existing column.

    All coordinates are in metres.
    """

    return (
        new_column["Zmin"]
        - existing_column["Zmax"]
    )


def is_potential_support(
    new_column,
    existing_column,
    max_vertical_gap=MAX_VERTICAL_GAP
):
    """
    Check whether an existing column is
    located at a relevant level below
    the new column.
    """

    if not has_valid_geometry(existing_column):
        return False

    if existing_column["Zmin"] >= new_column["Zmin"]:
        return False

    vertical_gap = calculate_vertical_gap(
        new_column,
        existing_column
    )

    return (
        -VERTICAL_OVERLAP_TOLERANCE
        <= vertical_gap
        <= max_vertical_gap
    )


# --------------------------------------------------
# 5. CALCULATE HORIZONTAL OFFSET
# --------------------------------------------------

def calculate_horizontal_offset(
    new_column,
    existing_column
):
    """
    Calculate the horizontal centre-to-centre
    distance between two columns.
    """

    dx = (
        new_column["X_center"]
        - existing_column["X_center"]
    )

    dy = (
        new_column["Y_center"]
        - existing_column["Y_center"]
    )

    horizontal_offset = math.hypot(dx, dy)

    return dx, dy, horizontal_offset


# --------------------------------------------------
# 6. FIND CLOSEST EXISTING COLUMN
# --------------------------------------------------

def find_closest_support(
    new_column,
    existing_columns,
    max_vertical_gap=MAX_VERTICAL_GAP
):
    """
    Find the closest existing load-bearing
    column at a relevant level below
    the new glulam column.
    """

    closest_column = None
    minimum_offset = float("inf")

    for existing_column in existing_columns:

        if not is_potential_support(
            new_column,
            existing_column,
            max_vertical_gap
        ):
            continue

        _, _, offset = calculate_horizontal_offset(
            new_column,
            existing_column
        )

        if offset < minimum_offset:

            minimum_offset = offset
            closest_column = existing_column

    return closest_column


# --------------------------------------------------
# 7. CREATE RESULT RECORD
# --------------------------------------------------

def create_result(column):
    """
    Create a consistent result structure
    for the CSV export.
    """

    return {

        "New_Column_ID": column["GlobalId"],
        "New_Column_Name": column["Name"],
        "New_Column_Storey": column["Storey"],
        "New_Column_Material": column["Material"],

        "Existing_Column_ID": "",
        "Existing_Column_Name": "",
        "Existing_Column_Storey": "",

        "Delta_X_mm": None,
        "Delta_Y_mm": None,
        "Horizontal_Offset_mm": None,
        "Vertical_Gap_mm": None,
        "Tolerance_mm": None,

        "Result": "",
        "Comment": ""

    }


# --------------------------------------------------
# 8. PERFORM COLUMN ALIGNMENT ANALYSIS
# --------------------------------------------------

def check_column_alignment(
    new_columns,
    existing_columns,
    tolerance=ALIGNMENT_TOLERANCE,
    max_vertical_gap=MAX_VERTICAL_GAP
):
    """
    Analyse each new glulam column and compare
    it with the closest eligible existing column.
    """

    if tolerance < 0 or max_vertical_gap < 0:
        raise ValueError(
            "Analysis tolerances must be non-negative."
        )

    results = []

    for new_column in new_columns:

        result = create_result(new_column)

        result["Tolerance_mm"] = tolerance * 1000

        # Check whether geometry is available
        if not has_valid_geometry(new_column):

            result["Result"] = "MISSING_GEOMETRY"

            result["Comment"] = (
                "New column geometry is unavailable."
            )

            results.append(result)
            continue

        # Find the closest potential support
        existing_column = find_closest_support(
            new_column,
            existing_columns,
            max_vertical_gap
        )

        # No eligible existing column found
        if existing_column is None:

            result["Result"] = "NO_SUPPORT_FOUND"

            result["Comment"] = (
                "No eligible existing load-bearing "
                "column was identified within the "
                "vertical search range."
            )

            results.append(result)
            continue

        # Calculate horizontal offset
        dx, dy, offset = calculate_horizontal_offset(
            new_column,
            existing_column
        )

        # Calculate vertical gap
        vertical_gap = calculate_vertical_gap(
            new_column,
            existing_column
        )

        # Store matching column information
        result["Existing_Column_ID"] = (
            existing_column["GlobalId"]
        )

        result["Existing_Column_Name"] = (
            existing_column["Name"]
        )

        result["Existing_Column_Storey"] = (
            existing_column["Storey"]
        )

        # Convert metres to millimetres
        result["Delta_X_mm"] = round(dx * 1000, 2)

        result["Delta_Y_mm"] = round(dy * 1000, 2)

        result["Horizontal_Offset_mm"] = round(
            offset * 1000,
            2
        )

        result["Vertical_Gap_mm"] = round(
            vertical_gap * 1000,
            2
        )

        # Evaluate horizontal alignment
        if offset <= tolerance:

            result["Result"] = "ALIGNED"

            result["Comment"] = (
                "Horizontal offset is within "
                "the defined screening tolerance."
            )

        else:

            result["Result"] = "REVIEW"

            result["Comment"] = (
                "Horizontal offset exceeds "
                "the defined screening tolerance."
            )

        results.append(result)

    return results


# --------------------------------------------------
# 9. GENERATE ANALYSIS SUMMARY
# --------------------------------------------------

def alignment_summary(results):
    """
    Summarise the column alignment results.
    """

    summary = {

        "Total_Checked": len(results),

        "Aligned": 0,
        "Review": 0,
        "No_Support_Found": 0,
        "Missing_Geometry": 0,

        "Evaluated": 0,
        "Alignment_Percentage": None

    }

    for result in results:

        status = result["Result"]

        if status == "ALIGNED":
            summary["Aligned"] += 1

        elif status == "REVIEW":
            summary["Review"] += 1

        elif status == "NO_SUPPORT_FOUND":
            summary["No_Support_Found"] += 1

        elif status == "MISSING_GEOMETRY":
            summary["Missing_Geometry"] += 1

    evaluated = (
        summary["Aligned"]
        + summary["Review"]
    )

    summary["Evaluated"] = evaluated

    if evaluated > 0:

        summary["Alignment_Percentage"] = round(
            summary["Aligned"] / evaluated * 100,
            2
        )

    return summary


# --------------------------------------------------
# 10. RUN COMPLETE ANALYSIS
# --------------------------------------------------

def run_analysis(
    elements,
    tolerance=ALIGNMENT_TOLERANCE,
    max_vertical_gap=MAX_VERTICAL_GAP
):
    """
    Main analysis function.

    Receives structural element data
    from ifc_reader.py and returns
    classification and alignment results.
    """

    (
        new_columns,
        existing_columns,
        unclassified_columns,
        other_columns

    ) = classify_columns(elements)

    results = check_column_alignment(
        new_columns,
        existing_columns,
        tolerance,
        max_vertical_gap
    )

    summary = alignment_summary(results)

    summary["New_Glulam_Columns"] = len(
        new_columns
    )

    summary["Existing_LoadBearing_Columns"] = len(
        existing_columns
    )

    summary["Unclassified_Columns"] = len(
        unclassified_columns
    )

    summary["Other_Columns"] = len(
        other_columns
    )

    summary["Existing_Missing_Geometry"] = sum(
        not has_valid_geometry(column)
        for column in existing_columns
    )

    return {
        "results": results,
        "summary": summary,
        "new_columns": new_columns,
        "existing_columns": existing_columns,
        "unclassified_columns": unclassified_columns,
        "other_columns": other_columns
    }

