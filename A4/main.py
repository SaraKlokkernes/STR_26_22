
# main.py

"""
Vertical Load Path Checker
Group 22 - STR - Structures
Assignment A4 - Tool Development

Project: Building 308

Aim:
Investigate whether new glulam columns are
positioned above existing load-bearing columns.

Workflow:
1. IFC element extraction
2. Column classification
3. Vertical load path analysis
4. Results and CSV export

This tool provides geometric screening only.
It does not verify structural capacity.
"""

from pathlib import Path
import csv

from ifc_reader import (
    read_ifc,
    extract_structural_elements,
    element_summary
)

from team_tool import (
    run_analysis,
    create_result,
    ALIGNMENT_TOLERANCE,
    MAX_VERTICAL_GAP,
    VERTICAL_OVERLAP_TOLERANCE
)


# --------------------------------------------------
# 1. LOCAL IFC MODEL PATH
# --------------------------------------------------

# Replace this path with the location of
# the IFC model on your local computer.

model_path = Path(
    r"C:/Users/YourName/Documents/Building308.ifc"
)

# The IFC model must not be uploaded to GitHub.


# --------------------------------------------------
# 2. OUTPUT DIRECTORY
# --------------------------------------------------

output_folder = (
    Path(__file__).resolve().parent / "output"
)


# --------------------------------------------------
# 3. CSV EXPORT FUNCTION
# --------------------------------------------------

def export_csv(data, file_path, fieldnames=None):
    """
    Export a list of dictionaries to a CSV file.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if fieldnames is None:

        if not data:

            print(
                f"No data available for "
                f"{file_path.name}"
            )

            # Remove an outdated result from
            # an earlier analysis, if present.
            if file_path.exists():
                file_path.unlink()

            return

        fieldnames = list(data[0].keys())

    with open(
        file_path,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(data)

    print(f"CSV exported: {file_path}")


# --------------------------------------------------
# 4. PRINT SECTION HEADINGS
# --------------------------------------------------

def print_section(title):
    """
    Display a readable section heading.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# --------------------------------------------------
# 5. PRINT ELEMENT EXTRACTION SUMMARY
# --------------------------------------------------

def print_element_summary(summary):
    """
    Display the structural element inventory.
    """

    print(f"Total elements: {summary['Total']}")

    print(f"Columns: {summary['Columns']}")
    print(f"Beams: {summary['Beams']}")
    print(f"Walls: {summary['Walls']}")
    print(f"Foundations: {summary['Foundations']}")

    print("\nGeometry availability:")

    print(
        f"Available: "
        f"{summary['Geometry_Available']}"
    )

    print(
        f"Missing: "
        f"{summary['Geometry_Missing']}"
    )

    print("\nMissing column information:")

    print(
        f"Unknown material: "
        f"{summary['Columns_Material_Unknown']}"
    )

    print(
        f"Unknown load-bearing property: "
        f"{summary['Columns_LoadBearing_Unknown']}"
    )

    print(
        f"Unknown construction status: "
        f"{summary['Columns_Status_Unknown']}"
    )


# --------------------------------------------------
# 6. PRINT CLASSIFICATION SUMMARY
# --------------------------------------------------

def print_classification_summary(summary):
    """
    Display the identified column categories.
    """

    print(
        f"New glulam columns: "
        f"{summary['New_Glulam_Columns']}"
    )

    print(
        f"Existing load-bearing columns: "
        f"{summary['Existing_LoadBearing_Columns']}"
    )

    print(
        f"Unclassified columns: "
        f"{summary['Unclassified_Columns']}"
    )

    print(
        f"Other columns: "
        f"{summary['Other_Columns']}"
    )

    print(
        f"Existing columns with missing geometry: "
        f"{summary['Existing_Missing_Geometry']}"
    )


# --------------------------------------------------
# 7. PRINT ALIGNMENT RESULTS
# --------------------------------------------------

def print_alignment_results(results):
    """
    Display the result for each new glulam column.
    """

    if not results:

        print("No new glulam columns were analysed.")

        return

    for result in results:

        print("\n" + "-" * 60)

        print(
            f"New column: "
            f"{result['New_Column_Name']}"
        )

        print(
            f"GlobalId: "
            f"{result['New_Column_ID']}"
        )

        print(
            f"Storey: "
            f"{result['New_Column_Storey']}"
        )

        existing_name = (
            result["Existing_Column_Name"]
            or "Not identified"
        )

        print(f"Existing column: {existing_name}")

        offset = result["Horizontal_Offset_mm"]

        if offset is not None:

            print(
                f"Horizontal offset: "
                f"{offset:.2f} mm"
            )

        else:

            print("Horizontal offset: Not available")

        vertical_gap = result["Vertical_Gap_mm"]

        if vertical_gap is not None:

            print(
                f"Vertical gap: "
                f"{vertical_gap:.2f} mm"
            )

        print(f"Result: {result['Result']}")

        print(f"Comment: {result['Comment']}")


# --------------------------------------------------
# 8. PRINT FINAL ANALYSIS SUMMARY
# --------------------------------------------------

def print_final_summary(summary):
    """
    Display the overall alignment assessment.
    """

    print(
        f"New glulam columns processed: "
        f"{summary['Total_Checked']}"
    )

    print(
        f"Evaluated column pairs: "
        f"{summary['Evaluated']}"
    )

    print(f"Aligned: {summary['Aligned']}")

    print(f"Review required: {summary['Review']}")

    print(
        f"No support found: "
        f"{summary['No_Support_Found']}"
    )

    print(
        f"Missing geometry: "
        f"{summary['Missing_Geometry']}"
    )

    print(
        f"Unclassified columns: "
        f"{summary['Unclassified_Columns']}"
    )

    percentage = summary["Alignment_Percentage"]

    if percentage is not None:

        print(
            f"\nAlignment among evaluated pairs: "
            f"{percentage:.2f}%"
        )

    else:

        print(
            "\nAlignment percentage: "
            "Not available"
        )

    print("\nInterpretation:")

    if summary["New_Glulam_Columns"] == 0:

        print(
            "The claim cannot be evaluated because "
            "no new glulam columns were identified."
        )

    elif summary["Evaluated"] == 0:

        print(
            "The claim cannot be evaluated because "
            "no column pairs could be assessed."
        )

    elif (
        summary["Aligned"]
        == summary["Total_Checked"]
        and summary["Unclassified_Columns"] == 0
        and summary["Existing_Missing_Geometry"] == 0
    ):

        print(
            "All identified new glulam columns "
            "are within the defined horizontal "
            "screening tolerance."
        )

        print(
            "The geometric results support the "
            "claim within the scope of this tool."
        )

    else:

        print(
            "The results require further review "
            "before drawing a conclusion about "
            "the claim."
        )

    print(
        "\nThis assessment does not constitute "
        "a structural safety or capacity check."
    )


# --------------------------------------------------
# 9. CHECK DATA QUALITY
# --------------------------------------------------

def print_data_quality_warnings(summary):
    """
    Report limitations caused by missing IFC data.
    """

    if summary["New_Glulam_Columns"] == 0:

        print(
            "\nWARNING: No new glulam columns "
            "were identified."
        )

        print(
            "Check material names and construction "
            "status properties in the IFC model."
        )

    if summary["Existing_LoadBearing_Columns"] == 0:

        print(
            "\nWARNING: No existing load-bearing "
            "columns were identified."
        )

        print(
            "Check construction status and "
            "LoadBearing properties."
        )

    if summary["Unclassified_Columns"] > 0:

        print(
            "\nWARNING: Some columns could not "
            "be classified reliably."
        )

        print(
            "Review the unclassified columns "
            "CSV file before interpreting results."
        )

    if summary["Existing_Missing_Geometry"] > 0:

        print(
            "\nWARNING: Some existing columns "
            "have missing geometry."
        )

        print(
            "Potential supports may be missing "
            "from the geometric analysis."
        )


# --------------------------------------------------
# 10. MAIN PROGRAM
# --------------------------------------------------

def main():

    print_section(
        "VERTICAL LOAD PATH CHECKER"
    )

    print("Group 22 - STR - Structures")
    print("Assignment A4")
    print("Project: Building 308")

    # Check local IFC model path

    if not model_path.is_file():

        raise FileNotFoundError(
            f"No IFC file found at {model_path}!"
        )

    print(f"\nIFC model: {model_path.name}")

    # ----------------------------------------------
    # Phase 1: IFC Element Extraction
    # ----------------------------------------------

    print_section(
        "PHASE 1 - IFC ELEMENT EXTRACTION"
    )

    model = read_ifc(model_path)

    elements = extract_structural_elements(
        model
    )

    inventory_summary = element_summary(
        elements
    )

    print_element_summary(inventory_summary)

    # ----------------------------------------------
    # Phase 2: Column Classification
    # ----------------------------------------------

    print_section(
        "PHASE 2 - COLUMN CLASSIFICATION"
    )

    analysis = run_analysis(
        elements,
        tolerance=ALIGNMENT_TOLERANCE,
        max_vertical_gap=MAX_VERTICAL_GAP
    )

    results = analysis["results"]
    summary = analysis["summary"]

    print_classification_summary(summary)

    print_data_quality_warnings(summary)

    # ----------------------------------------------
    # Phase 3: Vertical Load Path Analysis
    # ----------------------------------------------

    print_section(
        "PHASE 3 - VERTICAL LOAD PATH ANALYSIS"
    )

    print(
        f"Horizontal tolerance: "
        f"{ALIGNMENT_TOLERANCE * 1000:.0f} mm"
    )

    print(
        f"Maximum vertical gap: "
        f"{MAX_VERTICAL_GAP * 1000:.0f} mm"
    )

    print(
        f"Permitted vertical overlap: "
        f"{VERTICAL_OVERLAP_TOLERANCE * 1000:.0f} mm"
    )

    print_alignment_results(results)

    # ----------------------------------------------
    # Phase 4: Results and Export
    # ----------------------------------------------

    print_section(
        "PHASE 4 - RESULTS AND EXPORT"
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    model_name = model_path.stem

    # Export structural element inventory

    inventory_path = (
        output_folder
        / f"{model_name}_element_inventory.csv"
    )

    export_csv(
        elements,
        inventory_path
    )

    # Export column alignment results

    alignment_path = (
        output_folder
        / f"{model_name}_column_alignment.csv"
    )

    # Define the result columns so that an empty
    # analysis still produces a CSV header.

    result_fields = list(
        create_result({
            "GlobalId": "",
            "Name": "",
            "Storey": "",
            "Material": ""
        }).keys()
    )

    export_csv(
        results,
        alignment_path,
        fieldnames=result_fields
    )

    # Export unclassified columns

    unclassified_path = (
        output_folder
        / f"{model_name}_unclassified_columns.csv"
    )

    if elements:

        export_csv(
            analysis["unclassified_columns"],
            unclassified_path,
            fieldnames=list(elements[0].keys())
        )

    else:

        export_csv(
            [],
            unclassified_path
        )

    # Export analysis summary

    summary_path = (
        output_folder
        / f"{model_name}_analysis_summary.csv"
    )

    export_csv(
        [summary],
        summary_path
    )

    # Print final results

    print_section(
        "FINAL ANALYSIS SUMMARY"
    )

    print_final_summary(summary)

    print(
        f"\nResults folder: {output_folder}"
    )

    print("\nAnalysis completed.")


# --------------------------------------------------
# 11. RUN THE TOOL
# --------------------------------------------------

if __name__ == "__main__":

    main()
