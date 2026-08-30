<div align="left" style="padding: 24px 0 8px 0;">
  <div style="border: 3px solid #f57c00; border-radius: 12px; padding: 18px 32px; display: inline-block; background: #f5f5f5;">
    <span style="font-size: 54px; font-weight: 800; color: #111; font-family: Arial, Helvetica, sans-serif;">Databricks</span>
  </div>
</div>

# Databricks Tutorial

© TINITIATE.COM

## CONTENTS

- Setup in Databricks
  - Open a Databricks workspace
  - Create a notebook
  - Upload the project files
  - Run the lab cells in order
  - Use DBFS and Spark within the cluster

- Databricks Basics
  - DBFS operations
  - File creation and updates
  - Folder management
  - Spark reads and SQL queries
  - Delta and table creation

---

## Setup in Databricks

Students should complete these exercises inside a Databricks notebook, not on a local terminal.

1. Open your Databricks workspace.
2. Create a new Python notebook.
3. Upload the project files or paste the helper script into the notebook.
4. If the project includes a `databricks` folder, upload that folder to your Databricks workspace.
5. Run the notebook cells in order.

For a complete step-by-step student setup, see [setup.md](setup.md).

If you are working from a local repo clone only for reference, you can use this repository as a source, but the exercises are meant to be run in Databricks.

## Project Files

The files in this repository are arranged in a practical learning order:

1. [setup.md](setup.md) — Step-by-step Databricks setup guide for students
2. [CRUD.md](CRUD.md) — CRUD reference and notebook-ready examples to learn the core operations first
3. [EXERCISES.md](EXERCISES.md) — Student lab with DBFS tasks and checklist to practice the concepts
4. [DATBRICKS_EXAMPLES.md](DATBRICKS_EXAMPLES.md) — Supporting examples and reference notes
5. [databricks/exercises/dbfs_lab.py](databricks/exercises/dbfs_lab.py) — DBFS helper functions used in the notebook workflow
6. [databricks/datasets/sample/sample.csv](databricks/datasets/sample/sample.csv) — Sample dataset used by the exercises

This order helps students begin with setup, then understand the operations, then apply them through the exercises, and finally use the supporting examples and data files.

## Databricks Basics

- DBFS folder creation
- File upload and updates
- DBFS file listing
- Spark DataFrame loading
- SQL queries on tables
- Cleanup operations

This lab is designed to be executed in a Databricks notebook environment with a running cluster.


