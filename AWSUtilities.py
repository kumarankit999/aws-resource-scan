#Module for common AWS interaction functions

import subprocess
import boto3

def execute_command(command):
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        result = f"Command failed with exit code {e.returncode}: {e.output.decode('utf-8')}"
    return result

def list_regions():
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()['Regions']
    return [region['RegionName'] for region in regions]
