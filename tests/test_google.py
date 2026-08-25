from app.llm.providers import get_google_llm


llm = get_google_llm()

response = llm.invoke(
    "You are a PostgreSQL DBA assistant. Explain what VACUUM does in PostgreSQL."
)

print(response.content)