# NBA Dataset — Technical Spec

## Introduction

This document is the working technical spec for building an NBA dataset that backs a **SQL query generator** — a system that answers natural-language questions about NBA games, players, and teams by running queries against a local relational database rather than calling external APIs on the fly.

It captures our research and design decisions across three areas:

- **Data source evaluation** — comparing the available options (`nba_api`, the Kaggle Basketball SQLite DB, BALLDONTLIE, API-NBA, Sportradar, and others) on coverage, cost, recency, and reliability.
- **API capabilities & limitations** — what the underlying NBA APIs can and can't answer in a single call, their request format, response contracts, and pagination/rate limits, which together justify why we load data into our own SQL store.
- **Design choices** — the chosen architecture (a mostly-free, two-source hybrid: Kaggle for deep history + `nba_api` for backfill and live updates), how we handle live data, and the open questions around schema and relational DB infrastructure.

The goal is a near-comprehensive, near-live, query-ready relational database that lets the generator reliably handle complex, multi-season questions that the raw APIs cannot express directly.

---

## Data Source Options

### Option 1: nba_api

> Wraps the official stats.nba.com endpoints — https://github.com/swar/nba_api

This is the strongest free option and probably your backbone. It's a Python client over the same APIs that power NBA.com, so coverage is enormous: per-player and per-team box scores, advanced stats, play-by-play (PlayByPlayV2), shot-level data with court coordinates (shotchartdetail), game logs across all historical seasons, lineups, hustle stats, and more. Data updates effectively live during games (NBA.com itself runs on it), so a LeBron corner three shows up within seconds.

**Downsides:** it returns JSON, not a database — you'd write an ETL layer to load it into SQL (Postgres/SQLite). It's also unofficial/rate-limited and occasionally breaks when NBA.com changes endpoints. Injuries aren't a clean first-class feed here.

#### Deep-Dive: NBA API Request Format, Capabilities & Limitations

**Questions:** What is the API request format? What can we ask about the NBA games? What are examples of questions we can't directly ask with a single API call? For example, is it possible to query for every NBA player that has scored between 20 and 25 points between the years 2012 and 2015?

##### 1. The Request Format

Under the hood it's just an **HTTP GET to a URL with a query string**:

```
https://stats.nba.com/stats/{endpoint}?Param1=Value1&Param2=Value2&...
```

For the live API, you can even see the actual URL in the response:
`http://nba.cloud/league/00/2026/06/10/scoreboard?Format=json`

The package does three things for you:

- Picks the **endpoint** (the path — e.g. `leaguedashplayerstats`), which determines *what kind of data* you get.
- Turns your **parameters** into the `?key=value&...` query string — these are the *filters*.
- Attaches the **headers** NBA.com requires (`Referer: https://www.nba.com/`, a browser `User-Agent`, etc.). Without these the server rejects or hangs the request — that's the main reason people use the package instead of raw `requests`.

> **Conceptually:** endpoint = the question type, parameters = the filters on it.

##### 2. What You Can Ask — and the Key Limitation

You can ask anything that maps to (a) an existing endpoint and (b) its **predefined parameters**. For player stats (`LeagueDashPlayerStats`), the real filters available include:

```
season, season_type, per_mode (Totals/PerGame/Per36...),
measure_type (Base/Advanced/Defense...), date_from, date_to,
location (home/away), outcome (W/L), starter_bench,
draft_year, draft_pick, college, height, weight, ...
```

Notice what's in that list: **categorical dimensions** — *who, when, where, what type*. You filter by season, team, home/away, draft year, etc.

**What's NOT in the list: arbitrary numeric thresholds on the stats themselves.** There is no `points_min` / `points_max`, no `rebounds_between`. The API returns the *full table* of players for your scope, and you filter the numbers yourself afterward.

##### 3. Worked Example: Players Who Scored 20–25 Points, 2012–2015

**Not possible in a single call** — for two distinct reasons:

1. **No stat-range parameter.** You can't tell the API "only return players with 20 ≤ PTS ≤ 25." That filter has to happen on your side.
2. **`season` is a single value per call.** "2012–2015" spans three seasons (2012-13, 2013-14, 2014-15), so that's three calls minimum.

But it's **easily done in a few calls + a client-side filter**:

```python
for season in ["2012-13", "2013-14", "2014-15"]:
    df = LeagueDashPlayerStats(season=season,
                               per_mode_detailed="PerGame").get_data_frame()
    hits = df[(df.PTS >= 20) & (df.PTS <= 25)]   # ← the filter the API won't do
```

3 API calls, then pandas does the 20–25 filtering. The recurring theme: **the API scopes by category; you do the math/threshold filtering locally.**

###### A Note on Ambiguity

*"Scored between 20 and 25 points"* is ambiguous, and the answer changes the endpoint:

| Interpretation | Approach |
| --- | --- |
| **Per-game average** in those seasons | `LeagueDashPlayerStats` (as above) — filter avg PTS |
| **Season total** points | Same endpoint with `per_mode="Totals"` |
| In **any single game** during that span | Different endpoint — `LeagueGameLog` / `PlayerGameLogs` (one row per game), then filter game-level PTS |

##### Response Reliability & Contracts

| Question | Answer |
| --- | --- |
| Is the *shape* reliable? | **Yes** — always `headers` + `data` rows, in named datasets. |
| Can I know the fields in advance? | **Yes** — read the endpoint's `expected_data` / `_expected_data/*.py`. |
| Is it contractually guaranteed by NBA? | **No** — undocumented upstream; fields can change without notice. |
| How do I stay safe? | Pin to the field names in `expected_data`, prefer the newest endpoint version (V3 over V2), and don't assume a column exists without checking `get_available_data()` or the headers at runtime. |

##### How Much Data Can Be Returned?

There is no clear limit to the data returned, but it is also not paginated.

### Option 2: Kaggle "Basketball" SQLite Database (Wyatt Walsh)

> https://www.kaggle.com/datasets/wyattowalsh/basketball

- **Size:** 2.35 GB
- **Format:** main dataset .SQLite database file
- **Coverage:**
  - 30 teams
  - 4800+ players
  - 65,000+ games (every game since the inaugural 1946-47 NBA season)
  - Team Box Scores for over 95% of all games
  - Play-by-Play game data with 13M+ rows of Play-by-Play data in all!
- **Last Updated:** 2023

This is the one that's already SQL. A ready-made SQLite file with 16 tables covering games, box scores, play-by-play, players, teams, drafts, and standings from 1946–2023, sourced from the same NBA API. Perfect for instantly pointing a SQL generator at, but it's a periodic snapshot — not live. Best used as your historical base, topped up by nba_api for recency.

### Option 3: BALLDONTLIE

> https://www.balldontlie.io/

Clean, well-documented, free tier with a real SDK. Good for games, box scores, season averages, standings. Less granular than nba_api (historically no shot-level/play-by-play on the free tier) but far more pleasant to work with. Good if you want simplicity over depth.

- very limited data for free version
- API Calls to get data

<img width="405" height="841" alt="image" src="https://github.com/user-attachments/assets/03ed3142-bb9b-4d86-9186-f9246f407ad5" />

### Low-Cost Paid Options (best value for live + structured)

#### API-NBA / API-Sports

> https://www.api-basketball.com/ (NBA: https://rapidapi.com/api-sports/api/api-nba)

Free tier (100 req/day), then ~$15–35/mo for 75k–150k requests. ~10+ years of history, live updates roughly every 15 seconds, includes standings, lineups, player/team stats, and a structured games/stats schema. Strong cost-to-coverage ratio if you want a clean REST API without enterprise pricing.

#### Highlightly NBA API

> https://highlightly.net/nba-api/

Free Basic tier (100 req/day) with live scores, standings, lineups, player stats, highlights, and odds. Real-time quarter-by-quarter and game-clock tracking. Good middle option.

### Enterprise Options (deepest + most official, expensive)

#### Sportradar NBA API

> https://sportradar.com/media-tech/data-content/sports-data-api/ (docs: https://developer.sportradar.com/basketball/docs/nba-ig-api-basics)

The official NBA data partner. 36+ feeds, full near-real-time play-by-play, player/team stats, standings, injuries, odds, and editorial. 30-day free trial, but production pricing is B2B (~$500–1,000+/mo per sport). This is the gold standard for completeness and reliability of injury/official data, but overkill unless you're going commercial.

#### SportsDataIO

> https://sportsdata.io/nba-api

Comparable enterprise depth — decades of history, fantasy projections, depth charts, injuries, news, play-by-play. Pricing is sales-gated (~$500–1,000+/mo estimated).

---

## Claude Suggestion

Given you're building a SQL generator and want both maximum coverage and live recency, the optimal setup is a two-source hybrid, mostly free:

- Seed a Postgres/SQLite database from the Kaggle Basketball SQLite DB for instant, query-ready history back to the 1940s.
- Run nba_api on a schedule (and live during games) to append current-season box scores, play-by-play, and shot data into the same schema.

That gives you near-comprehensive, near-live data in a real relational schema at $0, which is exactly what a SQL generator wants. The only gap is clean injury data — if that's a priority, add API-NBA (~$15–35/mo) for an affordable injury/live feed, or Sportradar if you need official, contractual-grade injury and play-by-play data and have the budget.

If you'd like, I can scaffold the ETL: a schema + a Python loader that pulls from nba_api into SQLite/Postgres so your generator has a live-updating target. Just say the word.

---

## Final Plan

### Core Architecture — a Two-Source Hybrid, Free

The end goal is a local relational database (Postgres/SQLite) that a SQL generator queries, rather than hitting live APIs per question. Two data sources feed it:

1. Kaggle "Basketball" SQLite DB (Wyatt Walsh) — the historical backbone. ~2.35 GB, 16 tables, every game since 1946-47, box scores for 95%+ of games, 13M+ play-by-play rows. Already SQL, but a static snapshot ending 2023.
2. nba_api — the recency/live layer. Same source NBA.com runs on, updates within seconds during games. Used to backfill 2023→2026 and then keep the DB current.

## Design Choices

### Why SQL Instead of Direct API Calls (the central design justification)

Two hard limits of the raw APIs drove this decision:

- No pagination → large multi-year requests are unreliable, so you can't safely pull broad historical spans in one shot.
- Constrained query surface → you can't express things like "every player who scored 20–25 pts across 2012–2015" in a single call (no stat-range filters, one season per call).

### How We Tackle Live Data

we want to have a bot make regular generic calls to the NBA API endpoint during live games to update entries in our local SQL tables. We will first start our local SQL table from Kaggle which ranges from about 1946 to 2023. Then we can backfill with data from 2023 to 2026. Finally, we can work on a bot that will know when games are live and continue making live calls to NBA API.

For scaling, we can use paid APIs that update their information quicker and are more reliable than NBA API.

### How We Tackle Unstructured Data for Our SQL DB

we need to fully understand the Kaggle DB and then the associated API-NBA calls that can backfill the Kaggle DB with the most recent information.

### How We Want to Create Our Relational DB Infrastructure

Need to work on this once we have a good idea of what Kaggle returns. Then, we need to map out
what tables we think are appropriate based on Kaggle and actual NBA data. Finally, we need to 
write the design doc and create this Database.

### Rollout Sequence (Live-Data Strategy)

1. Seed the local DB from Kaggle (1946–2023).
2. Backfill 2023→2026 via nba_api.
3. Build a bot that detects when games are live and makes regular calls to the NBA API to update local tables in near-real-time.
4. Scale later with paid APIs (e.g. API-NBA, ~$15–35/mo) for faster, more reliable updates — and for the one real gap, clean injury data, which nba_api doesn't provide first-class.

### Open Work (Not Yet Decided)

- Understand the Kaggle DB schema in full — prerequisite for everything downstream.
- Map the API-NBA / nba_api calls needed to backfill Kaggle with recent data.
- Design the relational DB infrastructure — deferred until the Kaggle schema is well understood.

---

## Open Questions & Review Responses

Issues raised in review (grounded against the real schema in `reports/sqlite_eda.md`), with our current thinking on each.

### Join keys don't join cleanly

The schema isn't as relational as it looks. `game.team_id_home` is `TEXT`, `common_player_info.team_id` is `INTEGER`, `team.id` is `TEXT`, and `play_by_play.player1_team_id` is stored as a float-formatted string (`"1610612747.0"`, EDA line 543) vs. `team.id = "1610612737"`. A generated `JOIN ... ON team_id = id` silently returns nothing. The spec treats this as a clean relational schema; it isn't.

**Our take:**

- Have the agent handle it (cast in the generated SQL).
- Or write a script to cast the table schema — though the approach depends on the SQL DB used.

### No target question set or eval harness

There is no list of the 15–20 questions the generator must answer and no eval/accuracy harness. Without it you can't know whether the schema is sufficient — and you'd have caught the 20–25-points failure on day one.

### Scope: historical analytics or live scores?

These pull in opposite directions. The hard part of "live" is a player-grain ingestion pipeline, but the marquee examples are multi-season historical. Which is v1?

**Our take:**

- Address later — first, only historical data.

### Dedup / idempotency

There are already 56 duplicate `game_id`s (EDA line 71). Backfill + a live bot re-polling the same game will multiply duplicates. What's the upsert key and watermark? (Note `play_by_play` already lags `game` by 3 days within Kaggle itself — EDA line 60 — so "complete after ingest" needs a definition.)

**Our take:**

- Have the agent handle it.
- Maybe try to script and rewrite the data?

### SQLite vs. Postgres — decided how?

Lines 167 and 180 keep both. A live single-writer ingestion bot + concurrent reads on a 2.35 GB-and-growing file is exactly where SQLite's single-writer model bites. This decision gates the bot design and shouldn't be deferred.

### `season_id` encoding

The generator must know `2YYYY` = regular, `4YYYY` = playoffs, `3YYYY` = all-star, `1YYYY` = preseason, plus the `"All-Star"` vs. `"All Star"` label split (EDA lines 36–40, 71). This semantic layer is undocumented.

**Our take:**

- Keep this in mind.

### Coverage cliffs

`other_stats` and `play_by_play` only exist for ~28–30k games (1996+). Any "points in the paint," "fast-break points," or play-by-play question is unanswerable pre-1996. The design should surface these cliffs, not imply uniform 1946–present depth.

**Our take:**

- A disclaimer should be added for the user.

### Licensing / ToS

Redistributing stats.nba.com data and scraping it via a bot may violate NBA's terms. The spec only raises cost (for Sportradar), never legality of the free path.

**Our take:**

- Keep in mind.

---

*updated by Darren Lee*
*Last updated: 6/15/2026*