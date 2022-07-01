import os
from re import S
import boto3

def main():
    print ("main")
   
if __name__ == '__main__':
    #main()
    #######################################################################################
    #######################################################################################
    
    print_only = "Y"
    accounts = ["770409265803","583166431114"]
    accounts_apply_all = ["770409265803"]
    assume_role_name = "role_stop_start_instances"
    regions = ["us-east-1","us-east-2"]
    default_utc_stop_hour = "22"
    default_utc_start_hour = "12"
    # environments = ["DEV","HML","PREPROD","SANDBOX"]
    # environments = ["DEV","HML","PREPROD","SANDBOX"]
    environments = "*"

    from Geral_Functions import *
    from EC2_Functions import *
    
    account_instanceid_list = []
    for account in accounts:
        session = assume_role_session(account,assume_role_name)
        if accounts_apply_all.count(account):
            account_instanceid_list += stop_start_ec2_instances(account,session,regions,"*",default_utc_stop_hour,default_utc_start_hour,print_only)
        else:
            account_instanceid_list += stop_start_ec2_instances(account,session,regions,environments,default_utc_stop_hour,default_utc_start_hour,print_only)

    print(account_instanceid_list)
    
    #######################################################################################
    #######################################################################################