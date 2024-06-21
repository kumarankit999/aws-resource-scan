import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import json
import boto3
from AWSUtilities import execute_command, list_regions
from CreateJira import connect_to_jira, create_main_issue, create_subtask

def list_ec2_instances(region):
    command = ['aws', 'ec2', 'describe-instances', '--region', region]
    ec2_details = execute_command(command)
    try:
        return json.loads(ec2_details)
    except json.JSONDecodeError:
        return []

def get_instance_info(instance):
    instance_id = instance['InstanceId']
    instance_type = instance['InstanceType']
    instance_state = instance['State']['Name']
    public_ip = instance.get('PublicIpAddress', 'N/A')
    private_ip = instance.get('PrivateIpAddress', 'N/A')
    kernel_id = instance.get('KernelId', 'N/A')
    volumes = [volume['Ebs']['VolumeId'] for volume in instance['BlockDeviceMappings']]
    volumes_info = ", ".join(volumes)
    return {
        'Instance ID': instance_id,
        'Instance Type': instance_type,
        'Instance State': instance_state,
        'Public IP': public_ip,
        'Private IP': private_ip,
        'Kernel ID': kernel_id,
        'Volumes': volumes_info
    }

def main():
    jira, project_key = connect_to_jira()
    
    main_issue_summary = "EC2 Instances"
    main_issue_description = "Overview of EC2 instances across all regions."
    
    main_issue_key = create_main_issue(jira, project_key, main_issue_summary, main_issue_description)
    print(f"Main issue created: {main_issue_key}")
    
    regions = list_regions()
    for region in regions:
        try:
            instances = list_ec2_instances(region)
            if not instances:
                print(f"No EC2 instances found in {region}. Skipping sub-task creation.")
                continue

            instance_infos = [get_instance_info(instance) for reservation in instances['Reservations'] for instance in reservation['Instances']]
            
            if not instance_infos:
                print(f"No EC2 instances found in {region}. Skipping sub-task creation.")
                continue

            subtask_summary = f"EC2 Instances in {region}"
            subtask_description = "\n\n".join([f"{key}: {value}" for instance_info in instance_infos for key, value in instance_info.items()])

            create_subtask(jira, project_key, main_issue_key, subtask_summary, subtask_description)
            print(f"Sub-task created for region {region}")
        
        except Exception as e:
            print(f"Error processing region {region}: {str(e)}")
            continue

if __name__ == "__main__":
    main()
