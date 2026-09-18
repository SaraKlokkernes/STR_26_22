# STR_26_22
# A1 – Forensic BIM

**Group:** 22  
**Focus area:** STR – Structures  
**Project:** Building 308

## Identified Issue

The client report describes Building 308 as having a structural system consisting mainly of reinforced-concrete beams, columns and slabs.

**Source:** 26_01_A_ClientReport, Section 3.3, p. 11.

When analysing `B308X.ifc` with IfcOpenShell, only **2 elements are classified as `IfcBeam`**. The model contains **211 `IfcColumn`** elements and **951 `IfcMember`** elements.

The inspected `IfcMember` elements are mainly named `Rectangular Mullion`, indicating that they are likely façade/window mullions rather than structural beams.

This indicates a possible **modelling, classification or IFC export issue**.

## Possible Solutions

- Check whether structural beams are correctly modelled in Building 308.
- Check the IFC classification of structural elements.
- Ensure structural beams are exported as `IfcBeam`.
- Re-export and validate the IFC model.

## Additional Observation

The IFC contains **4 `IfcGrid` objects**, but each grid has **13 U-axes and 42 V-axes**. Therefore, the issue is not simply the number of grid lines.

**Source:** A1 Client Report, p. 8.

## Script

`main.py` uses IfcOpenShell to analyse the IFC model and identify structural elements and potential classification issues.
