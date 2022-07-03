import boto3
import os
import sys
from datetime import datetime, timedelta

def get_ec2_instances(account,session,regions,environments,default_utc_stop_hour,default_utc_start_hour,print_only):
    instance_list = []
    try:
        
        for region in regions:
            ec2_client = session.client('ec2', region_name=region)
            ec2_instances = []
            # to get instances filtering by environment tag
            if environments == "*":
                ec2_instances += ec2_client.describe_instances()["Reservations"]
            else:
                for environment in environments:
                    ec2_instances += ec2_client.describe_instances(
                        Filters=[
                                    {
                                        'Name': 'tag:environment',
                                        'Values': [
                                            environment
                                            ]
                                    },
                                    {
                                        'Name': 'instance-state-name', 
                                        'Values': [
                                            'stopped', 
                                            'running'
                                            ]
                                    }
                                ]
                    )["Reservations"]
                
            # print("instances: ",ec2_instances)
            # print(">"*100)
            # print (type(ec2_instances))
            
            for instance in ec2_instances:
                # print (type(instance))
                instance_detail = instance["Instances"][0]
                # print (instance_detail)
                instance_id = instance_detail["InstanceId"]
                instance_actual_state = instance_detail["State"]["Name"]
                server_name = ""
                instance_name = ""
                
                # tags that will control stop start
                skip_until = ""  
                utc_stop_hour = "" 
                utc_start_hour = "" 
                auto_start = ""
                start_order = ""
                stop_order = ""
                
                for tags in instance_detail["Tags"]:
                    if tags["Key"] == 'server_name':
                        server_name = tags["Value"]
                    if tags["Key"] == 'Name':
                        instance_name = tags["Value"]
                    if tags["Key"] == 'skip_until':
                        skip_until = tags["Value"]
                    if tags["Key"] == 'utc_stop_hour':
                        utc_stop_hour = tags["Value"]
                    if tags["Key"] == 'utc_start_hour':
                        utc_start_hour = tags["Value"]
                    if tags["Key"] == 'auto_start':
                        auto_start = tags["Value"]
                    if tags["Key"] == 'start_order':
                        start_order = tags["Value"]
                    if tags["Key"] == 'stop_order':
                        stop_order = tags["Value"]
                
                if skip_until == "":
                    skip_until="01/01/1900"
                if utc_stop_hour == "":
                    utc_stop_hour = default_utc_stop_hour
                if utc_start_hour == "":
                    utc_start_hour = default_utc_start_hour
                if start_order == "":
                    start_order = "0"
                if stop_order == "":
                    stop_order = "0"
                
                
                date_now = datetime.utcnow().date()
                date_skip_until = datetime.strptime(skip_until, '%d/%m/%Y').date()
                hour_now_str = datetime.utcnow().strftime("%H")
                
                # print("date now: ",date_now)
                # print("date skip until: ",date_skip_until)
        
                if date_now > date_skip_until and utc_stop_hour != utc_start_hour :
                
                    if hour_now_str == utc_stop_hour:
                        instance_dict = {"print_only":print_only,"action":"stop","account":account,"region":region,"instance_id":instance_id,"instance_actual_state":instance_actual_state,"instance_name":instance_name,"server_name":server_name
                            ,"skip_until":skip_until,"utc_stop_hour":utc_stop_hour,"utc_start_hour":utc_start_hour,"auto_start":auto_start,"start_order":start_order,"stop_order":stop_order};
                        instance_list.append(instance_dict)
                        
                    if hour_now_str == utc_start_hour and auto_start != "N" :
                        instance_dict = {"print_only":print_only,"action":"start","account":account,"region":region,"instance_id":instance_id,"instance_actual_state":instance_actual_state,"instance_name":instance_name,"server_name":server_name
                            ,"skip_until":skip_until,"utc_stop_hour":utc_stop_hour,"utc_start_hour":utc_start_hour,"auto_start":auto_start,"start_order":start_order,"stop_order":stop_order};
                        instance_list.append(instance_dict)
                        
                # print(account," >>> ",region," >>> ",instance_id," >>> ",instance_name," >>> ",server_name)
                
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(f"---Ocorreu a seguinte exceção: {e}")
    finally:
        return instance_list

