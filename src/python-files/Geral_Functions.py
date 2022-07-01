import boto3
import botocore
import datetime
from dateutil.tz import tzlocal

def assume_role_session(account,assume_role_name):
    
    sts_client = boto3.client('sts')
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    role_arn = "arn:aws:iam::"+account+":role/"+assume_role_name
    role_session_name = "RoleSession"+account+"_"+assume_role_name
    assumed_role_object=sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
    
    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    credentials=assumed_role_object['Credentials']
    
    session = boto3.session.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    
    return session

def assumed_role_session_2(account,assume_role_name):
    
    role_arn = "arn:aws:iam::"+account+":role/"+assume_role_name
    
    botocore.session.Session = None
    base_session = base_session or boto3.session.Session()._session
    fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
        client_creator = base_session.create_client,
        source_credentials = base_session.get_credentials(),
        role_arn = role_arn,
        extra_args = {
        #    'RoleSessionName': None # set this if you want something non-default
        }
    )
    creds = botocore.credentials.DeferredRefreshableCredentials(
        method = 'assume-role',
        refresh_using = fetcher.fetch_credentials,
        time_fetcher = lambda: datetime.datetime.now(tzlocal())
    )
    botocore_session = botocore.session.Session()
    botocore_session._credentials = creds
    return boto3.Session(botocore_session = botocore_session)