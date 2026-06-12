# NBA Chat Agent — Project Plan

## Overview

Natural-language NBA analytics agent: plain-English questions → SQL → validated query results → summary + visualization.

---

## Phase 1: Foundation

> **Priority:** Get Phase 1 right before writing application code. The schema description (Deliverable 4) is the brain of the agent — if the LLM doesn't understand your tables, nothing downstream works well.

| # | Deliverable | Owner(s) | Due |
|---|-------------|----------|-----|
| 1 | [Development environment](#1-development-environment) | Derek, Darren ✅ | **Sat, Jun 13** |
| 2 | [NBA data source](#2-nba-data-source) | Darren | **Fri, Jun 12** |
| 3 | [Format this doc](#3-format-this-doc) | Darren ✅ | **Fri, Jun 12** |
| 4 | [SQL proof of concept + schema](#4-sql-proof-of-concept--schema) | Derek | **Wed, Jun 17** |

### 1. Development Environment

**Goal:** Align on a shared coding + AI development environment.

- **Decision:** VS Code + Claude Code
- **Requirement:** Everyone uses the same setup

### 2. NBA Data Source

**Goal:** Find a usable NBA database for the project.

- [ ] Find an up-to-date, easy-access NBA DB with rich historical data
- [ ] Identify a less up-to-date fallback suitable for demo purposes
- [ ] Investigate live NBA data access options
- [ ] Evaluate the [NBA API](https://github.com/swar/nba_api) package
- [ ] Try datasets on [Kaggle](https://www.kaggle.com/datasets?search=nba)

### 3. Format This Doc ✅

**Goal:** Publish a clear, shareable project plan in the repository.

### 4. SQL Proof of Concept + Schema

**Goal:** Prove the data layer works and document it for the agent.

- [ ] Run a successful SQL query against the chosen NBA database
- [ ] Write a schema description for the agent (table names, columns, relationships, example values)

---

## Phase 2: Core Agent Pipeline

> **Focus:** Most iteration happens here. Test against questions like *"Who led the league in assists in 2018?"* and *"Which team had the best home record in the 2022 playoffs?"* — if those return correct results, the pipeline is solid.

| # | Deliverable | Description |
|---|-------------|-------------|
| 5 | SQL generation | Python function: plain-English question → SQL query (Claude API + schema as system prompt) |
| 6 | Query validation & execution | Validate SQL with `sqlglot`, execute read-only against SQLite, enforce row limit, return a DataFrame |
| 7 | Result analysis | Second Claude call: query results → 2–3 sentence plain-English summary |

### 5. SQL Generation Function

```python
def generate_sql(question: str, schema: str) -> str:
    """Takes a plain English question; returns a SQL query."""
```

- Uses Claude API
- Schema description passed as system prompt

### 6. Query Validation & Execution

- Validate generated SQL with **sqlglot**
- Execute read-only against the SQLite database
- Enforce a row limit
- Return results as a **pandas DataFrame**

### 7. Result Analysis Function

- Second Claude API call
- Input: query results
- Output: 2–3 sentence plain-English summary of what the data shows

---

## Phase 3: Backend

> **Note:** Lightweight once the pipeline works — FastAPI is roughly ~20 lines of code.

| # | Deliverable | Description |
|---|-------------|-------------|
| 8 | Wire full pipeline | Connect Deliverables 5–7 into one function: question in → SQL, results, summary out. Test with 5 NBA questions. |
| 9 | FastAPI endpoint | `POST /query` — accepts a plain-English question; returns SQL, result rows, column names, and summary as JSON |

### 8. Wire the Full Pipeline

**Single function signature (conceptual):**

```python
def ask(question: str) -> dict:
    # Returns: { "sql", "columns", "rows", "summary" }
```

**Test questions (minimum 5):**

1. Who led the league in assists in 2018?
2. Which team had the best home record in the 2022 playoffs?
3. *(Add 3 more representative questions)*

### 9. FastAPI Endpoint

```
POST /query
```

**Request body:**

```json
{ "question": "Who led the league in assists in 2018?" }
```

**Response:**

```json
{
  "sql": "SELECT ...",
  "columns": ["player", "assists"],
  "rows": [["...", 732]],
  "summary": "..."
}
```

---

## Phase 4: Frontend

| # | Deliverable | Description |
|---|-------------|-------------|
| 10 | UI (Claude artifact) | Text input, generated SQL display, auto-selected Recharts chart, data table, summary paragraph |

### 10. Frontend UI

Claude artifact with:

- [ ] Text input for natural-language questions
- [ ] Generated SQL display
- [ ] **Recharts** visualization (auto-select chart type from result shape)
- [ ] Data table
- [ ] Summary paragraph

---

## Target Demos (Roadmap)

| Stage | Scope |
|-------|--------|
| **Demo 1** | Single local chat — one question at a time with the NBA chat agent (possibly limited DB) |
| **Demo 2** | Follow-up questions with conversation context within a single session |
| **Demo 3** | Expand DB to live or very recent data |
| **Demo 4** | Multiple concurrent live chat sessions |

---

## Sequencing Summary

```
Phase 1 (Foundation)  →  Phase 2 (Pipeline)  →  Phase 3 (API)  →  Phase 4 (UI)
     ↑ critical              ↑ most iteration       ↑ ~20 LOC        ↑ demo-ready
  schema first
```

1. **Phase 1** — Schema and data source must be solid before any agent code.
2. **Phase 2** — Core pipeline; validate with real NBA questions.
3. **Phase 3** — Thin wrapper once pipeline is reliable.
4. **Phase 4** — Polish for demos and stakeholders.

---

## Team

| Person | Focus areas |
|--------|-------------|
| **Darren** | Data source, doc, dev environment |
| **Derek** | Schema, SQL POC, pipeline implementation |

---

*Last updated: June 2026*
