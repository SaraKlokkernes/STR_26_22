
# main.py

"""
Vertical Load Path Checker

Phase 1:
Read an IFC model and extract structural elements.
Generate a structural element inventory in CSV format.
"""

import csv
import argparse

from pathlib import Path

from ifc_reader import (
    read_ifc,
    extract_structural_elements,
    element_summary
)


# --------------------------------------------------
# 1. SELECT IFC MODEL
# --------------------------------------------------

def select_ifc_file():

    path = input(
        "\nEnter the path to your IFC model: "
    ).strip().strip('"')

    ifc_path = Path(path).expanduser()

    if not ifc_path.is_file():
        raise FileNotFoundError(
            f"IFC file not found: {ifc_path}"
        )

    if ifc_path.suffix.lower() != ".ifc":
        raise ValueError(
            "The selected file must be an IFC file."
        )

    return ifc_path


# --------------------------------------------------
# 2. DISPLAY SUMMARY
# --------------------------------------------------

def display_summary(summary, schema):

    print("\n" + "=" * 45)
    print("VERTICAL LOAD PATH CHECKER")
    print("PHASE 1: IFC ELEMENT EXTRACTION")
    print("=" * 45)

    print(f"\nIFC schema: {schema}")

    print("\nSTRUCTURAL ELEMENTS")

    print("-" * 35)

    print(f"Columns:             {summary['Columns']}")
    print(f"Beams:               {summary['Beams']}")
    print(f"Walls:               {summary['Walls']}")
    print(f"Foundations:         {summary['Foundations']}")

    print("-" * 35)

    print(f"Total elements:      {summary['Total']}")

    print(
        f"Geometry available:  "
        f"{summary['Geometry_Available']}"
    )

    print(
        f"Geometry missing:    "
        f"{summary['Geometry_Missing']}"
    )


# --------------------------------------------------
# 3. EXPORT CSV INVENTORY
# --------------------------------------------------

def export_inventory(elements, output_path):

    if not elements:
        print("\nNo structural elements found.")
        return

    fieldnames = list(elements[0].keys())

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(elements)

    print("\nInventory exported successfully:")
    print(output_path)


# --------------------------------------------------
# 4. MAIN PROGRAM
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Vertical Load Path Checker"
    )

    parser.add_argument(
        "ifc_file",
        nargs="?",
        help="Path to IFC model"
    )

    args = parser.parse_args()

    try:

        # Select IFC file
        if args.ifc_file:

            ifc_path = Path(
                args.ifc_file
            ).expanduser()

            if not ifc_path.is_file():
                raise FileNotFoundError(
                    f"IFC file not found: {ifc_path}"
                )

            if ifc_path.suffix.lower() != ".ifc":
                raise ValueError(
                    "The selected file must be an IFC file."
                )

        else:

            ifc_path = select_ifc_file()

        # Read IFC model
        model = read_ifc(ifc_path)

        # Extract structural elements
        print("\nExtracting structural elements...")

        elements = extract_structural_elements(model)

        # Generate summary
        summary = element_summary(elements)

        # Display results
        display_summary(
            summary,
            model.schema
        )

        # Export inventory
        output_path = (
            ifc_path.parent
            / f"{ifc_path.stem}_element_inventory.csv"
        )

        export_inventory(
            elements,
            output_path
        )

        print("\nPhase 1 completed.")

    except Exception as error:

        print(f"\nERROR: {error}")

        raise SystemExit(1)


# --------------------------------------------------
# RUN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    main()

