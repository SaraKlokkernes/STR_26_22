
# main.py

"""
Vertical Load Transfer Checker
Main program

Imports the checking functions from team_tool.py,
opens an IFC model, analyses the structural columns
and exports the results to a CSV report.
"""

import argparse
import csv
from pathlib import Path

import ifcopenshell

from team_tool import analyse


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

DEFAULT_VERTICAL_TOLERANCE = 0.15
DEFAULT_MIN_OVERLAP_RATIO = 0.50


# --------------------------------------------------
# SELECT IFC MODEL
# --------------------------------------------------

def select_model():

    model_path = input(
        "\nEnter the path to your IFC model: "
    ).strip().strip('"')

    model_path = Path(model_path).expanduser()

    if not model_path.is_file():
        raise FileNotFoundError(
            f"No IFC file found at: {model_path}"
        )

    if model_path.suffix.lower() != ".ifc":
        raise ValueError("Please select an IFC file.")

    return model_path


# --------------------------------------------------
# OPEN IFC MODEL
# --------------------------------------------------

def open_model(model_path):

    print("\nOpening IFC model...")

    model = ifcopenshell.open(str(model_path))

    print("IFC model successfully opened.")

    return model


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

def display_results(report):

    print("\n" + "=" * 55)
    print("VERTICAL LOAD TRANSFER CHECKER")
    print("=" * 55)

    print(f"Elements analysed: {report['Element_Count']}")
    print(f"Columns analysed:  {report['Column_Count']}")

    print("-" * 55)

    print(f"SUPPORTED:         {report['Supported']}")
    print(f"UNSUPPORTED:       {report['Unsupported']}")
    print(f"REVIEW:            {report['Review']}")

    print("-" * 55)

    if not report["Results"]:
        print("No columns were found in the IFC model.")
        return

    print("\nCOLUMN RESULTS")
    print("-" * 55)

    for result in report["Results"]:

        print(f"\nColumn: {result['Column_Name']}")
        print(f"GlobalId: {result['Column_ID']}")

        print(f"Status: {result['Status']}")

        if result["Support_ID"]:

            print(
                f"Supporting element: "
                f"{result['Support_Name']}"
            )

            print(
                f"Support type: "
                f"{result['Support_Type']}"
            )

            print(
                f"Overlap: "
                f"{result['Overlap_Percent']}%"
            )

            print(
                f"Vertical gap: "
                f"{result['Vertical_Gap_m']} m"
            )

        else:

            print("No potential supporting element found.")


# --------------------------------------------------
# EXPORT CSV REPORT
# --------------------------------------------------

def export_report(report, output_path):

    fieldnames = [
        "Column_ID",
        "Column_Name",
        "Support_ID",
        "Support_Name",
        "Support_Type",
        "Overlap_Percent",
        "Vertical_Gap_m",
        "Status"
    ]

    with open(
        output_path,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(report["Results"])

    print("\nCSV report successfully created:")
    print(output_path)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Vertical Load Transfer Checker"
    )

    parser.add_argument(
        "ifc_file",
        nargs="?",
        help="Path to the IFC model"
    )

    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_VERTICAL_TOLERANCE,
        help="Vertical tolerance in metres"
    )

    parser.add_argument(
        "--overlap",
        type=float,
        default=DEFAULT_MIN_OVERLAP_RATIO,
        help="Minimum horizontal overlap ratio"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Optional output CSV path"
    )

    args = parser.parse_args()

    try:

        # 1. Select IFC model
        if args.ifc_file:
            model_path = Path(
                args.ifc_file
            ).expanduser()
        else:
            model_path = select_model()

        if not model_path.is_file():
            raise FileNotFoundError(
                f"No IFC file found at: {model_path}"
            )

        if model_path.suffix.lower() != ".ifc":
            raise ValueError("Please provide an IFC file.")

        # 2. Open IFC model
        model = open_model(model_path)

        # 3. Analyse the model
        print("\nAnalysing structural elements...")

        report = analyse(
            model,
            vertical_tolerance=args.tolerance,
            min_overlap_ratio=args.overlap
        )

        # 4. Display results
        display_results(report)

        # 5. Export CSV
        if args.output:
            output_path = Path(args.output).expanduser()
        else:
            output_path = (
                model_path.parent
                / f"{model_path.stem}_load_transfer_report.csv"
            )

        export_report(report, output_path)

        print("\nAnalysis completed successfully!")

    except Exception as error:

        print(f"\nERROR: {error}")
        raise SystemExit(1)


# --------------------------------------------------
# RUN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    main()

