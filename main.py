# main.py

import os
import sys
import time

# local imports
from create_agent_role import create_bedrock_agent_role
from bedrock_agent_ops import create_agent, prepare_agent, invoke_agent


def main():
    # 1) Create or retrieve the IAM role for the agent
    role = create_bedrock_agent_role()
    agent_role_arn = role.arn
    print(f"Using agent role ARN: {agent_role_arn}")

    # 2) Create a new agent
    AGENT_NAME = "my-bedrock-agent-demo"
    FOUNDATION_MODEL = "anthropic.claude-v2"  # or "meta.llama2-13b-chat-v1", etc.
    # This 'instruction' is the "system prompt" or "base context" the agent always uses
    BASE_INSTRUCTION = """
You are a helpful agent that answers questions about general knowledge.
If the user asks something outside your context, politely say you cannot answer.
"""
    agent_obj = create_agent(
        agent_name=AGENT_NAME,
        foundation_model=FOUNDATION_MODEL,
        instruction=BASE_INSTRUCTION,
        agent_role_arn=agent_role_arn
    )
    agent_id = agent_obj["agentId"]

    # 3) Prepare the agent
    agent_version = prepare_agent(agent_id)

    # 4) Invoke the agent with a sample question
    # Alias can be the agent_version or you can create an "alias" if you prefer
    session_id = "my-session-001"
    question = "Hi agent, can you tell me a bit about the city of Seattle?"
    result = invoke_agent(
        agent_id=agent_id,
        agent_alias_id=agent_version,  # can also set up an alias separately
        session_id=session_id,
        user_input=question
    )

    print("\nFinal Combined Output:\n", result)


if __name__ == "__main__":
    main()