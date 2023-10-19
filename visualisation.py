"""
Example of light and dark color modes available in
  dash-bootstrap-component >= 1.5.0
  dash-bootstrap-templates >= 1.1.0
"""

# dash related
from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
import dash_loading_spinners as dls

import pandas as pd
import numpy as np
import pickle


# tab content
from UsefulPlottingFunctions.dashapp import app
from UsefulPlottingFunctions.visualiation_aggregated_information_flows import agg_flow_layout
from UsefulPlottingFunctions.visualisation_individual_information_flows import ind_flow_layout
from UsefulPlottingFunctions.geo_tab import geo_layout

### SET UP

# AESTHETICS
# figure templates
template_theme1 = "flatly"
template_theme2 = "darkly"

# themes
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# load in data
df = px.data.stocks()

theme_switch = ThemeSwitchAIO(
    aio_id="theme", themes=[url_theme1, url_theme2]
)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Br(),
    html.H1(' Australian Information Landscape'),
    html.Br(),
    dcc.Markdown('''
        A visualisation of the information landscape in Australia and some socioeconomic indicators. Each geographical region is a federal electorate and can be mapped to a single member of the House of Representatives. All data shown in this visualisation is simulated and does not represent real information.
                 
        This dashboard was made using Dash and Plotly. All of the Twitter data was collected through the Twitter API.
        '''),
    html.Hr(),
    html.Br(),
    # dbc.Container([theme_switch], className="p-5"),
        dbc.Tabs(
            [
                dbc.Tab(label='Australian Context', tab_id='geo_layout'),
                dbc.Tab(label='Aggregated Information Flows', tab_id='agg_layout'),
                dbc.Tab(label='Individual Information Flows', tab_id='ind_layout')],
            active_tab='geo_layout',
            id='tabs'
        ),
    html.Div(id='tabs-content'),
    html.Br(),
    dcc.Markdown('''
        This dashboard was made by Bridget Smart. A version with sample data is available on [GitHub](https://github.com/bridget-smart/DashVisualisation).
        ''')
],
style={"padding": "15px"}
)

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'active_tab')])
def render_content(tab):
    if tab == 'agg_layout':
        return agg_flow_layout
    elif tab == 'ind_layout':
        return ind_flow_layout
    elif tab == 'geo_layout':
        return geo_layout
    
# app.css.append_css(
#     [
#         {
#             "selector": ".form-check-input:checked + .form-check-label",
#             "rule": "background-color: #007BFF; color: #fff; border-color: #007BFF;",
#         }
#     ]
# )
    

# # updating theme - removed 
# @app.callback(
#     Output("theme-switch-graph", "figure"),
#     Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
# )
# def update_graph_theme(toggle):
#     template = "darkly" if toggle else "flatly"
#     return px.line(df, x="date", y="GOOG", template=template)

# @app.callback(
#     Output("theme-switch-graph2", "figure"),
#     Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
# )
# def update_graph_theme(toggle):
#     template = "darkly" if toggle else "flatly"
#     return px.line(df, x="date", y="GOOG", template=template)


# run app
if __name__ == "__main__":
    app.run_server(debug=True)
 