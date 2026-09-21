import ifcopenshell


# Load the IFC model
ifc = ifcopenshell.open("B308X.ifc")

print("A1 – Forensic BIM")
print("Project: Building 308")
print("Focus area: STR – Structures")
print("-" * 40)


# Count structural elements
beams = ifc.by_type("IfcBeam")
columns = ifc.by_type("IfcColumn")
members = ifc.by_type("IfcMember")
grids = ifc.by_type("IfcGrid")


print("\nStructural elements:")
print("IfcBeam:", len(beams))
print("IfcColumn:", len(columns))
print("IfcMember:", len(members))
print("IfcGrid:", len(grids))


# List the beams
print("\nIfcBeam elements:")
for beam in beams:
    print("-", beam.Name)


# Check IfcMember names
print("\nIfcMember elements:")
for member in members[:10]:
    print("-", member.Name)


# Analyse grids
print("\nGrid information:")

for i, grid in enumerate(grids, 1):
    print(
        f"Grid {i}: "
        f"{len(grid.UAxes)} U-axes, "
        f"{len(grid.VAxes)} V-axes"
    )


# Summary
print("\n" + "-" * 40)
print("SUMMARY")
print("-" * 40)

print(f"Only {len(beams)} elements are classified as IfcBeam.")

if len(beams) < 3:
    print("This may indicate a modelling, classification, or IFC export issue.")

print(
    f"The IFC also contains {len(members)} IfcMember elements. "
    "The first inspected members are named as mullions."
)
