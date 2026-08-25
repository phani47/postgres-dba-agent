from app.tools.postgres_tools import (
    get_database_size,
    get_active_sessions,
    get_long_running_queries,
)


print("Database Size:")
print(get_database_size())

print("\nActive Sessions:")
print(get_active_sessions())

print("\nLong Running Queries:")
print(get_long_running_queries())