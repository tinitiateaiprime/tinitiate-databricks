"""Databricks DBFS and Delta table helper utilities.

These helpers are intended to run on a Databricks cluster or notebook. They
use `dbutils` when available and fallback to `pyspark` APIs where appropriate.
"""
from typing import List, Optional
import os
import json

try:
    dbutils  # type: ignore
except NameError:
    dbutils = None

from pyspark.sql import SparkSession


def spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def list_files(path: str) -> List[str]:
    """List files under a DBFS or mounted path.

    Example paths: '/dbfs/tmp/', 'dbfs:/tmp/', '/mnt/data/'
    """
    if dbutils is not None:
        ls_path = path
        # dbutils expects 'dbfs:/...' or '/mnt/...'
        return [f.path for f in dbutils.fs.ls(ls_path)]
    # Fallback: try Spark filesystem
    sc = spark().sparkContext
    try:
        fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(sc._jsc.hadoopConfiguration())
        p = sc._jvm.org.apache.hadoop.fs.Path(path)
        status = fs.listStatus(p)
        return [str(s.getPath()) for s in status]
    except Exception:
        return []


def upload_text_to_dbfs(dbfs_path: str, text: str, overwrite: bool = True):
    """Write small text content to DBFS. Use from notebooks."""
    if dbutils is None:
        raise RuntimeError('dbutils is not available. Run inside Databricks notebook.')
    dbutils.fs.put(dbfs_path, text, overwrite=overwrite)
    return True


def read_text_from_dbfs(dbfs_path: str) -> str:
    if dbutils is None:
        # Try reading via spark
        p = dbfs_path
        if p.startswith('dbfs:/'):
            local_path = '/dbfs/' + p[len('dbfs:/'):]
            with open(local_path, 'r', encoding='utf-8') as f:
                return f.read()
        raise RuntimeError('dbutils not available and path not local-accessible')
    return dbutils.fs.head(dbfs_path, 10000000)


def delete_dbfs_path(path: str):
    if dbutils is None:
        raise RuntimeError('dbutils is not available. Run inside Databricks notebook.')
    dbutils.fs.rm(path, recurse=True)
    return True


def create_delta_table(df=None, table_name: str = None, path: str = None, mode: str = 'overwrite'):
    """Write a DataFrame as a Delta table either managed or at a path.

    Provide either `table_name` (managed) or `path` (external path).
    """
    if df is None:
        raise ValueError('df DataFrame is required')
    if path:
        df.write.format('delta').mode(mode).save(path)
        if table_name:
            spark().sql(f"CREATE TABLE IF NOT EXISTS {table_name} USING DELTA LOCATION '{path}'")
        return True
    if table_name:
        df.write.format('delta').mode(mode).saveAsTable(table_name)
        return True
    raise ValueError('Either table_name or path must be provided')


def read_table(table: str):
    return spark().table(table)


def select_table_sql(sql: str):
    return spark().sql(sql)


if __name__ == '__main__':
    print('Databricks DBFS and Delta helpers. Import and use from notebooks or jobs.')
