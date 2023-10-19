from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import numpy as np
from UsefulPlottingFunctions.plotting_functions import create_network_graph, create_flow_dist_plot
import dash_bootstrap_components as dbc
# tab content

from UsefulPlottingFunctions.dashapp import app

# funct to get network fig
fn = 'Data/sample_aggregated_net_information_flows.csv'
fn_ind = 'Data/sample_net_information_flows.csv'
var_interest = 'net_flow_2017'

# values for years
slider_values = ['2013', '2014','2015','2016','2017','2018','2019','2020','2021','All years']
slider_values = {i:slider_values[i] for i in range(len(slider_values))}

# parties
# import cmap
with open('supplementary_data/cmap.pkl', 'rb') as f:
    cmap = pickle.load(f)


parties = [{'label': html.Div([" " + k + " "], style={'color': v}), 'value': k} for k, v in cmap.items()]



# Layout of the app
agg_flow_layout = html.Div([
    html.Br(),
    dcc.Markdown('''
                The text from every account within each party was aggregated to create aggregated information flows. For a discussion of a similar procedure, see [this paper](https://link.springer.com/chapter/10.1007/978-3-031-19097-1_3).
                '''),
    html.Br(),
    # add slider to select years
    html.Div([
        html.Br(),
        html.H5('Select which parties to include:'),
        dbc.Checklist(options = parties, 
                      value = list(cmap.keys()), 
                      id='party_checklist_agg',
                      inline=False,
                      style={"font-size": "16px"},
                      labelStyle={"display": "inline-block"},#, "padding": "15px"},
                    ),
        html.Br(),
        html.H5('Select a year of interest, moving the slider all the way to the right will select all years between 2013 and 2023.'),
        dcc.Slider(0, 9, step=1, marks =slider_values, id='slider_agg', value = 9),
        html.Br(),
        html.H4('Network of aggregated information flows'),
        dcc.Graph(id='updated-network-plot_agg', 
                  figure=create_network_graph(fn , 'net_flow', list(cmap.keys()))),
    ]),
    html.Br(),
    html.H4('Distribution plot of aggregated information flows by party'),
    html.Div([
        dcc.Graph(id='dist-plot_agg', figure=create_flow_dist_plot(fn_ind, 'net_flow', list(cmap.keys())))
    ])
], className="dbc")


@callback(
    Output('updated-network-plot_agg', 'figure'),
    Input('slider_agg', 'value'),
    Input('party_checklist_agg', 'value'))
def update_figure(i, parties):
    var_interest = f'net_flow_{slider_values[i]}'
    if var_interest == 'net_flow_All years':
        var_interest = 'net_flow'
    return create_network_graph(fn , var_interest, parties)

# # subsequent box plot
@app.callback(
    Output('dist-plot_agg', 'figure'),
    Input('slider_agg', 'value'),
    Input('party_checklist_agg', 'value'))
def update_box_plot(i, parties):    
    
    var_interest = f'net_flow_{slider_values[i]}'
    if var_interest == 'net_flow_All years':
        var_interest = 'net_flow'

    return create_flow_dist_plot(fn_ind, var_interest, parties)



