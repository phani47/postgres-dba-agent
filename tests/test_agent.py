from app.llm.providers import get_google_llm

from app.tools.postgres_tools import (
    get_database_size,
    get_active_sessions,
    get_long_running_queries,
)


llm = get_google_llm()

tools = [
    get_database_size,
    get_active_sessions,
    get_long_running_queries,
]

llm_with_tools = llm.bind_tools(tools)

tool_map = {
    tool.name: tool
    for tool in tools
}


messages = [
    (
        "human",
        "Check the PostgreSQL database and tell me the database size."
    )
]


# --------------------------------------------------
# 1. Ask Gemini
# --------------------------------------------------

response = llm_with_tools.invoke(messages)

print("\n--- Gemini Initial Response ---")
print(response)


# Add Gemini's response to the conversation
messages.append(response)


# --------------------------------------------------
# 2. Execute requested tools
# --------------------------------------------------

for tool_call in response.tool_calls:

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print("\n--- Executing Tool ---")
    print("Tool:", tool_name)
    print("Arguments:", tool_args)

    tool_result = tool_map[tool_name].invoke(tool_args)

    print("Result:", tool_result)

    # Add tool result back to conversation
    messages.append(
        {
            "role": "tool",
            "content": tool_result,
            "tool_call_id": tool_call["id"],
        }
    )


# --------------------------------------------------
# 3. Send result back to Gemini
# --------------------------------------------------

final_response = llm_with_tools.invoke(messages)

print("\n--- Final Gemini Response ---")
print(final_response.content)