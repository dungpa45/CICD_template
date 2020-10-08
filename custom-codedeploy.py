import boto3
import botocore
import random
import string
from crhelper import CfnResource

helper = CfnResource()

def createCodeDeployDMG(event):
    codeDeployApp_name = event['ResourceProperties']['ApplicationName']
    codeDeployDMG_name = event['ResourceProperties']['DeploymentGroupName']
    asg_name = event['ResourceProperties']['AutoScalingGroup']
    codeDeploy_role_arn = event['ResourceProperties']['CodeDeployRoleArn']
    elb_name = event['ResourceProperties']['LoadBalancerName']
    targetgroup_name = event['ResourceProperties']['TargetGroupName']
    region = event['ResourceProperties']['Region']
    code_deploy = boto3.client('codedeploy', region_name=region)
    response = code_deploy.create_deployment_group(
        applicationName=codeDeployApp_name,
        deploymentGroupName=codeDeployDMG_name,
        deploymentConfigName = 'CodeDeployDefault.AllAtOnce',
        autoScalingGroups=[
            asg_name,
        ],
        serviceRoleArn=codeDeploy_role_arn,
        autoRollbackConfiguration={
            'enabled': True,
            'events': [
                'DEPLOYMENT_FAILURE'
            ]
        },
        deploymentStyle={
            'deploymentType': 'BLUE_GREEN',
            'deploymentOption': 'WITH_TRAFFIC_CONTROL'
        },
        blueGreenDeploymentConfiguration={
            'terminateBlueInstancesOnDeploymentSuccess': {
                'action': 'TERMINATE',
                'terminationWaitTimeInMinutes': 0
            },
            'deploymentReadyOption': {
                'actionOnTimeout': 'STOP_DEPLOYMENT',
                'waitTimeInMinutes': 45
            },
            'greenFleetProvisioningOption': {
                'action': 'COPY_AUTO_SCALING_GROUP'
            }
        },
        loadBalancerInfo={
            'targetGroupInfoList': [
                {
                    'name': targetgroup_name
                },
            ]
        }
    )
    return codeDeployDMG_name

def deleteCodeDeployDMG(event):
    codeDeployApp_name = event['ResourceProperties']
    codeDeployDMG_name = event['ResourceProperties']
    region = event['ResourceProperties']['Region']
    codedeploy = boto3.client('codedeploy', region_name=region)
    try:
        response = codedeploy.delete_deployment_group(
            applicationName=codeDeployApp_name,
            deploymentGroupName=codeDeployDMG_name
        )
    except codedeploy.Client.exceptions.InvalidDeploymentConfigNameException:
        pass
    except codedeploy.Client.exceptions.DeploymentConfigNameRequiredException:
        pass
    except codedeploy.Client.exceptions.DeploymentConfigInUseException:
        pass
    except codedeploy.Client.exceptions.InvalidOperationException:
        pass

def updateCodeDeployDMG(event):
    deleteCodeDeployDMG(event)
    return createCodeDeployDMG(event)

def createRandomString():
    valid_char = string.ascii_letters+string.digits
    ran_string = ''.join(random.choice(valid_char) for i in range(9))
    ran_string = ran_string.upper()
    return ran_string

def getSubnetArn(event):
    region = event['ResourceProperties']['Region']
    l_subnet = event['ResourceProperties']['SubnetIds']
    subnet = boto3.client("ec2", region_name=region)
    l_res = subnet.describe_subnets(
        SubnetIds=l_subnet
    )["Subnets"]
    l_subnetArn = [i["SubnetArn"] for i in l_res]
    s_arn = ''
    for arn in l_subnetArn:
        s_arn=s_arn+','+arn
    str_arn = s_arn[1:]
    return str_arn

def convertLowercase(event):
    string_convert = event['ResourceProperties']['NameConvert']
    low_str = string_convert.lower()
    return low_str

@helper.create
def createResource(event,_):
    resourceType = event["ResourceType"]
    if resourceType == "Custom::CodeDeployDMG":
        return createCodeDeployDMG(event)
    elif resourceType == "Custom::RandomString":
        return createRandomString()
    elif resourceType == "Custom::GetSubnetArn":
        return getSubnetArn(event)
    elif resourceType == "Custom::ConvertLowercase":
        return convertLowercase(event)
    else:
        raise Exception("Invalid resource type: "+resourceType)

@helper.delete
def deleteResource(event,_):
    resourceType = event["ResourceType"]
    if resourceType == "Custom::CodeDeployDMG":
        return createCodeDeployDMG(event)
    elif resourceType == "Custom::RandomString":
        return createRandomString()
    elif resourceType == "Custom::GetSubnetArn":
        return getSubnetArn(event)
    elif resourceType == "Custom::ConvertLowercase":
        return convertLowercase(event)
    else:
        raise Exception("Invalid resource type: "+resourceType)

@helper.update
def updateResource(event,_):
    resourceType = event["ResourceType"]
    if resourceType == "Custom::CodeDeployDMG":
        return createCodeDeployDMG(event)
    elif resourceType == "Custom::RandomString":
        pass
    elif resourceType == "Custom::GetSubnetArn":
        return getSubnetArn(event)
    elif resourceType == "Custom::ConvertLowercase":
        return convertLowercase(event)
    else:
        raise Exception("Invalid resource type: "+resourceType)

def lambda_handler(event,context):
    helper(event,context)