import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import base64
import io
import os

from .database import ISO42001Database
from . import __version__
from .layout import (
    create_app_layout, 
    render_assets_tab, 
    render_risks_tab, 
    render_controls_tab, 
    render_incidents_tab, 
    render_compliance_tab, 
    render_admin_tab,
    get_version_major_minor
)

# Initialize the database
db = ISO42001Database()

# Initialize Dash app with IBM Carbon theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = f"ISO 42001 Bookkeeping System {get_version_major_minor()}"

# Set the app layout
app.layout = create_app_layout()

@callback(Output('tab-content', 'children'),
          Input('main-tabs', 'value'))
def render_tab_content(active_tab):
    """Render content based on active tab"""
    if active_tab == 'assets':
        return render_assets_tab()
    elif active_tab == 'risks':
        return render_risks_tab()
    elif active_tab == 'controls':
        return render_controls_tab()
    elif active_tab == 'incidents':
        return render_incidents_tab()
    elif active_tab == 'compliance':
        return render_compliance_tab()
    elif active_tab == 'admin':
        return render_admin_tab()
    
    return html.Div()

# Import callbacks after app is defined
from . import callbacks