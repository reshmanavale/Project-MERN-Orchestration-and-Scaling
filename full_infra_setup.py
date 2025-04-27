import boto3
import time

# Global config
REGION = "us-west-1"
AMI_ID = "ami-04f7a54071e74f488"  # 👉 Replace with your valid AMI ID
INSTANCE_TYPE = "t2.micro"
KEY_NAME = "Reshma-keypaire"    # 👉 Replace with your EC2 Key Pair name
BACKEND_PORT = 3001               # Example backend port (hello-service runs here)

ec2 = boto3.client('ec2', region_name=REGION)
autoscaling = boto3.client('autoscaling', region_name=REGION)
elbv2 = boto3.client('elbv2', region_name=REGION)

def create_vpc_and_subnets():
    print("[+] Creating VPC...")
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

    print(f"[+] VPC Created: {vpc_id}")

    # Create two subnets
    subnet1 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone=f'{REGION}a')
    subnet2 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone=f'{REGION}b')

    subnet1_id = subnet1['Subnet']['SubnetId']
    subnet2_id = subnet2['Subnet']['SubnetId']

    print(f"[+] Subnets Created: {subnet1_id}, {subnet2_id}")
    return vpc_id, [subnet1_id, subnet2_id]

def create_security_groups(vpc_id):
    print("[+] Creating Security Group...")
    sg = ec2.create_security_group(
        GroupName='backend-sg',
        Description='Allow backend access',
        VpcId=vpc_id
    )
    sg_id = sg['GroupId']

    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': BACKEND_PORT,
                'ToPort': BACKEND_PORT,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )

    print(f"[+] Security Group Created: {sg_id}")
    return sg_id

def create_launch_template(sg_id):
    print("[+] Creating Launch Template...")
    lt = ec2.create_launch_template(
        LaunchTemplateName='backend-launch-template',
        LaunchTemplateData={
            'ImageId': AMI_ID,
            'InstanceType': INSTANCE_TYPE,
            'KeyName': KEY_NAME,
            'SecurityGroupIds': [sg_id],
            'UserData': get_user_data_script()
        }
    )
    lt_id = lt['LaunchTemplate']['LaunchTemplateId']
    print(f"[+] Launch Template Created: {lt_id}")
    return lt_id

def get_user_data_script():
    script = """#!/bin/bash
    yum update -y
    yum install docker -y
    service docker start
    docker run -d -p 3001:3001 975050024946.dkr.ecr.us-west-1.amazonaws.com/hello-service:latest
    """
    import base64
    return base64.b64encode(script.encode('utf-8')).decode('utf-8')

def create_auto_scaling_group(lt_id, subnet_ids):
    print("[+] Creating Auto Scaling Group...")
    asg_name = "backend-asg"
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchTemplate={'LaunchTemplateId': lt_id},
        MinSize=1,
        MaxSize=2,
        DesiredCapacity=1,
        VPCZoneIdentifier=','.join(subnet_ids),
        HealthCheckType='EC2',
    )
    print(f"[+] Auto Scaling Group Created: {asg_name}")
    return asg_name

def create_load_balancer(vpc_id, subnet_ids, sg_id):
    print("[+] Creating Load Balancer...")
    lb = elbv2.create_load_balancer(
        Name='backend-lb',
        Subnets=subnet_ids,
        SecurityGroups=[sg_id],
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
    )
    lb_arn = lb['LoadBalancers'][0]['LoadBalancerArn']
    lb_dns = lb['LoadBalancers'][0]['DNSName']
    print(f"[+] Load Balancer Created: {lb_dns}")

    target_group = elbv2.create_target_group(
        Name='backend-target-group',
        Protocol='HTTP',
        Port=BACKEND_PORT,
        VpcId=vpc_id,
        TargetType='instance',
        HealthCheckProtocol='HTTP',
        HealthCheckPort=str(BACKEND_PORT),
        HealthCheckPath='/'
    )
    tg_arn = target_group['TargetGroups'][0]['TargetGroupArn']

    print("[+] Creating Listener...")
    elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            }
        ]
    )
    print("[+] Load Balancer Listener and Target Group setup done!")
    return lb_dns

def main():
    vpc_id, subnet_ids = create_vpc_and_subnets()
    sg_id = create_security_groups(vpc_id)
    lt_id = create_launch_template(sg_id)
    create_auto_scaling_group(lt_id, subnet_ids)
    lb_dns = create_load_balancer(vpc_id, subnet_ids, sg_id)
    print(f"[✔] Deployment Completed. Access your app at: http://{lb_dns}")

if __name__ == "__main__":
    main()
