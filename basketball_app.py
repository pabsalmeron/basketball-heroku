from PIL import Image
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#from shot_chart import *
from matplotlib.patches import mpl
from nba_api.stats.endpoints import shotchartdetail
import json
import requests

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))
# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

sorted_unique_player = sorted(playerstats.Player)
selected_player = st.sidebar.multiselect('Player', sorted_unique_player)

prev_year = str(int(selected_year) - 1)
formated_year = prev_year + '-' + str(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]


df_selected_player = playerstats[playerstats.Player.isin(selected_player)]

st.header('Player Stats That You Are Looking For! ')
st.markdown("""
*Just Write in the Search Box!*
""")
st.dataframe(df_selected_player)

st.header('Display Players Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
st.markdown("""
*Display an Amazing Heatmap!*
""")
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f) 

st.markdown("""
*Display an Amazing Shot Chart!*
""")

#Creating infraestructure
teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)

def get_team_id(team_name):
    for team in teams:
        if team['teamName'] == team_name:
            return team['teamId']
    return -1

# Players
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)
all_stars_dict = {'Stephen Curry': 201939,
                  'LeBron James': 2544,
                  'Luka Doncic': 1629029,
                  'Giannis Antetokounmpo': 203507,
                  'Kawhi Leonard': 202695}

#CHOOSING PLAYER - SHOT CHART
st.sidebar.header('Shot Chart Player')
st.set_option('deprecation.showPyplotGlobalUse', False)
player_selector = st.sidebar.radio('Select your Player!', ('Stephen Curry','LeBron James','Giannis Antetokounmpo'))

#elif player_selector == 'Luka Doncic':
#    name = 'Luka'
#    lastname = 'Doncic'
#    selected_team = 'Dallas Mavericks'
if player_selector == 'Stephen Curry':
    image = Image.open('Stephen-shot-chart.png')
    st.image(image, use_column_width=True)
    st.pyplot()
    
elif player_selector == 'LeBron James':
    image = Image.open('LeBron-shot-chart.png')
    st.image(image, use_column_width=True)
    st.pyplot()
    
elif player_selector == 'Giannis Antetokounmpo':
    image = Image.open('Giannis-shot-chart.png')
    st.image(image, use_column_width=True)
    st.pyplot()


