from app.tools.postgres_tools import (
    get_database_size,
    get_active_sessions,
    get_long_running_queries,
)


print("Available tools:")

for tool in [
    get_database_size,
    get_active_sessions,
    get_long_running_queries,
]:
    print(f"- {tool.name}: {tool.description}")


print("\nTesting tools:")

print(get_database_size.invoke({}))
print(get_active_sessions.invoke({}))
print(get_long_running_queries.invoke({}))