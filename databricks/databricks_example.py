"""Databricks notebook-style example for running AWS operations with boto3.

Notes:
 - Install boto3 on the cluster or run `pip install boto3` in a notebook cell.
 - Configure AWS credentials in the cluster (instance profile) or via environment variables.
"""
from pyspark.sql import SparkSession
import boto3

def list_s3_buckets():
    s3 = boto3.client('s3')
    print('Buckets:', [b['Name'] for b in s3.list_buckets().get('Buckets', [])])

def invoke_lambda(function_name, payload: dict):
    lam = boto3.client('lambda')
    resp = lam.invoke(FunctionName=function_name, Payload=bytes(str(payload), 'utf-8'))
    print('Lambda status:', resp.get('StatusCode'))

if __name__ == '__main__':
    list_s3_buckets()
