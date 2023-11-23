# AWS Infrastructure Setup for Auto-Scaling Web Application

This README provides a step-by-step guide to set up an AWS infrastructure for an auto-scaling web application. The setup includes creating a Virtual Private Cloud (VPC), creating 2 public subnets, setting up gateways, and launching an EC2 instance with auto-scaling capabilities.

## Step 1: Create VPC

1. Navigate to VPC service from the research bar and click `Create VPC`
2. Name tag your VPC as `VPC-group1`
3. For `IPv4 CIDR` write `10.0.0.0/16`
4. Click the orange button `Create VPC`

## Step 2: Create 2 public subnets

1. Navigate to `Subnets` and click `Create subnet`
2. Select your VPC create before
3. Under `Subnet settings`:
	- Name your subnet as `Public-Subnet-1`
	- Select an Aviability Zone (AZ)
	- For `IPv4 subnet CIDR block` assign `10.0.0.0/24`
4. Click on `Add Subnet`
5. Under `Subnet settings`:
	- Name your subnet as `Public-Subnet-2`
	- Select a different AZ than before
	- For `IPv4 subnet CIDR block` assign `10.0.1.0/24`
6. Click on orange button `Create subnet`
7. Select a subnet you still created and click on `Actions` > `Edit subnet settings`
8. Under `Auto-assign IP settings` select `Enable auto-assign public IPv4 address` > click on `Save` orange button
9. Repeat for the second subnet point 7 and 8

## Step 3: Associate subnets to main route table

1. Navigate to `Route tables` and select the existing MAIN route table and click on `Subnet associations`
2. Scroll down and select `Edit subnet associations` and select both Subnets, than `Save changes`

## Step4: Create internet gateway

1. Navigate to `Internet gateways` and click on `Create internet gateway`
2. Name it as `IG-group1` and clic on orange button `Create internet gateway`
3. Click on `Attach to VPC` and select yours, than save with `Attach internet gateway` orange button
4. Go back to your main Route table, select it, click on `Routes and than on `Edit routes`
5. Click on `Add route` and under:
	- Destination: select 0.0.0.0/0
	- Target: `Internet Gateway` and select your IG
6. Click on `Save changes` orange button

## Step 5: Create Security Group to allow traffic from ALoadBalancer to instances

1. Under `Security` click on `Security groups` and `Create security group`
2. For `Security group name` type `SG-group1`
3. Under `Description` write `allow HTTP from Anywhere`
4. Select your VPC
5. Under `Inbound Rules` click on `Add rule`:
	- Type: `HTTP`
	- Source type: `Anywhere-IPv4`
6. Scroll down and click on orange button `Create security group`

## Step 6: Create a Target Group

1. Move to the EC2 dashboard and click under `Load balancing` > `Target Groups`
2. Click on `Create target group`
3. For `Chosse a target type` choose `Instances`, and select a `Target group name` as `TargetGroup-Group1`
4. Select your `VPC`
5. Leave the `default` value for `Health checks`
6. Click on `Next`
7. Click on `Create target group`

## Step 7: Create a Launch Template for your ASG

1. Navigate to `Instances` > `Launch templates`
2. Click on orange button `Create launch template`
3. Name your launch template as `LT-group1`
4. For `Template version description` write `dev`
5. Enable `Auto Scaling guidance`
6. For `Amazon Machine Image (AMI)` select `Amazon Linux 2 2023 AMI` free tier eligible
7. For `instance type` choose `t2.micro` free tier eligible
8. Under `Key pair (login)` select a key pair, or generate a new keypair
9. Under `Network settings`, select `Select existing security group` and specify your security group in `Security groups`
10. Under `Advanced network configuration` click on `Add network` and enable `Auto-assign public IP`
11. Scroll all the way to the bottom under `Advanced details`, in the `User data` section paste this script:
```
#!/bin/bash
yum update -y
yum install -y httpd
yum install -y php

systemctl start httpd
systemctl enable httpd

echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php
```
12. Click on `Create launch template`

## Step 8: Create an Application Load Balancer

1. Under `Load Balancing` click `Load Balancers` and 'Create load balancer`
2. Choose for `Application Load Balancer` and `Create`
3. Name your load balancer as `ALB-group1`
4. Leave as default and select your VPC under `Network mapping`
5. under `Mappings`, select both your AZ
6. for `Security group`, delete the `default` security group, and select your `SG-group1`
7. Under `Listeners and routing` select your `Target group`
8. Click `Create load balancer` orange button

## Step 9: Create Auto Scaling group

1. Under `Auto scaling`, navigate to `Auto scaling groups` and `Create Auto Scaling group`
2. Define your name as `ASG-group1` and select your `Launch template`
3. Click on `Next` and under `Network` select your `VPC` and both your `Public subnets`
4. For `Load balancer`, `Attach to an existing load balancer`
5. For `Existing load balancer target groups` select your target group
8. Under `Additional settings`, in `Monitoring`, enable `group metrics collection within CloudWatch
9. Click on `Next`
10. For `Group size` set:
	- Desired capacity: `2`
	- Minimum capacity: `1`
	- Maximum capacity: `4`
11. Under `Scaling policies`, choose `Target traking scaling policy` and select `Target Value` up to `70`
12. Click on `Next`, `Skip to review` and `Create Auto Scaling group`
13. Check on left pane `Instances` the check status of your instances until is "2/2 checks passed"

## Step 10: Access the PHP Page

1. On the left pane of EC2 Dashboard click on `Load balancers` and copy the dns name of your load balancer
2. Enter the public IP or DNS name of your EC2 instance followed by `/phpinfo.php`, on your web browser 
3. Check the result

 ## Step 11: Access to EC2 and stress-test
1. move to the folder of your key.pem from your terminal
2. type
```
chmod 400 key.pem
```
and
```
ssh -i key.pem ec2-user@<instance-IP>
```
3. Download and install the stress test tool
```
sudo amazon-linux-extras install epel -y
```
```
sudo yum install stress -y
```
4. Launch the stress test in background (for 800 seconds in that example)
```
sudo stress -c 100 -v
```
Now you can go to your instance dashboard and check for its number and CPUutilization%

*Warning*: remember to Ctrl+C

## Challenges
### Task 1: Creating Another Tier to Host a Python Application - Double Load Balancer

- Create a new tier to host a Python application within a cloud environment (e.g., on AWS, Azure, or GCP).

- Install and configure the necessary Python environment, including the required packages and dependencies for the application.

- Ensure that the application can execute its functions correctly and is accessible.

You can find the code of app.py [here](https://github.com/Sysnove/flask-hello-world/blob/master/hello.py)

### Task 2: Rewriting User Data for Instances in the Auto Scaling Group Using Cloud-Init

- Rewrite the User Data file for all instances within an Auto Scaling Group on a cloud platform (such as AWS, Azure, or GCP) to utilize the Cloud-Init service for the initialization and configuration of the instances within the group.

- Verify that the initialization process using Cloud-Init is well-documented and can be applied to all new instances launched in the Auto Scaling Group.
  
- Test the initialization process using the new User Data based on Cloud-Init and ensure that all new instances are configured correctly and operational

Documentation [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-cloud-init)

## Troubleshooting
- [Helath checks issue](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ts-as-healthchecks.html#ts-failed-elb-health-checks)
