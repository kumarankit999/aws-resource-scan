# Script for listing EC2 instances and creating JIRA tickets

from jira_module import create_jira_issue

def create_ec2_instance():
    # Code to create EC2 instance
    instance_id = "XYZ"
    region = "ABC"
    
    # Create Jira issue
    summary = "EC2 Instance Creation"
    description = f"New EC2 instance created with ID {instance_id} in region {region}"
    create_jira_issue(summary, description)

