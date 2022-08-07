#Conta Principal 
#--Virginia 

##stop
aws ec2 run-instances --image-id ami-0cff7528ff583bf9a --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-853cd19c --subnet-id subnet-75fbb954 --region us-east-1 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Stop},{Key=utc_stop_hour,Value=19}]'

##start
aws ec2 run-instances --image-id ami-0cff7528ff583bf9a --count 1 --instance-type t2.micro --key-name kp-wallydata --security-group-ids sg-853cd19c --subnet-id subnet-75fbb954 --region us-east-1 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=start},{Key=utc_start_hour,Value=19}]'

