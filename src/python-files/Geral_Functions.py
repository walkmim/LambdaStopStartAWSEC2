import boto3
import botocore
import datetime
import math
import json
from decimal import Decimal

def assume_role_session(account,assume_role_name):
    
    sts_client = boto3.client('sts')
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    role_arn = "arn:aws:iam::"+account+":role/"+assume_role_name
    role_session_name = "RoleSession"+account+"_"+assume_role_name
    assumed_role_object=sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
    
    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    credentials=assumed_role_object['Credentials']
    
    session = boto3.session.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    
    return session

def get_parameters ():
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='/automation/stop_start_instances')
    
    params = parameter['Parameter']['Value'].split("|")
    # print(params)
    
    for param in params:
        # print(param.strip)
        exec(param.strip(), globals())

    # print("print_only",print_only)
    # print("accounts",accounts)
    # print("accounts_apply_all",accounts_apply_all)
    # print("assume_role_name",assume_role_name)
    # print("regions",regions)
    # print("sleep_sec_next_order",sleep_sec_next_order)
    # print("default_utc_stop_hour",default_utc_stop_hour)
    # print("default_utc_start_hour",default_utc_start_hour)
    # print("environments",environments)
    
    return print_only,accounts,accounts_apply_all,assume_role_name,regions,sleep_sec_next_order,default_utc_stop_hour,default_utc_start_hour,environments,dynamodb_table

def dynamodb_put_item(dynamodb_table):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(dynamodb_table)

    instance_list = [{'unique_id': '433921a4-d501-479b-a674-216919f7a3e1', 'utc_date_time': '07/03/2022 05:51:14', 'action': 'stop'}
                    ,{'unique_id': 'c7d459d6-9f65-4c11-ad3b-0d8347140aca', 'utc_date_time': '07/03/2022 05:51:14', 'action': 'stop'}]

    item = json.loads(json.dumps(instance_list), parse_float=Decimal)

    print(item)

    response = table.put_item(
            Item={
                item
            }
    )