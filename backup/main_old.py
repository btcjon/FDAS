from metaapi_cloud_sdk import MetaApi
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from panel.widgets import Tabulator
import os
import asyncio
import panel as pn

# Load environment variables
load_dotenv()
print("Environment variables loaded.")

# Get MetaApi token and account id
api_token = os.getenv('META_API_TOKEN')
account_id = os.getenv('META_API_ACCOUNT_ID')

# Get MongoDB URI and database name
mongodb_uri = os.getenv('MONGODB_URI')
db_name = os.getenv('DB_NAME')

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[db_name]
positions_collection = db['positions']
print("Connected to MongoDB.")

async def fetch_account(api):
    try:
        return await api.metatrader_account_api.get_account(account_id)
    except Exception as e:
        raise

async def fetch_positions(account):
    try:
        # Ensure the account is deployed and connected to the broker
        if account.state not in ['DEPLOYED', 'DEPLOYING']:
            await account.deploy()
        await account.wait_connected()

        # Connect to MetaApi API
        connection = account.get_streaming_connection()
        await connection.connect()

        # Wait until terminal state synchronized to the local state
        await connection.wait_synchronized()

        # Fetch current open positions without logging each position
        positions = connection.terminal_state.positions
        # The detailed positions data is not logged to avoid cluttering the terminal
        return positions
    except Exception as e:
        raise

def store_positions(positions):
    try {
        positions_collection.insert_many(positions)
    except Exception as e:
        raise

def fetch_positions_from_db():
    try:
        positions_from_db = list(positions_collection.find())
        return positions_from_db
    except Exception as e:
        raise

def create_dataframe(positions):
    df = pd.DataFrame(positions)
    df = df.drop(columns=['_id'])
    return df

def create_panel_table(df):
    return Tabulator(df, pagination='remote', layout='fit_columns', frozen_rows=1, frozen_columns=1, name='Positions')

async def main():
    # Create MetaApi instance
    api = MetaApi(api_token)

    account = await fetch_account(api)
    print("Account information fetched.")
    positions = await fetch_positions(account)
    print(f"{len(positions)} positions fetched.")
    store_positions(positions)
    print(f"{positions_collection.count_documents({})} positions stored to MongoDB.")
    positions_from_db = fetch_positions_from_db()
    print("Positions fetched from MongoDB.")
    df = create_dataframe(positions_from_db)
    print("DataFrame created from positions.")
    table = create_panel_table(df)
    print("Panel table created from DataFrame.")
    
    # Serve the Panel table in the browser
    pn.serve(table)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())