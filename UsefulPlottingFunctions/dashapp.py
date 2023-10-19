from dash import Dash
import dash_bootstrap_components as dbc


############ CACHING SETUP ############
import time
import os
from uuid import uuid4

# CACHING
from dash import Dash, html, DiskcacheManager, CeleryManager, Input, Output, callback

launch_uid = uuid4()

# if 'REDIS_URL' in os.environ:
#     # Use Redis & Celery if REDIS_URL set as an env variable
#     from celery import Celery
#     celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
#     background_callback_manager = CeleryManager(
#         celery_app, cache_by=[lambda: launch_uid], expire=60
#     )

# else:
    # Diskcache for non-production apps when developing locally
import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(
    cache, cache_by=[lambda: launch_uid], expire=60
)

# AESTHETICS
# figure templates
template_theme1 = "flatly"
template_theme2 = "darkly"

# themes
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# set up app
app = Dash(__name__, external_stylesheets=[url_theme1], background_callback_manager=background_callback_manager)