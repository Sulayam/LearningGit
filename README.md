# AWS Bedrock Agent Example (REACT-Style Starter)

This example project demonstrates how to programmatically:

1. Create an IAM role for a Bedrock Agent
2. Create an Agent using a foundation model (e.g., `anthropic.claude-v2`)
3. Prepare the Agent so it’s ready to answer queries
4. Invoke the Agent with an example question

## Quickstart

1. Clone the repo or copy these files into your working directory.
2. Ensure you have valid AWS credentials with permissions to call:
   - IAM (to create roles)
   - bedrock
   - bedrock-agent
   - bedrock-agent-runtime

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
