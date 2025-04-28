import boto3

REGION = 'us-west-1'  # your region
LOAD_BALANCER_ARN = 'arn:aws:elasticloadbalancing:us-west-1:975050024946:loadbalancer/app/backend-lb/e6482c8d21ef158d'  # Replace your Load Balancer ARN

elbv2 = boto3.client('elbv2', region_name=REGION)

def create_listener():
    print("[+] Creating HTTP Listener on Load Balancer...")

    response = elbv2.create_listener(
        LoadBalancerArn=LOAD_BALANCER_ARN,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'fixed-response',
                'FixedResponseConfig': {
                    'ContentType': 'text/plain',
                    'MessageBody': 'Default response',
                    'StatusCode': '200'
                }
            }
        ]
    )

    listener_arn = response['Listeners'][0]['ListenerArn']
    print(f"[+] Listener created: {listener_arn}")

if __name__ == "__main__":
    create_listener()
