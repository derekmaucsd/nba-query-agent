- coding + AI development environment
- (what do we want to use? we should use the same env)

- find an up-to-date, easy access, lots of data NBA DB to use
- maybe settle for something less up-to-date as a demo
- is there live NBA data we can access?
- investigate NBA API Package

- make a successful SQL Query to the NBA Database

- Write a schema description for the agent

- Core agent pipeline

- SQL generation function
- A Python function that takes a plain English question and returns a SQL query. Uses Claude API with the schema description as the system prompt.

- Query validation and execution
- Validate the generated SQL with sqlglot, execute it read-only against the SQLite db, enforce a row limit, and return the results as a dataframe.

- Result analysis function
- A second Claude API call that takes the query results and writes a 2–3 sentence plain English summary of what the data shows.

- BE Layer

- Wire the full pipeline together
- Connect deliverables 3–5 into a single function: question in, SQL out, results out, summary out. Test it against 5 NBA questions.

- FastAPI endpoint
- A single POST /query endpoint that accepts a plain English question and returns the SQL query, result rows, column names, and summary as JSON.

- Frontend UI
- A Claude artifact with a text input, generated SQL display, a Recharts visualization that picks the right chart type automatically, a data table, and the summary paragraph.

A few notes on the sequencing:
Phase 1 is the most important to get right before writing any code. The schema description you write in deliverable 2 is basically the brain of the agent — if the LLM doesn't understand your tables, nothing downstream works well. Spend real time on it.
Phase 2 is the core and where most of the iteration will happen. I'd run deliverable 6's test against questions like "who led the league in assists in 2018" and "which team had the best home record in 2022 playoffs" — if those come back with correct results, the pipeline is solid.
Phase 3 is lightweight — FastAPI is maybe 20 lines of code once the pipeline works.
Phase 4 is where it becomes something you can actually show people.


Target Demos:

- single local chat, single question with NBA chat agent with possibly limited DB functionality
- support follow up questions that uses context within that conversation
- expand DB to live/very recent data
- can handle multiple live chats

