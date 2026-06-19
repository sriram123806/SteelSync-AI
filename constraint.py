import os
import asyncio

from dotenv import load_dotenv

from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver


async def main():

    # Load environment variables
    load_dotenv()

    # Load Constraint Agent credentials
    agent_id, api_key = load_agent_config("constraint")

    print("Constraint Agent ID loaded successfully")
    print("Agent ID:", agent_id)

    # Connect AIMLAPI
    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        base_url="https://api.aimlapi.com/v1",
        api_key=os.getenv("AIMLAPI_API_KEY"),
    )

    print("GPT-4o Mini connected through AIMLAPI")

    adapter = LangGraphAdapter(
        llm=llm,
        checkpointer=InMemorySaver(),
        custom_section="""
ROLE

You are SteelSync Constraint Agent.

AUTHORIZATION

Only Commander may call you.

RESPONSIBILITIES

Identify shipment constraints.

OUTPUT

{
"shipment_id":"string",
"constraints":[],
"status":"completed"
}

EXECUTION

Receive Input
→ Detect Constraints
→ Return JSON
→ STOP


VALID JSON RULE

Return ONLY valid JSON.

If output cannot be produced:

Return NOTHING.

Never return greetings.

Never return explanations.

Never return acknowledgements.

Never return markdown.

Never return code blocks.

After JSON:

STOP IMMEDIATELY.
"""
    )

    print("Creating agent...")

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    print("Agent created successfully")
    print("Starting Band runtime...")

    print("====================================")
    print("SteelSync Constraint Agent is ONLINE")
    print("Waiting for Band messages...")
    print("====================================")

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())