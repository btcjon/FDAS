from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from panel.widgets import Tabulator
import os
import panel as pn
import threading
from panel.viewable import Layoutable
from panel.widgets import IntSlider
from panel.template import FastGridTemplate
from datetime import datetime
from panel.widgets import Checkbox
import time

# Load environment variables and check if they are set
load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')
db_name = os.getenv('DB_NAME')
if not mongodb_uri or not db_name:
    raise EnvironmentError("MONGODB_URI and/or DB_NAME environment variables are not set.")

print("Environment variables loaded and verified.")

# Create a MongoDB client with exception handling
try:
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force a call to check if connected
    db = client[db_name]
    collection = db['positions']
    print("MongoDB client created and connected.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

# Ensure the MongoDB client is closed properly when the script ends
import atexit
atexit.register(client.close)

def process_data(dataframe):
    dataframe['_id'] = dataframe['_id'].astype(str)  # Convert ObjectId instances to strings
    # Group by 'symbol' and 'type', and aggregate the other columns for df1
    df1 = dataframe.groupby(['symbol', 'type']).agg({
        'volume': 'sum',
        'unrealizedProfit': 'sum',
        'swap': 'sum',
        'openPrice': lambda x: (x * dataframe.loc[x.index, 'volume']).sum() / dataframe.loc[x.index, 'volume'].sum(),
        'time': 'min',  # Get the oldest time
        'magic': lambda x: ', '.join(f"{v}-{k}" for k, v in x.value_counts().items()),
        'comment': lambda x: ', '.join(f"{v}-{k}" for k, v in x.value_counts().items()),
        'profit': 'sum',
        'realizedProfit': 'sum',
        'unrealizedSwap': 'sum',
        'realizedSwap': 'sum',
    }).reset_index()

    # Ensure 'time' is in datetime format
    df1['time'] = pd.to_datetime(df1['time'])

    # Calculate 'Days'
    df1['Days'] = (datetime.now() - df1['time']).dt.days

    # Drop the 'time' column
    df1 = df1.drop(columns=['time'])

    # Get the current index of 'openPrice' and add 1 to place 'Days' right after it
    idx = df1.columns.get_loc('openPrice') + 1

    # Move 'Days' to right after 'openPrice'
    df1.insert(idx, 'Days', df1.pop('Days'))

    # rename columns for readability
    df1 = df1.rename(columns={'unrealizedProfit': 'uProfit', 'openPrice': 'BE'})

    # make 'type' prettier
    df1['type'] = df1['type'].replace({'POSITION_TYPE_BUY': 'BUY', 'POSITION_TYPE_SELL': 'SELL'})

    df1['uProfit'] = df1['uProfit'].map('${:,.0f}'.format)
    df1['swap'] = df1['swap'].map('${:,.0f}'.format)

    return df1

# Create a Panel table
df = pd.DataFrame(list(collection.find()))
df_processed = process_data(df)
print(df_processed.head())  # This will print the first 5 rows of the processed DataFrame

# Group by 'symbol' and 'type', and aggregate the other columns for df1
df1 = df.groupby(['symbol', 'type']).agg({
    'volume': 'sum',
    'unrealizedProfit': 'sum',
    'swap': 'sum',
    'openPrice': lambda x: (x * df.loc[x.index, 'volume']).sum() / df.loc[x.index, 'volume'].sum(),
    'time': 'min',  # Get the oldest time
    'magic': lambda x: ', '.join(f"{v}-{k}" for k, v in x.value_counts().items()),
    'comment': lambda x: ', '.join(f"{v}-{k}" for k, v in x.value_counts().items()),
    'profit': 'sum',
    'realizedProfit': 'sum',
    'unrealizedSwap': 'sum',
    'realizedSwap': 'sum',
}).reset_index()

# Ensure 'time' is in datetime format
df1['time'] = pd.to_datetime(df1['time'])

# Calculate 'Days'
df1['Days'] = (datetime.now() - df1['time']).dt.days

# Drop the 'time' column
df1 = df1.drop(columns=['time'])

# Get the current index of 'openPrice' and add 1 to place 'Days' right after it
idx = df1.columns.get_loc('openPrice') + 1

# Move 'Days' to right after 'openPrice'
df1.insert(idx, 'Days', df1.pop('Days'))

# rename columns for readability
df1 = df1.rename(columns={'unrealizedProfit': 'uProfit', 'openPrice': 'BE'})

# make 'type' prettier
df1['type'] = df1['type'].replace({'POSITION_TYPE_BUY': 'BUY', 'POSITION_TYPE_SELL': 'SELL'})

df1['uProfit'] = df1['uProfit'].map('${:,.0f}'.format)
df1['swap'] = df1['swap'].map('${:,.0f}'.format)

#disables editing in all columns
tabulator_editors = {col: None for col in df1.columns}

# positions_summary df1 - 1st table
positions_summary = pn.widgets.Tabulator(df1, page_size=40, layout='fit_data_fill', hidden_columns=['index', 'magic', 'comment', 'profit', 'realizedProfit', 'unrealizedSwap', 'realizedSwap'], sorters=[{
    'column': 'volume',
    'dir': 'desc'
}],editors=tabulator_editors, sizing_mode='stretch_both')

#start checkboxes to show
# Create Checkbox widgets
checkbox_magic = pn.widgets.Checkbox(name='Show magic', value=False)
checkbox_comment = pn.widgets.Checkbox(name='Show comment', value=False)
checkbox_profit = pn.widgets.Checkbox(name='Show profit', value=False)
checkbox_realizedProfit = pn.widgets.Checkbox(name='Show realizedProfit', value=False)
checkbox_unrealizedSwap = pn.widgets.Checkbox(name='Show unrealizedSwap', value=False)
checkbox_realizedSwap = pn.widgets.Checkbox(name='Show realizedSwap', value=False)

# Define callback functions
def callback_magic(event):
    hidden_columns = set(positions_summary.hidden_columns)
    if event.new:
        hidden_columns.discard('magic')
    else:
        hidden_columns.add('magic')
    positions_summary.hidden_columns = list(hidden_columns)

def callback_comment(event):
    hidden_columns = set(positions_summary.hidden_columns)
    if event.new:
        hidden_columns.discard('comment')
    else:
        hidden_columns.add('comment')
    positions_summary.hidden_columns = list(hidden_columns)

def callback_profit(event):
    hidden_columns = set(positions_summary.hidden_columns)
    if event.new:
        hidden_columns.discard('profit')
    else:
        hidden_columns.add('profit')
    positions_summary.hidden_columns = list(hidden_columns)

def callback_realizedProfit(event):
    hidden_columns = set(positions_summary.hidden_columns)
    if event.new:
        hidden_columns.discard('realizedProfit')
    else:
        hidden_columns.add('realizedProfit')
    positions_summary.hidden_columns = list(hidden_columns)

def callback_unrealizedSwap(event):
    hidden_columns = set(positions_summary.hidden_columns)
    if event.new:
        hidden_columns.discard('unrealizedSwap')
    else:
        hidden_columns.add('unrealizedSwap')
    positions_summary.hidden_columns = list(hidden_columns)

def callback_realizedSwap(event):
    hidden_columns = set(positions_summary.hidden_columns)
    if event.new:
        hidden_columns.discard('realizedSwap')
    else:
        hidden_columns.add('realizedSwap')
    positions_summary.hidden_columns = list(hidden_columns)

# Add callbacks to checkboxes
checkbox_magic.param.watch(callback_magic, 'value')
checkbox_comment.param.watch(callback_comment, 'value')
checkbox_profit.param.watch(callback_profit, 'value')
checkbox_realizedProfit.param.watch(callback_realizedProfit, 'value')
checkbox_unrealizedSwap.param.watch(callback_unrealizedSwap, 'value')
checkbox_realizedSwap.param.watch(callback_realizedSwap, 'value')

# positions_all df2 - 2nd table
df2 = df[['symbol', 'type', 'volume', 'profit', 'swap', 'openPrice', 'time', 'comment', 'magic']]
positions_all_grouped = pn.widgets.Tabulator(df2, groupby=['symbol', 'type'])

# Create a FastGridTemplate with dark theme
template = FastGridTemplate(
title='TTB FDAS',
theme='dark',
theme_toggle=True,
collapsed_sidebar=True,
sidebar_width=200,
prevent_collision=True,
header_background='#000000',  # Change to your desired color
logo='assets/images/ttb-logo-small-200.png'  # URL or local path to your logo
)

# Add the tables to the template's main area
template.sidebar.append(checkbox_magic)
template.sidebar.append(checkbox_comment)
template.sidebar.append(checkbox_profit)
template.sidebar.append(checkbox_realizedProfit)
template.sidebar.append(checkbox_unrealizedSwap)
template.sidebar.append(checkbox_realizedSwap)
template.main[0:6, 0:7] = positions_summary
template.main[6:12, 0:7] = positions_all_grouped


# This block is already correct and does not need to be replaced.

# Define a function to process and update the tables with new data
def process_and_update_tables(new_data):
    processed_data = process_data(new_data)
    # Update the positions_summary table
    positions_summary.value = processed_data
    # Update the positions_all_grouped table with the original new data, not processed
    positions_all_grouped.value = new_data

# Define a function to handle change stream documents
import logging

# Configure logging at the top of your script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_change_stream(change):
    logging.info(f"Change detected: Operation {change['operationType']} on document {change['documentKey']['_id']}")
    if change['operationType'] in ['insert', 'update', 'replace']:
        new_data = change.get('fullDocument')
        if new_data:
            logging.info(f"Processing new data: {new_data}")
            # Convert new_data to a DataFrame
            new_data_df = pd.DataFrame([new_data])
            # Process and update the tables with the new data
            process_and_update_tables(new_data_df)
    elif change['operationType'] == 'delete':
        # Handle delete operation if necessary
        pass

# This block is already correct and does not need to be replaced.

# Function to periodically fetch data from the database and update the tables
def periodic_fetch_and_update():
    df = pd.DataFrame(list(collection.find()))
    process_and_update_tables(df)

# Start the periodic data fetch and update immediately when the script is run
def start_periodic_callback():
    pn.state.add_periodic_callback(periodic_fetch_and_update, period=60000, start=True)

# Call the function to start the periodic callback
start_periodic_callback()

# Serve the Panel application
pn.serve(template, show=True, start=False)
