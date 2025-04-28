import boto3

REGION = "us-west-1"  # Your region
AMI_ID = "ami-04f7a54071e74f488"  # Example AMI ID, change it to your desired AMI
INSTANCE_TYPE = "t2.micro"  # Choose any instance type

ec2 = boto3.client('ec2', region_name=REGION)
autoscaling = boto3.client('autoscaling', region_name=REGION)
elbv2 = boto3.client('elbv2', region_name=REGION)

# Step 1: Create VPC and Subnets
def create_vpc_and_subnets():
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc['Vpc']['VpcId']
    print(f"[+] VPC Created: {vpc_id}")
    
    subnet1 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone=f'{REGION}a')
    subnet2 = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone=f'{REGION}c')
    
    subnet_ids = [subnet1['Subnet']['SubnetId'], subnet2['Subnet']['SubnetId']]
    print(f"[+] Subnets Created: {', '.join(subnet_ids)}")
    
    return vpc_id, subnet_ids

# Step 2: Create Security Group
def create_security_group(vpc_id):
    sg = ec2.create_security_group(
        GroupName='backend-sg',
        Description='Security group for backend instances',
        VpcId=vpc_id
    )
    sg_id = sg['GroupId']
    print(f"[+] Security Group Created: {sg_id}")
    
    # Allow inbound HTTP traffic
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpProtocol='tcp',
        FromPort=80,
        ToPort=80,
        CidrIp='0.0.0.0/0'
    )
    
    return sg_id

# Step 3: Create Launch Template
def create_launch_template(sg_id):
    lt = ec2.create_launch_template(
        LaunchTemplateName='backend-launch-template',
        VersionDescription='v1',
        LaunchTemplateData={
            'ImageId': AMI_ID,
            'InstanceType': INSTANCE_TYPE,
            'SecurityGroupIds': [sg_id],
            'KeyName': 'Reshma-keypair'  # Replace with your key pair
        }
    )
    lt_id = lt['LaunchTemplate']['LaunchTemplateId']
    print(f"[+] Launch Template Created: {lt_id}")
    
    return lt_id

# Step 4: Create Auto Scaling Group
def create_auto_scaling_group(lt_id, subnet_ids):
    autoscaling.create_auto_scaling_group(
        AutoScalingGroupName='backend-asg',
        LaunchTemplate={
            'LaunchTemplateId': lt_id,
            'Version': '1'
        },
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=2,
        VPCZoneIdentifier=','.join(subnet_ids)
    )
    print(f"[+] Auto Scaling Group Created: backend-asg")

# Step 5: Create Internet Gateway and Attach to VPC
def create_internet_gateway(vpc_id):
    igw = ec2.create_internet_gateway()
    igw_id = igw['InternetGateway']['InternetGatewayId']
    print(f"[+] Internet Gateway Created: {igw_id}")

    # Attach the Internet Gateway to the VPC
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"[+] Internet Gateway {igw_id} attached to VPC {vpc_id}")
    
    return igw_id

# Step 6: Update Route Table to Route Traffic to IGW
def update_route_table(vpc_id, igw_id):
    route_tables = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    route_table_id = route_tables['RouteTables'][0]['RouteTableId']
    
    # Create a route to the internet via the Internet Gateway
    ec2.create_route(RouteTableId=route_table_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
    print(f"[+] Route to the internet added to the route table {route_table_id} using IGW {igw_id}")

# Step 7: Create Load Balancer
def create_load_balancer(vpc_id, subnet_ids, sg_id):
    lb = elbv2.create_load_balancer(
        Name='backend-lb',
        Subnets=subnet_ids,
        SecurityGroups=[sg_id],
        Scheme='internet-facing',
        Type='application',          # <-- Corrected here
        IpAddressType='ipv4'
    )
    lb_dns = lb['LoadBalancers'][0]['DNSName']
    print(f"[+] Load Balancer Created: {lb_dns}")
    
    return lb_dns


# Main function to orchestrate everything
def main():
    # Step 1: Create VPC and subnets
    vpc_id, subnet_ids = create_vpc_and_subnets()

    # Step 2: Create Security Group
    sg_id = create_security_group(vpc_id)

    # Step 3: Create Launch Template
    lt_id = create_launch_template(sg_id)

    # Step 4: Create Auto Scaling Group
    create_auto_scaling_group(lt_id, subnet_ids)

    # Step 5: Create Internet Gateway and Attach it to VPC
    igw_id = create_internet_gateway(vpc_id)

    # Step 6: Update Route Table to Route Traffic to the IGW
    update_route_table(vpc_id, igw_id)

    # Step 7: Create Load Balancer
    lb_dns = create_load_balancer(vpc_id, subnet_ids, sg_id)

    print(f"[+] Load Balancer DNS: {lb_dns}")

if __name__ == "__main__":
    main()


