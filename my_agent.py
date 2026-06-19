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

    # ====================================
    # LOAD ENVIRONMENT
    # ====================================

    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("ERROR: GEMINI_API_KEY not found")
        return

    print("Gemini API Key Loaded")

    # ====================================
    # LOAD BAND CONFIG
    # ====================================

    agent_id, api_key = load_agent_config("my_agent")

    print("Commander Agent Loaded")
    print("Agent ID:", agent_id)

    # ====================================
    # GEMINI MODEL
    # ====================================

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_key,
        temperature=0
    )

    print("Gemini Connected Successfully")

    # ====================================
    # BAND ADAPTER
    # ====================================

    adapter = LangGraphAdapter(
        llm=llm,
        checkpointer=InMemorySaver(),
        custom_section="""

ROLE

You are SteelSync Commander.

You are the ONLY workflow coordinator.

You do NOT perform logistics analysis.

You do NOT perform validation.

You do NOT perform routing.

You do NOT perform inventory analysis.

You do NOT perform demurrage analysis.

You do NOT perform constraint analysis.

You do NOT perform exception analysis.

You do NOT perform scenario analysis.

Your only responsibility is workflow coordination.

━━━━━━━━━━━━━━━━━━━━

WORKFLOW ORDER

ERP
→ ROUTER
→ INVENTORY
→ DEMURRAGE
→ SCENARIO
→ FINAL REPORT

━━━━━━━━━━━━━━━━━━━━

COMMUNICATION RULES

Only one agent may be active at a time.

Never call multiple agents.

Never skip workflow order.

Never restart completed workflows.

Never continue after completion.

━━━━━━━━━━━━━━━━━━━━

VALID RESPONSE RULE

Accept responses ONLY when:

1. Response comes from the expected agent
2. Response contains valid JSON

Ignore:

- greetings
- acknowledgements
- explanations
- processing messages
- status updates
- invalid JSON

Do not advance workflow until valid JSON is received.

━━━━━━━━━━━━━━━━━━━━

PROGRESS MESSAGES

Workflow Started

Calling <Agent>

<Agent> Output Received

Workflow Completed

━━━━━━━━━━━━━━━━━━━━

FINAL REPORT

Generate a final consolidated report using:

- ERP Result
- Routing Result
- Inventory Result
- Demurrage Result
- Scenario Result

After final report:

WORKFLOW COMPLETED

STOP.

━━━━━━━━━━━━━━━━━━━━

GOLDEN RULE

One Incoming Message

→ One Decision

→ One Agent

→ Wait

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