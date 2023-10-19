"""
Preamble for most code and jupyter notebooks
@author: bridgetsmart
@notebook date: 25 Aug 2023
"""
import logging
import numpy as np, pandas as pd

import matplotlib.pyplot as plt, seaborn as sns
import matplotlib as mpl

import math, string, re, pickle, json, time, os, sys, datetime, itertools

from tqdm.notebook import tqdm

import pandas as pd
import geopandas as gpd
import shutil



# tooltip
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import vaex

import dash_bootstrap_components as dbc

fn_all = "Data/news_by_electorate_with_info_flows.csv"

from UsefulPlottingFunctions.au_visualisation_plots import *
# import dash_leaflet as dl
# from dash_extensions.enrich import Input, Output, State, Dash

# load in data
FED = np.load('supplementary_data/FED_unique.npy', allow_pickle=True)

# mapping to better human readable names for variables
variable_dict = {
# 'Demographic classification':{'Demographic classification':'DemographicClassification'},
#                 'State or Territory' :{'State or Territory':'StateTerritory'},
                'Population':{'Population in 2017': 'Population2017'},
                'Ages':{'0 to 17 years':'Age0_17',
                        '18 to 34 years':'Age18_34',
                        '35 to 49 years':'Age35_49',
                        '50 to 64 years':'Age50_64',
                        '65 to 79 years':'Age65_79',
                        '80 years and over':'Age80_up'},
                'Family Dynamic':{'Couple with\nno children': 'CoupleNoChild',
                        'Couple with children': 'CoupleChild',
                        'Single parent family': 'OneParentFamily',
                        'Other': 'OtherFamily'},
                'Income':{'Median weekly\nhousehold income':'MedianWeeklyHouseholdIncome'},
                'Housing costs':{'Median weekly rent':'MedianWeeklyRent',
                                'Median monthly\nmortgage repayment': 'MedianMonthlyMortgageRepayments'},
                'Housing type': {'Owned outright': 'OwnedOutright',
                                    'Owned with a mortgage': 'OwnedMortgage',
                                    'Rented': 'Rented',
                                    'Other': 'OtherTenure'},
                'Family background' : {'Aboriginal and/or\nTorres Strait Islander': 'AboriginalTorresStraitIslander',
                                        'Born overseas': 'BornOverseas',
                                        'Migrated between 2006 and 2016': 'RecentMigrants2006_2016',
                                        'Language other than\nEnglish spoken at home': 'LanguageOtherThanEnglish'},
                'Education': {'Year 12 or equivalent': 'Yr12',
                                'Certificate III or higher':'CIII_Plus'},
                'Occupation': {'Professionals': 'Professionals',
                                'Managers': 'Managers',
                                'Technicians and Trades Workers': 'TechniciansTradesWorkers',
                                'Community and Personal\nService Workers': 'CommunityPersonalServiceWorkers',
                                'Clerical and\nAdministrative Workers': 'ClericalAdministrativeWorkers',
                                'Sales Workers': 'SalesWorkers',
                                'Machinery Operators\nand Drivers': 'MachineryOperatorsDrivers',
                                'Labourers': 'Labourers'},
                'News availability' : {'Number of news sources (all)': 'NumberNewsSources',
                                        'Number of news sources (radio)': 'NumberNewsSourcesRadio',
                                        'Number of news sources (television)': 'NumberNewsSourcesTelevision',
                                        'Number of news sources (digital)': 'NumberNewsSourcesDigital',
                                        'Number of news sources (print)': 'NumberNewsSourcesPrint'},
                }

# read in json
with open('geospatialdata/geojson_t.json') as f:
    jgeo_json = json.load(f)

vaex_df = vaex.read_csv('Data/commonwealth electorate data - with num news sources.csv')
vaex_df = vaex_df[vaex_df.id.isin(FED)]

# commented out PANDAS version
# load in data from electorates
# electorate_data = pd.read_csv('Data/commonwealth electorate data - with num news sources.csv.csv')

# electorate_data = electorate_data[electorate_data['id'].isin(FED)]


# Make sure the data is cached locally
used_columns = list(vaex_df.columns)
for col in used_columns:
    # print(f'Making sure column "{col}" is cached...')
    vaex_df.nop(col, progress=False)

# change columns to categorical
vaex_df.ordinal_encode(column='StateTerritory')
vaex_df.ordinal_encode(column='DemographicClassification')



# # def to make geoplot
# def geo_plot_pandas(df, selected_variable, selected_label):
#     fig = px.choropleth_mapbox(df, 
#                             geojson = jgeo_json,
#                             locations='id', 
#                             featureidkey="properties.CED_NAME21",
#                             color=selected_variable,
#                             color_continuous_scale="Viridis",
#                             # range_color=(0, 1),
#                             mapbox_style="carto-positron",
#                             zoom=3,
#                             center = {"lat": -28.5299, "lon": 134.2117},
#                             opacity=0.8,
#                             labels={'id':'Electorate ',selected_variable:selected_label + " "}
#                             )
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     return fig

def get_label(value_chosen, options):
    # get label from options dictionary
    the_label = [x['label'] for x in options if x['value'] == value_chosen]
    return the_label[0]


# def create_selection_pandas(pd_df, var_of_interest):
#     '''
#     Function to create selection of data (df) based on variable of interest (column name)

#     Returns dataframe and selection
#     '''
#     selection = None
#     if var_of_interest:
#         df = pd_df[['id',var_of_interest]]
#         selection = True
#     return df, selection


def vaex_sub_dataframe_to_dict(vaex_df, selected_variable):
    '''
    Filter by columns and return a dict for making geomap
    '''
    df_ = vaex_df.copy() # create shallow copy to manage multiple users

    di_ = df_[['id',selected_variable]].to_dict()
    return di_

# modify this function to use a vaex dataframe rather than a pandas one
def geo_plot_vaex(di, selected_variable, selected_label):
    
    fig = px.choropleth_mapbox(di, 
                            geojson = jgeo_json,
                            locations='id', 
                            featureidkey="properties.CED_NAME21",
                            color=selected_variable,
                            color_continuous_scale="Viridis",
                            # range_color=(0, 1),
                            mapbox_style="carto-positron",
                            zoom=3,
                            center = {"lat": -28.5299, "lon": 134.2117},
                            opacity=0.8,
                            labels={'id':'Electorate ',selected_variable:selected_label + " "}
                            )
    # coloraxis_colorbar=dict(
    #     title="%",  # Label for the color bar
    #     tickformat='%'),  # Format for tick labels as percentages

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


geo_layout = html.Div(
    [    html.Br(),
     dcc.Markdown('''
                  Use the two dropdowns to select a variable of interest. To make things more simple, the variables have been grouped into categories. 

                  The variable of interest is then mapped to each electorate. The darker the colour, the higher the value of the variable of interest. This data comes from several sources, including the Australian Bureau of Statistics, the Australian Electoral Commission and The Australian News Data Report.
                  '''),
        html.Br(),

        dbc.Row([
        dbc.Col([
            dcc.Markdown('##### Select a category of interest:'),
            dcc.Dropdown(
                list(variable_dict.keys()),
                'Population',
                id='category-dropdown',
                style={'width': '420px'}
            )], width=5),

        dbc.Col([
            dcc.Markdown('##### Select a variable of interest:'),
            dcc.Dropdown(id='variable-dropdown', style={'width': '420px'}
                        )], width=6),
        ]),

        html.Br(),
        # geoplot
        dcc.Graph(id='updated-geoplot', 
                    figure = geo_plot_vaex(vaex_sub_dataframe_to_dict(vaex_df, 'Population2017'), 'Population2017', 'Population in 2017'),
                    config={"modeBarButtonsToRemove": ['lasso2d', 'select2d']}),
        html.Br(),
        dcc.Markdown('##### Net information flow out of the Twitter accounts against the selected variable'),
        dcc.Markdown('Plots showing the net information flow out of the Twitter accounts against the selected variable for each of the 2019 and 2022 House of Representative members, coloured by party.'),
        dcc.Graph(id='updated-geoscatter',figure = geo_extras_scatterplot('Population2017', 'Population in 2017', fn_all)),
        dbc.Container([
                        dbc.Row([
                                dbc.Col([dcc.Markdown('##### Distribution of the selected variable, coloured by party'),
                                    dcc.Graph(id='updated-geohist',figure = get_hist_au_var('Population2017', 'Population in 2017', fn_all))],
                                    width=7,
                                ),
                                dbc.Col([dcc.Markdown('##### Net information flow out of each account, coloured by party'),
                                    dcc.Graph(id='violinplot',figure = get_violin_au_var(fn_all))],
                                    width=5,
                                )
                            ],
                            className="h-5",
                        ),
                    ]),
        dcc.Markdown('''
                  The [Australian News Data Report](https://newsindex.piji.com.au/) (ANDR) assesses media diversity and plurality. It also identify communities lacking fair and equal access to public interest journalism, local news, and news infrastructure to keep them safe during emergencies. 
                     
                    The Australian Bureau of Statistics (ABS) has deidentified census data available [here](https://data.gov.au/home).
                    ''')
    ],
    className="dbc"
)



@callback(
    Output('variable-dropdown', 'options'),
    Input('category-dropdown', 'value'))
def update_value_options(selected_category):
    return [{'label':k, 'value':v} for k,v in variable_dict[selected_category].items()]


@callback(
    Output('variable-dropdown', 'value'),
    Input('variable-dropdown', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value'] # set default to first value

@callback(
    Output('updated-geoplot', 'figure'),
    Input('variable-dropdown', 'value'),
    Input('variable-dropdown', 'options'))
def update_figure(selected_variable, options, vaex_df=vaex_df):
    # get label from options dictionary
    selected_label = get_label(selected_variable, options)
    # filter df to dict using shallow copy to allow multiple users
    di_ = vaex_sub_dataframe_to_dict(vaex_df, selected_variable)
    # make fig
    fig = geo_plot_vaex(di_, selected_variable, selected_label)

    return fig

@callback(
    Output('updated-geoscatter', 'figure'),
    Input('variable-dropdown', 'value'),
    Input('variable-dropdown', 'options'))
def update_figure(selected_variable, options, fn=fn_all):
    # get label from options dictionary
    selected_label = get_label(selected_variable, options)
    # filter df to dict using shallow copy to allow multiple users
    # make fig
    fig = geo_extras_scatterplot(selected_variable, selected_label, fn_all)

    return fig

@callback(
    Output('updated-geohist', 'figure'),
    Input('variable-dropdown', 'value'),
    Input('variable-dropdown', 'options'))
def update_figure(selected_variable, options, fn=fn_all):
    # get label from options dictionary
    selected_label = get_label(selected_variable, options)
    # filter df to dict using shallow copy to allow multiple users
    # make fig
    fig = get_hist_au_var(selected_variable, selected_label, fn_all)

    return fig



