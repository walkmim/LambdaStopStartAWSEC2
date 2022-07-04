import json
import boto3
from decimal import Decimal
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

dynamodb_table = "tb_stop_start_instances"

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