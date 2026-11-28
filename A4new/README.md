# A4 – Tool: Column Support Check

**Group:** 22  
**Focus area:** STR – Structures  
**Role:** Analyst  
**Project:** Building 308  
**Software:** Python, IfcOpenShell, node-comply IFC starter template

This folder is built on the course's node-comply IFC starter template
(Week 11, extending the
[Working Together example](https://github.com/timmcginley/41934/blob/main/Activities/workingTogether.md)).
The runner (`runall.py`, `settings.py`) is from the template. Our analysis is
in [`column_support_check/`](column_support_check/). The template's
`window_count` example is kept so the template's own tests still run.

---

## 1. About the tool

### Problem and claim

A column that stands on a slab with nothing directly below it delivers a
concentrated point load into the slab. The slab then has to carry that load
in bending and punching shear to the nearest support. This is usually
unintended, expensive to fix late in design, and easy to miss in a large
model.

The claim we check:

> Columns are placed so that their loads are carried directly down to a
> supporting element (column, load-bearing wall, beam or foundation), and
> do not land on a slab with no support below.

> **TODO (group):** Insert the exact wording, section and page from the
> structural report for Building 308 that states this load path principle.
> Our A2 claim referred to Structural Report 2601, Section 2.4 (p. 4) and
> Section 8.1 (p. 20).

This widens the claim from A2. A2 only looked at new glulam columns over
existing columns. The tool now checks **every column in the building**, of
any material, against **any supporting element** below.

### Description of the tool

For each `IfcColumn`, the tool looks straight down from the column base.
It uses five points inside the column's footprint (the centre and four
points halfway to the edges). This means a wall or beam under part of the
column is still found.

```text
               column
                 │
   ══════════════╧══════════════   slab
                 ?                 ← what is directly below here?
```

| Result | Meaning | Review? |
|---|---|---|
| `DIRECT_SUPPORT` | Column stands directly on a column, wall, beam, member, footing or pile. | No |
| `SUPPORTED_THROUGH_SLAB` | Column stands on a slab, and a supporting element is directly below the slab at the same place. | No |
| `UNSUPPORTED_SLAB` | Column stands on a slab with **nothing below it**: a point load into the slab. The nearest support within 2 m is reported. | **Yes** |
| `NO_BEARING_ELEMENT` | Nothing is modelled under the column at all (e.g. missing foundations). | **Yes** |
| `ON_BASE_SLAB` | Column stands on a ground slab: `PredefinedType = BASESLAB`, or the lowest slab in the model (see below). The load is assumed to go into the ground. | Note |
| `MISSING_GEOMETRY` | The column has no usable geometry and could not be checked. | **Yes** |

Details:

- Geometry is triangulated with IfcOpenShell in world coordinates (metres).
  The tool finds where a vertical line crosses each element's faces, so it
  follows the real shape of slabs and walls, not just bounding boxes.
- Stacked slabs (e.g. topping on a structural slab) are followed downwards,
  up to three layers.
- Columns are both checked and treated as possible supports for columns
  above.
- Walls, beams and columns with `Pset_*Common.LoadBearing = FALSE` are not
  accepted as supports. Elements with no `LoadBearing` value are accepted,
  and their number is reported.

Screening tolerances are set at the top of
[`column_support_check/src/main.py`](column_support_check/src/main.py):

| Parameter | Default | Meaning |
|---|---:|---|
| `max_gap` | 0.05 m | Largest gap between two surfaces still counted as contact |
| `below_eps` | 0.01 m | How far an element must reach below a level to count as underneath it |
| `overlap` | 0.05 m | Allowed modelled overlap (clash) at a contact |
| `max_slab_layers` | 3 | Stacked slabs followed downwards |
| `search_radius` | 2.0 m | Radius for reporting the nearest support of a flagged column |
| `lowest_slab_is_ground` | `True` | Treat the lowest slab in the model as a ground slab, even if it is typed `FLOOR` |
| `ground_tolerance` | 0.10 m | Slabs whose underside is within this distance of the lowest slab also count as ground slabs |

**Why the lowest-slab rule?** In B308X the 600 mm ground slab
(`Floor:EX_Heavy Weight_600mm`) is exported from Revit as `FLOOR`, not
`BASESLAB`. Without the rule, every ground-floor column was flagged as
standing on an unsupported slab (89 false flags). Each such result now shows
`ground_slab_reason`, so the assumption stays visible. The IDS rule STR22-02
still reports the wrong `PredefinedType` to the model author. Set
`lowest_slab_is_ground=False` to switch the rule off.

These are preliminary screening values and must be reviewed by the
structural engineer.

### Output

Each run writes
`column_support_check/results/run-<UTC-time>-<suffix>/result.json`:

```json
{
  "summary": {
    "columns_total": 211,
    "result_counts": {"UNSUPPORTED_SLAB": 3, "SUPPORTED_THROUGH_SLAB": 94, "...": 0},
    "columns_needing_review": 3,
    "share_with_vertical_support_percent": 98.6
  },
  "flagged_columns": ["2O2Fr$t4X7Zf8NOew3FLOH", "..."],
  "columns": [
    {
      "global_id": "2O2Fr$t4X7Zf8NOew3FLOH",
      "storey": "E1_1. sal",
      "result": "UNSUPPORTED_SLAB",
      "lands_on": [{"global_id": "...", "ifc_type": "IfcSlab"}],
      "nearest_support": {"ifc_type": "IfcWall", "distance_from_column_centre_m": 0.35},
      "comment": "Column delivers a point load into a slab with no supporting element directly below."
    }
  ],
  "parameters": {"max_gap_m": 0.05, "...": 0}
}
```

*(The numbers above are illustrative only. They are not results for B308X.)*

Flagged columns are listed first. You can search for `flagged_columns`
GlobalIds in Bonsai/Blender to inspect them.

---

## 2. How to run

### Install (once)

| Windows | macOS |
|---|---|
| `py -m venv .venv` | `python3 -m venv .venv` |
| `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` | `.venv/bin/python -m pip install -r requirements.txt` |

### Put the model in place

Copy the IFC model to **`A4/data/B308X.ifc`**. `settings.py` points to this
relative path, so it works on Windows and macOS without anyone editing the
code. The `data/` folder and all `*.ifc` files are ignored by git, so the
model is never uploaded.

### Run

| | Windows | macOS |
|---|---|---|
| Default model | `.\.venv\Scripts\python.exe runall.py` | `.venv/bin/python runall.py` |
| Another model | `.\.venv\Scripts\python.exe runall.py "C:\path\model.ifc"` | `.venv/bin/python runall.py ~/path/model.ifc` |
| Tests | `.\.venv\Scripts\python.exe -m unittest discover -s tests` | `.venv/bin/python -m unittest discover -s tests` |

If the model is missing, the runner stops with `IFC file not found: …`.

### Reuse in another script

```python
from column_support_check.src.main import analyse
result = analyse(model)   # model = ifcopenshell.open(...)
```

Importing the function does not load a model or write files.

---

## 3. Advanced Building Design

### Stage

**Stage C (Design).** At this stage the structural system and column grid
are being fixed and coordinated with architecture. Columns that land on
unsupported slabs can still be moved, or a transfer beam can be added,
cheaply.

The check is also useful in **stage B** (to test early structural layouts)
and when the model is updated in **stage D**.

### Subjects that might use it

- Structural design (load paths, transfer structures, punching)
- Architecture and design coordination (column grid changes)
- BIM coordination and model quality assurance

### Information the model must contain

| Information | Why |
|---|---|
| Columns as `IfcColumn` with 3D geometry | Columns to check |
| Slabs as `IfcSlab` with geometry | What columns stand on |
| `IfcSlab.PredefinedType` (`BASESLAB` for ground slabs) | Separate ground slabs from suspended slabs |
| Walls, beams, members, footings, piles with geometry | Possible supports |
| `Pset_*Common.LoadBearing` on columns, walls and beams | Exclude non-load-bearing partitions as supports |
| Columns contained in an `IfcBuildingStorey` | Report results per storey |
| One consistent coordinate system for all disciplines | Elements from different models must line up vertically |

---

## 4. IDS

[`column_support_check/requirements.ids`](column_support_check/requirements.ids)
checks that a model is ready for the tool:

| ID | Applies to | Requirement |
|---|---|---|
| STR22-01 | `IfcColumn` (at least one required) | Contained in an `IfcBuildingStorey`; `Pset_ColumnCommon.LoadBearing` (boolean) |
| STR22-02 | `IfcSlab` (at least one required) | `PredefinedType` is `FLOOR`, `ROOF`, `LANDING` or `BASESLAB` |
| STR22-03 | `IfcWall` | `Pset_WallCommon.LoadBearing` (boolean) |
| STR22-04 | `IfcBeam` | `Pset_BeamCommon.LoadBearing` (boolean) |

The IDS targets IFC4 and IFC4X3. It cannot check geometry or alignment;
that is what the Python tool does.

---

## 5. Workflow (BPMN)

> **TODO (group):** Update the as-is and to-be BPMN diagrams from A2
> (`../A2/IMG/`) to this wider check, and link them here.

**As-is:** The structural engineer opens the model, goes storey by storey,
looks under each column for a supporting element, and notes the columns that
stand on a slab. This is slow, and it is easy to miss columns in a large
model.

**To-be:** The model is checked against the IDS → `runall.py` runs the
column support check → the engineer reviews only the flagged columns in
`result.json` (and in Bonsai, using their GlobalIds) → the columns are moved,
or a transfer beam or wall is added → run again.

---

## 6. Testing

`tests/test_column_support.py` builds a small two-storey test model from
boxes: a base slab, a floor slab, a wall, a beam and columns. It checks each
result type:

- a column over a column, wall or beam → `SUPPORTED_THROUGH_SLAB`
- a column on a slab with nothing below → `UNSUPPORTED_SLAB`
- a column 0.35 m beside a wall → `UNSUPPORTED_SLAB`, with that wall
  reported as the nearest support
- a column directly on a wall top → `DIRECT_SUPPORT`
- a ground column → `ON_BASE_SLAB`, also when the ground slab is typed `FLOOR`
  (lowest-slab rule), and `UNSUPPORTED_SLAB` when the rule is switched off
- a floating column → `NO_BEARING_ELEMENT`
- the gap tolerance (0.03 m counts as contact, 0.25 m does not)

These tests do not need IfcOpenShell. `tests/test_starter.py` holds the
template's runner tests, which need IfcOpenShell.

### First run on B308X (IFC4X3, 211 columns, 4 slabs)

Before the lowest-slab rule was added:

| Storey | OK | `UNSUPPORTED_SLAB` | `NO_BEARING_ELEMENT` |
|---|---:|---:|---:|
| ES_Stue (ground floor) | 3 | 89 | 2 |
| E1_1. sal (1st floor) | 69 | 46 | 2 |

- **Ground floor:** all 89 flags were columns on the 600 mm ground slab,
  which is typed `FLOOR` (a model information issue, not a structural one).
  This is why the lowest-slab rule was added.
- **1st floor:** 46 columns stand on the 160 mm slab
  (`Floor:IN_Heavy Weight_160mm`) with no column or wall directly below.
  39 of these have no support within 2 m. Examples are the rows of
  200×240 mm columns at y = −221.88 and y = −209.37, where the columns
  below are at y = −214.8 and −227.9. These are the point loads the tool is
  meant to find.

> **TODO (group):** Run again with the lowest-slab rule and update the
> table. Check two or three flagged 1st-floor columns visually in Bonsai.

---

## 7. Limitations

- This is geometric screening. It does not check load size, capacity,
  punching or connections.
- A column counts as supported only if the support is **directly** below
  it, within the tolerances. Supports that are offset are reported as
  nearest support for the engineer to judge.
- Results depend on model quality: missing foundations give
  `NO_BEARING_ELEMENT`, and a missing `LoadBearing` property means
  partitions may be accepted as supports.
- Existing and new structures in separate IFC files must be merged, or
  share coordinates, before the check is meaningful.
- A slab supported only at its edges (spanning between walls) can still
  give `UNSUPPORTED_SLAB` for a column in the middle. That is intended:
  the column load goes into the slab.

---

## 8. Folder structure

```text
A4/
├── README.md                 this report
├── CHANGELOG.md
├── requirements.txt
├── settings.py               MODEL_PATH = "data/B308X.ifc"
├── runall.py                 template runner (opens IFC once, runs analyses)
├── data/                     local IFC models (ignored by git)
├── column_support_check/     our analysis
│   ├── requirements.ids
│   ├── src/
│   │   ├── main.py           analyse(model) + tolerances + IFC extraction
│   │   ├── support_check.py  load path logic (no IfcOpenShell)
│   │   └── geometry.py       mesh / vertical line intersection
│   └── results/run-.../result.json
├── window_count/             template example
└── tests/
```

## References

- Course node-comply IFC starter template and the Working Together example.
- IfcOpenShell: https://ifcopenshell.org/
- buildingSMART IDS: https://technical.buildingsmart.org/projects/information-delivery-specification-ids/
- Future AEC Software Specification: https://future-aec-software-specification.com/data-framework/
