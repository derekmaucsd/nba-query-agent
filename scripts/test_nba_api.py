# gets scoreboard for SA at NYK game 4 6/10/2026
# writes scoreboard to scoreboard_2026-06-10.json

from nba_api.stats.endpoints.scoreboardv3 import ScoreboardV3

scoreboard = ScoreboardV3(game_date="2026-06-10")

raw_json = scoreboard.get_json()
print(raw_json)

with open("scoreboard_2026-06-10.json", "w") as f:
    f.write(raw_json)
