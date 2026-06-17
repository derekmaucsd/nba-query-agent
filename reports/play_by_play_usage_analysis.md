# Play-By-Play Table Usage Analysis

Date: 2026-06-16

## Summary

The `play_by_play` table is the most detailed table in the SQLite dataset. It contains event-level NBA game data from the 1996-97 season through June 9, 2023. It can unlock player-level questions that are not directly answerable from the team-level `game` table, but it should not be used by the LLM as raw ad hoc SQL for complex player stat questions.

The right approach is to use `play_by_play` as a source table for deterministic derived tables, especially:

- `player_game_stats`
- `player_season_stats`
- `player_career_stats`

Once those tables exist, the agent can answer player scoring, blocks, steals, assists, rebounds, and turnover questions with normal SQL.

## Basic Shape

`play_by_play` has 13,592,899 rows across 29,818 games.

Coverage from joined game metadata:

- Minimum game date: 1996-11-01
- Maximum game date: 2023-06-09
- Regular season games: 27,391
- Playoff games: 1,757
- Preseason games: 650
- All-Star games: 20, with duplicate-label caveats

Important columns:

- `game_id`: NBA game ID.
- `eventnum`: event number within the game.
- `eventmsgtype`: high-level event type.
- `eventmsgactiontype`: subtype/action code.
- `period`: quarter or overtime period.
- `pctimestring`: game clock.
- `homedescription`, `visitordescription`, `neutraldescription`: text descriptions.
- `score`: score after the event, formatted as `away - home`.
- `scoremargin`: margin after the event from the home team's perspective, with `TIE` for ties.
- `player1_*`, `player2_*`, `player3_*`: player/team slots whose meanings depend on event type.

The table currently has no SQLite indexes.

## Event Type Map

Observed `eventmsgtype` counts:

| eventmsgtype | likely meaning | rows | notes |
| ---: | --- | ---: | --- |
| 1 | Made field goal | 2,242,357 | `player1` is scorer, `player2` is usually assister. |
| 2 | Missed field goal | 2,699,376 | `player1` is shooter, `player3` is blocker when blocked. |
| 3 | Free throw | 1,442,567 | `player1` is shooter; made free throws have `score`. |
| 4 | Rebound | 3,049,623 | `player1` is rebounder for player rebounds; team rebounds use team ID in `player1_id`. |
| 5 | Turnover | 868,202 | `player1` is turnover player/team; `player2` is stealer when present. |
| 6 | Foul | 1,305,746 | `player1` is usually fouler; `player2` may be drawn-by player. |
| 7 | Violation | 53,184 | player/team violation events. |
| 8 | Substitution | 1,226,332 | `player1` exits, `player2` enters. |
| 9 | Timeout | 380,586 | team timeout/official timeout. |
| 10 | Jump ball | 52,099 | `player1` and `player2` jump; `player3` receives tip. |
| 11 | Ejection | 1,984 | player/coach ejections. |
| 12 | Start period | 121,226 | neutral clock event. |
| 13 | End period | 121,424 | neutral clock event, often has score. |
| 18 | Instant replay | 28,193 | neutral replay event, sometimes has score. |

## Player Slot Semantics

The three player slots are useful, but only if interpreted by event type.

Common patterns:

- Made field goal (`eventmsgtype = 1`):
  - `player1`: scorer
  - `player2`: assister, if assisted
  - `player3`: generally unused

- Missed field goal (`eventmsgtype = 2`):
  - `player1`: shooter
  - `player3`: blocker, if blocked

- Free throw (`eventmsgtype = 3`):
  - `player1`: free throw shooter
  - made free throws have non-null `score`
  - missed free throws generally have null `score`

- Rebound (`eventmsgtype = 4`):
  - `player1`: rebounder for player rebounds
  - team rebounds use a team ID in `player1_id`, with `player1_name` null

- Turnover (`eventmsgtype = 5`):
  - `player1`: player or team committing turnover
  - `player2`: player credited with steal, if present

- Foul (`eventmsgtype = 6`):
  - `player1`: player committing foul
  - `player2`: often player who drew the foul, but this is less clean than scoring/rebound/steal/block events

- Substitution (`eventmsgtype = 8`):
  - `player1`: player leaving game
  - `player2`: player entering game

- Jump ball (`eventmsgtype = 10`):
  - `player1`, `player2`: jump ball participants
  - `player3`: player receiving tip

## Score Field

The `score` field is formatted as:

```text
away_score - home_score
```

Example from game `0029600012`:

- Home made shot by Shaquille O'Neal: `score = '0 - 2'`
- Away made shot by Wesley Person: `score = '4 - 4'`

This matters because point values can be derived from score deltas:

- If `homedescription` is non-null, use the change in `home_score`.
- If `visitordescription` is non-null, use the change in `away_score`.
- Normal scoring deltas should be 1, 2, or 3.

This is more robust than parsing text such as `(23 PTS)` from descriptions, because that text is the player's running total at that point in the game, not the event's point value.

## What Can Be Derived Reliably

These are good candidates for deterministic extraction from `play_by_play`:

- Player points from made field goals and made free throws.
- Field goal attempts from `eventmsgtype IN (1, 2)`.
- Field goals made from `eventmsgtype = 1`.
- Three-point makes/attempts, using score delta or `3PT` action/description checks.
- Free throw attempts from `eventmsgtype = 3`.
- Free throws made from free throw rows with a positive score delta.
- Assists from made field goals with `player2_id <> '0'`.
- Rebounds from `eventmsgtype = 4`, excluding team rebounds.
- Blocks from missed field goals where `player3_id <> '0'`.
- Turnovers from `eventmsgtype = 5`, excluding team turnovers when needed.
- Steals from turnovers where `player2_id <> '0'`.
- Substitution events and rough lineup reconstruction.

These are possible but need more care:

- Offensive vs defensive rebounds, because the cleanest signal is often embedded in description text such as `(Off:0 Def:1)`.
- Personal fouls drawn/committed, because foul subtypes and `player2` meanings are less consistent.
- Minutes played, because this requires lineup reconstruction from substitutions and starters.
- Plus/minus, because it requires reliable on-court lineup state.

## What Should Not Be Done By Generated Ad Hoc SQL

The LLM should not be asked to invent complex one-off SQL directly over `play_by_play` for player stat questions. Reasons:

- The table has 13.6M rows.
- There are no indexes on `play_by_play`.
- Player slot semantics vary by event type.
- Some games have duplicate event rows.
- Scoring derivation requires ordered score deltas.
- Team rebounds and team turnovers can look like player rows unless filtered.
- Full-history claims are impossible because play-by-play starts in 1996-97, while the `game` table starts in 1946-47.

The better pattern is:

1. Use deterministic ETL to derive player stats from `play_by_play`.
2. Validate derived totals against known team/game totals where possible.
3. Let the LLM query the derived tables.

## Duplicate Rows

There are duplicate `game_id/eventnum` rows:

- Total rows: 13,592,899
- Distinct `game_id:eventnum` pairs: 13,585,539
- Duplicate event-number rows: 7,360

Duplicates are concentrated in All-Star games. For example, game `0031000001` has each event duplicated because the `game` table includes both `All Star` and `All-Star` labels for the same game.

Any derived-table build should de-duplicate source rows before aggregating. A practical first pass is `SELECT DISTINCT` over the columns used by the extractor, or a stronger de-dupe key based on:

- `game_id`
- `eventnum`
- `eventmsgtype`
- `eventmsgactiontype`
- `period`
- `pctimestring`
- descriptions
- `score`
- player IDs

## Performance Findings

The current table has no indexes.

A generated SQL query attempting to derive rookie single-game points directly from `play_by_play` timed out after 90 seconds. The same calculation as a Python streaming extractor over 2022-23 regular-season score rows finished in about 2.8 seconds.

This suggests:

- The data is usable.
- The current ad hoc SQL path is not the right execution model.
- A derived-table ETL script is the right next step.

Recommended permanent indexes if keeping this in SQLite:

```sql
CREATE INDEX IF NOT EXISTS idx_pbp_game_event
ON play_by_play(game_id, eventnum);

CREATE INDEX IF NOT EXISTS idx_pbp_event_type
ON play_by_play(eventmsgtype);

CREATE INDEX IF NOT EXISTS idx_pbp_player1
ON play_by_play(player1_id);

CREATE INDEX IF NOT EXISTS idx_pbp_player2
ON play_by_play(player2_id);

CREATE INDEX IF NOT EXISTS idx_pbp_player3
ON play_by_play(player3_id);
```

The most important one is `idx_pbp_game_event`, because score-delta derivation and lineup reconstruction both need event ordering within games.

## Prototype: Rookie Single-Game Points In 2022-23

The previous agent response said this was not directly possible because it would require parsing text descriptions. That answer was too conservative.

A better answer is:

```text
It is not safe as generated ad hoc SQL right now, but it can be derived from play-by-play by using score deltas for scoring events and joining rookie metadata.
```

Prototype method:

- Filter regular season games with IDs like `00222%`.
- Read score rows in `game_id, eventnum` order.
- Parse `score` as `away - home`.
- For made shots and made free throws, compute the scoring-side delta.
- Keep deltas in `{1, 2, 3}`.
- Attribute points to `player1_id`.
- Join rookies using `common_player_info.from_year = 2022`.

Prototype result:

| points | player | team | game_id | game_date | matchup |
| ---: | --- | --- | --- | --- | --- |
| 42 | Kenneth Lofton Jr. | MEM | `0022201226` | 2023-04-09 | MEM @ OKC |
| 33 | Paolo Banchero | ORL | `0022200132` | 2022-11-05 | SAC @ ORL |
| 33 | Jaden Ivey | DET | `0022201122` | 2023-03-27 | MIL @ DET |
| 32 | Bennedict Mathurin | IND | `0022200083` | 2022-10-29 | IND @ BKN |
| 31 | Andrew Nembhard | IND | `0022200359` | 2022-12-05 | IND @ GSW |

Caveats:

- This prototype treats `from_year = 2022` as rookie season.
- It uses play-by-play scoring deltas, not official player box scores.
- It filtered anomalous scoring deltas outside `{1, 2, 3}`.
- It should be validated against official box-score totals before being promoted.

## Implication For Blocks Greater Than Points

Question:

```text
who has more blocks than points scored in NBA history?
```

This should not be answered as "NBA history" from the current raw table.

Correct classification:

```text
Not directly answerable for full NBA history. Potentially answerable for the play-by-play coverage era, 1996-97 through 2022-23, after deriving and validating player career points and blocks from play_by_play.
```

For play-by-play-era career totals:

- Points can be derived from scoring event score deltas attributed to `player1_id`.
- Blocks can be derived from missed field goals where `player3_id <> '0'`.
- The final comparison should use a derived `player_career_stats` table.

The agent should not claim the descriptions are unusable. The better explanation is that raw `play_by_play` is an event source, not a validated player stat table, and it has incomplete historical coverage for "NBA history."

## Recommended Derived Table

Build `player_game_stats` first.

Suggested columns:

```text
game_id
season_id
season_type
game_date
player_id
player_name
team_id
team_abbreviation
pts
fgm
fga
fg3m
fg3a
ftm
fta
oreb
dreb
reb
ast
stl
blk
tov
pf
source_row_count
anomaly_count
created_at
```

Then build:

- `player_season_stats` by grouping `player_game_stats` by player and season.
- `player_career_stats` by grouping `player_game_stats` by player.

The agent should prefer these derived tables for all player stat questions.

## Recommended Agent Rules

Add these rules to the SQL planner:

- Do not use raw `play_by_play` for player stat totals unless the user asks for event-level details.
- For player points, blocks, steals, assists, rebounds, turnovers, and career totals, require a derived player stats table.
- If no derived table exists, explain that the question is derivable from play-by-play but not currently exposed as a validated stat table.
- For "NBA history" player-stat questions, mention play-by-play coverage starts in 1996-97.
- For "single game" player-stat questions, use `player_game_stats` once available.
- For "career" or "history" player-stat questions, use `player_career_stats` once available.

## Recommended Next Step

Create a script under `scripts/` that builds `player_game_stats` from `play_by_play`.

The script should:

1. Read games in chronological/event order.
2. De-duplicate source events.
3. Parse score deltas for points.
4. Use event/player-slot rules for assists, rebounds, steals, blocks, turnovers, and fouls.
5. Track anomaly counts.
6. Validate team totals against `game.pts_home`, `game.pts_away`, `game.blk_home`, and `game.blk_away` where possible.
7. Write the derived table to SQLite.
8. Add indexes on `player_game_stats(player_id)`, `player_game_stats(game_id)`, and `player_game_stats(season_id, season_type)`.

This would convert `play_by_play` from a difficult raw event table into a reliable query surface for the agent.
