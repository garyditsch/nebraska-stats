import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, datetime, timedelta

DATA_URL = 'https://gist.githubusercontent.com/garyditsch/c3e517a561ee1bc1d68dbadec8c917b2/raw/6e7b718880883744bb5b59ff809e0f39e493ff93/2023_Minnesota_Game_1.csv'

# Get the data from gist 
@st.cache_data
def get_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    return data

df = get_data(DATA_URL)

# Nebraska Offensive Plays
nebraska_offense = df[(df['Offense'] == 'Nebraska')]

# Get all the play types from offense
offensive_types = nebraska_offense['Play Type'].tolist()

# Get only the unique values from that play type list
unique_play_type_list = list(set(offensive_types))

# List of all play types
all_types = df['Play Type'].tolist()

# List of all play types that are runs
run_play = ['Fumble Recovery (Opponent)', 'Rush']

# List of all play types that are pass
pass_play = ['Interception', 'Pass Incompletion', 'Pass Reception', 'Pass Touchdown']

# List of other play types
# Putting a sack in other because it is unclear if it was a run or pass play
other_plays = ['Field Goal Good', 'Kickoff', 'Penalty', 'Timeout', 'Sack', 'End Period', 'Punt']

# set if run play
df['Run Play'] = df.apply(lambda row: row['Play Type'] in run_play, axis=1)

# set if pass play
df['Pass Play'] = df.apply(lambda row: row['Play Type'] in pass_play, axis=1)

# set if other play
df['Other Plays'] = df.apply(lambda row: row['Play Type'] in other_plays, axis=1)

fourth_quarter = df[['Period', 'Offense', 'Defense', 'Offense Score', 'Defense Score']]

ne_run_fourth_count = len(df[(df['Run Play'] == True) & (df['Offense'] == 'Nebraska') & (df['Period'] == 4)])

ne_pass_fourth_count = len(df[(df['Pass Play'] == True) & (df['Offense'] == 'Nebraska') & (df['Period'] == 4)])

ne_other_fourth_count = len(df[(df['Other Plays'] == True) & (df['Offense'] == 'Nebraska') & (df['Period'] == 4)])

fourth_run_yards = df[(df['Run Play'] == True) & (df['Offense'] == 'Nebraska') & (df['Period'] == 4)].sum()

fourth_quarter_run_yards = fourth_run_yards['Yards Gained']

# List of turnovers
lost_turnovers = ['Interception', 'Fumble Recovery (Opponent)']
turnovers = df.apply(lambda x : True if (x['Play Type'] in lost_turnovers and x['Offense'] == 'Nebraska') else False, axis = 1)

turnover_count = 0
for turnover in turnovers:
    if turnover == True:
        turnover_count = turnover_count + 1

st.title('Game Stats that Matter')
col1, col2, col3 = st.columns(3)
col1.metric("Turnovers Lost", turnover_count)


# Metric Row
st.title('Fourth Quarter Play Selection')

col1, col2, col3 = st.columns(3)
col1.metric("Ran The Ball", ne_run_fourth_count)
col2.metric("Passed The Ball", ne_pass_fourth_count)
col3.metric("Other Play Types", ne_other_fourth_count)

# Metric Row
st.title('Fourth Quarter Results')

col1, col2, col3 = st.columns(3)
col1.metric("4th Quarter Run Yards", fourth_run_yards['Yards Gained'])

st.dataframe(fourth_quarter)
# st.dataframe(df) 