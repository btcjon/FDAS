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
df = df[['symbol', 'type', 'volume', 'profit', 'swap', 'comment', 'time',  'magic']]  # Replace with your column names in the order you want
table = pn.widgets.Tabulator(df, page_size=40, hidden_columns=['index', '_id', 'id', 'platform', 'brokerTime', 'updateTime', 'realizedSwap', 'realizedCommission', 'reason', 'accountCurrencyExchangeRate', 'brokerComment' , 'updateSequenceNumber', 'currentTickValue', 'unrealizedSwap', 'commission', 'unrealizedComission', 'realizedProfit', 'unrealizedProfit', 'currentPrice'])
print(table)  # This will print the representation of the Panel table
print("Panel table created.")

# Define a function to update the table when new data arrives
def update_table(change):
    new_data = pd.DataFrame([change['fullDocument']])
    new_data['_id'] = new_data['_id'].astype(str)  # Convert ObjectId instances to strings
    print(new_data.head())  # This will print the first 5 rows of the new data
    table.stream(new_data)
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

    # Serve the table directly
    pn.serve(table)
    print("Panel table served in the browser.")

if __name__ == '__main__':
    asyncio.run(main())

