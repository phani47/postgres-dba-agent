from app.agent.agent import create_postgres_agent


agent = create_postgres_agent()


response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Give me a quick PostgreSQL health check.",
            }
        ]
    }
)

print(response["messages"][-1].content)