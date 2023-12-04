from metaapi_cloud_sdk import MetaApi
from dotenv import load_dotenv
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
import os
import asyncio
import time

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

async def fetch_and_update():
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
    count = 0
    for position in positions:
        collection.update_one({'id': position['id']}, {"$set": position}, upsert=True)
        count += 1
    print(f"{count} positions updated or inserted in MongoDB.")

# Create a background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: asyncio.run(fetch_and_update()), 'interval', minutes=5)  # Adjust the interval as needed
scheduler.start()

if __name__ == '__main__':
    asyncio.run(fetch_and_update())
    while True:
        time.sleep(15)  # Sleep for 1 second to prevent high CPU usage
