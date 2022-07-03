import boto3
import os
import sys
from datetime import datetime, timedelta
from geral_functions import *

def clear_instances(accounts,assume_role_name,regions):

    for account in accounts:
        session = assume_role_session(account,assume_role_name)

        for region in regions:
            ec2_client = session.client('ec2', region_name=region)
            ec2_instances = []
            
            ec2_instances += ec2_client.describe_instances()["Reservations"]
            
            for instance in ec2_instances:
                
                instance_detail = instance["Instances"][0]
                    # print (instance_detail)
                instance_id = instance_detail["InstanceId"]
                
                ec2_client.terminate_instances(
                    InstanceIds=[
                        instance_id,
                    ],
                )
                print(instance_id,"deleted")