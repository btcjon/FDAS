import logging
from metaapi_cloud_sdk import MetaApi
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import panel as pn
import os

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

# Create MetaApi instance
api = MetaApi(api_token)

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[db_name]
positions_collection = db['positions']

# Fetch account
logger.info("Fetching account...")
account = await api.metatrader_account_api.get_account(account_id)

# Fetch positions
logger.info("Fetching positions...")
positions = await account.get_positions()

# Store positions in MongoDB
logger.info("Storing positions in MongoDB...")
positions_collection.insert_many(positions)

# Fetch positions from MongoDB
logger.info("Fetching positions from MongoDB...")
positions_from_db = list(positions_collection.find())

# Convert positions to DataFrame
logger.info("Converting positions to DataFrame...")
df = pd.DataFrame(positions_from_db)

# Create Panel table
logger.info("Creating Panel table...")
table = pn.widgets.DataFrame(df, name='Positions')

# Display table
logger.info("Displaying table...")
table.show()