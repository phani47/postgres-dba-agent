# 🤖 PostgreSQL DBA Agent

An AI-powered PostgreSQL DBA Assistant that combines **PostgreSQL, Python, LLMs, FastAPI, Streamlit, and Guardrails** to help DBAs monitor, diagnose, and understand PostgreSQL environments using natural language.

The project is being developed as a practical **AI-powered DBA Copilot**, evolving from basic monitoring tools toward intelligent diagnosis, recommendations, and controlled automation.

---

## 🛠️ Technology Stack

| Technology        | Purpose                                      |
| ----------------- | -------------------------------------------- |
| **Python**        | Core application and DBA automation          |
| **PostgreSQL**    | Database platform                            |
| **Gemini / LLM**  | Reasoning and natural-language understanding |
| **LangChain**     | Agent and tool orchestration                 |
| **FastAPI**       | Backend REST API layer                       |
| **Streamlit**     | Interactive DBA dashboard                    |
| **Guardrails**    | Input/output validation and AI safety        |
| **psycopg**       | PostgreSQL connectivity                      |
| **python-dotenv** | Environment configuration                    |
| **Git / GitHub**  | Version control                              |

---

# 🏗️ High-Level Architecture

```text
                         ┌─────────────────────────┐
                         │        DBA / User       │
                         └────────────┬────────────┘
                                      │
                         Natural Language Request
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
           ┌─────────────────┐                 ┌─────────────────┐
           │    Streamlit    │                 │     FastAPI     │
           │   DBA Dashboard │                 │   REST Backend  │
           └────────┬────────┘                 └────────┬────────┘
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │      Guardrails     │
                           │                     │
                           │ Input Validation    │
                           │ Output Validation   │
                           │ Tool Safety         │
                           │ SQL Safety          │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │     LLM / Agent     │
                           │                     │
                           │ Gemini / LangChain  │
                           └──────────┬──────────┘
                                      │
                              Tool Selection
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
          Database Size          Connections          Long Queries
               Tool                  Tool                  Tool
                 │                    │                    │
                 └────────────────────┼────────────────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │     PostgreSQL      │
                           └─────────────────────┘
```

---

# 🖥️ Application Layers

## 1. Streamlit — DBA Dashboard

Streamlit provides the interactive UI for DBAs.

Planned dashboard capabilities include:

* Database health overview
* Database size
* Connection utilization
* Long-running queries
* Blocking sessions
* Lock monitoring
* Autovacuum status
* Dead tuples
* WAL usage
* Replication status
* Tablespace/storage usage
* AI-generated recommendations

Example:

```text
┌──────────────────────────────────────────────────────┐
│              PostgreSQL DBA Copilot                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│ Database Health       🟢 Healthy                     │
│ Database Size         125 GB                         │
│ Connections           42 / 200                       │
│ Long Queries          3                              │
│ Blocking Sessions     1                              │
│ WAL Usage             Normal                         │
│                                                      │
├──────────────────────────────────────────────────────┤
│ Ask your DBA Agent                                   │
│                                                      │
│ > Why is my database slow?                           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

# ⚡ 2. FastAPI — Backend API

FastAPI acts as the backend service between the UI, agent, and PostgreSQL environment.

Example API endpoints:

```text
GET  /health
GET  /database/size
GET  /database/connections
GET  /database/queries
GET  /database/locks
GET  /database/vacuum
GET  /database/wal
POST /agent/query
```

Example workflow:

```text
Streamlit
    │
    │ HTTP Request
    ▼
FastAPI
    │
    ▼
Guardrails
    │
    ▼
Agent
    │
    ▼
PostgreSQL Tools
    │
    ▼
PostgreSQL
```

FastAPI also provides a clean foundation for eventually integrating the DBA agent with:

* Web applications
* Monitoring platforms
* Chat applications
* Automation pipelines
* External enterprise systems

---

# 🛡️ 3. Guardrails — AI Safety Layer

Guardrails will provide an additional safety layer around the DBA agent.

This is particularly important because a database agent can potentially execute sensitive operations.

### Input Validation

Validate user requests before they reach the agent.

```text
User Request
     │
     ▼
Input Validation
     │
     ├── Valid → Agent
     │
     └── Invalid → Reject
```

### SQL Safety

The system should distinguish between:

```text
READ OPERATIONS
    │
    ├── SELECT
    ├── EXPLAIN
    └── Monitoring Queries

WRITE / DESTRUCTIVE OPERATIONS
    │
    ├── DELETE
    ├── DROP
    ├── TRUNCATE
    ├── ALTER
    └── Terminate Session
```

Read-only monitoring operations can be automatically executed.

Potentially destructive operations should require explicit approval.

---

# 🧠 Agent Workflow

The target workflow is:

```text
User Question
      │
      ▼
Input Guardrails
      │
      ▼
LLM Agent
      │
      ▼
Determine Required DBA Tools
      │
      ▼
Execute Monitoring Query
      │
      ▼
Analyze Result
      │
      ▼
Generate DBA Explanation
      │
      ▼
Output Guardrails
      │
      ▼
User / Dashboard
```

For example:

```text
User:
Why is my PostgreSQL database slow?
```

The agent could investigate:

```text
1. Active connections
        ↓
2. Long-running queries
        ↓
3. Blocking sessions
        ↓
4. Locks
        ↓
5. pg_stat_statements
        ↓
6. CPU / Memory
        ↓
7. I/O
        ↓
8. WAL
        ↓
9. Autovacuum
        ↓
10. Table statistics
```

The agent then produces a diagnosis such as:

```text
Root Cause:
A long-running transaction is preventing vacuum cleanup.

Evidence:
• PID: 28451
• Transaction age: 3 hours
• Dead tuples: 12.4M
• Autovacuum is unable to clean the affected rows.

Recommendation:
Investigate the transaction before terminating the session.
```

---

# 🗺️ Updated Roadmap

## Phase 1 — PostgreSQL DBA Tools

* [x] PostgreSQL connectivity
* [x] Database size monitoring
* [x] Basic DBA monitoring
* [x] Python-based monitoring tools

## Phase 2 — AI Agent

* [x] Gemini integration
* [x] Tool calling
* [x] Natural-language DBA questions
* [x] LangChain integration
* [ ] Multi-tool reasoning

## Phase 3 — API & Dashboard

* [ ] FastAPI backend
* [ ] REST APIs
* [ ] Streamlit dashboard
* [ ] Real-time PostgreSQL metrics
* [ ] Agent chat interface

## Phase 4 — Safety & Guardrails

* [ ] Input validation
* [ ] SQL validation
* [ ] Read-only execution mode
* [ ] Tool allowlist
* [ ] Risk classification
* [ ] Human approval workflow
* [ ] Output validation
* [ ] Audit logging

## Phase 5 — DBA Intelligence

* [ ] Query performance analysis
* [ ] Lock diagnosis
* [ ] Autovacuum recommendations
* [ ] Index recommendations
* [ ] Replication analysis
* [ ] WAL analysis
* [ ] Anomaly detection
* [ ] Capacity prediction

## Phase 6 — Autonomous DBA Copilot

```text
Observe
   ↓
Understand
   ↓
Investigate
   ↓
Diagnose
   ↓
Recommend
   ↓
Ask for Approval
   ↓
Execute
   ↓
Verify
   ↓
Report
```

The final objective is to build a **safe, explainable, and production-oriented AI PostgreSQL DBA Copilot**.

---

# 🎯 Project Vision

The project combines traditional DBA expertise with modern AI technologies:

```text
                 PostgreSQL DBA Expertise
                           +
                        Python
                           +
                     PostgreSQL
                           +
                         LLM
                           +
                    Agentic AI
                           +
                       FastAPI
                           +
                      Streamlit
                           +
                      Guardrails
                           │
                           ▼
              ┌────────────────────────┐
              │  AI PostgreSQL DBA     │
              │       Copilot          │
              └────────────────────────┘
```

The long-term goal is not simply to build a chatbot that answers PostgreSQL questions.

The goal is to build an **agent capable of observing a PostgreSQL environment, investigating problems, reasoning across multiple database signals, explaining root causes, recommending actions, and safely executing approved DBA operations.**

---

## 🚧 Project Status

**Status: 🚀 Active Development**

Current focus:

**PostgreSQL DBA Tools → Agent → FastAPI → Streamlit → Guardrails → Intelligent DBA Copilot**
