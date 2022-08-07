
Provisionar recursos via AWS CLI v2:

Recursos a serem provisionados na conta executora (centralizada)

IAM Policy:
aws iam create-policy --policy-name policy_lambda_stop_start_instance --policy-document file://policy_lambda_stop_start_instance.json

IAM Role:
aws iam create-role --role-name role_lambda_stop_start_instance --assume-role-policy-document file://lambda_role_service.json

Atachar Policy à role:
aws iam attach-role-policy --policy-arn arn:aws:iam::770409265803:policy/policy_lambda_stop_start_instance --role-name role_lambda_stop_start_instance


Parameter Store:
aws ssm put-parameter \
    --name "AUTOMATION-STOP-START-EC2" \
    --value 'print_only = "Y"|accounts = ["770409265803","583166431114"]|accounts_apply_all = ["770409265803"]|assume_role_name = "role_stop_start_instances"| regions = ["us-east-1","us-east-2"]|sleep_sec_next_order = 30|default_utc_stop_hour = 22|default_utc_start_hour = 12|environments = ["DEV","HML","PREPROD","SANDBOX"]|dynamodb_table = "tb_stop_start_instances"|log_actions_cw_logs = "Y"' \
    --type StringList \
    --tags "Key=objective,Value=test" 

Tabela DynamoDB para Log:
aws dynamodb create-table \
    --table-name tb_stop_start_instances \
    --attribute-definitions AttributeName=unique_id,AttributeType=S AttributeName=utc_timestamp,AttributeType=N \
    --key-schema AttributeName=unique_id,KeyType=HASH AttributeName=utc_timestamp,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --tags "Key=objective,Value=test" 

Repositório AWS ECR (Elastic Container Registry):
aws ecr create-repository \
    --repository-name app-stop-start-ec2 \
    --image-scanning-configuration scanOnPush=true

Realizar push da imagem (Executar no diretório "python_code"):
docker build -t app-stop-start-ec2 .
docker tag app-stop-start-ec2:latest 770409265803.dkr.ecr.us-east-1.amazonaws.com/app-stop-start-ec2:latest
docker push 770409265803.dkr.ecr.us-east-1.amazonaws.com/app-stop-start-ec2:latest

Lambda Function (Executar no diretorio .../Resource Provisioning após o ECR ser provisionado por completo):
aws lambda create-function --cli-input-json file://lambda_function.json

******************************************************************************

Deletar recursos provisionados via AWS CLI v2 na conta executora:


aws lambda delete-function \
    --function-name lambda_stop_start_instance

aws ssm delete-parameter \
    --name "AUTOMATION-STOP-START-EC2"
    
aws dynamodb delete-table \
    --table-name tb_stop_start_instances

aws ecr delete-repository \
    --repository-name app-stop-start-ec2 \
    --force

IAM Detach:
aws iam detach-role-policy --policy-arn arn:aws:iam::770409265803:policy/policy_lambda_stop_start_instance --role-name role_lambda_stop_start_instance

IAM Role:
aws iam delete-role --role-name role_lambda_stop_start_instance

IAM Policy (Necessário deletar todas as versões da policy, exceto a ultima antes de deletar a mesma ):
aws iam list-policy-versions --policy-arn arn:aws:iam::770409265803:policy/policy_lambda_stop_start_instance

aws iam delete-policy-version --policy-arn arn:aws:iam::770409265803:policy/policy_lambda_stop_start_instance --version-id v4
aws iam delete-policy --policy-arn arn:aws:iam::770409265803:policy/policy_lambda_stop_start_instance

* Deletar log group da lambda através da Console AWS na Sessão CloudWatch/Logs/Log groups

******************************************************************************

Recursos a serem provisionados na conta cliente a qual os recursos serão desligados/ligados:

IAM Policy:
aws iam create-policy --policy-name policy_stop_start_instances --policy-document file://policy_stop_start_instances.json

IAM Role:
aws iam create-role --role-name role_stop_start_instances --assume-role-policy-document file://trust_relationship_account.json

Atachar Policy à role:
aws iam attach-role-policy --policy-arn arn:aws:iam::770409265803:policy/policy_stop_start_instances --role-name role_stop_start_instances

******************************************************************************

Deletar recursos provisionados via AWS CLI v2 na conta cliente a qual os recursos serão desligados/ligados:

IAM Detach:
aws iam detach-role-policy --policy-arn arn:aws:iam::770409265803:policy/policy_stop_start_instances --role-name role_stop_start_instances

IAM Role:
aws iam delete-role --role-name role_stop_start_instances

IAM Policy (Necessário deletar todas as versões da policy, exceto a ultima antes de deletar a mesma ):
aws iam list-policy-versions --policy-arn arn:aws:iam::770409265803:policy/policy_stop_start_instances

aws iam delete-policy-version --policy-arn arn:aws:iam::770409265803:policy/policy_stop_start_instances --version-id v4
aws iam delete-policy --policy-arn arn:aws:iam::770409265803:policy/policy_stop_start_instances


******************************************************************************

Provisionando EC2s para validar lambda function via AWS CLI v2:

