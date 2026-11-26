# A4 – Tool Development

## Vertical Load Path Checker

**Group:** 22  
**Focus area:** STR – Structures  
**Role:** Analyst  
**Project:** Building 308  
**BIM purpose:** Analyse  
**BIM use case:** Design Coordination  

## 00 – Preparation

### Working approach

Following the use case analysis developed in Assignment A2, we continue in the role of a Analyst within the structural focus area.

Our objective is to develop a Python-based tool that analyses the spatial relationship between new glulam columns and existing load-bearing columns in the Building 308 IFC model.

The tool follows a modular structure, allowing the IFC data extraction and structural alignment analysis to be developed separately and potentially integrated into a larger structural checking workflow.

The development builds upon the existing Vertical Load Path Checker and extends its structural element extraction functionality with a column alignment assessment.

### Tool objective

The objective of the tool is to investigate whether new glulam columns are positioned directly above existing load-bearing columns, supporting the intended direct vertical load paths described in the structural report.

The tool identifies potential horizontal misalignments and provides results that can support structural engineers during design coordination.

### Software and tools

- Python – development of the analysis tool.
- IfcOpenShell – extraction of IFC information and geometry.
- Visual Studio Code – code development and testing.
- GitHub – version control and collaboration.
- Blender / Bonsai – visual inspection and verification of the IFC model.

### Repository structure

The tool is developed within the A4 folder of the group repository.

The intended file structure consists of:

- `main.py` – main program and execution of the analysis workflow.
- `ifc_reader.py` – extraction of structural elements, properties and geometry.
- `team_tool.py` – column classification and alignment analysis.
- `requirements.txt` – required Python dependencies.
- `requirements.ids` – information requirements for the IFC model.
- `README.md` – documentation of the tool.
- `.gitignore` – exclusion of local IFC model files from the repository.

The IFC model is stored locally and is not included in the GitHub repository.

## 01 – Tool Development

### Phase 1 – IFC Element Extraction

The IFC reader provides the input data required for the structural column alignment analysis.

The existing `ifc_reader.py` module has been extended to extract additional semantic and geometric information from the IFC model.

The extracted information includes:

- IFC element GlobalId and name.
- IFC entity and structural category.
- Assigned element type and material.
- Building storey.
- Load-bearing properties.
- Construction status.
- Global bounding box coordinates.
- Bounding box centre coordinates and element height.

The geometry is extracted in global model coordinates using metres as a consistent unit of measurement.

The horizontal centre coordinates are calculated from the minimum and maximum bounding box coordinates. For regular vertical columns, these coordinates provide an approximation of the column centreline.

Missing material, construction status or load-bearing information is reported as unknown rather than assumed.

The extracted information forms the basis for the subsequent identification of new glulam columns and existing load-bearing columns.

The separation of IFC data extraction and structural analysis supports a modular workflow and allows the extracted information to be reused in other structural checking tools.

The extraction method and its assumptions are subject to verification using the Building 308 IFC model.


### Phase 2 – Column Classification

The `team_tool.py` module receives the extracted structural element information from the IFC reader and identifies the columns relevant to the analysis.

The columns are classified into four categories:

- New glulam columns.
- Existing load-bearing columns.
- Unclassified columns with insufficient or unsupported information.
- Other columns outside the scope of the analysis.

New glulam columns are identified using material information and construction status. Existing load-bearing columns are identified using construction status and load-bearing properties.

Columns that cannot be classified reliably are reported separately. This prevents missing IFC information from being interpreted as a confirmed structural condition.

### Phase 3 – Vertical Load Path Analysis

The analysis investigates the spatial relationship between new glulam columns and existing load-bearing columns.

For each new glulam column, the tool identifies potential existing supports located at a relevant level below the new column.

The vertical relationship is evaluated using the difference between the bottom elevation of the new column and the top elevation of the existing column.

The horizontal offset is calculated using the X and Y centre coordinates of the respective column bounding boxes.

The closest eligible existing load-bearing column is selected for comparison.

The horizontal offset is calculated as the Euclidean distance between the two column centres in the XY plane.

#### Analysis parameters

The initial analysis uses the following configurable parameters:

| Parameter | Initial value |
|---|---:|
| Horizontal alignment tolerance | 150 mm |
| Maximum vertical gap | 500 mm |
| Permitted vertical overlap | 50 mm |

These values are preliminary screening parameters and are not derived from structural design standards. They must be reviewed and adjusted according to the actual building geometry and the requirements of the structural engineer.

#### Analysis results

Each new glulam column receives one of the following results:

- **ALIGNED:** The horizontal offset is within the defined screening tolerance.
- **REVIEW:** The horizontal offset exceeds the defined screening tolerance.
- **NO_SUPPORT_FOUND:** No eligible existing load-bearing column was identified within the vertical search range.
- **MISSING_GEOMETRY:** The required geometric information is unavailable.

The tool also generates a summary of the classified columns and alignment results. The alignment percentage is calculated using only column pairs for which a horizontal offset could be evaluated. Unclassified columns and columns without an eligible support are reported separately.

#### Limitations

The tool provides a geometric assessment of potential vertical load paths. It does not perform structural capacity calculations or verify the structural adequacy of connections, slabs, beams or foundations.

Bounding box centres are used as an approximation of the column centrelines. This approach is most suitable for regular vertical columns.

The analysis is limited to column-to-column relationships. Alternative load transfer mechanisms through walls, beams or other structural elements are not assessed.

A geometrically aligned column does not necessarily represent a verified structural load path. Similarly, a column flagged for review does not necessarily indicate a structural design error.

The final interpretation of the results remains the responsibility of the structural engineer.

The classification rules, analysis parameters and geometric assumptions must be verified using the Building 308 IFC model.

### Phase 4 – Main Workflow and Results Export

The `main.py` script provides the main entry point for the Vertical Load Path Checker.

It imports the IFC extraction functions from `ifc_reader.py` and the column classification and alignment analysis functions from `team_tool.py`.

The complete workflow is organised into four phases:

1. IFC element extraction.
2. Column classification.
3. Vertical load path analysis.
4. Results and CSV export.

The IFC model is accessed through a local file path defined in `main.py`. The model is not included in the GitHub repository.

The tool automatically generates an output folder containing the following CSV files:

| Output file | Description |
|---|---|
| Element inventory | Extracted structural elements, properties and geometry. |
| Column alignment | Horizontal offsets, vertical gaps, matching columns and alignment results. |
| Unclassified columns | Columns that could not be reliably classified. |
| Analysis summary | Overall classification and alignment statistics. |

The results are also displayed in the Python terminal to provide immediate feedback to the user.

The tool reports missing information and unavailable geometry to support transparent interpretation of the results.

The alignment percentage is calculated only for evaluated column pairs. Columns without an eligible support or with missing geometry are reported separately.

The output supports structural design coordination by identifying potential column misalignments that require further investigation.

The results are intended to support engineering judgement rather than replace structural calculations.

### Instructions to run the tool

#### Requirements

- Python 3
- IfcOpenShell
- A locally stored Building 308 IFC model

#### Installation

Open the A4 folder in Visual Studio Code and install the required dependency:

```bash
python -m pip install -r requirements.txt
```

#### Model configuration

Open `main.py` and replace the example model path with the actual location of the IFC file on your computer.

```python
model_path = Path(
    r"C:/Users/YourName/Documents/Building308.ifc"
)
```

The IFC model must remain outside the GitHub repository.

#### Execution

Run the following command in the terminal:

```bash
python main.py
```

On systems where Python is accessed using `python3`, use:

```bash
python3 main.py
```

#### Results

After execution, the analysis results are stored in the automatically generated `output` folder.

The CSV files can be opened in Microsoft Excel or another spreadsheet application for further investigation and documentation.

#### Validation status

The implementation must be tested using the actual Building 308 IFC model to verify the classification rules, geometry extraction, information availability and suitability of the screening tolerances.
