from metaapi_cloud_sdk import MetaApi
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

# Load environment variables
load_dotenv()
print("Environment variables loaded.")

# Get MetaApi token and account id
api_token = os.getenv('META_API_TOKEN')
account_id = os.getenv('META_API_ACCOUNT_ID')
print("MetaApi token and account id retrieved.")

# Get MongoDB URI and database name
mongodb_uri = os.getenv('MONGODB_URI')
db_name = os.getenv('DB_NAME')
print("MongoDB URI and database name retrieved.")

# Create a MongoDB client
client = MongoClient(mongodb_uri)
db = client[db_name]
collection = db['positions']
print("MongoDB client created.")

# Create a change stream
change_stream = collection.watch()
print("Change stream created.")

# Create a Panel table
df = pd.DataFrame(list(collection.find()))
df['_id'] = df['_id'].astype(str)  # Convert ObjectId instances to strings
print(df.head())  # This will print the first 5 rows of the DataFrame

# Group by 'symbol' and 'type', and aggregate the other columns for df1
df1 = df.groupby(['symbol', 'type']).agg({
    'volume': 'sum',
    'profit': 'sum',
    'swap': 'sum',
    'openPrice': lambda x: (x * df.loc[x.index, 'volume']).sum() / df.loc[x.index, 'volume'].sum(),
    'time': 'min',  # Get the oldest time
    'magic': lambda x: ', '.join(f"{v}-{k}" for k, v in x.value_counts().items()),
    'comment': lambda x: ', '.join(f"{v}-{k}" for k, v in x.value_counts().items())
}).reset_index()

# Ensure 'time' is in datetime format
df1['time'] = pd.to_datetime(df1['time'])

# Calculate 'Days Old'
df1['Days Old'] = (datetime.now() - df1['time']).dt.days

# Drop the 'time' column
df1 = df1.drop(columns=['time'])

# Get the current index of 'openPrice' and add 1 to place 'Days Old' right after it
idx = df1.columns.get_loc('openPrice') + 1

# Move 'Days Old' to right after 'openPrice'
df1.insert(idx, 'Days Old', df1.pop('Days Old'))

#disables editing in all columns
tabulator_editors = {col: None for col in df1.columns}

# positions_summary df1 - 1st table
positions_summary = pn.widgets.Tabulator(df1, page_size=40, layout='fit_data_table', hidden_columns=['index'], sorters=[{
    'column': 'volume',
    'dir': 'desc'
}],editors=tabulator_editors)

# positions_all df2 - 2nd table
df2 = df[['symbol', 'type', 'volume', 'profit', 'swap', 'openPrice', 'time', 'comment', 'magic']]
#positions_all = pn.widgets.Tabulator(df2, page_size=40, hidden_columns=['index', '_id', 'id', 'platform', 'brokerTime', 'updateTime', 'realizedSwap', 'realizedCommission', 'reason', 'accountCurrencyExchangeRate', 'brokerComment' , 'updateSequenceNumber', 'currentTickValue', 'unrealizedSwap', 'commission', 'unrealizedCommission', 'realizedProfit', 'unrealizedProfit', 'currentPrice'])
#print(positions_all)  # This will print the representation of the Panel table
#print("Panel table created.")

# Create a Tabulator widget for the grouped DataFrame
positions_all_grouped = pn.widgets.Tabulator(df2, groupby=['symbol', 'type'])
# Print the Tabulator widget
print(positions_all_grouped)


def update_table(change):
    new_data = pd.DataFrame([change['fullDocument']])
    new_data['_id'] = new_data['_id'].astype(str)  # Convert ObjectId instances to strings
    print(new_data.head())  # This will print the first 5 rows of the new data
    positions_all.stream(new_data)
    print("Table updated.")

def listen_to_changes():
    for change in change_stream:
        update_table(change)

# Start a new thread for the change stream listener
change_stream_thread = threading.Thread(target=listen_to_changes)
change_stream_thread.start()

async def main():
    # Create a MetaApi instance
    api = MetaApi(api_token)
    print("MetaApi instance created.")

    # Fetch account and create a streaming connection
    account = await api.metatrader_account_api.get_account(account_id)
    connection = account.get_streaming_connection()
    await connection.connect()

    # Wait until synchronization completed
    await connection.wait_synchronized()

    # Access local copy of terminal state
    terminalState = connection.terminal_state

    # Access positions from the terminal state
    positions = terminalState.positions
    print("Account and positions fetched.")

    # Store positions in MongoDB
    for position in positions:
        if not collection.find_one({'id': position['id']}):
            collection.insert_one(position)
    print("Positions stored in MongoDB.")

    # Create a FastGridTemplate with dark theme
    template = FastGridTemplate(
    title='',
    theme='dark',
    prevent_collision=True,
    header_background='#000000',  # Change to your desired color
    logo='assets/images/ttb-logo-small-200.png'  # URL or local path to your logo
)

    # Add the tables to the template's main area
    template.main[0:6, 0:7] = positions_summary
    template.main[6:12, 0:7] = positions_all_grouped

    # Serve the template instead of the table
    pn.serve(template)
    print("Panel table served in the browser.")

if __name__ == '__main__':
    asyncio.run(main())
