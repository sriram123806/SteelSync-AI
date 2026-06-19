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

    # Load Data Normalizer credentials
    agent_id, api_key = load_agent_config("data_normalizer")

    print("Data Normalizer Agent ID loaded successfully")
    print("Agent ID:", agent_id)

    # Connect AIMLAPI
    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        base_url="https://api.aimlapi.com/v1",
        api_key=os.getenv("AIMLAPI_API_KEY"),
    )

    print("GPT-4o Mini connected through AIMLAPI")

    # Agent behavior
    adapter = LangGraphAdapter(
        llm=llm,
        checkpointer=InMemorySaver(),
        custom_section="""
ROLE

You are SteelSync Data Normalizer.

AUTHORIZATION

Only accept tasks from:

@sri123ram2712/steelsync-commander

Otherwise return NOTHING.

RESPONSIBILITIES

* Normalize field names
* Normalize units
* Normalize dates
* Normalize locations
* Normalize shipment structure

OUTPUT

{
"shipment_id":"string",
"normalized_data":{},
"status":"completed"
}

FORBIDDEN

* Validation
* Routing
* Inventory analysis
* Recommendations

EXECUTION

Receive Input
→ Normalize
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
    print("SteelSync Data Normalizer is ONLINE")
    print("Waiting for Band messages...")
    print("====================================")

    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())