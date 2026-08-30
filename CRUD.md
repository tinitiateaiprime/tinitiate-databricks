# DBFS CRUD Reference (full)

<div align="left">
  <a href="README.md"><button>🏠 Home</button></a>
  <a href="javascript:history.back()"><button>⬅ Back</button></a>
</div>

This file consolidates the full student lab content: repository download, how to load the `dbfs_lab` helpers, step-by-step CRUD examples (create/rename/delete/list folders and files), and how to read files into Spark for querying.

Before you begin
- Ensure you have a Databricks workspace and permission to run notebooks and write to DBFS.
- Download or clone this repository locally so you can access `databricks/exercises/dbfs_lab.py` and the sample data.

Clone the repository and open it locally (optional for reference):

```bash
git clone https://github.com/your-username/tinitiate-databricks.git
cd tinitiate-databricks
```

Example:
- `git clone https://github.com/your-username/tinitiate-databricks.git` downloads the project to your machine.
- `cd tinitiate-databricks` moves you into the repository folder so you can inspect the files locally.

This step is only for local reference. The actual exercises are run inside Databricks notebooks.

Files referenced in these examples:
- `databricks/exercises/dbfs_lab.py` — helper functions for DBFS and file operations.
- `databricks/datasets/sample/sample.csv` — sample CSV used in the exercises.

Load the helpers into a notebook

Option A — upload the script to Workspace and `%run` it:

1. In Databricks UI: Workspace → Create → Library/Upload → Upload `dbfs_lab.py` under a folder (for example `/Shared/dbfs_lab`).
2. In a notebook cell run:

```python
%run /Shared/dbfs_lab
from dbfs_lab import *
```

Option B — paste the contents directly into the first notebook cell and run it.

Option C — copy to driver and then to DBFS (one-off):

```python
# in a notebook cell
dbutils.fs.cp('file:/databricks/driver/databricks/datasets/sample/sample.csv', 'dbfs:/tmp/sample.csv')
```

Folder (Bucket) operations — create / rename / delete / list

- Create folder (equivalent to creating a bucket or logical folder):

```python
create_folder('dbfs:/tmp/yourname/')
```

- Rename folder (move):

```python
rename_folder('dbfs:/tmp/yourname/', 'dbfs:/tmp/yourname_renamed/')
```

- Delete folder (recursively):

```python
delete_folder('dbfs:/tmp/yourname_renamed/')
```

- List folders under a path:

```python
print(list_folders('dbfs:/tmp/'))
```

File operations — create / update / delete / list

- List files in a folder:

```python
print(list_files('dbfs:/tmp/yourname/'))
```

- Create file (write text or CSV). Example: upload sample CSV from local driver to DBFS path and write it:

```python
text = open('/dbfs/databricks/datasets/sample/sample.csv','r', encoding='utf-8').read()  # when driver has the file
create_file('dbfs:/tmp/yourname/sample.csv', text, overwrite=True)
```

- Alternate: copy directly from local driver using `dbutils.fs.cp` when available.

- Update file (overwrite):

```python
update_file('dbfs:/tmp/yourname/sample.csv', new_text, append=False)
```

- Update file (append):

```python
update_file('dbfs:/tmp/yourname/sample.csv', '\n4,Dan,250', append=True)
```

- Delete file:

```python
delete_file('dbfs:/tmp/yourname/sample.csv')
```

Select / Query file (read into Spark and register as a temp view)

- Read CSV, register as a temp view and query from SQL:

```python
df = select_file_as_table('dbfs:/tmp/yourname/sample.csv', format='csv', table_name='lab_sample')
display(df)
%sql
select * from lab_sample
```

Expanded student checklist

1. Create a folder for your exercises:

```python
create_folder('dbfs:/tmp/<yourname>/')
```

2. Add the sample CSV to your folder. Options:
- Upload via Databricks UI (Data → Add Data).
- Copy from repo/driver:

```python
create_file('dbfs:/tmp/<yourname>/sample.csv', open('/dbfs/databricks/datasets/sample/sample.csv','r').read(), overwrite=True)
```

3. List files and confirm presence:

```python
print(list_files('dbfs:/tmp/<yourname>/'))
```

4. Read the CSV into a DataFrame and run a SQL query:

```python
select_file_as_table('dbfs:/tmp/<yourname>/sample.csv', format='csv', table_name='lab_sample')
%sql
select id, name, amount from lab_sample where amount > 150
```

5. Rename your folder and verify files moved:

```python
rename_folder('dbfs:/tmp/<yourname>/', 'dbfs:/tmp/<yourname>_v2/')
print(list_files('dbfs:/tmp/<yourname>_v2/'))
```

6. Append a row to the CSV and re-run the select:

```python
update_file('dbfs:/tmp/<yourname>_v2/sample.csv', '\n4,Dan,250', append=True)
select_file_as_table('dbfs:/tmp/<yourname>_v2/sample.csv', format='csv', table_name='lab_sample2')
%sql
select * from lab_sample2
```

7. Delete the file and folder when finished:

```python
delete_file('dbfs:/tmp/<yourname>_v2/sample.csv')
delete_folder('dbfs:/tmp/<yourname>_v2/')
```

Tips & Notes

- When running inside Databricks, the helpers use `dbutils` for filesystem operations. If `dbutils` is not available (local testing), the helpers attempt to map `dbfs:/` paths to `/dbfs/` local filesystem.
- Use a unique folder name (your initials, username, or student id) to avoid collisions with other students.
- If you need to copy the sample from your local machine into DBFS using the Databricks UI, upload it to Files → Upload and then copy it to `dbfs:/` using the UI or `dbutils.fs.cp`.
- The helper functions are intentionally simple for teaching purposes; in production use the Spark APIs, mount points, and managed tables with Unity Catalog as appropriate.

Cleanup reminder

```python
delete_folder('dbfs:/tmp/<yourname>/')
```

If you want this exact content in another format (a ready-to-import Databricks notebook or a shorter student handout), tell me which format and I'll create it.

