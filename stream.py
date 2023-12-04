from metaapi_cloud_sdk import MetaApi, SynchronizationListener
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from panel.widgets import Tabulator
import os
import asyncio
import panel as pn
import threading
from panel.viewable import Layoutable
from panel.widgets import IntSlider
from panel.template import FastGridTemplate
from datetime import datetime
from panel.widgets import Checkbox

# Load environment variables
load_dotenv()
print("Environment variables loaded.")

# Get MetaApi token and account id
api_token = os.getenv('META_API_TOKEN')
account_id = os.getenv('META_API_ACCOUNT_ID')
print("MetaApi token and account id retrieved.")

# Create a FastGridTemplate with dark theme
template = FastGridTemplate(
    title='Stream Positions',
    theme='dark',
    theme_toggle=True,
    collapsed_sidebar=True,
    sidebar_width=250,
    prevent_collision=True,
    header_background='#000000',  # Change to your desired color
    logo='assets/images/ttb-logo-small-200.png'  # URL or local path to your logo
)

# Create a Tabulator widget
positions = pd.DataFrame(...)
tabulator = pn.widgets.Tabulator(positions)
template.main[0:6, 0:7] = tabulator

# Define a function to stream new data to the Tabulator
def stream_positions(new_positions):
    # Assuming 'new_positions' is a DataFrame with new data
    tabulator.stream(new_positions)

# Stream new data every 1000ms (i.e., 1 second)
pn.state.add_periodic_callback(stream_positions, period=1000)

# Serve the template instead of the table
pn.serve(template)
print("Panel table served in the browser.")

print("MetaApi token and account id retrieved.")

