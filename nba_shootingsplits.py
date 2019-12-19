# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:27:28 2019

@author: aasim
"""

#import pandas as pd
from matplotlib import pyplot as plt
from pywaffle import Waffle
from nba_api.stats.endpoints import playerdashboardbygeneralsplits
import math

#--LOADING/GATHERING THE DATA

#Current 2019-20 Top 10 PPG, Player ID data
player_dict = {
   'James Harden': 201935,
   'Giannis Antetokounmpo': 203507,
   'Luka Doncic': 1629029,
   'Trae Young': 1629027,
   'Bradley Beal': 203078,
   'Anthony Davis': 203076,
   'Damian Lillard': 203081,
   'Karl-Anthony Towns': 1626157,
   'LeBron James':2544,
   'Kawhi Leonard':202695
   }

#find the stats of all the players using the NBA API
for i in player_dict.keys():
    nba_id = player_dict.get(i)
    overall_stats = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id = nba_id)
    player_data = overall_stats.overall_player_dashboard.get_dict()
    #--CLEANING THE DATA--
    #get the headers for the columns of data
    col_data = player_data.get('headers')
    #get the actual data values
    data_val = player_data.get('data')[0]
    #combine these headers and values into a dictionary
    final_data ={col_data[i]: data_val[i] for i in range(len(col_data))}
    #extract only the columns we need to compare shooting splits
    players_stats_pct = {'2PTS': None, '3PTS': None, 'FTS': None}
    #convert our stats into shooting %'s
    players_stats_pct['3PTS'] = round(math.floor(((final_data['FG3M'] * 3) / final_data['PTS']) * 100))
    players_stats_pct['FTS'] = round(math.floor((final_data['FTM'] / final_data['PTS']) * 100))
    #Since there isn't a data point for 2pt attempts
    players_stats_pct['2PTS'] = round(math.floor(((final_data['PTS'] - + \
                     (final_data['FG3M'] * 3 + final_data['FTM'])) / final_data['PTS']) * 100))
    
    #--VISUALIZING THE DATA
    #create waffle chart
    fig = plt.figure(
            FigureClass=Waffle,
            plots={
                '311': {
                        'values': players_stats_pct,
                        'labels':["{0} ({1}%)".format(k,v) for k,v in players_stats_pct.items()],
                        'legend':{'loc':'lower center', 'bbox_to_anchor':(0.5,-0.2), 'ncol': len(players_stats_pct), 'framealpha': 0},
                        'title': {'label':'Percentage of Shooting Splits: '+ i}
                        }
                },
            rows=10,
            colors=("#0080FF", "#979EA3","#253744"),
            figsize=(18,10)
    )
    
    fig.gca().set_facecolor('#EEEEEE')
    fig.set_facecolor('#EEEEEE')
    plt.show()
    
    
    
    
