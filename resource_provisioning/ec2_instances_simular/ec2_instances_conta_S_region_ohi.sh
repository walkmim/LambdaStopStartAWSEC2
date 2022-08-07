#Conta Secundária 
#--ohio 

##stop
aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Stop},{Key=environment,Value=HML},{Key=utc_stop_hour,Value=19}]'

##start
aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Start},{Key=environment,Value=HML},{Key=utc_start_hour,Value=19}]'

##stop Order
aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Stop_order_1},{Key=environment,Value=HML},{Key=utc_stop_hour,Value=19},{Key=stop_order,Value=1}]'

aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Stop_order_0},{Key=environment,Value=HML},{Key=utc_stop_hour,Value=19},{Key=stop_order,Value=0}]'


##start Order
aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Start_order_1},{Key=environment,Value=HML},{Key=utc_start_hour,Value=19},{Key=start_order,Value=1}]'

aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Start_order_0},{Key=environment,Value=HML},{Key=utc_start_hour,Value=19},{Key=start_order,Value=0}]'


##auto_start + server_name
aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=auto_start},{Key=environment,Value=HML},{Key=utc_start_hour,Value=19},{Key=auto_start,Value=N},{Key=server_name,Value=Salamandra}]'

##skip_until + server_name
aws ec2 run-instances --image-id ami-051dfed8f67f095f5 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-e4499a97 --subnet-id subnet-5060221c --region us-east-2 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=skip_until},{Key=environment,Value=HML},{Key=utc_stop_hour,Value=19},{Key=skip_until,Value=30/08/2022},{Key=server_name,Value=Carnaval}]'

