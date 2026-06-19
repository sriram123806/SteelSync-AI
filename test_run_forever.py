# test_run_forever.py

import os
import asyncio

from dotenv import load_dotenv
from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver


async def main():
    load_dotenv()

    agent_id, api_key = load_agent_config("erp_validator")

    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        base_url="https://api.aimlapi.com/v1",
        api_key=os.getenv("AIMLAPI_API_KEY"),
    )

    adapter = LangGraphAdapter(
        llm=llm,
        checkpointer=InMemorySaver(),
        custom_section="You are ERP Validator. Reply to every message."
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    print("ERP ONLINE")

    await agent.run_forever()


if __name__ == "__main__":
    asyncio.run(main())