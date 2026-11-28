# Path to the local IFC model.
#
# A relative path is resolved from this A4 folder, so the same setting works
# on Windows and macOS for everyone in the group. Put the model here:
#
#     A4/data/B308X.ifc
#
# The data folder is ignored by git, so the model is never uploaded.
# To use a model somewhere else for one run, pass its path instead:
#
#     python runall.py "C:\Users\Name\Downloads\B308X.ifc"   (Windows)
#     python3 runall.py ~/Downloads/B308X.ifc                (macOS)
MODEL_PATH = "data/B308X.ifc"
