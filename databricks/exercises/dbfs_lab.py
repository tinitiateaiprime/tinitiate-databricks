"""DBFS lab helpers for student exercises.

Designed to be pasted into a Databricks Python notebook or uploaded to Workspace and
imported from there. Uses `dbutils` when available, otherwise falls back to local
filesystem helpers for testing.
"""
from typing import List, Optional
import os
from pyspark.sql import SparkSession

try:
    dbutils  # type: ignore
except NameError:
    dbutils = None


def spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def create_folder(path: str) -> bool:
    """Create a folder on DBFS (e.g., 'dbfs:/tmp/myfolder')."""
    if dbutils:
        dbutils.fs.mkdirs(path)
        return True
    # local fallback
    local = _to_local(path)
    os.makedirs(local, exist_ok=True)
    return True


def rename_folder(src: str, dst: str) -> bool:
    """Rename (move) a folder on DBFS."""
    if dbutils:
        dbutils.fs.mv(src, dst)
        return True
    os.rename(_to_local(src), _to_local(dst))
    return True


def delete_folder(path: str) -> bool:
    if dbutils:
        dbutils.fs.rm(path, recurse=True)
        return True
    import shutil
    shutil.rmtree(_to_local(path), ignore_errors=True)
    return True


def list_folders(path: str) -> List[str]:
    """List folders under a path (returns names)."""
    items = []
    if dbutils:
        for info in dbutils.fs.ls(path):
            if info.isDir():
                items.append(info.path)
        return items
    for name in os.listdir(_to_local(path)):
        if os.path.isdir(os.path.join(_to_local(path), name)):
            items.append(os.path.join(path, name))
    return items


def list_files(path: str) -> List[str]:
    items = []
    if dbutils:
        for info in dbutils.fs.ls(path):
            if not info.isDir():
                items.append(info.path)
        return items
    for name in os.listdir(_to_local(path)):
        if os.path.isfile(os.path.join(_to_local(path), name)):
            items.append(os.path.join(path, name))
    return items


def create_file(path: str, text: str, overwrite: bool = False) -> bool:
    """Create a file with text content. Use overwrite=True to replace."""
    if dbutils:
        dbutils.fs.put(path, text, overwrite=overwrite)
        return True
    local = _to_local(path)
    mode = 'w' if overwrite else 'x'
    with open(local, mode, encoding='utf-8') as f:
        f.write(text)
    return True


def update_file(path: str, text: str, append: bool = False) -> bool:
    """Update file: overwrite or append depending on `append`."""
    if dbutils and not append:
        dbutils.fs.put(path, text, overwrite=True)
        return True
    local = _to_local(path)
    mode = 'a' if append else 'w'
    with open(local, mode, encoding='utf-8') as f:
        f.write(text)
    return True


def delete_file(path: str) -> bool:
    if dbutils:
        dbutils.fs.rm(path)
        return True
    try:
        os.remove(_to_local(path))
    except FileNotFoundError:
        pass
    return True


def select_file_as_table(path: str, format: str = 'csv', table_name: Optional[str] = None):
    """Read a file into a Spark DataFrame and optionally register as a table/view.

    Supported formats: 'csv', 'json', 'parquet'. For CSV, header is assumed.
    """
    spark_sess = spark()
    if format == 'csv':
        df = spark_sess.read.option('header', 'true').csv(path)
    elif format == 'json':
        df = spark_sess.read.json(path)
    elif format == 'parquet':
        df = spark_sess.read.parquet(path)
    else:
        raise ValueError('Unsupported format')
    if table_name:
        df.createOrReplaceTempView(table_name)
    return df


def _to_local(path: str) -> str:
    """Convert a dbfs:/... or /dbfs/... path to a local driver path for testing."""
    if path.startswith('dbfs:/'):
        return '/dbfs/' + path[len('dbfs:/'):]
    if path.startswith('/dbfs/'):
        return path
    return path


if __name__ == '__main__':
    print('DBFS lab helpers loaded. Import into a Databricks notebook and use the functions.')
