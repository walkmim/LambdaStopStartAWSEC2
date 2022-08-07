#Conta Secundária
#--Virginia 

##stop
aws ec2 run-instances --image-id ami-090fa75af13c156b4 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-8a37b182 --subnet-id subnet-4a179c2c --region us-east-1 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Stop},{Key=environment,Value=HML},{Key=utc_stop_hour,Value=19}]'

##start
aws ec2 run-instances --image-id ami-090fa75af13c156b4 --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-8a37b182 --subnet-id subnet-4a179c2c --region us-east-1 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=start},{Key=environment,Value=DEV},{Key=utc_start_hour,Value=19}]'


