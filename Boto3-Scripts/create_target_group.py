import boto3
import time

REGION = 'us-west-1'  # your region
VPC_ID = 'vpc-0105c14ae6db35835'  # Replace with your created VPC ID
LOAD_BALANCER_ARN = 'arn:aws:elasticloadbalancing:us-west-1:975050024946:loadbalancer/app/backend-lb/e6482c8d21ef158d'  # Replace with your created Load Balancer ARN

ec2 = boto3.client('ec2', region_name=REGION)
elbv2 = boto3.client('elbv2', region_name=REGION)
autoscaling = boto3.client('autoscaling', region_name=REGION)

def create_target_groups():
    print("[+] Creating Target Groups...")

    tg_hello = elbv2.create_target_group(
        Name='tg-hello-service',
        Protocol='HTTP',
        Port=3001,
        VpcId=VPC_ID,
        TargetType='instance'
    )

    tg_profile = elbv2.create_target_group(
        Name='tg-profile-service',
        Protocol='HTTP',
        Port=3002,
        VpcId=VPC_ID,
        TargetType='instance'
    )

    hello_arn = tg_hello['TargetGroups'][0]['TargetGroupArn']
    profile_arn = tg_profile['TargetGroups'][0]['TargetGroupArn']

    print(f"[+] Target Group for Hello Service created: {hello_arn}")
    print(f"[+] Target Group for Profile Service created: {profile_arn}")
    return hello_arn, profile_arn

def create_listener_rules(hello_tg_arn, profile_tg_arn):
    print("[+] Creating Listener and Rules...")
    
    # Fetch the listener attached to Load Balancer
    listeners = elbv2.describe_listeners(LoadBalancerArn=LOAD_BALANCER_ARN)
    listener_arn = listeners['Listeners'][0]['ListenerArn']

    # Create rules for path-based routing
    elbv2.create_rule(
        ListenerArn=listener_arn,
        Conditions=[{'Field': 'path-pattern', 'Values': ['/hello']}],
        Priority=10,
        Actions=[{'Type': 'forward', 'TargetGroupArn': hello_tg_arn}]
    )

    elbv2.create_rule(
        ListenerArn=listener_arn,
        Conditions=[{'Field': 'path-pattern', 'Values': ['/profile']}],
        Priority=20,
        Actions=[{'Type': 'forward', 'TargetGroupArn': profile_tg_arn}]
    )

    print("[+] Listener Rules created successfully!")

def main():
    hello_tg_arn, profile_tg_arn = create_target_groups()
    # wait for target groups to be fully created
    time.sleep(5)
    create_listener_rules(hello_tg_arn, profile_tg_arn)

if __name__ == "__main__":
    main()
