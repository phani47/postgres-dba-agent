from langchain.agents import create_agent

from app.llm.providers import get_google_llm

from app.tools.postgres_tools import (
    get_database_size,
    get_active_sessions,
    get_long_running_queries,
    get_connection_usage,
    get_blocking_sessions,
)


def create_postgres_agent():

    llm = get_google_llm()

    tools = [
        get_database_size,
        get_active_sessions,
        get_long_running_queries,
        get_connection_usage,
        get_blocking_sessions,
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
You are a PostgreSQL Database Administrator assistant.

Your responsibilities are:

1. Analyze PostgreSQL database health.
2. Use the available PostgreSQL tools whenever database information
   is required.
3. Never invent database metrics.
4. Clearly distinguish observed database information from recommendations.
5. Provide concise DBA-oriented explanations.
6. Do not execute destructive operations.
""",
    )

    return agent