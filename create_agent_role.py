# create_agent_role.py

import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

ROLE_NAME = "AmazonBedrockExecutionRoleForAgents_Example"
POLICY_NAME = "AllowBedrockInvokeModelPolicy"
FOUNDATION_MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2"

def create_bedrock_agent_role():
    """
    Creates an IAM role that the Bedrock Agent will assume, 
    with permission to invoke the chosen foundation model.
    """

    iam = boto3.resource('iam')

    # 1) Create trust policy so 'bedrock.amazonaws.com' can assume this role
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "bedrock.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # 2) Create a role with that trust policy
    try:
        role = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="IAM role for Bedrock Agent to invoke foundation models."
        )
        print(f"Created role: {ROLE_NAME}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            # If the role already exists, just retrieve it
            print(f"Role '{ROLE_NAME}' already exists, re-using.")
            role = iam.Role(ROLE_NAME)
        else:
            raise e

    # 3) Attach a policy to allow bedrock:InvokeModel on a chosen model
    inline_policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "bedrock:InvokeModel",
                "Resource": FOUNDATION_MODEL_ARN
            }
        ]
    }

    try:
        role.Policy(POLICY_NAME).put(
            PolicyDocument=json.dumps(inline_policy_doc)
        )
        print(f"Attached inline policy '{POLICY_NAME}' to {ROLE_NAME}")
    except ClientError as e:
        print("Error attaching policy:", e)
        raise

    return role


if __name__ == "__main__":
    create_bedrock_agent_role()

    