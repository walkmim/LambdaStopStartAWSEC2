import os
from re import S
import boto3
from geral_functions import *
from ec2_get import *
from ec2_stop_start import *
from datetime import datetime, timedelta
from inspect import currentframe, getframeinfo


print('Loading function >> ',datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

def handler(event, context):

    try:
    
        #######################################################################################
        parameter_store_name = "AUTOMATION-STOP-START-EC2"
        
        print_only,accounts,accounts_apply_all,assume_role_name \
        ,regions,sleep_sec_next_order,default_utc_stop_hour \
        ,default_utc_start_hour,environments \
        ,dynamodb_table, log_actions_cw_logs,debug = get_parameters(parameter_store_name)
        
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

        
        instance_list_all = []
        instance_list_action_result_all = []
        
        # Selecting instances to apply appropriate action
        for account in accounts:
            session = assume_role_session(account,assume_role_name)
            if accounts_apply_all.count(account) > 0:
                instance_list_all+=get_ec2_instances(account,session,regions,"*",default_utc_stop_hour,default_utc_start_hour,print_only,debug)
            else:
                instance_list_all+=get_ec2_instances(account,session,regions,environments,default_utc_stop_hour,default_utc_start_hour,print_only,debug)
        
        if debug == "Y":
            print('app.py',"line = "+str(currentframe().f_back.f_lineno))
            print (instance_list_all)
        
        # Logging in DynamoDB - Instancias do escopo
        # dynamodb_put_item(dynamodb_table,instance_list)
                    
        # Applying appropriate action
        for account in accounts:
            session = assume_role_session(account,assume_role_name)
            instance_list_action_result_all+=stop_start_ec2_instances(account,session,regions,instance_list_all,sleep_sec_next_order,debug)
        
        if debug == "Y":
            print('app.py',"line = "+str(currentframe().f_back.f_lineno))
            print (instance_list_action_result_all)
            
        # Logging in CloudWatch
        if log_actions_cw_logs == "Y":
            print(">"*15,' List ',"<"*15)
            print(instance_list_all)
            print(">"*15,' Action ',"<"*15)
            print(instance_list_action_result_all)
            print("*"*15)
        
        # Logging actions in DynamoDB
        dynamodb_put_item(dynamodb_table,instance_list_action_result_all)
        

        
        #######################################################################################
        #######################################################################################
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(f"---Ocorreu a seguinte exceção: {e}")
        raise e
    finally:
        return 'AWS Lambda using Python' + sys.version + '!'