def build_final_sql_prompt(
    user_question: str,
    schema_summary: str,
    evidence: str = "",
    previous_attempts: str = "",
) -> str:
    evidence_block = f"""
Validated subquery evidence:
{evidence}
""" if evidence else ""
    attempts_block = f"""
Previous failed attempts:
{previous_attempts}
""" if previous_attempts else ""

    return f"""
You are writing a SQLite query for the local NBA database.
Return only SQL, no markdown, no explanation.
Only return a single read-only SELECT statement or WITH query.
If the database does not contain the data needed to answer the question, return a
SELECT statement with one text column named answer explaining the limitation.

Database schema:
{schema_summary}

{evidence_block}
{attempts_block}

User question:
{user_question}
"""


def build_subquery_plan_prompt(
    user_question: str,
    schema_summary: str,
    max_subqueries: int,
    previous_evidence: str = "",
    validation_feedback: str = "",
) -> str:
    previous_evidence_block = f"""
Previous subquery evidence:
{previous_evidence}
""" if previous_evidence else ""
    validation_feedback_block = f"""
Validation feedback to address:
{validation_feedback}
""" if validation_feedback else ""

    return f"""
You are helping plan a reliable SQLite answer for a local NBA database.

Break the user's question into up to {max_subqueries} small read-only diagnostic
subqueries. These subqueries should verify:
- which table(s) contain the needed facts,
- the relevant column names and grains,
- sample values or aggregate counts,
- whether the database can actually answer the question.

Return only valid JSON in this shape:
{{
  "subqueries": [
    {{
      "name": "short_snake_case_name",
      "purpose": "what this validates",
      "sql": "single read-only SQLite SELECT/WITH query",
      "expected_signal": "what a useful result should show"
    }}
  ]
}}

Rules:
- Use only tables and columns from the schema below.
- Each SQL value must be one statement and must start with SELECT or WITH.
- Prefer COUNT, GROUP BY, DISTINCT, MIN/MAX, and small LIMIT samples.
- Include LIMIT on non-aggregate sample queries.
- Do not write INSERT, UPDATE, DELETE, CREATE, DROP, PRAGMA, or ATTACH.

Database schema:
{schema_summary}

{previous_evidence_block}
{validation_feedback_block}

User question:
{user_question}
"""


def build_evidence_validation_prompt(
    user_question: str,
    schema_summary: str,
    evidence: str,
) -> str:
    return f"""
You are validating whether executed SQL subqueries provide enough evidence to
answer a user's NBA database question reliably.

Return only valid JSON in this shape:
{{
  "is_sufficient": true,
  "can_answer": true,
  "reason": "short explanation",
  "missing_checks": ["additional checks needed, if any"]
}}

Set "is_sufficient" to true when the evidence is enough either to answer the
question or to confidently say the database lacks the required data.
Set "can_answer" to false if the schema/evidence shows the requested facts are
not available at the needed grain.

Database schema:
{schema_summary}

Executed subquery evidence:
{evidence}

User question:
{user_question}
"""
