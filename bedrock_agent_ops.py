# bedrock_agent_ops.py

import time
import sys
import boto3
from botocore.exceptions import ClientError


def create_agent(agent_name, foundation_model, instruction, agent_role_arn):
    """
    Creates a new Bedrock Agent in AWS, with a base instruction (system prompt).
    Returns the newly created agent object (dict).
    """

    client = boto3.client("bedrock-agent", region_name="us-east-1")

    print(f"Creating agent: {agent_name} with model={foundation_model}")
    try:
        response = client.create_agent(
            agentName=agent_name,
            foundationModel=foundation_model,
            instruction=instruction,
            agentResourceRoleArn=agent_role_arn
            # If you want advanced prompt overrides, see the "promptOverrideConfiguration" param
        )
        agent = response["agent"]
        print("Agent creation initiated. Current status:", agent["agentStatus"])
        return agent

    except ClientError as e:
        print("Error creating Bedrock Agent:", e)
        raise


def prepare_agent(agent_id):
    """
    Prepares (deploys) the Agent so it's in "PREPARED" state.
    This can take some time, so we poll until status is 'PREPARED'.
    Returns the agentVersion.
    """

    client = boto3.client("bedrock-agent", region_name="us-east-1")
    print(f"Preparing agent: {agent_id} ...")
    resp = client.prepare_agent(agentId=agent_id)
    agent_version = resp["agentVersion"]

    # Poll for status
    while True:
        get_resp = client.get_agent(agentId=agent_id)
        status = get_resp["agent"]["agentStatus"]
        print(f"  Current agent status: {status}")
        if status == "PREPARED":
            break
        elif status in ["FAILED", "DELETED"]:
            raise RuntimeError(f"Agent in unexpected status: {status}")
        else:
            time.sleep(5)

    print(f"Agent is prepared! agentVersion={agent_version}")
    return agent_version


def invoke_agent(agent_id, agent_alias_id, session_id, user_input):
    """
    Invoke the prepared agent to get an answer to user_input.
    Streams the response chunk by chunk.
    Returns the final text completion as a string.
    """

    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

    print(f"Invoking agentId={agent_id}, aliasId={agent_alias_id} with user input:\n{user_input}")
    response = client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=user_input
    )

    final_output = []
    print("Response stream from the agent:\n---------------------------------")
    for event in response["completion"]:
        # The bedrock agent runtime returns a stream of "event" dicts
        if "chunk" in event:
            chunk_text = event["chunk"]["bytes"].decode()
            final_output.append(chunk_text)
            print(chunk_text, end="", flush=True)
        elif "trace" in event:
            # agent might produce a "trace" event for internal steps
            pass

    print("\n---------------------------------")
    return "".join(final_output)
