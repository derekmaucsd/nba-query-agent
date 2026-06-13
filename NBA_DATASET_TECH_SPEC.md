Introduction:




Options:
nba_api (wraps the official stats.nba.com endpoints) — https://github.com/swar/nba_api

This is the strongest free option and probably your backbone. It's a Python client over the 
same APIs that power NBA.com, so coverage is enormous: per-player and per-team box scores, 
advanced stats, play-by-play (PlayByPlayV2), shot-level data with court coordinates (shotchartdetail), 
game logs across all historical seasons, lineups, hustle stats, and more. Data updates effectively live 
during games (NBA.com itself runs on it), so a LeBron corner three shows up within seconds. Downsides: 
it returns JSON, not a database — you'd write an ETL layer to load it into SQL (Postgres/SQLite). It's 
also unofficial/rate-limited and occasionally breaks when NBA.com changes endpoints. Injuries aren't a 
clean first-class feed here.

questions

What is the API request format? What can we ask about the NBA games? What are examples of questions we can't 
directly ask with a single API call? For example, is it possible to query for every NBA player that has scored 
between 20 and 25 points between the years 2012 and 2015?
# NBA API: Request Format, Capabilities & Limitations

## 1. The Request Format

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

## 2. What You Can Ask — and the Key Limitation

You can ask anything that maps to (a) an existing endpoint and (b) its **predefined parameters**. For player stats (`LeagueDashPlayerStats`), the real filters available include:

```
season, season_type, per_mode (Totals/PerGame/Per36...),
measure_type (Base/Advanced/Defense...), date_from, date_to,
location (home/away), outcome (W/L), starter_bench,
draft_year, draft_pick, college, height, weight, ...
```

Notice what's in that list: **categorical dimensions** — *who, when, where, what type*. You filter by season, team, home/away, draft year, etc.

**What's NOT in the list: arbitrary numeric thresholds on the stats themselves.** There is no `points_min` / `points_max`, no `rebounds_between`. The API returns the *full table* of players for your scope, and you filter the numbers yourself afterward.

## 3. Worked Example: Players Who Scored 20–25 Points, 2012–2015

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

### A note on ambiguity

*"Scored between 20 and 25 points"* is ambiguous, and the answer changes the endpoint:

| Interpretation | Approach |
| --- | --- |
| **Per-game average** in those seasons | `LeagueDashPlayerStats` (as above) — filter avg PTS |
| **Season total** points | Same endpoint with `per_mode="Totals"` |
| In **any single game** during that span | Different endpoint — `LeagueGameLog` / `PlayerGameLogs` (one row per game), then filter game-level PTS |




| Question | Answer |
| --- | --- |
| Is the *shape* reliable? | **Yes** — always `headers` + `data` rows, in named datasets. |
| Can I know the fields in advance? | **Yes** — read the endpoint's `expected_data` / `_expected_data/*.py`. |
| Is it contractually guaranteed by NBA? | **No** — undocumented upstream; fields can change without notice. |
| How do I stay safe? | Pin to the field names in `expected_data`, prefer the newest endpoint version (V3 over V2), and don't assume a column exists without checking `get_available_data()` or the headers at runtime. |


Up to how much data can be returned?
There is no clear limit to the data returned, but it is also not paginated.



Kaggle "Basketball" SQLite database (Wyatt Walsh) — https://www.kaggle.com/datasets/wyattowalsh/basketball
2.35 GB
main dataset .SQLite database file

30 teams
4800+ players
65,000+ games (every game since the inaugural 1946-47 NBA season)
Box Scores for over 95% of all games
Play-by-Play game data with 13M+ rows of Play-by-Play data in all!
Last Updated: 2023

This is the one that's already SQL. A ready-made SQLite file with ~30 tables covering games, box scores, 
play-by-play, players, teams, drafts, and standings from 1946–present, sourced from the same NBA API. Perfect 
for instantly pointing a SQL generator at, but it's a periodic snapshot — not live. Best used as your historical 
base, topped up by nba_api for recency.


BALLDONTLIE — https://www.balldontlie.io/

Clean, well-documented, free tier with a real SDK. Good for games, box scores, season averages, standings. 
Less granular than nba_api (historically no shot-level/play-by-play on the free tier) but far more pleasant to 
work with. Good if you want simplicity over depth.

very limited data for free version

API Calls to get data

<img width="405" height="841" alt="image" src="https://github.com/user-attachments/assets/03ed3142-bb9b-4d86-9186-f9246f407ad5" />


Low-cost paid (best value for live + structured)

API-NBA / API-Sports — https://www.api-basketball.com/ (NBA: https://rapidapi.com/api-sports/api/api-nba)
Free tier (100 req/day), then ~$15–35/mo for 75k–150k requests. ~10+ years of history, live updates roughly every 15 seconds, includes standings, lineups, player/team stats, and a structured games/stats schema. Strong cost-to-coverage ratio if you want a clean REST API without enterprise pricing.


Highlightly NBA API — https://highlightly.net/nba-api/
Free Basic tier (100 req/day) with live scores, standings, lineups, player stats, highlights, and odds. Real-time quarter-by-quarter and game-clock tracking. Good middle option.



Enterprise (deepest + most official, expensive)
Sportradar NBA API — https://sportradar.com/media-tech/data-content/sports-data-api/ (docs: https://developer.sportradar.com/basketball/docs/nba-ig-api-basics)

The official NBA data partner. 36+ feeds, full near-real-time play-by-play, player/team stats, standings, injuries, odds, and editorial. 30-day free trial, but production pricing is B2B (~$500–1,000+/mo per sport). This is the gold standard for completeness and reliability of injury/official data, but overkill unless you're going commercial.
SportsDataIO — https://sportsdata.io/nba-api




Comparable enterprise depth — decades of history, fantasy projections, depth charts, injuries, news, play-by-play. Pricing is sales-gated (~$500–1,000+/mo estimated).



Claude Suggestion:
Given you're building a SQL generator and want both maximum coverage and live recency, the optimal setup is a two-source hybrid, mostly free:
Seed a Postgres/SQLite database from the Kaggle Basketball SQLite DB for instant, query-ready history back to the 1940s.

Run nba_api on a schedule (and live during games) to append current-season box scores, play-by-play, and shot data into the same schema.
That gives you near-comprehensive, near-live data in a real relational schema at $0, which is exactly what a SQL generator wants. The only gap is clean injury data — if that's a priority, add API-NBA (~$15–35/mo) for an affordable injury/live feed, or Sportradar if you need official, contractual-grade injury and play-by-play data and have the budget.
If you'd like, I can scaffold the ETL: a schema + a Python loader that pulls from nba_api into SQLite/Postgres so your generator has a live-updating target. Just say the word.



Final Plan:

Core architecture — a two-source hybrid, free

The end goal is a local relational database (Postgres/SQLite) that a SQL generator queries, rather than hitting live APIs per question. Two data sources feed it:

1. Kaggle "Basketball" SQLite DB (Wyatt Walsh) — the historical backbone. ~2.35 GB, ~30 tables, every game since 1946-47, box scores for 95%+ of games, 13M+ play-by-play rows. Already SQL, but a static snapshot ending 2023.
2. nba_api — the recency/live layer. Same source NBA.com runs on, updates within seconds during games. Used to backfill 2023→2026 and then keep the DB current.
 

Design Choices:

Why SQL instead of direct API calls (the central design justification)

Two hard limits of the raw APIs drove this decision:
- No pagination → large multi-year requests are unreliable, so you can't safely pull broad historical spans in one shot.
- Constrained query surface → you can't express things like "every player who scored 20–25 pts across 2012–2015" in a single call (no stat-range filters, one season per call).


how we tackle live data
we want to have a bot make regular generic calls to the NBA API endpoint during live games to update entries in our local SQL tables. We will first start our local SQL table
from Kaggle which ranges from about 1950 to 2023. Then we can backfill with data from 2023 to 2026. Finally, we can work on a bot that will know when games are live
and continue making live calls to NBA API.
For scaling, we can use paid APIs that update their information quicker and are more reliable than NBA API.



how we tackle unstructured data for our SQL DB
we need to fully understand the Kaggle DB and then the associated API-NBA calls that can backfill the Kaggle DB with the most recent information. 


how we want to create our relational DB infrastructure
Need to work on this once we have a good idea of what Kaggle returns





Rollout sequence (live-data strategy):

1. Seed the local DB from Kaggle (~1950–2023).
2. Backfill 2023→2026 via nba_api.
3. Build a bot that detects when games are live and makes regular calls to the NBA API to update local tables in near-real-time.
4. Scale later with paid APIs (e.g. API-NBA, ~$15–35/mo) for faster, more reliable updates — and for the one real gap, clean injury data, which nba_api doesn't provide first-class.




Open work (not yet decided)

- Understand the Kaggle DB schema in full — prerequisite for everything downstream.
- Map the API-NBA / nba_api calls needed to backfill Kaggle with recent data.
- Design the relational DB infrastructure — deferred until the Kaggle schema is well understood.



updated by Darren Lee
Last updated: 6/12/2026



