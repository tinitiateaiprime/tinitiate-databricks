# Databricks Examples — Overview

<div align="left">
  <a href="README.md"><button>🏠 Home</button></a>
  <a href="javascript:history.back()"><button>⬅ Back</button></a>
</div>

This document summarizes the example scripts and utilities included in this repository. Use these from Databricks notebooks or from local management scripts (where noted).

Included items:

- `databricks/dbfs_ops.py` — DBFS and Delta helper utilities for notebooks. Functions: `list_files`, `upload_text_to_dbfs`, `read_text_from_dbfs`, `create_delta_table`, `select_table_sql`.
- `databricks/job_examples/job_submit.py` — example for creating and running Databricks Jobs using the `databricks-sdk` (requires `databricks-sdk` and proper auth configuration).
- `databricks/exercises/dbfs_lab.py` — student-facing exercise helpers (see `EXERCISES.md`).
- `databricks/datasets/sample/sample.csv` — sample dataset used in exercises.
- `databricks/databricks_example.py` — illustrative example (may contain cloud-specific code; adapt to your workspace before using).

Requirements (for local management scripts):

```bash
python -m pip install -r requirements.txt
```

Notes:

- The helper modules are intended to run on Databricks clusters where `dbutils` is available. When used locally, some helpers provide file-path fallbacks (e.g., `/dbfs/` local mount) for testing.
- To use the Job submission script you must configure authentication for the Databricks SDK (environment variables or `~/.databricks/config`). See `databricks-sdk` docs.
