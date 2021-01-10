import numpy as np
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def get_player_shotchartdetail(player_name, selected_year):
    
    # player dictionary
    nba_players = player.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    
    # career dataframe
    career = playercareerstats.PlayerCareerStats(player_id= player_dict['id'])
    career_df = career.get_data_frames()[0]
    
    # team id during season
    team_id = career_df[career_df['SEASON_ID'] == selected_year]['TEAM_ID']
    
    # shotchartdetail endpoints
    shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id),
                                                   player_id=int(player_dict['id']),
                                                   season_type_all_star='Regular Season',
                                                   season_nullable=selected_year,
                                                   context_measure_simple='FGA').get_data_frames()
    return shotchartlist[0], shotchartlist[1]

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
    ax.set_ylim(0, 470)
    
    return ax

mpl.rcParams['font.family'] = 'Dejavu Sans'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
# Create figure and axes
fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])

# Draw court
ax = create_court(ax, 'black')

# Plot hexbin of shots
ax.hexbin(player_data['LOC_X'], player_data['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='coolwarm_r')

# Annotate player name and season
ax.text(0, 1.05, '{player_name} \n {selected_year} Regular Season', transform=ax.transAxes, ha='left', va='baseline')

# Save and show figure
plt.savefig('ShotChart.png', dpi=300, bbox_inches='tight')
plt.show()
