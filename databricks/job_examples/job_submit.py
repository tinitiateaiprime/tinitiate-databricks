"""Example: submit and run a Databricks job using the Databricks SDK for Python.

Requires `databricks-sdk` installed and environment variable `DATABRICKS_CONFIG_FILE`
or equivalent to authenticate. See https://pypi.org/project/databricks-sdk/
"""
import os
import json
from databricks.sdk import WorkspaceClient


def create_job(name: str, notebook_path: str, existing_cluster_id: str = None):
    client = WorkspaceClient()
    job_settings = {
        'name': name,
        'notebook_task': {'notebook_path': notebook_path},
    }
    if existing_cluster_id:
        job_settings['existing_cluster_id'] = existing_cluster_id
    resp = client.jobs.create(job_settings)
    return resp


def run_job(job_id: str, notebook_params: dict = None):
    client = WorkspaceClient()
    run_resp = client.jobs.run_now(job_id=job_id, notebook_params=notebook_params or {})
    return run_resp


if __name__ == '__main__':
    # Simple demo (edit the notebook path and cluster id as needed)
    nb = '/Users/you@example.com/demo-notebook'
    print('Creating job...')
    job = create_job('demo-job', nb, existing_cluster_id=os.environ.get('DATABRICKS_CLUSTER_ID'))
    print('Job created:', job)
