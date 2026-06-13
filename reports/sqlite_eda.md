# NBA SQLite EDA

Database: `nba.sqlite`
Size: 2,349,588,480 bytes
Tables: 16

## Table Summary

| table | rows | columns | foreign_keys | indexes |
| --- | ---: | ---: | ---: | ---: |
| `common_player_info` | 3,632 | 33 | 0 | 0 |
| `draft_combine_stats` | 1,633 | 47 | 0 | 0 |
| `draft_history` | 8,257 | 14 | 0 | 0 |
| `game` | 65,698 | 55 | 0 | 0 |
| `game_info` | 58,053 | 4 | 0 | 0 |
| `game_summary` | 58,110 | 14 | 0 | 0 |
| `inactive_players` | 110,191 | 9 | 0 | 0 |
| `line_score` | 58,053 | 43 | 0 | 0 |
| `officials` | 70,971 | 5 | 0 | 0 |
| `other_stats` | 28,271 | 26 | 0 | 0 |
| `play_by_play` | 13,592,899 | 34 | 0 | 0 |
| `player` | 4,815 | 5 | 0 | 0 |
| `team` | 30 | 7 | 0 | 0 |
| `team_details` | 27 | 14 | 0 | 0 |
| `team_history` | 50 | 5 | 0 | 0 |
| `team_info_common` | 0 | 26 | 0 | 0 |

## Tables

### `common_player_info`

Rows: 3,632

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `person_id` | `TEXT` | yes |  |  |
| `first_name` | `TEXT` | yes |  |  |
| `last_name` | `TEXT` | yes |  |  |
| `display_first_last` | `TEXT` | yes |  |  |
| `display_last_comma_first` | `TEXT` | yes |  |  |
| `display_fi_last` | `TEXT` | yes |  |  |
| `player_slug` | `TEXT` | yes |  |  |
| `birthdate` | `TIMESTAMP` | yes |  |  |
| `school` | `TEXT` | yes |  |  |
| `country` | `TEXT` | yes |  |  |
| `last_affiliation` | `TEXT` | yes |  |  |
| `height` | `TEXT` | yes |  |  |
| `weight` | `TEXT` | yes |  |  |
| `season_exp` | `REAL` | yes |  |  |
| `jersey` | `TEXT` | yes |  |  |
| `position` | `TEXT` | yes |  |  |
| `rosterstatus` | `TEXT` | yes |  |  |
| `games_played_current_season_flag` | `TEXT` | yes |  |  |
| `team_id` | `INTEGER` | yes |  |  |
| `team_name` | `TEXT` | yes |  |  |
| `team_abbreviation` | `TEXT` | yes |  |  |
| `team_code` | `TEXT` | yes |  |  |
| `team_city` | `TEXT` | yes |  |  |
| `playercode` | `TEXT` | yes |  |  |
| `from_year` | `REAL` | yes |  |  |
| `to_year` | `REAL` | yes |  |  |
| `dleague_flag` | `TEXT` | yes |  |  |
| `nba_flag` | `TEXT` | yes |  |  |
| `games_played_flag` | `TEXT` | yes |  |  |
| `draft_year` | `TEXT` | yes |  |  |
| `draft_round` | `TEXT` | yes |  |  |
| `draft_number` | `TEXT` | yes |  |  |
| `greatest_75_flag` | `TEXT` | yes |  |  |

Sample rows (3):

| person_id | first_name | last_name | display_first_last | display_last_comma_first | display_fi_last | player_slug | birthdate | school | country | last_affiliation | height | weight | season_exp | jersey | position | rosterstatus | games_played_current_season_flag | team_id | team_name | team_abbreviation | team_code | team_city | playercode | from_year | to_year | dleague_flag | nba_flag | games_played_flag | draft_year | draft_round | draft_number | greatest_75_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 76001 | Alaa | Abdelnaby | Alaa Abdelnaby | Abdelnaby, Alaa | A. Abdelnaby | alaa-abdelnaby | 1968-06-24 00:00:00 | Duke | USA | Duke/USA | 6-10 | 240 | 5.0 | 30 | Forward | Inactive | N | 1610612757 | Trail Blazers | POR | blazers | Portland | HISTADD_alaa_abdelnaby | 1990.0 | 1994.0 | N | Y | Y | 1990 | 1 | 25 | N |
| 76002 | Zaid | Abdul-Aziz | Zaid Abdul-Aziz | Abdul-Aziz, Zaid | Z. Abdul-Aziz | zaid-abdul-aziz | 1946-04-07 00:00:00 | Iowa State | USA | Iowa State/USA | 6-9 | 235 | 10.0 | 54 | Center | Inactive | N | 1610612745 | Rockets | HOU | rockets | Houston | HISTADD_zaid_abdul-aziz | 1968.0 | 1977.0 | N | Y | Y | 1968 | 1 | 5 | N |
| 76003 | Kareem | Abdul-Jabbar | Kareem Abdul-Jabbar | Abdul-Jabbar, Kareem | K. Abdul-Jabbar | kareem-abdul-jabbar | 1947-04-16 00:00:00 | UCLA | USA | UCLA/USA | 7-2 | 225 | 20.0 | 33 | Center | Inactive | N | 1610612747 | Lakers | LAL | lakers | Los Angeles | HISTADD_kareem_abdul-jabbar | 1969.0 | 1988.0 | N | Y | Y | 1969 | 1 | 1 | Y |

### `draft_combine_stats`

Rows: 1,633

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `season` | `TEXT` | yes |  |  |
| `player_id` | `TEXT` | yes |  |  |
| `first_name` | `TEXT` | yes |  |  |
| `last_name` | `TEXT` | yes |  |  |
| `player_name` | `TEXT` | yes |  |  |
| `position` | `TEXT` | yes |  |  |
| `height_wo_shoes` | `REAL` | yes |  |  |
| `height_wo_shoes_ft_in` | `TEXT` | yes |  |  |
| `height_w_shoes` | `REAL` | yes |  |  |
| `height_w_shoes_ft_in` | `TEXT` | yes |  |  |
| `weight` | `TEXT` | yes |  |  |
| `wingspan` | `REAL` | yes |  |  |
| `wingspan_ft_in` | `TEXT` | yes |  |  |
| `standing_reach` | `REAL` | yes |  |  |
| `standing_reach_ft_in` | `TEXT` | yes |  |  |
| `body_fat_pct` | `TEXT` | yes |  |  |
| `hand_length` | `TEXT` | yes |  |  |
| `hand_width` | `TEXT` | yes |  |  |
| `standing_vertical_leap` | `REAL` | yes |  |  |
| `max_vertical_leap` | `REAL` | yes |  |  |
| `lane_agility_time` | `REAL` | yes |  |  |
| `modified_lane_agility_time` | `REAL` | yes |  |  |
| `three_quarter_sprint` | `REAL` | yes |  |  |
| `bench_press` | `REAL` | yes |  |  |
| `spot_fifteen_corner_left` | `TEXT` | yes |  |  |
| `spot_fifteen_break_left` | `TEXT` | yes |  |  |
| `spot_fifteen_top_key` | `TEXT` | yes |  |  |
| `spot_fifteen_break_right` | `TEXT` | yes |  |  |
| `spot_fifteen_corner_right` | `TEXT` | yes |  |  |
| `spot_college_corner_left` | `TEXT` | yes |  |  |
| `spot_college_break_left` | `TEXT` | yes |  |  |
| `spot_college_top_key` | `TEXT` | yes |  |  |
| `spot_college_break_right` | `TEXT` | yes |  |  |
| `spot_college_corner_right` | `TEXT` | yes |  |  |
| `spot_nba_corner_left` | `TEXT` | yes |  |  |
| `spot_nba_break_left` | `TEXT` | yes |  |  |
| `spot_nba_top_key` | `TEXT` | yes |  |  |
| `spot_nba_break_right` | `TEXT` | yes |  |  |
| `spot_nba_corner_right` | `TEXT` | yes |  |  |
| `off_drib_fifteen_break_left` | `TEXT` | yes |  |  |
| `off_drib_fifteen_top_key` | `TEXT` | yes |  |  |
| `off_drib_fifteen_break_right` | `TEXT` | yes |  |  |
| `off_drib_college_break_left` | `TEXT` | yes |  |  |
| `off_drib_college_top_key` | `TEXT` | yes |  |  |
| `off_drib_college_break_right` | `TEXT` | yes |  |  |
| `on_move_fifteen` | `TEXT` | yes |  |  |
| `on_move_college` | `TEXT` | yes |  |  |

Sample rows (3):

| season | player_id | first_name | last_name | player_name | position | height_wo_shoes | height_wo_shoes_ft_in | height_w_shoes | height_w_shoes_ft_in | weight | wingspan | wingspan_ft_in | standing_reach | standing_reach_ft_in | body_fat_pct | hand_length | hand_width | standing_vertical_leap | max_vertical_leap | lane_agility_time | modified_lane_agility_time | three_quarter_sprint | bench_press | spot_fifteen_corner_left | spot_fifteen_break_left | spot_fifteen_top_key | spot_fifteen_break_right | spot_fifteen_corner_right | spot_college_corner_left | spot_college_break_left | spot_college_top_key | spot_college_break_right | spot_college_corner_right | spot_nba_corner_left | spot_nba_break_left | spot_nba_top_key | spot_nba_break_right | spot_nba_corner_right | off_drib_fifteen_break_left | off_drib_fifteen_top_key | off_drib_fifteen_break_right | off_drib_college_break_left | off_drib_college_top_key | off_drib_college_break_right | on_move_fifteen | on_move_college |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2000 | 2124 | Malik | Allen | Malik Allen | PF-C | 80.25 | 6' 8.25'' |  |  | 271 | 86.5 | 7' 2.5'' | 109.0 | 9' 1'' |  |  |  | 25.5 | 29.0 | 11.83 |  | 3.38 | 13.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2000 | 12019 | Harold | Arceneaux | Harold Arceneaux | SG-SF | 76.5 | 6' 4.5'' |  |  | 219 | 80.5 | 6' 8.5'' | 103.0 | 8' 7'' |  |  |  |  | 29.0 | 13.8 |  |  | 0.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2000 | 12020 | Lamont | Barnes | Lamont Barnes | PF-C | 80.5 | 6' 8.5'' |  |  | 235.5 | 87.5 | 7' 3.5'' | 108.0 | 9' 0'' |  |  |  | 28.0 | 29.5 | 12.3 |  | 3.4 | 10.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### `draft_history`

Rows: 8,257

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `person_id` | `TEXT` | yes |  |  |
| `player_name` | `TEXT` | yes |  |  |
| `season` | `TEXT` | yes |  |  |
| `round_number` | `INTEGER` | yes |  |  |
| `round_pick` | `INTEGER` | yes |  |  |
| `overall_pick` | `INTEGER` | yes |  |  |
| `draft_type` | `TEXT` | yes |  |  |
| `team_id` | `TEXT` | yes |  |  |
| `team_city` | `TEXT` | yes |  |  |
| `team_name` | `TEXT` | yes |  |  |
| `team_abbreviation` | `TEXT` | yes |  |  |
| `organization` | `TEXT` | yes |  |  |
| `organization_type` | `TEXT` | yes |  |  |
| `player_profile_flag` | `TEXT` | yes |  |  |

Sample rows (3):

| person_id | player_name | season | round_number | round_pick | overall_pick | draft_type | team_id | team_city | team_name | team_abbreviation | organization | organization_type | player_profile_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 79299 | Clifton McNeeley | 1947 | 1 | 1 | 1 | Draft | 1610610031 | Pittsburgh | Ironmen | PIT | Texas-El Paso | College/University | 0 |
| 78109 | Glen Selbo | 1947 | 1 | 2 | 2 | Draft | 1610610035 | Toronto | Huskies | HUS | Wisconsin | College/University | 1 |
| 76649 | Eddie Ehlers | 1947 | 1 | 3 | 3 | Draft | 1610612738 | Boston | Celtics | BOS | Purdue | College/University | 1 |

### `game`

Rows: 65,698

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `season_id` | `TEXT` | yes |  |  |
| `team_id_home` | `TEXT` | yes |  |  |
| `team_abbreviation_home` | `TEXT` | yes |  |  |
| `team_name_home` | `TEXT` | yes |  |  |
| `game_id` | `TEXT` | yes |  |  |
| `game_date` | `TIMESTAMP` | yes |  |  |
| `matchup_home` | `TEXT` | yes |  |  |
| `wl_home` | `TEXT` | yes |  |  |
| `min` | `INTEGER` | yes |  |  |
| `fgm_home` | `REAL` | yes |  |  |
| `fga_home` | `REAL` | yes |  |  |
| `fg_pct_home` | `REAL` | yes |  |  |
| `fg3m_home` | `REAL` | yes |  |  |
| `fg3a_home` | `REAL` | yes |  |  |
| `fg3_pct_home` | `REAL` | yes |  |  |
| `ftm_home` | `REAL` | yes |  |  |
| `fta_home` | `REAL` | yes |  |  |
| `ft_pct_home` | `REAL` | yes |  |  |
| `oreb_home` | `REAL` | yes |  |  |
| `dreb_home` | `REAL` | yes |  |  |
| `reb_home` | `REAL` | yes |  |  |
| `ast_home` | `REAL` | yes |  |  |
| `stl_home` | `REAL` | yes |  |  |
| `blk_home` | `REAL` | yes |  |  |
| `tov_home` | `REAL` | yes |  |  |
| `pf_home` | `REAL` | yes |  |  |
| `pts_home` | `REAL` | yes |  |  |
| `plus_minus_home` | `INTEGER` | yes |  |  |
| `video_available_home` | `INTEGER` | yes |  |  |
| `team_id_away` | `TEXT` | yes |  |  |
| `team_abbreviation_away` | `TEXT` | yes |  |  |
| `team_name_away` | `TEXT` | yes |  |  |
| `matchup_away` | `TEXT` | yes |  |  |
| `wl_away` | `TEXT` | yes |  |  |
| `fgm_away` | `REAL` | yes |  |  |
| `fga_away` | `REAL` | yes |  |  |
| `fg_pct_away` | `REAL` | yes |  |  |
| `fg3m_away` | `REAL` | yes |  |  |
| `fg3a_away` | `REAL` | yes |  |  |
| `fg3_pct_away` | `REAL` | yes |  |  |
| `ftm_away` | `REAL` | yes |  |  |
| `fta_away` | `REAL` | yes |  |  |
| `ft_pct_away` | `REAL` | yes |  |  |
| `oreb_away` | `REAL` | yes |  |  |
| `dreb_away` | `REAL` | yes |  |  |
| `reb_away` | `REAL` | yes |  |  |
| `ast_away` | `REAL` | yes |  |  |
| `stl_away` | `REAL` | yes |  |  |
| `blk_away` | `REAL` | yes |  |  |
| `tov_away` | `REAL` | yes |  |  |
| `pf_away` | `REAL` | yes |  |  |
| `pts_away` | `REAL` | yes |  |  |
| `plus_minus_away` | `INTEGER` | yes |  |  |
| `video_available_away` | `INTEGER` | yes |  |  |
| `season_type` | `TEXT` | yes |  |  |

Sample rows (3):

| season_id | team_id_home | team_abbreviation_home | team_name_home | game_id | game_date | matchup_home | wl_home | min | fgm_home | fga_home | fg_pct_home | fg3m_home | fg3a_home | fg3_pct_home | ftm_home | fta_home | ft_pct_home | oreb_home | dreb_home | reb_home | ast_home | stl_home | blk_home | tov_home | pf_home | pts_home | plus_minus_home | video_available_home | team_id_away | team_abbreviation_away | team_name_away | matchup_away | wl_away | fgm_away | fga_away | fg_pct_away | fg3m_away | fg3a_away | fg3_pct_away | ftm_away | fta_away | ft_pct_away | oreb_away | dreb_away | reb_away | ast_away | stl_away | blk_away | tov_away | pf_away | pts_away | plus_minus_away | video_available_away | season_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 21946 | 1610610035 | HUS | Toronto Huskies | 0024600001 | 1946-11-01 00:00:00 | HUS vs. NYK | L | 0 | 25.0 |  |  |  |  |  | 16.0 | 29.0 | 0.552 |  |  |  |  |  |  |  |  | 66.0 | -2 | 0 | 1610612752 | NYK | New York Knicks | NYK @ HUS | W | 24.0 |  |  |  |  |  | 20.0 | 26.0 | 0.769 |  |  |  |  |  |  |  |  | 68.0 | 2 | 0 | Regular Season |
| 21946 | 1610610034 | BOM | St. Louis Bombers | 0024600003 | 1946-11-02 00:00:00 | BOM vs. PIT | W | 0 | 20.0 | 59.0 | 0.339 |  |  |  | 16.0 |  |  |  |  |  |  |  |  |  | 21.0 | 56.0 | 5 | 0 | 1610610031 | PIT | Pittsburgh Ironmen | PIT @ BOM | L | 16.0 | 72.0 | 0.222 |  |  |  | 19.0 |  |  |  |  |  |  |  |  |  | 25.0 | 51.0 | -5 | 0 | Regular Season |
| 21946 | 1610610032 | PRO | Providence Steamrollers | 0024600002 | 1946-11-02 00:00:00 | PRO vs. BOS | W | 0 | 21.0 |  |  |  |  |  | 17.0 |  |  |  |  |  |  |  |  |  |  | 59.0 | 6 | 0 | 1610612738 | BOS | Boston Celtics | BOS @ PRO | L | 21.0 |  |  |  |  |  | 11.0 |  |  |  |  |  |  |  |  |  |  | 53.0 | -6 | 0 | Regular Season |

### `game_info`

Rows: 58,053

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `game_id` | `TEXT` | yes |  |  |
| `game_date` | `TIMESTAMP` | yes |  |  |
| `attendance` | `INTEGER` | yes |  |  |
| `game_time` | `TEXT` | yes |  |  |

Sample rows (3):

| game_id | game_date | attendance | game_time |
| --- | --- | --- | --- |
| 0024600001 | 1946-11-01 00:00:00 |  |  |
| 0024600003 | 1946-11-02 00:00:00 |  |  |
| 0024600002 | 1946-11-02 00:00:00 |  |  |

### `game_summary`

Rows: 58,110

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `game_date_est` | `TIMESTAMP` | yes |  |  |
| `game_sequence` | `INTEGER` | yes |  |  |
| `game_id` | `TEXT` | yes |  |  |
| `game_status_id` | `INTEGER` | yes |  |  |
| `game_status_text` | `TEXT` | yes |  |  |
| `gamecode` | `TEXT` | yes |  |  |
| `home_team_id` | `TEXT` | yes |  |  |
| `visitor_team_id` | `TEXT` | yes |  |  |
| `season` | `TEXT` | yes |  |  |
| `live_period` | `INTEGER` | yes |  |  |
| `live_pc_time` | `TEXT` | yes |  |  |
| `natl_tv_broadcaster_abbreviation` | `TEXT` | yes |  |  |
| `live_period_time_bcast` | `TEXT` | yes |  |  |
| `wh_status` | `INTEGER` | yes |  |  |

Sample rows (3):

| game_date_est | game_sequence | game_id | game_status_id | game_status_text | gamecode | home_team_id | visitor_team_id | season | live_period | live_pc_time | natl_tv_broadcaster_abbreviation | live_period_time_bcast | wh_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1946-11-01 00:00:00 |  | 0024600001 | 3 |  | 19461101/NYKHUS | 1610610035 | 1610612752 | 1946 | 5 |  |  | Q5  -  | 1 |
| 1946-11-02 00:00:00 |  | 0024600003 | 3 |  | 19461102/PITBOM | 1610610034 | 1610610031 | 1946 | 4 |  |  | Q4  -  | 1 |
| 1946-11-02 00:00:00 |  | 0024600002 | 3 |  | 19461102/BOSPRO | 1610610032 | 1610612738 | 1946 | 4 |  |  | Q4  -  | 1 |

### `inactive_players`

Rows: 110,191

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `game_id` | `TEXT` | yes |  |  |
| `player_id` | `TEXT` | yes |  |  |
| `first_name` | `TEXT` | yes |  |  |
| `last_name` | `TEXT` | yes |  |  |
| `jersey_num` | `TEXT` | yes |  |  |
| `team_id` | `TEXT` | yes |  |  |
| `team_city` | `TEXT` | yes |  |  |
| `team_name` | `TEXT` | yes |  |  |
| `team_abbreviation` | `TEXT` | yes |  |  |

Sample rows (3):

| game_id | player_id | first_name | last_name | jersey_num | team_id | team_city | team_name | team_abbreviation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0029600034 | 184 | Bobby | Phills | 14 | 1610612739 | Cleveland | Cavaliers | CLE |
| 0029600034 | 781 | Will | Perdue | 41 | 1610612759 | San Antonio | Spurs | SAS |
| 0029600132 | 120 | Steven | Smith | 8 | 1610612737 | Atlanta | Hawks | ATL |

### `line_score`

Rows: 58,053

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `game_date_est` | `TIMESTAMP` | yes |  |  |
| `game_sequence` | `INTEGER` | yes |  |  |
| `game_id` | `TEXT` | yes |  |  |
| `team_id_home` | `TEXT` | yes |  |  |
| `team_abbreviation_home` | `TEXT` | yes |  |  |
| `team_city_name_home` | `TEXT` | yes |  |  |
| `team_nickname_home` | `TEXT` | yes |  |  |
| `team_wins_losses_home` | `TEXT` | yes |  |  |
| `pts_qtr1_home` | `TEXT` | yes |  |  |
| `pts_qtr2_home` | `TEXT` | yes |  |  |
| `pts_qtr3_home` | `TEXT` | yes |  |  |
| `pts_qtr4_home` | `TEXT` | yes |  |  |
| `pts_ot1_home` | `INTEGER` | yes |  |  |
| `pts_ot2_home` | `INTEGER` | yes |  |  |
| `pts_ot3_home` | `INTEGER` | yes |  |  |
| `pts_ot4_home` | `INTEGER` | yes |  |  |
| `pts_ot5_home` | `INTEGER` | yes |  |  |
| `pts_ot6_home` | `INTEGER` | yes |  |  |
| `pts_ot7_home` | `INTEGER` | yes |  |  |
| `pts_ot8_home` | `INTEGER` | yes |  |  |
| `pts_ot9_home` | `INTEGER` | yes |  |  |
| `pts_ot10_home` | `INTEGER` | yes |  |  |
| `pts_home` | `REAL` | yes |  |  |
| `team_id_away` | `TEXT` | yes |  |  |
| `team_abbreviation_away` | `TEXT` | yes |  |  |
| `team_city_name_away` | `TEXT` | yes |  |  |
| `team_nickname_away` | `TEXT` | yes |  |  |
| `team_wins_losses_away` | `TEXT` | yes |  |  |
| `pts_qtr1_away` | `INTEGER` | yes |  |  |
| `pts_qtr2_away` | `TEXT` | yes |  |  |
| `pts_qtr3_away` | `TEXT` | yes |  |  |
| `pts_qtr4_away` | `INTEGER` | yes |  |  |
| `pts_ot1_away` | `INTEGER` | yes |  |  |
| `pts_ot2_away` | `INTEGER` | yes |  |  |
| `pts_ot3_away` | `INTEGER` | yes |  |  |
| `pts_ot4_away` | `INTEGER` | yes |  |  |
| `pts_ot5_away` | `INTEGER` | yes |  |  |
| `pts_ot6_away` | `INTEGER` | yes |  |  |
| `pts_ot7_away` | `INTEGER` | yes |  |  |
| `pts_ot8_away` | `INTEGER` | yes |  |  |
| `pts_ot9_away` | `INTEGER` | yes |  |  |
| `pts_ot10_away` | `INTEGER` | yes |  |  |
| `pts_away` | `REAL` | yes |  |  |

Sample rows (3):

| game_date_est | game_sequence | game_id | team_id_home | team_abbreviation_home | team_city_name_home | team_nickname_home | team_wins_losses_home | pts_qtr1_home | pts_qtr2_home | pts_qtr3_home | pts_qtr4_home | pts_ot1_home | pts_ot2_home | pts_ot3_home | pts_ot4_home | pts_ot5_home | pts_ot6_home | pts_ot7_home | pts_ot8_home | pts_ot9_home | pts_ot10_home | pts_home | team_id_away | team_abbreviation_away | team_city_name_away | team_nickname_away | team_wins_losses_away | pts_qtr1_away | pts_qtr2_away | pts_qtr3_away | pts_qtr4_away | pts_ot1_away | pts_ot2_away | pts_ot3_away | pts_ot4_away | pts_ot5_away | pts_ot6_away | pts_ot7_away | pts_ot8_away | pts_ot9_away | pts_ot10_away | pts_away |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1946-11-01 00:00:00 |  | 0024600001 | 1610610035 | HUS | Toronto | Huskies | - |  |  |  |  | 18 |  |  |  |  |  |  |  |  |  | 66.0 | 1610612752 | NYK | New York | Knicks | - |  |  |  |  | 24 |  |  |  |  |  |  |  |  |  | 68.0 |
| 1946-11-02 00:00:00 |  | 0024600003 | 1610610034 | BOM | St. Louis | Bombers | - | 16 | 16 | 18 | 6 |  |  |  |  |  |  |  |  |  |  | 56.0 | 1610610031 | PIT | Pittsburgh | Ironmen | - | 5 | 15 | 17 | 14 |  |  |  |  |  |  |  |  |  |  | 51.0 |
| 1946-11-02 00:00:00 |  | 0024600002 | 1610612738 | BOS | Boston | Celtics | - | 10.0 | 16 | 14 | 13 |  |  |  |  |  |  |  |  |  |  | 53.0 | 1610610032 | PRO | Providence | Steamrollers | - |  | 12 | 18 | 15 |  |  |  |  |  |  |  |  |  |  | 59.0 |

### `officials`

Rows: 70,971

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `game_id` | `TEXT` | yes |  |  |
| `official_id` | `TEXT` | yes |  |  |
| `first_name` | `TEXT` | yes |  |  |
| `last_name` | `TEXT` | yes |  |  |
| `jersey_num` | `TEXT` | yes |  |  |

Sample rows (3):

| game_id | official_id | first_name | last_name | jersey_num |
| --- | --- | --- | --- | --- |
| 0029600059 | 1140 | Bruce | Alexander | 9 |
| 0029600059 | 1165 | Luis | Grillo | 8 |
| 0029600059 | 1153 | Joe | Crawford | 17 |

### `other_stats`

Rows: 28,271

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `game_id` | `TEXT` | yes |  |  |
| `league_id` | `TEXT` | yes |  |  |
| `team_id_home` | `TEXT` | yes |  |  |
| `team_abbreviation_home` | `TEXT` | yes |  |  |
| `team_city_home` | `TEXT` | yes |  |  |
| `pts_paint_home` | `INTEGER` | yes |  |  |
| `pts_2nd_chance_home` | `INTEGER` | yes |  |  |
| `pts_fb_home` | `INTEGER` | yes |  |  |
| `largest_lead_home` | `INTEGER` | yes |  |  |
| `lead_changes` | `INTEGER` | yes |  |  |
| `times_tied` | `INTEGER` | yes |  |  |
| `team_turnovers_home` | `INTEGER` | yes |  |  |
| `total_turnovers_home` | `INTEGER` | yes |  |  |
| `team_rebounds_home` | `INTEGER` | yes |  |  |
| `pts_off_to_home` | `INTEGER` | yes |  |  |
| `team_id_away` | `TEXT` | yes |  |  |
| `team_abbreviation_away` | `TEXT` | yes |  |  |
| `team_city_away` | `TEXT` | yes |  |  |
| `pts_paint_away` | `INTEGER` | yes |  |  |
| `pts_2nd_chance_away` | `INTEGER` | yes |  |  |
| `pts_fb_away` | `INTEGER` | yes |  |  |
| `largest_lead_away` | `INTEGER` | yes |  |  |
| `team_turnovers_away` | `INTEGER` | yes |  |  |
| `total_turnovers_away` | `INTEGER` | yes |  |  |
| `team_rebounds_away` | `INTEGER` | yes |  |  |
| `pts_off_to_away` | `INTEGER` | yes |  |  |

Sample rows (3):

| game_id | league_id | team_id_home | team_abbreviation_home | team_city_home | pts_paint_home | pts_2nd_chance_home | pts_fb_home | largest_lead_home | lead_changes | times_tied | team_turnovers_home | total_turnovers_home | team_rebounds_home | pts_off_to_home | team_id_away | team_abbreviation_away | team_city_away | pts_paint_away | pts_2nd_chance_away | pts_fb_away | largest_lead_away | team_turnovers_away | total_turnovers_away | team_rebounds_away | pts_off_to_away |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0029600012 | 00 | 1610612756 | PHX | Phoenix | 44 | 18 | 2 | 1 | 4 | 1 | 0 | 12 | 11 |  | 1610612747 | LAL | Los Angeles | 42 | 10 | 13 | 19 | 0 | 23 | 11 |  |
| 0029600005 | 00 | 1610612737 | ATL | Atlanta | 32 | 9 | 6 | 0 | 0 | 0 | 1 | 24 | 7 |  | 1610612748 | MIA | Miami | 32 | 15 | 14 | 16 | 1 | 19 | 6 |  |
| 0029600002 | 00 | 1610612739 | CLE | Cleveland | 36 | 14 | 6 | 20 | 1 | 1 | 0 | 15 | 5 |  | 1610612751 | NJN | New Jersey | 26 | 16 | 4 | 2 | 1 | 22 | 12 |  |

### `play_by_play`

Rows: 13,592,899

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `game_id` | `TEXT` | yes |  |  |
| `eventnum` | `INTEGER` | yes |  |  |
| `eventmsgtype` | `INTEGER` | yes |  |  |
| `eventmsgactiontype` | `INTEGER` | yes |  |  |
| `period` | `INTEGER` | yes |  |  |
| `wctimestring` | `TEXT` | yes |  |  |
| `pctimestring` | `TEXT` | yes |  |  |
| `homedescription` | `TEXT` | yes |  |  |
| `neutraldescription` | `TEXT` | yes |  |  |
| `visitordescription` | `TEXT` | yes |  |  |
| `score` | `TEXT` | yes |  |  |
| `scoremargin` | `TEXT` | yes |  |  |
| `person1type` | `REAL` | yes |  |  |
| `player1_id` | `TEXT` | yes |  |  |
| `player1_name` | `TEXT` | yes |  |  |
| `player1_team_id` | `TEXT` | yes |  |  |
| `player1_team_city` | `TEXT` | yes |  |  |
| `player1_team_nickname` | `TEXT` | yes |  |  |
| `player1_team_abbreviation` | `TEXT` | yes |  |  |
| `person2type` | `REAL` | yes |  |  |
| `player2_id` | `TEXT` | yes |  |  |
| `player2_name` | `TEXT` | yes |  |  |
| `player2_team_id` | `TEXT` | yes |  |  |
| `player2_team_city` | `TEXT` | yes |  |  |
| `player2_team_nickname` | `TEXT` | yes |  |  |
| `player2_team_abbreviation` | `TEXT` | yes |  |  |
| `person3type` | `REAL` | yes |  |  |
| `player3_id` | `TEXT` | yes |  |  |
| `player3_name` | `TEXT` | yes |  |  |
| `player3_team_id` | `TEXT` | yes |  |  |
| `player3_team_city` | `TEXT` | yes |  |  |
| `player3_team_nickname` | `TEXT` | yes |  |  |
| `player3_team_abbreviation` | `TEXT` | yes |  |  |
| `video_available_flag` | `TEXT` | yes |  |  |

Sample rows (3):

| game_id | eventnum | eventmsgtype | eventmsgactiontype | period | wctimestring | pctimestring | homedescription | neutraldescription | visitordescription | score | scoremargin | person1type | player1_id | player1_name | player1_team_id | player1_team_city | player1_team_nickname | player1_team_abbreviation | person2type | player2_id | player2_name | player2_team_id | player2_team_city | player2_team_nickname | player2_team_abbreviation | person3type | player3_id | player3_name | player3_team_id | player3_team_city | player3_team_nickname | player3_team_abbreviation | video_available_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0029600012 | 0 | 12 | 0 | 1 | 14:43 PM | 12:00 |  | Start of 1st Period (14:43 PM EST) |  |  |  | 0.0 | 0 |  |  |  |  |  | 0.0 | 0 |  |  |  |  |  | 0.0 | 0 |  |  |  |  |  | 0 |
| 0029600012 | 2 | 10 | 0 | 1 | 14:50 PM | 12:00 | Jump Ball O'Neal vs. Kleine: Tip to Cassell |  |  |  |  | 4.0 | 406 | Shaquille O'Neal | 1610612747.0 | Los Angeles | Lakers | LAL | 5.0 | 170 | Joe Kleine | 1610612756.0 | Phoenix | Suns | PHX | 5.0 | 208 | Sam Cassell | 1610612756.0 | Phoenix | Suns | PHX | 0 |
| 0029600012 | 3 | 2 | 1 | 1 | 14:51 PM | 11:45 |  |  | MISS Cassell 15' Jump Shot |  |  | 5.0 | 208 | Sam Cassell | 1610612756.0 | Phoenix | Suns | PHX | 0.0 | 0 |  |  |  |  |  | 0.0 | 0 |  |  |  |  |  | 0 |

### `player`

Rows: 4,815

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `id` | `TEXT` | yes |  |  |
| `full_name` | `TEXT` | yes |  |  |
| `first_name` | `TEXT` | yes |  |  |
| `last_name` | `TEXT` | yes |  |  |
| `is_active` | `INTEGER` | yes |  |  |

Sample rows (3):

| id | full_name | first_name | last_name | is_active |
| --- | --- | --- | --- | --- |
| 76001 | Alaa Abdelnaby | Alaa | Abdelnaby | 0 |
| 76002 | Zaid Abdul-Aziz | Zaid | Abdul-Aziz | 0 |
| 76003 | Kareem Abdul-Jabbar | Kareem | Abdul-Jabbar | 0 |

### `team`

Rows: 30

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `id` | `TEXT` | yes |  |  |
| `full_name` | `TEXT` | yes |  |  |
| `abbreviation` | `TEXT` | yes |  |  |
| `nickname` | `TEXT` | yes |  |  |
| `city` | `TEXT` | yes |  |  |
| `state` | `TEXT` | yes |  |  |
| `year_founded` | `REAL` | yes |  |  |

Sample rows (3):

| id | full_name | abbreviation | nickname | city | state | year_founded |
| --- | --- | --- | --- | --- | --- | --- |
| 1610612737 | Atlanta Hawks | ATL | Hawks | Atlanta | Georgia | 1949.0 |
| 1610612738 | Boston Celtics | BOS | Celtics | Boston | Massachusetts | 1946.0 |
| 1610612739 | Cleveland Cavaliers | CLE | Cavaliers | Cleveland | Ohio | 1970.0 |

### `team_details`

Rows: 27

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `team_id` | `TEXT` | yes |  |  |
| `abbreviation` | `TEXT` | yes |  |  |
| `nickname` | `TEXT` | yes |  |  |
| `yearfounded` | `REAL` | yes |  |  |
| `city` | `TEXT` | yes |  |  |
| `arena` | `TEXT` | yes |  |  |
| `arenacapacity` | `REAL` | yes |  |  |
| `owner` | `TEXT` | yes |  |  |
| `generalmanager` | `TEXT` | yes |  |  |
| `headcoach` | `TEXT` | yes |  |  |
| `dleagueaffiliation` | `TEXT` | yes |  |  |
| `facebook` | `TEXT` | yes |  |  |
| `instagram` | `TEXT` | yes |  |  |
| `twitter` | `TEXT` | yes |  |  |

Sample rows (3):

| team_id | abbreviation | nickname | yearfounded | city | arena | arenacapacity | owner | generalmanager | headcoach | dleagueaffiliation | facebook | instagram | twitter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1610612737 | ATL | Hawks | 1949.0 | Atlanta | State Farm Arena | 18729.0 | Tony Ressler | Travis Schlenk | Quin Snyder | College Park Skyhawks | https://www.facebook.com/hawks | https://instagram.com/atlhawks | https://twitter.com/ATLHawks |
| 1610612738 | BOS | Celtics | 1946.0 | Boston | TD Garden | 18624.0 | Wyc Grousbeck | Brad Stevens | Joe Mazzulla | Maine Celtics | https://www.facebook.com/bostonceltics | https://instagram.com/celtics | https://twitter.com/celtics |
| 1610612739 | CLE | Cavaliers | 1970.0 | Cleveland | Rocket Mortgage FieldHouse | 20562.0 | Dan Gilbert | Koby Altman | JB Bickerstaff | Cleveland Charge | https://www.facebook.com/Cavs | https://instagram.com/cavs | https://twitter.com/cavs |

### `team_history`

Rows: 50

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `team_id` | `TEXT` | yes |  |  |
| `city` | `TEXT` | yes |  |  |
| `nickname` | `TEXT` | yes |  |  |
| `year_founded` | `INTEGER` | yes |  |  |
| `year_active_till` | `INTEGER` | yes |  |  |

Sample rows (3):

| team_id | city | nickname | year_founded | year_active_till |
| --- | --- | --- | --- | --- |
| 1610612737 | Atlanta | Hawks | 1968 | 2019 |
| 1610612737 | St. Louis | Hawks | 1955 | 1967 |
| 1610612737 | Milwaukee | Hawks | 1951 | 1954 |

### `team_info_common`

Rows: 0

| column | type | nullable | primary_key | default |
| --- | --- | --- | --- | --- |
| `team_id` | `TEXT` | yes |  |  |
| `season_year` | `TEXT` | yes |  |  |
| `team_city` | `TEXT` | yes |  |  |
| `team_name` | `TEXT` | yes |  |  |
| `team_abbreviation` | `TEXT` | yes |  |  |
| `team_conference` | `TEXT` | yes |  |  |
| `team_division` | `TEXT` | yes |  |  |
| `team_code` | `TEXT` | yes |  |  |
| `team_slug` | `TEXT` | yes |  |  |
| `w` | `INTEGER` | yes |  |  |
| `l` | `INTEGER` | yes |  |  |
| `pct` | `REAL` | yes |  |  |
| `conf_rank` | `INTEGER` | yes |  |  |
| `div_rank` | `INTEGER` | yes |  |  |
| `min_year` | `INTEGER` | yes |  |  |
| `max_year` | `INTEGER` | yes |  |  |
| `league_id` | `TEXT` | yes |  |  |
| `season_id` | `TEXT` | yes |  |  |
| `pts_rank` | `INTEGER` | yes |  |  |
| `pts_pg` | `REAL` | yes |  |  |
| `reb_rank` | `INTEGER` | yes |  |  |
| `reb_pg` | `REAL` | yes |  |  |
| `ast_rank` | `INTEGER` | yes |  |  |
| `ast_pg` | `REAL` | yes |  |  |
| `opp_pts_rank` | `INTEGER` | yes |  |  |
| `opp_pts_pg` | `REAL` | yes |  |  |
