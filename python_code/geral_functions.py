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

def get_parameters (parameter_store_name):
    ssm = boto3.client('ssm')
    
    parameter = ssm.get_parameter(Name=parameter_store_name)
    
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
    
    return print_only,accounts,accounts_apply_all,assume_role_name,regions,sleep_sec_next_order,default_utc_stop_hour,default_utc_start_hour,environments,dynamodb_table,log_cw_logs

def dynamodb_put_item(dynamodb_table,instance_list):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table)

    
    for instance in instance_list:
        
        # print (instance)
        
        try:
            action_state = instance["action_state"]
        except: 
            action_state = ""
            pass
            
        try:
            action_exception = instance["action_exception"]
        except: 
            action_exception = ""
            pass
            
        
        response = table.put_item(
                Item={
                    "unique_id" : instance["unique_id"]
                    ,"type" : instance["type"]
                    ,"print_only" : instance["print_only"]
                    ,"action" : instance["action"]
                    ,"account" : instance["account"]
                    ,"region" : instance["region"]
                    ,"instance_id" : instance["instance_id"]
                    ,"instance_current_state" : instance["instance_current_state"]
                    ,"instance_name" : instance["instance_name"]
                    ,"server_name" : instance["server_name"]
                    ,"skip_until" : instance["skip_until"]
                    ,"utc_stop_hour" : instance["utc_stop_hour"]
                    ,"utc_start_hour" : instance["utc_start_hour"]
                    ,"start_order" : instance["start_order"]
                    ,"stop_order" : instance["stop_order"]
                    ,"utc_date_time" : instance["utc_date_time"]
                    ,"utc_timestamp" : instance["utc_timestamp"]
                    ,"action_state" : action_state
                    ,"action_exception" : action_exception
                }
        )