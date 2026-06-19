import os
import asyncio

from dotenv import load_dotenv

from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver


async def create_agent_with_retry(agent_id, api_key, adapter):
    while True:
        try:
            agent = Agent.create(
                adapter=adapter,
                agent_id=agent_id,
                api_key=api_key,
            )
            return agent

        except Exception as e:
            print("\n================================")
            print("AGENT CREATION FAILED")
            print(str(e))
            print("Retrying in 60 seconds...")
            print("================================\n")
            await asyncio.sleep(60)


async def run_agent_with_retry(agent):
    while True:
        try:
            await agent.run()

        except Exception as e:
            print("\n================================")
            print("RUNTIME ERROR")
            print(str(e))
            print("Waiting 60 seconds...")
            print("================================\n")
            await asyncio.sleep(60)


async def main():
    load_dotenv()

    # -----------------------------------
    # BAND CONFIG
    # -----------------------------------
    agent_id, api_key = load_agent_config("erp_validator")

    print("ERP Validator Agent Loaded")
    print("Agent ID:", agent_id)

    # -----------------------------------
    # GEMINI CONFIG
    # -----------------------------------
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("ERROR: GEMINI_API_KEY not found")
        return

    print("Gemini API Key Loaded")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_key,
        temperature=0
    )

    print("Gemini Connected Successfully")

    # -----------------------------------
    # ERP VALIDATOR PROMPT
    # -----------------------------------
    adapter = LangGraphAdapter(
        llm=llm,
        checkpointer=InMemorySaver(),
        custom_section="""

ROLE
SteelSync ERP Validator

You are ONLY an ERP validation agent.

You are NOT:
- Commander
- Router
- Inventory Agent
- Scenario Agent
- Workflow Controller

━━━━━━━━━━━━━━━━━━━━
AUTHORIZATION
Process ONLY requests coming from:
@sri123ram2712/steelsync-commander

If sender is not Commander:
Return NOTHING.
STOP.

━━━━━━━━━━━━━━━━━━━━
TASK
Validate:
- shipment_id
- origin
- destination
- cargo_type
- weight_kg
- container_count

Check:
- missing fields
- empty fields
- invalid fields

Do NOT repair.
Do NOT modify.
Do NOT explain.

━━━━━━━━━━━━━━━━━━━━
OUTPUT
Return ONLY JSON.

Example:
{
  "shipment_id":"TEST-001",
  "status":"passed",
  "missing_fields":[],
  "invalid_fields":[]
}

OR

{
  "shipment_id":"TEST-001",
  "status":"failed",
  "missing_fields":["destination"],
  "invalid_fields":[]
}

━━━━━━━━━━━━━━━━━━━━
FORBIDDEN
Never return:
Hello
Hi
Received
Processing
Acknowledged
Thank you
Markdown
Code Blocks
Explanation

━━━━━━━━━━━━━━━━━━━━
RULE
Input
↓
Validate
↓
Return JSON
↓
STOP

Never send a second message.
STOP.

"""
    )

    # -----------------------------------
    # CREATE AGENT WITH RETRY
    # -----------------------------------
    agent = await create_agent_with_retry(
        agent_id,
        api_key,
        adapter
    )

    print("===================================")
    print("ERP VALIDATOR ONLINE")
    print("Waiting For Messages...")
    print("===================================")

    await run_agent_with_retry(agent)


# Ensure the execution block is strictly unindented at the module level
if __name__ == "__main__":
    asyncio.run(main())