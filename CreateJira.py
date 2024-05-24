# Module for creating JIRA issues and sub-tasks

import json
from jira import JIRA
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_aws_secrets():
    try:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId='jira_credentials')
        secrets = json.loads(response['SecretString'])
        return secrets
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found.")
        return None
    except Exception as e:
        print(f"Error retrieving secrets: {str(e)}")
        return None

def connect_to_jira():
    secrets = get_aws_secrets()
    if not secrets:
        raise Exception("Unable to retrieve JIRA credentials.")

    jira_options = {'server': secrets['jira_server']}
    jira = JIRA(options=jira_options, basic_auth=(secrets['jira_username'], secrets['jira_token']))
    project_key = secrets['jira_project_key']
    
    return jira, project_key

def create_main_issue(jira, project_key, summary, description):
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    return new_issue.key

def create_subtask(jira, project_key, parent_issue_key, summary, description):
    subtask_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Sub-task'},
        'parent': {'key': parent_issue_key},
    }
    new_subtask = jira.create_issue(fields=subtask_dict)
    return new_subtask.key

