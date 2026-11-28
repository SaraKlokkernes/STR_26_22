# Changelog

## 2026-11-28 (b) – Group 22 (STR)

- The lowest slab in the model now counts as a ground slab (`ON_BASE_SLAB`)
  even when typed `FLOOR` (`lowest_slab_is_ground`, default on). In B308X
  this removes 89 false flags on the ground floor. Each such result has a
  `ground_slab_reason` field.

## 2026-11-28 – Group 22 (STR)

- Added `column_support_check`: for every `IfcColumn`, reports what the
  column stands on and flags columns that land on a slab with no supporting
  element directly below (`UNSUPPORTED_SLAB`). This replaces our earlier
  glulam-only alignment tool.
- Registered the analysis in `runall.py`; results are written to
  `column_support_check/results/run-.../result.json`.
- `settings.py` now uses the relative path `data/B308X.ifc`, so the same
  setting works on Windows and macOS. `data/` and `*.ifc` are ignored by git.
- Added `column_support_check/requirements.ids` and
  `tests/test_column_support.py`.
- Effect on receiving teams: `flagged_columns` is a list of column GlobalIds
  needing structural review. The check is geometric screening, not a
  structural verification.

## 2026-11-16

- Grouped each analysis's source and results in its own top-level folder:
  `window_count/src/main.py` and `window_count/results/run-.../result.json`.
  The shared `runall.py` and `settings.py` are now at the template root.
  Register additional analysis folder names in `ANALYSES`.
- The optional `--results-dir` override retains its separate output-root layout.
  Existing results are left untouched.
  The shared runner opens the IFC once for the registered analyses.

- Initial starter: count IFC windows using an import-safe callable function.
- Added a local runner that writes JSON to a new folder on each run.
- Added `settings.py` for the local model path, keeping setup separate from
  the analysis. A command-line path can still override it.
- No automatic publishing, run metadata or engineering assessment.

Add dated entries for your meaningful changes and explain their effect on the
receiving team. Routine executions do not need changelog entries.
