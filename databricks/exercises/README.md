# DBFS & Delta Exercises (Student Lab)

<div align="left">
  <a href="../../README.md"><button>🏠 Home</button></a>
  <a href="javascript:history.back()"><button>⬅ Back</button></a>
</div>

Download the files in this folder and run them on your Databricks workspace. The lab shows common file and folder operations in DBFS and basic table/select operations using Spark.

Files in this folder:

- `dbfs_lab.py` — Python helper functions you can paste into a Databricks Python notebook or import after uploading to Workspace. Functions use `dbutils` and `pyspark` and include examples for:
  - create_folder(path)
  - rename_folder(src, dst)
  - delete_folder(path)
  - list_folders(path)
  - list_files(path)
  - create_file(path, text)
  - update_file(path, text)
  - delete_file(path)
  - select_file_as_table(path, format, table_name)

- `../datasets/sample/sample.csv` — small sample CSV data you can upload to DBFS or read directly from the repo in local development.

Quick start (Databricks notebook):

1. Create a new Python notebook in Databricks.
2. Copy the contents of `dbfs_lab.py` into the first notebook cell and run it.
3. Upload `databricks/datasets/sample/sample.csv` to DBFS using the UI or use `dbutils.fs.cp('file:/databricks/driver/databricks/datasets/sample/sample.csv', 'dbfs:/tmp/sample.csv')` after uploading the file to the driver.
4. Use the helper functions from the next cell, for example:

```python
from dbfs_lab import create_folder, list_files, create_file, select_file_as_table

create_folder('dbfs:/tmp/lab_demo')
create_file('dbfs:/tmp/lab_demo/sample.csv', open('/dbfs/tmp/sample.csv','r').read())
print(list_files('dbfs:/tmp/lab_demo'))
select_file_as_table('dbfs:/tmp/lab_demo/sample.csv', format='csv', table_name='lab_demo_sample')
%sql
select * from lab_demo_sample
```

Notes:

- When running in Databricks, `dbutils` is available; the helper will use it. If you run the helpers locally for testing, they will use the local filesystem instead (paths like `/dbfs/` expected).
- The `select_file_as_table` function registers a temporary view or creates a managed/external Delta table depending on arguments — see the function docstring in `dbfs_lab.py`.

Exercise tasks:

1. Create a folder `dbfs:/tmp/<yourname>/`.
2. Upload or create a file `sample.csv` into that folder.
3. List files and confirm `sample.csv` is present.
4. Read the CSV into a Spark DataFrame and run a simple SELECT query.
5. Rename the folder and confirm files moved.
6. Update the file by appending a row and re-run the SELECT.
7. Delete the file and the folder when done.
