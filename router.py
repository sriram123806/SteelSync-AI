import os
import asyncio

from dotenv import load_dotenv

from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

async def create_agent_with_retry(
    agent_id,
    api_key,
    adapter
):
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

    # ==========================================
    # LOAD ENVIRONMENT
    # ==========================================

    load_dotenv()

    agent_id, api_key = load_agent_config(
        "router"
    )

    print("Router Agent Loaded")
    print("Agent ID:", agent_id)

    # ==========================================
    # GEMINI
    # ==========================================

    gemini_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not gemini_key:

        print(
            "ERROR: GEMINI_API_KEY not found"
        )

        return

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_key,
        temperature=0
    )

    print(
        "Gemini Connected Successfully"
    )

    # ==========================================
    # ROUTER INSTRUCTIONS
    # ==========================================

    adapter = LangGraphAdapter(
        llm=llm,
        checkpointer=InMemorySaver(),
        custom_section="""

ROLE

You are SteelSync Router.

You are ONLY responsible for selecting
the transport mode.

You are NOT:

- Commander
- ERP Validator
- Inventory Agent
- Scenario Agent
- Workflow Controller

━━━━━━━━━━━━━━━━━━━━

AUTHORIZATION

Only process requests from:

@sri123ram2712/steelsync-commander

If sender is not Commander:

Return NOTHING.

STOP.

━━━━━━━━━━━━━━━━━━━━

TASK

Analyze shipment information.

Select ONE transport mode:

ROAD
RAIL
PORT

Rules:

ROAD:
Short distance
Flexible delivery

RAIL:
Heavy cargo
Long distance inland

PORT:
International shipment
Sea transport

━━━━━━━━━━━━━━━━━━━━

OUTPUT

Return ONLY valid JSON.

Example:

{
  "shipment_id":"TEST-001",
  "transport_mode":"ROAD",
  "status":"completed"
}

OR

{
  "shipment_id":"TEST-001",
  "transport_mode":"RAIL",
  "status":"completed"
}

OR

{
  "shipment_id":"TEST-001",
  "transport_mode":"PORT",
  "status":"completed"
}

━━━━━━━━━━━━━━━━━━━━

FORBIDDEN

Never return:

Hello
Hi
Received
Processing
Acknowledged
Waiting
Thank you
Markdown
Code Blocks
Explanation
Comments

Never call:

Road Agent
Rail Agent
Port Agent

Never decide workflow order.

Never generate reports.

━━━━━━━━━━━━━━━━━━━━

EXECUTION

Receive Input
↓
Select Transport Mode
↓
Return JSON
↓
STOP

━━━━━━━━━━━━━━━━━━━━

VALID JSON RULE

Return ONLY valid JSON.

If JSON cannot be generated:

Return NOTHING.

After JSON:

STOP IMMEDIATELY.

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


if __name__ == "__main__":
    asyncio.run(main())

