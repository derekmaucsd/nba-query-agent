# nba-query-agent

## Data

The NBA dataset is not stored in this GitHub repo because the SQLite database
and CSV exports are large. Download the data locally from Kaggle:

https://www.kaggle.com/datasets/wyattowalsh/basketball?resource=download

After downloading, place the files in the repo root like this:

```text
nba-query-agent/
  nba.sqlite
  csv/
    common_player_info.csv
    game.csv
    play_by_play.csv
    ...
```

The local data files are ignored by Git via `.gitignore`.

## SQLite EDA

Run a quick schema and sample-data report with:

```powershell
python scripts\eda_sqlite.py --db nba.sqlite --out reports\sqlite_eda.md
```
