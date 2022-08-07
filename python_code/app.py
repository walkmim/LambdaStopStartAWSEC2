import os
from re import S
import boto3
from geral_functions import *
from ec2_get import *
from ec2_stop_start import *


print('Loading function')

def handler(event, context):

    try:
    
        #######################################################################################
        parameter_store_name = "AUTOMATION-STOP-START-EC2"
        
        print_only,accounts,accounts_apply_all,assume_role_name \
        ,regions,sleep_sec_next_order,default_utc_stop_hour \
        ,default_utc_start_hour,environments \
        ,dynamodb_table, log_actions_cw_logs = get_parameters(parameter_store_name)
        
        ##################################################
        # from Clear_tests import *
        # clear_instances(accounts,assume_role_name,regions)
        ##################################################
        
        # print_only = "N"
        # accounts = ["770409265803","583166431114"]
        # accounts_apply_all = ["770409265803"]
        # assume_role_name = "role_stop_start_instances"
        # regions = ["us-east-1","us-east-2"]
        # sleep_sec_next_order = 30
        # default_utc_stop_hour = "22"
        # default_utc_start_hour = "12"
        # environments = ["DEV","HML","PREPROD","SANDBOX"]
        # environments = "*"

        
        instance_list = []
        instance_list_action_result = []
        
        # Selecting instances to apply appropriate action
        for account in accounts:
            session = assume_role_session(account,assume_role_name)
            if accounts_apply_all.count(account) > 0:
                instance_list += get_ec2_instances(account,session,regions,"*",default_utc_stop_hour,default_utc_start_hour,print_only)
            else:
                instance_list += get_ec2_instances(account,session,regions,environments,default_utc_stop_hour,default_utc_start_hour,print_only)
        
        # Logging in DynamoDB - Instancias do escopo
        # dynamodb_put_item(dynamodb_table,instance_list)
                    
        # Applying appropriate action
        for account in accounts:
            session = assume_role_session(account,assume_role_name)
            instance_list_action_result += stop_start_ec2_instances(account,session,regions,instance_list,sleep_sec_next_order)
        
        # Logging in CloudWatch
        if log_actions_cw_logs == "Y":
            print("*"*15)
            print(instance_list_action_result)
            print("*"*15)
        
        # Logging actions in DynamoDB
        dynamodb_put_item(dynamodb_table,instance_list_action_result)
        

        
        #######################################################################################
        #######################################################################################
    
    except Exception as e:
        print(e)
        raise e
    finally:
        return 'AWS Lambda using Python' + sys.version + '!'