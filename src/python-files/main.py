import os
from re import S
import boto3
from geral_functions import *
from ec2_get import *
from ec2_stop_start import *

def main():
    print ("main")
   
if __name__ == '__main__':
    #main()
    #######################################################################################
    #######################################################################################
    parameter_store_name = "AUTOMATION-STOP-START-EC2"
    
    print_only,accounts,accounts_apply_all,assume_role_name,regions,sleep_sec_next_order,default_utc_stop_hour,default_utc_start_hour,environments,dynamodb_table = get_parameters(parameter_store_name)
    
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

    for instance in instance_list:
        print(instance)
    
    
    # Applying appropriate action
    for account in accounts:
        session = assume_role_session(account,assume_role_name)
        instance_list_action_result += stop_start_ec2_instances(account,session,regions,instance_list,sleep_sec_next_order)
    
    
    dynamodb_put_item(dynamodb_table)
    
    print("*"*150)
    for action_result in instance_list_action_result:
        print(action_result)
        
    
    # from Clear_tests import *
    # clear_instances(accounts,assume_role_name,regions)
    
    
    
    #######################################################################################
    #######################################################################################