import logging
from metaapi_cloud_sdk import MetaApi
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import panel as pn
import os
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

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

async def fetch_account(api):
    try:
        logger.info("Fetching account...")
        return await api.metatrader_account_api.get_account(account_id)
    except Exception as e:
        logger.error(f"Error fetching account: {e}")
        raise

async def fetch_positions(account):
    try:
        logger.info("Fetching positions...")
        # Ensure the account is deployed and connected to the broker
        if account.state not in ['DEPLOYED', 'DEPLOYING']:
            logger.info('Deploying account')
            await account.deploy()
        logger.info('Waiting for API server to connect to broker (may take a couple of minutes)')
        await account.wait_connected()

        # Connect to MetaApi API
        connection = account.get_streaming_connection()
        await connection.connect()

        # Wait until terminal state synchronized to the local state
        logger.info('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
        await connection.wait_synchronized()

        # Fetch current open positions without logging each position
        positions = connection.terminal_state.positions
        # Commented out to avoid cluttering the terminal
        # logger.info(f"Fetched {len(positions)} positions from MetaApi, not displaying them to avoid clutter")
        return positions
    except Exception as e:
        logger.error(f"Error fetching positions: {e}")
        raise

def store_positions(positions):
    try:
        logger.info("Storing positions in MongoDB...")
        positions_collection.insert_many(positions)
    except Exception as e:
        logger.error(f"Error storing positions in MongoDB: {e}")
        raise

def fetch_positions_from_db():
    try:
        positions_from_db = list(positions_collection.find())
        logger.info(f"Fetched {len(positions_from_db)} positions from MongoDB")
        return positions_from_db
    except Exception as e:
        logger.error(f"Error fetching positions from MongoDB: {e}")
        raise

def create_dataframe(positions):
    logger.info("Converting positions to DataFrame...")
    return pd.DataFrame(positions)

def create_panel_table(df):
    logger.info("Creating Panel table...")
    return pn.widgets.DataFrame(df, name='Positions')

async def main():
    # Create MetaApi instance
    api = MetaApi(api_token)

    account = await fetch_account(api)
    positions = await fetch_positions(account)
    # store_positions(positions)
    logger.info("Storing to MongoDB is currently disabled.")
    positions_from_db = fetch_positions_from_db()
    df = create_dataframe(positions_from_db)
    table = create_panel_table(df)
    # Commented out to avoid cluttering the terminal with the table data
    # logger.info("Displaying table...")
    # table.show()
    logger.info("Panel table has been created and is ready for display.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
