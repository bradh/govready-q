#!/usr/bin/env python

################################################################
#
# rds.py
#
# Usage: rds.py
#
################################################################

# for debugging
from pprint import pprint

# for control-C handling
import sys
import signal

# parse command-line arguments
import argparse

# regular expressions
import re

# OS-specific (paths)
import os

# AWS/S3 interface
import boto3
from botocore.client import Config

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='rds.py')
    return parser

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # make AWS connections
    ec2 = boto3.client('ec2', region_name='us-east-2')
    rds = boto3.client('rds', region_name='us-east-2', config=Config(retries=dict(max_attempts=20)))

    # create VPC
    response = ec2.create_vpc(CidrBlock='192.168.0.0/16')
    vpc = response["Vpc"];
    print(vpc)
    ec2.get_waiter('vpc_available', VpcIds=vpc['VpcId'])
    print(vpc)

    # create subnet
    subnet = vpc.create_subnet(CidrBlock='192.168.1.0/24', AvailabilityZone="us-east-2")
    print(subnet.id)

    # Create sec group
    sg = ec2.create_security_group(
        GroupName='slice_0', Description='slice_0 sec group', VpcId=vpc.id)
    sg.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='icmp',
        FromPort=-1,
        ToPort=-1
    )
    print(sec_group.id)

    # create db instance
    db_vars = {
        "DBName": "db_name",
        "DBInstanceIdentifier": "instance_name",
        "AllocatedStorage": 20,
        "DBInstanceClass": "db.m3.medium",
        "Engine": "postgres",
        "MasterUsername": "username",
        "MasterUserPassword": "password",
        "VpcSecurityGroupIds": [
            sg.id
        ],
        "DBSubnetGroupName": "my-subnet",
        "DBParameterGroupName": "my-parameter-group",
        "BackupRetentionPeriod": 7,
        "MultiAZ": True,
        "EngineVersion": "10.0.1",
        "PubliclyAccessible": False,
        "StorageType": "gp2",
    }
    rds.create_db_instance(**db_vars)
        
if __name__ == "__main__":
    exit(main())
