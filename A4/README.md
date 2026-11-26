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
