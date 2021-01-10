#!/usr/bin/env python
# coding: utf-8

# In[28]:


from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.pyplot as plt

# Teams
teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)

def get_team_id(team_name):
    for team in teams:
        if team['teamName'] == team_name:
            return team['teamId']
    return -1

# Players
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

#SOLO MODIFICAR ESTOS PARÁMETROS
name = 'Stephen'
lastname = 'Curry'
selected_team = 'Golden State Warriors'
selected_year = '2018-19'
def get_player_id(first, last):
    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            return player['playerId']
    return -1

shot_json = shotchartdetail.ShotChartDetail(
            team_id = get_team_id(f'{selected_team}'),
            player_id = get_player_id(f'{name}', f'{lastname}'),
            context_measure_simple = 'PTS',
            season_nullable = f'{selected_year}',
            season_type_all_star = 'Regular Season')

shot_data = json.loads(shot_json.get_json())

relevant_data = shot_data['resultSets'][0]
headers = relevant_data['headers']
rows = relevant_data['rowSet']

# Create pandas DataFrame
player_data = pd.DataFrame(rows)
player_data.columns = headers

player_data.columns

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

# Annotate player name and season
fig.text(0, 1.05, f'{name} {lastname} \n{selected_year} Regular Season', transform=ax.transAxes, ha='left', va='baseline')
ax.text(0, -0.075, 'Author: Pablo Salmerón', transform=ax.transAxes, ha='left')

plt.show()


# In[ ]:




