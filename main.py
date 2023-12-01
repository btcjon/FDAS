import os
import asyncio
import json
from metaapi_cloud_sdk import MetaApi
from datetime import datetime, timedelta
from dotenv import load_dotenv
from airtable import Airtable
from collections import defaultdict

load_dotenv()

token = os.getenv('TOKEN')
accountId = os.getenv('ACCOUNT_ID')

# Initialize Airtable client for the 'Positions' table
airtable_api_key = os.getenv('AIRTABLE_API_KEY')
airtable_base_id = os.getenv('AIRTABLE_BASE_ID')
airtable_table_name = 'Positions'
airtable = Airtable(airtable_base_id, airtable_table_name, api_key=airtable_api_key)

def convert_position_to_airtable_format(position):
    # Convert position data to match Airtable structure
    airtable_position = {
        'Symbol': position['symbol'],
        'Type': position['type'],
        'Volume': position['volume'],
        'Profit': position['profit'],
        'Swap': position['swap'],
        'Commission': position['commission'],
        'Times': position['times'],
        'Count': position['Count'],
        'Oldest': position['Oldest'],  
        'Comments': position['Comments'],
    }
    return airtable_position

async def get_positions():
    api = MetaApi(token)
    try:
        account = await api.metatrader_account_api.get_account(accountId)

        print('Waiting for API server to connect to broker (may take couple of minutes)')
        await account.wait_connected()

        connection = account.get_rpc_connection()
        await connection.connect()

        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
        await connection.wait_synchronized()

        print('Getting positions')
        positions = await connection.get_positions()

        # Fetch all existing records from the 'Positions' table
        existing_records = airtable.get_all()

        # Create a dictionary of existing records keyed by 'Symbol' and 'Type'
        existing_records_dict = {(record['fields']['Symbol'], record['fields']['Type']): record for record in existing_records}

        # Aggregate positions by 'Symbol' and 'Type'
        aggregated_positions = defaultdict(lambda: defaultdict(float))
        for position in positions:
            key = (position['symbol'], position['type'])
            aggregated_positions[key]['symbol'] = position['symbol']
            aggregated_positions[key]['type'] = position['type']
            aggregated_positions[key]['volume'] += position.get('volume', 0)
            aggregated_positions[key]['profit'] += position.get('profit', 0)
            aggregated_positions[key]['swap'] += position.get('swap', 0)
            aggregated_positions[key]['commission'] += position.get('commission', 0)
            time_str = str(position['time'])
            if 'times' not in aggregated_positions[key] or not aggregated_positions[key]['times']:
                aggregated_positions[key]['times'] = time_str
            else:
                aggregated_positions[key]['times'] += ', ' + time_str
            if 'Count' not in aggregated_positions[key]:
                aggregated_positions[key]['Count'] = 1
            else:
                aggregated_positions[key]['Count'] += 1
            if 'Oldest' not in aggregated_positions[key] or time_str < aggregated_positions[key]['Oldest']:
                aggregated_positions[key]['Oldest'] = time_str
            comment_str = str(position.get('comment', 'na')) if position.get('comment') is not None else 'na'
            if 'Comments' not in aggregated_positions[key] or not aggregated_positions[key]['Comments']:
                aggregated_positions[key]['Comments'] = comment_str
            else:
                aggregated_positions[key]['Comments'] += ', ' + comment_str

        # Update existing records or insert new records in Airtable
        for key, position in aggregated_positions.items():
            airtable_position = convert_position_to_airtable_format(position)
            if key in existing_records_dict:
                # Update the existing record
                airtable.update(existing_records_dict[key]['id'], airtable_position)
            else:
                # Insert a new record
                airtable.insert(airtable_position)

        # Delete records in Airtable that do not correspond to any open position
        for key, record in existing_records_dict.items():
            if key not in aggregated_positions:
                airtable.delete(record['id'])

    except Exception as err:
        print(api.format_error(err))

async def main():
    while True:
        await get_positions()
        await asyncio.sleep(240)

asyncio.run(main())
