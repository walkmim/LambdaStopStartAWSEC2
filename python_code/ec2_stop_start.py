import boto3
import os
import sys
import time
from datetime import datetime, timedelta
from operator import itemgetter
from uuid import uuid4
from decimal import Decimal
from inspect import currentframe, getframeinfo

def stop_start_ec2_instances(account,session,regions,instance_list,sleep_sec_next_order,debug):
    
    try:
        instance_list_action_result = []
        for region in regions:
            ec2_client = session.client('ec2', region_name=region)
            
            instance_list_stop_order = sorted(instance_list, key=itemgetter('stop_order')) 
            instance_list_start_order = sorted(instance_list, key=itemgetter('start_order')) 
            
            last_stopped_order = 0
            last_start_order = 0
            
            # 
            for instance in instance_list_stop_order:
                # print(instance)
                if instance["action"] == "stop" and instance["instance_current_state"] == "running" and instance["print_only"] == "N":
                    if last_stopped_order < int(instance["stop_order"]):
                        time.sleep(sleep_sec_next_order)
                        last_stopped_order = int(instance["stop_order"])
                        
                    if instance["account"] == account and instance["region"] == region:
                        
                        date_time_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        utc_timestamp = datetime.timestamp(datetime.utcnow())
                        
                        try:
                            ec2_client.stop_instances(
                                InstanceIds=[
                                    instance["instance_id"],
                                ],
                            )
                            action_state = "Success"
                            action_exception = ""
                        except Exception as e:
                            action_exception = e
                            print("Exception:",e)
                        finally:
                            # print("Instance",instance["instance_id"],"stopped!")
                            instance_dict = {"unique_id":str(uuid4()),"type":"stop_start_instances"
                                            ,"account":account,"region":region,"instance_id":instance["instance_id"]
                                            ,"instance_name":instance["instance_name"],"server_name":instance["server_name"]
                                            ,"utc_date_time":str(date_time_now),"utc_timestamp":Decimal(utc_timestamp)
                                            ,"action":instance["action"],"action_state":action_state,"action_exception":action_exception}
                            instance_list_action_result.append(instance_dict)
                    
                    
            for instance in instance_list_start_order:
                if instance["action"] == "start" and instance["instance_current_state"] == "stopped" and instance["print_only"] == "N":
                    
                    if last_start_order < int(instance["start_order"]):
                        time.sleep(sleep_sec_next_order)
                        last_start_order = int(instance["start_order"])
                    
                    if instance["account"] == account and instance["region"] == region:
                        
                        date_time_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        utc_timestamp = datetime.timestamp(datetime.utcnow())
                    
                        try:
                            ec2_client.start_instances(
                                InstanceIds=[
                                    instance["instance_id"],
                                ],
                            )
                            action_state = "Success"
                            action_exception = ""
                        except Exception as e:
                            action_state = "Fail"
                            action_exception = e
                        finally:
                            # print("Instance",instance["instance_id"],"started!")
                            instance_dict = {"unique_id":str(uuid4()),"type":"stop_start_instances"
                                            ,"account":account,"region":region,"instance_id":instance["instance_id"]
                                            ,"instance_name":instance["instance_name"],"server_name":instance["server_name"]
                                            ,"utc_date_time":str(date_time_now),"utc_timestamp":Decimal(utc_timestamp)
                                            ,"action":instance["action"],"action_state":action_state,"action_exception":action_exception}
                            instance_list_action_result.append(instance_dict)
                            if debug == "Y":
                                print("line = "+str(currentframe().f_back.f_lineno))
                                print (instance_dict)
                              
                
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(f"---Ocorreu a seguinte exceção: {e}")
    finally:
        if debug == "Y":
            print("line = "+str(currentframe().f_back.f_lineno))
            print (instance_list_action_result)
        return instance_list_action_result

