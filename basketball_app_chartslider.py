import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
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

player_selector = st.sidebar.radio('Select your Player!', ('Stephen Curry','LeBron James','Giannis Antetokounmpo'))

#elif player_selector == 'Luka Doncic':
#    name = 'Luka'
#    lastname = 'Doncic'
#    selected_team = 'Dallas Mavericks'
if player_selector == 'Stephen Curry':
    name = 'Stephen'
    lastname = 'Curry'
    selected_team = 'Golden State Warriors'
    #Player picture
    #Curry
    player_pic = urllib.request.urlretrieve('http://stats.nba.com/media/players/230x185/201939.png', '201939.png')
    player_profile_pic = plt.imread(player_request[0])    
    #Team Logo
    logo_team = 'GSW'
    logo_url = "https://d2p3bygnnzw9w3.cloudfront.net/req/202001161/tlogo/bbr/" + logo_team + ".png"
    team_pic = urllib.request.urlretrieve(logo_url)
    team_logo = plt.imread(team_pic[0])
    
elif player_selector == 'LeBron James':
    name = 'LeBron'
    lastname = 'James'
    selected_team = 'Los Angeles Lakers'
    #Lebron
    player_pic = urllib.request.urlretrieve('http://stats.nba.com/media/players/230x185/2544.png', '2544.png')
    player_profile_pic = plt.imread(player_pic[0])   
    #Team Logo
    logo_team = 'LAL'
    logo_url = "https://d2p3bygnnzw9w3.cloudfront.net/req/202001161/tlogo/bbr/" + logo_team + ".png"
    team_pic = urllib.request.urlretrieve(logo_url)
    team_logo = plt.imread(team_pic[0])    
    
elif player_selector == 'Giannis Antetokounmpo':
    name = 'Giannis'
    lastname = 'Antetokounmpo'
    selected_team = 'Milwaukee Bucks'
    #Anteto
    player_pic = urllib.request.urlretrieve('http://stats.nba.com/media/players/230x185/203507.png', '203507.png')
    player_profile_pic = plt.imread(player_pic[0])    
    #Team Logo
    logo_team = 'MIL'
    logo_url = "https://d2p3bygnnzw9w3.cloudfront.net/req/202001161/tlogo/bbr/" + logo_team + ".png"
    team_pic = urllib.request.urlretrieve(logo_url)
    team_logo = plt.imread(team_pic[0])


def get_player_id(first, last):
    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            return player['playerId']
    return -1

shot_json = shotchartdetail.ShotChartDetail(
            team_id = get_team_id(f'{selected_team}'),
            player_id = get_player_id(f'{name}', f'{lastname}'),
            context_measure_simple = 'PTS',
            season_nullable = '2018-19',
            season_type_all_star = 'Regular Season')

shot_data = json.loads(shot_json.get_json())

relevant_data = shot_data['resultSets'][0]
headers = relevant_data['headers']
shots = relevant_data['rowSet']

# Create pandas DataFrame
player_data = pd.DataFrame(shots)
player_data.columns = headers

def create_court(ax, color):
    
    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    
    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(470, 0)
    
    return ax

# Create figure and axes
fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])

# Draw court
ax = create_court(ax, 'black')

# Plot hexbin of shots
ax.hexbin(player_data['LOC_X'], player_data['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='Blues')

#Add Player Picture

player_imagebox = OffsetImage(player_profile_pic, zoom=0.32)
player_imagebox.set_offset((0,0))
xy = [0,0]
ab_player_imagebox = AnnotationBbox(player_imagebox, xy, xybox=(-102,-237), boxcoords='offset points', frameon=False)
ax.add_artist(ab_player_imagebox)

    # Put the logo behind
team_logo_img = OffsetImage(team_logo, zoom=1)
team_logo_img.set_offset((180,250))
ax.add_artist(team_logo_img)

# Annotate player name and season
fig.text(0, 1.05, f'{name} {lastname} \n{selected_year} RS Shot Chart', transform=ax.transAxes, ha='left', va='baseline',fontsize=11.5)
ax.text(0, -0.075, 'Data Source: stats.nba.com'
        '\nAuthor: Pablo Salmerón', transform=ax.transAxes, ha='left', fontsize=8)

st.pyplot(fig)





