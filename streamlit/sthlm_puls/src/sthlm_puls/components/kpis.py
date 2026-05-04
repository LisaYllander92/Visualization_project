from sthlm_puls.utils.helpers import get_events_df
import duckdb
import streamlit as st

df = get_events_df()

def diff_music_events(genres, label):
    diff_music = (
        duckdb.sql(f"""--sql
        SELECT genre,
        COUNT(*) as num_events
        FROM df
        WHERE segment = 'Music' AND month_num = 5
        GROUP BY genre
            return diff_music
""")
    )