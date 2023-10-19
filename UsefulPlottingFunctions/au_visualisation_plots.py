from load_data import politics_AU_cmap

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# tooltip
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import vaex

import matplotlib.pyplot as plt, seaborn as sns
import matplotlib as mpl

import math, string, re, pickle, json, time, os, sys, datetime, itertools

from tqdm.notebook import tqdm

import pandas as pd
import geopandas as gpd
import shutil

import dash_bootstrap_components as dbc


def compress_legend(fig):
   # mostly from https://community.plotly.com/t/plotly-express-how-to-separate-symbol-and-color-in-legend/38950/4 with some minor adaptions
   group1_base, group2_base  = fig.data[0].name.split(",")
   lines_marker_name = []
   for i, trace in enumerate(fig.data):
       part1,part2 = trace.name.split(',')
       if part1 == group1_base:
           if part2.lstrip(" ") not in set([x["name"] for x in lines_marker_name]):
                lines_marker_name.append({"marker": trace.marker.to_plotly_json(), "name": part2.lstrip(" ")})
       if part2 != group2_base:
           trace['name'] = ''
           trace['showlegend']=False
       else:
           trace['name'] = part1
   
   ## Add the line/markers for the 2nd group
   for lmn in lines_marker_name:
       lmn["marker"]["color"] = "black"
       fig.add_trace(go.Scatter(y=[None], mode = "markers", **lmn))
       
   fig.update_layout(legend_title_text='')

def geo_extras_scatterplot(var_interest, selected_label, fn):
    # load in data
    df_scatterplot = pd.read_csv(fn)

    # colour dict
    alpha = 0.8
    p_cmap = {k:"rgba"+str(tuple([255*j for j in v]+[alpha])) for k,v in politics_AU_cmap().items()}


    # set up figure

    fig = px.scatter(data_frame=df_scatterplot, 
                x=var_interest, 
                y='net_flow', 
                symbol='scale',
                color='SourceParty', 
                size = 'Population2017',
                size_max = 10, 
                hover_data=['Electorate','SourceParty','NumberNewsSources','net_flow'],
                color_discrete_map=p_cmap)

    compress_legend(fig)

    fig.update_layout(
        xaxis_title=selected_label,
        yaxis_title="Net Information Flow"
    )

    return fig

def get_hist_au_var(var_interest, selected_label, fn):
    # load in data
    df_scatterplot = pd.read_csv(fn)

    # colour dict
    alpha = 0.6
    p_cmap = {k:"rgba"+str(tuple([255*j for j in v]+[alpha])) for k,v in politics_AU_cmap().items()}


    # set up figure

    fig = px.histogram(data_frame=df_scatterplot, 
                x=var_interest, 
                color='SourceParty', 
                hover_data=['Electorate','SourceParty','NumberNewsSources','net_flow'],
                color_discrete_map=p_cmap,
                nbins=50)

    fig.update_layout(
        xaxis_title=selected_label,
        yaxis_title="Count",
        showlegend=False
    )

    return fig

def get_violin_au_var(fn):
    # load in data
    df_scatterplot = pd.read_csv(fn)

    # colour dict
    alpha = 0.6
    p_cmap = {k:"rgba"+str(tuple([255*j for j in v]+[alpha])) for k,v in politics_AU_cmap().items()}


    # set up figure

    fig = px.violin(data_frame=df_scatterplot, 
                y="net_flow", 
                color='SourceParty', 
                hover_data=['Electorate','SourceParty','NumberNewsSources','net_flow'],
                color_discrete_map=p_cmap)

    fig.update_layout(
        yaxis_title="Net Information Flow",
        # yaxis={'side': 'right'},
        showlegend=False
    )

    return fig

