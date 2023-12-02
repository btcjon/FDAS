import os
import pandas as pd
import panel as pn
import asyncio
from dotenv import load_dotenv
from metaapi_cloud_sdk import MetaApi

# Load environment variables
load_dotenv()

token = os.getenv('TOKEN')
accountId = os.getenv('ACCOUNT_ID')

async def main():
    # Initialize MetaApi
    api = MetaApi(token)

    # Fetch account information
    account = await api.metatrader_account_api.get_account(accountId)

    # Get a streaming connection
    connection = account.get_streaming_connection()

    # Connect to the streaming API
    await connection.connect()

    # Wait until synchronization is completed
    await connection.wait_synchronized()

    # Access the terminal state
    terminalState = connection.terminal_state

    # Fetch the initial state of the positions
    positions = terminalState.positions

    # Convert the positions to a pandas DataFrame
    df = pd.DataFrame(positions)

    # Create a Panel DataFrame from the pandas DataFrame
    panel_df = pn.widgets.DataFrame(df)

    # Display the Panel DataFrame
    panel_df.show()

# Run the main function inside an asyncio event loop
asyncio.run(main())
