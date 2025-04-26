import boto3
import time

# --- Configuration ---
REGION = 'us-west-1'
AMI_ID = 'ami-0c55b159cbfafe1f0'  # Amazon Linux 2 AMI (Change if needed)
INSTANCE_TYPE = 't2.micro'
KEY_PAIR = 'your-key-pair-name'  # Replace with your actual key pair
SECURITY_GROUP_ID = 'your-security-group-id'  # Replace with your security group ID
SUBNET_IDS = ['subnet-xxxxxxxx', 'subnet-yyyyyyyy']  # Replace with your subnet IDs
IAM_INSTANCE_PROFILE = 'your-iam-role-name'  # Optional: only if needed for ECR access
LAUNCH_TEMPLATE_NAME = 'backend-launch-template'
ASG_NAME = 'backend-asg'

# Docker commands (you can modify this as per your container names)
USER_DATA_SCRIPT = '''#!/bin/bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Pull your docker images from ECR (update URIs)
# docker login --username AWS --password-stdin <your-ecr-uri>
# echo "ECR_PASSWORD" | docker login --username AWS --password-stdin <your-ecr-uri>

# For now, assume images are public or build locally if needed
docker run -d -p 3001:3001 hello-service
docker run -d -p 3002:3002 profile-service
'''

# --- Boto3 Clients ---
ec2_client = boto3.client('ec2', region_name=REGION)
autoscaling_client = boto3.client('autoscaling', region_name=REGION)

# --- Step 1: Create Launch Template ---
def create_launch_template():
    response = ec2_client.create_launch_template(
        LaunchTemplateName=LAUNCH_TEMPLATE_NAME,
        LaunchTemplateData={
            'ImageId': AMI_ID,
            'InstanceType': INSTANCE_TYPE,
            'KeyName': KEY_PAIR,
            'SecurityGroupIds': [SECURITY_GROUP_ID],
            'UserData': base64.b64encode(USER_DATA_SCRIPT.encode('utf-8')).decode('utf-8'),
            'IamInstanceProfile': {
                'Name': IAM_INSTANCE_PROFILE
            } if IAM_INSTANCE_PROFILE else {}
        }
    )
    print(f"✅ Launch Template '{LAUNCH_TEMPLATE_NAME}' created.")
    return response

# --- Step 2: Create Auto Scaling Group ---
def create_auto_scaling_group():
    response = autoscaling_client.create_auto_scaling_group(
        AutoScalingGroupName=ASG_NAME,
        LaunchTemplate={
            'LaunchTemplateName': LAUNCH_TEMPLATE_NAME,
        },
        MinSize=2,
        MaxSize=4,
        DesiredCapacity=2,
        VPCZoneIdentifier=','.join(SUBNET_IDS),
        Tags=[
            {
                'Key': 'Name',
                'Value': 'backend-ec2-instance',
                'PropagateAtLaunch': True
            }
        ]
    )
    print(f"✅ Auto Scaling Group '{ASG_NAME}' created.")
    return response

# --- Main ---
if __name__ == "__main__":
    import base64

    create_launch_template()
    time.sleep(5)  # Little wait before creating ASG
    create_auto_scaling_group()
    print("🎯 Backend Deployment (EC2 + ASG) Completed Successfully!")
