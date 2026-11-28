# A4 – Column Support Check

**Group 22 · STR (Structures) · Analyst · Building 308**

A Python tool that finds columns that **stand on a slab with nothing
underneath**. Such columns put a large point load into the slab.

## 1. Problem and claim

> Columns are placed so their loads go directly down to a supporting element
> (column, load-bearing wall, beam or foundation), and not onto a slab with
> nothing underneath.


In A2 we only looked at new glulam columns. The tool now checks all columns.

## 2. How it works

For each column, the tool looks straight down from its base and checks what
it stands on:

| Result | Meaning | Review? |
|---|---|---|
| `DIRECT_SUPPORT` | On a column, wall, beam or foundation | No |
| `SUPPORTED_THROUGH_SLAB` | On a slab, with a support directly below | No |
| `ON_BASE_SLAB` | On the ground slab | No |
| `UNSUPPORTED_SLAB` | **On a slab with nothing below** | **Yes** |
| `NO_BEARING_ELEMENT` | Nothing modelled below at all | **Yes** |
| `MISSING_GEOMETRY` | No 3D shape, so it cannot be checked | **Yes** |

Elements with `LoadBearing = FALSE` do not count as supports. The lowest slab
in the model counts as a ground slab. Tolerances are set in
`column_support_check/src/main.py`.

## 3. How to run

1. Put the model in `A4new/data/B308X.ifc` (not uploaded to GitHub).
2. Open a terminal in `A4new` and run:

```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe runall.py
```

On macOS, use `python3` and `.venv/bin/python`.
The result is saved in `column_support_check/results/run-.../result.json`.
Tests: `python -m unittest discover -s tests`.

## 4. Results for B308X

| Result | Columns |
|---|---:|
| `DIRECT_SUPPORT` | 48 |
| `SUPPORTED_THROUGH_SLAB` | 24 |
| `ON_BASE_SLAB` | 89 |
| `UNSUPPORTED_SLAB` | **46** |
| `NO_BEARING_ELEMENT` | **4** |

**161 of 211 columns (76 %) have a clear load path. 50 need review.**

- **46 columns on the 1st floor** stand on the 160 mm slab with nothing
  below. Most are in rows shifted from the ground floor columns.
- **4 columns at the building edge** have nothing below. This is probably a
  modelling issue.

**Model issue:** The 600 mm ground slab is typed `FLOOR`, not `BASESLAB`. On
the first run this gave 89 false flags. The model should be fixed; our IDS
checks for this.

## 5. Advanced Building Design

- **Stage:** C (Design), when the column grid can still be changed cheaply.
- **Users:** structural engineers, architects, BIM coordinators.
- **Model must contain:** `IfcColumn`, `IfcSlab`, walls, beams and
  foundations with geometry; `PredefinedType` on slabs; `LoadBearing` on
  columns, walls and beams; columns placed on a storey.

## 6. IDS

`column_support_check/requirements.ids` checks that columns are on a storey
and have `LoadBearing`, that slabs have a valid `PredefinedType`, and that
walls and beams have `LoadBearing`.

## 7. Workflow

**As-is:** The engineer checks each column by hand in the model.
**To-be:** Check the model with the IDS → run the tool → review only the
flagged columns → fix → run again.

## 8. Limitations

- Geometry only. No check of loads, strength or punching.
- The support must be directly below the column to count.
- The results depend on the quality of the model.

## Use of AI

We used an AI assistant (Claude, by Anthropic) to help write the code, tests,
IDS and README, to read the results, and to set up GitHub. The group chose
the claim, ran the tool on the model and checked the results.


---

Built on the course's node-comply IFC starter template. References:
[IfcOpenShell](https://ifcopenshell.org/),
[buildingSMART IDS](https://technical.buildingsmart.org/projects/information-delivery-specification-ids/),
[Future AEC Software Specification](https://future-aec-software-specification.com/data-framework/).
