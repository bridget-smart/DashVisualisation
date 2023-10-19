from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import numpy as np
from UsefulPlottingFunctions.plotting_functions import create_network_graph, create_box_plot
# tab content

from UsefulPlottingFunctions.dashapp import app

# funct to get network fig
fn_ind = 'Data/sample_net_information_flows.csv'
var_interest = 'net_flow_2017'

# values
slider_values = ['2013', '2014','2015','2016','2017','2018','2019','2020','2021','All years']
slider_values = {i:slider_values[i] for i in range(len(slider_values))}

# parties
# import cmap
with open('supplementary_data/cmap.pkl', 'rb') as f:
    cmap = pickle.load(f)


parties = [{'label': html.Div([" " + k + " "], style={'color': v}), 'value': k} for k, v in cmap.items()]



# Layout of the app
ind_flow_layout = html.Div([
    html.Br(),
    dcc.Markdown('''
                The pairwise information flow for each pair of accounts was calculated. Only instances where accounts had posted at least 200 Tweets were included.
                 
                 Use the slider to select a year of interest. The following plots will only show the pairwise information flows the selected year and accounts which are included in the selected parties.
                '''),
    html.Br(),
    # add slider to select years
    html.Div([
        html.H5('Select which parties to include:'),
        dcc.Checklist(options = parties, 
                      id='party_checklist',
                      value = list(cmap.keys()), 
                      inline=False,
                      style={"font-size": "16px"},
                      labelStyle={"display": "inline-block", "padding": "15px"}),
        html.Br(),
        html.H5('Select a year of interest, moving the slider all the way to the right will select all years between 2013 and 2023.'),
        html.Div([dcc.Slider(0, 9, step=1, marks =slider_values, id='slider', value = 9)], style={'width': '60%'}),
        html.Br(),
        html.H4('Network of aggregated information flows'),
        dcc.Graph(id='updated-network-plot', 
                  figure=create_network_graph(fn_ind , 'net_flow', list(cmap.keys())))
    ]),
    html.Br(),
    html.H4('Individual information flows grouped by party'),
    html.Div([
        dcc.Graph(id='box-plot', figure=create_box_plot(fn_ind, 'net_flow', list(cmap.keys())))
    ])
], className="dbc")

@callback(
    Output('updated-network-plot', 'figure'),
    Input('slider', 'value'),
    Input('party_checklist', 'value'))
def update_figure(i, parties):
    var_interest = f'net_flow_{slider_values[i]}'
    if var_interest == 'net_flow_All years':
        var_interest = 'net_flow'
    return create_network_graph(fn_ind , var_interest, parties)

# # subsequent box plot
@app.callback(
    Output('box-plot', 'figure'),
    Input('slider', 'value'),
    Input('party_checklist', 'value'))
def update_box_plot(i, parties):    
    
    var_interest = f'net_flow_{slider_values[i]}'
    if var_interest == 'net_flow_All years':
        var_interest = 'net_flow'

    return create_box_plot(fn_ind, var_interest, parties)
