 # A4 – Tool Development

## Vertical Load Path Checker

**Group:** 22  
**Focus area:** STR – Structures  
**Role:** Analyst  
**Project:** Building 308  
**Software:** Python, IfcOpenShell, Visual Studio Code, GitHub

## 1. About the Tool

### Problem and Claim

The structural design of the Building 308 transformation requires consideration of the relationship between newly introduced glulam columns and existing load-bearing structural elements.

The claim developed in Assignment A2 is:

> New glulam columns should be positioned directly above existing load-bearing elements wherever possible to establish direct vertical load paths.

The objective of the tool is to support the structural engineer in investigating this claim through an automated geometric analysis of IFC model information.

The current implementation focuses on column-to-column alignment.

### Source of the Claim

The claim is based on the structural design principles described in Structural Report 2601:

- Section 2.4, page 4.
- Section 8.1, page 20.

The tool translates the design principle identified in Assignment A2 into a computational workflow.

### Business Value

The tool supports a more efficient structural design review by reducing the need for repetitive manual inspections of the BIM model.

Potential benefits include:

- Faster identification of potential column misalignments.
- Improved structural design coordination.
- Consistent and repeatable geometric checks.
- Improved documentation of missing model information.
- Reduced manual modelling and coordination effort.

### Societal Value

Improved coordination of structural load paths may contribute to reduced construction errors, unnecessary material consumption and rework.

The tool supports informed engineering decisions but does not independently verify structural safety.

## 2. As-Is Workflow

In the conventional workflow, the structural engineer manually opens the BIM model, identifies new and existing structural elements, inspects their spatial relationships and records potential misalignments.

This process requires repeated visual inspections and depends on the availability and interpretation of model information.

The manual process can be time-consuming, particularly when a large number of structural elements must be reviewed.

## 3. To-Be Workflow

The proposed workflow introduces automated IFC-based information extraction, classification and geometric analysis.

The workflow consists of:

1. Access the local IFC model.
2. Extract structural elements and relevant properties.
3. Identify new glulam columns and existing load-bearing columns.
4. Check the availability of required information.
5. Calculate geometric relationships between eligible column pairs.
6. Identify potential misalignments.
7. Export results for structural engineering review.

If required information is missing, the affected elements are reported rather than assigned an unsupported classification.

## 4. Tool Architecture

The tool is organised into three Python modules.

| File | Function |
|---|---|
| `main.py` | Main entry point, workflow execution and results export. |
| `ifc_reader.py` | IFC model access, structural element extraction, property extraction and geometry processing. |
| `team_tool.py` | Column classification, geometric alignment analysis and result generation. |
| `requirements.txt` | Python dependencies. |
| `requirements.ids` | Proposed machine-readable information requirements. |
| `.gitignore` | Exclusion of local IFC models and generated files. |

The modular architecture separates IFC data extraction from the analytical logic and allows the individual components to be maintained independently.

## 5. Tool Description

### Phase 1 – IFC Element Extraction

IfcOpenShell is used to access the IFC model and extract structural elements.

The extracted information includes:

- IFC entity type.
- GlobalId.
- Element name.
- Element type.
- Building storey.
- Material.
- Load-bearing property.
- Construction status.
- Geometric bounding box.
- Geometric centre coordinates.

The extracted geometry is processed using consistent spatial coordinates and units.

### Phase 2 – Column Classification

The extracted columns are classified according to their material, construction status and load-bearing information.

The relevant categories are:

- New glulam columns.
- Existing load-bearing columns.
- Other columns.
- Unclassified columns.

Elements with insufficient information are reported separately.

### Phase 3 – Vertical Load Path Analysis

The tool investigates the spatial relationship between new glulam columns and existing load-bearing columns.

The horizontal offset is calculated using the difference between the X and Y coordinates of the geometric bounding box centres.

Horizontal offset:

d = sqrt((Xnew - Xexisting)^2 + (Ynew - Yexisting)^2)

The vertical relationship is evaluated using the bottom elevation of the new column and the top elevation of the potential supporting column.

The tool uses configurable screening parameters for horizontal alignment, vertical separation and permitted vertical overlap.

The current example horizontal tolerance is 150 mm. The example maximum vertical gap is 500 mm.

These parameters are preliminary screening assumptions and must be reviewed by the structural engineer before professional application.

The results indicate whether further investigation is required.

### Phase 4 – Results and Export

The tool exports the extracted information and analysis results into CSV files.

| Output | Description |
|---|---|
| `element_inventory.csv` | Extracted structural elements and properties. |
| `column_alignment.csv` | Geometric relationships and alignment results. |
| `unclassified_columns.csv` | Elements with insufficient classification information. |
| `analysis_summary.csv` | Overall analysis statistics. |

The results are also displayed in the Python terminal.

## 6. Advanced Building Design

### Design Stage

The proposed application is Stage C – Design, subject to confirmation against the course-specific Advanced Building Design stage definitions.

The tool supports the evaluation and coordination of structural design decisions before construction.

### Relevant Subjects

- Structural analysis.
- Building information modelling.
- Computational design.
- Design coordination.
- Information management.
- Model quality assurance.

### Required Model Information

| Information | Purpose |
|---|---|
| IFC entity type | Identify structural columns. |
| GlobalId | Identify and trace individual elements. |
| Material | Identify glulam columns. |
| Construction status | Distinguish new and existing elements. |
| LoadBearing | Identify load-bearing elements. |
| Building storey | Provide spatial context. |
| Geometry | Determine spatial relationships. |
| Coordinate system and units | Enable consistent geometric calculations. |

## 7. Information Delivery Specification

The proposed IDS defines information requirements for structural columns.

The purpose is to assess whether the IFC model contains the information required for reliable column classification.

The requirements include element identification, material information, load-bearing information and construction status.

The IDS complements the Python tool by checking semantic model readiness.

The geometric alignment calculation, coordinate consistency and structural interpretation remain part of the Python workflow and subsequent engineering review.

The proposed property conventions must be agreed with the model author.

## 8. Installation and Execution

### Requirements

- Python 3.
- IfcOpenShell.
- Visual Studio Code or another Python development environment.
- A locally stored IFC model.

### Installation

Open the A4 directory in the terminal and execute:

```bash
python -m pip install -r requirements.txt
```

### IFC Model Configuration

The IFC model must be stored locally and must not be uploaded to the GitHub repository.

Open `main.py` and modify the model path to match the local file location.

Example for macOS:

```python
model_path = Path.home() / "Downloads" / "B308X.ifc"
```

Example for Windows:

```python
model_path = Path.home() / "Documents" / "B308X.ifc"
```

The script checks whether the specified file exists before starting the analysis.

### Execution

Run:

```bash
python main.py
```

Depending on the local Python installation, the command may alternatively be:

```bash
python3 main.py
```

The generated results are stored in the local `output` directory.

On macOS, this directory can be opened using:

```bash
open output
```

## 9. Tool Testing and Validation

The initial implementation was executed successfully using the Building 308 IFC model named `B308X.ifc`.

The test was performed using macOS, Python 3.12.12 and IfcOpenShell 0.9.0.post1.

### Actual Test Results

| Indicator | Result |
|---|---:|
| Extracted columns | 211 |
| Columns with available geometry | 211 |
| Columns with concrete material | 211 |
| Columns with LoadBearing = True | 211 |
| Columns with unknown construction status | 211 |
| Identified new glulam columns | 0 |
| Classified existing load-bearing columns | 0 |
| Unclassified columns | 211 |
| Evaluated column pairs | 0 |
| Alignment percentage | Not available |

### Distribution by Building Storey

| Building storey | Number of columns |
|---|---:|
| ES_Stue | 94 |
| E1_1. sal | 117 |
| Total | 211 |

All extracted columns were associated with the following material:

`DTU_Concrete_Generic_Natural_Mat`

### Interpretation

The IFC model was accessed successfully, structural information and geometry were extracted, and the analysis summary was exported.

However, the extracted column information did not contain a recognised construction status, and no new glulam columns were identified.

The supplied model may represent the existing building rather than the complete proposed transformation. This must be confirmed with the model author.

Consequently, the structural claim could not be evaluated using the available input data.

This result demonstrates the importance of model readiness and reliable information delivery before automated structural analysis.

### Test Status

| Test | Status |
|---|---|
| IFC model access | Passed |
| Column extraction | Passed |
| Geometry availability | Passed |
| Column classification | Inconclusive due to input information |
| Column alignment analysis | Not evaluated |
| CSV export | Confirmed for the uploaded inventory and summary files |
| Independent geometric validation | Pending |

## 10. Limitations

The tool provides preliminary geometric screening rather than structural verification.

The following limitations apply:

- The analysis depends on the quality and completeness of the IFC model.
- The current implementation focuses on column-to-column relationships.
- Other supporting elements, such as walls, beams and foundations, are not fully evaluated as alternative load paths.
- Bounding box centres are approximations of structural column axes.
- Geometric alignment does not demonstrate structural capacity or connection adequacy.
- The screening tolerances require engineering validation.
- Separate existing and proposed models may require a coordinated model exchange before analysis.

## 11. Future Development

Future development should focus on:

- Obtaining the proposed transformation model containing new glulam columns.
- Confirming the construction status property convention.
- Validating material classification.
- Checking the IDS against the relevant IFC schema and model.
- Testing aligned and misaligned column pairs.
- Comparing selected results with model geometry in Blender/Bonsai.
- Extending the analysis to other potential supporting structural elements.
- Reviewing the screening parameters with the structural engineer.

The implementation may be integrated into a broader automated BIM analysis workflow.

The Future AEC Software Specification Data Framework provides a reference for further development of interoperable and modular AEC tools:

https://future-aec-software-specification.com/data-framework/

## 12. Conclusion

The Vertical Load Path Checker demonstrates how IFC model information can be extracted and processed to support structural design coordination.

The initial test successfully extracted 211 structural columns and their geometric information.

However, the absence of recognised construction status information and identified new glulam columns prevented the evaluation of the structural claim.

The tool therefore highlights both the potential of automated structural model analysis and the importance of clearly defined information delivery requirements.

Further validation using the proposed transformation model is required before a final conclusion regarding the structural claim can be drawn.

## References

- Structural Report 2601, Section 2.4 and Section 8.1, as referenced in Assignment A2.
- Assignment A2 – Group 22.
- Building 308 IFC model – B308X.ifc.
- IfcOpenShell: https://ifcopenshell.org/
- buildingSMART Information Delivery Specification: https://technical.buildingsmart.org/projects/information-delivery-specification-ids/
- Future AEC Software Specification: https://future-aec-software-specification.com/data-framework/
