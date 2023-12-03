1. Data Fetching:
- Use MetaApi's RPC for one-time requests (e.g., account info, positions, orders). See ALL_rpcExample.py.
- Use MetaApi's Synchronization API for real-time state synchronization. See ALL_synchronizationExample.py.
- Use MetaApi's Streaming API for real-time updates (e.g., market data, account status). See ALL_streamingApi.rst.

2. Data Storage:
- Store fetched data in Atlas MongoDB, a scalable NoSQL database ideal for JSON-like documents.

3. Data Usage:
- Fetch stored data from MongoDB as needed. Create views or endpoints for specific data retrieval.

4. Visualization:
- Use Panel HoloViz for interactive data visualization. It works well with PyData tools (pandas, numpy, matplotlib).
- Panel "Template" to use?
    - We will start with the available ReactTemplate, built on react-grid-layout.

5. Implementation Steps:
- Establish MetaApi connection and fetch initial data via RPC API.
- Set up Synchronization API for state updates.
- Store fetched data in MongoDB.
- Set up Streaming API for real-time updates and store these in MongoDB.
- Build a Panel HoloViz app and fetch data from MongoDB for visualization.
- Update visualizations in real-time with data from the Streaming API.

6. Step-by-Step Implementation:
- For each type ('account_information', 'positions', 'orders', 'deals', 'history_orders'):
- Fetch data locally.
- Determine optimal fetch method (sync, real-time, or combination of both)
- Store data (Atlas mongoDB)
- Decide on visualization approach. (Panel widget)
- Test data retrieval from store to basic visualization (panel).
- Create and store additional calculated/manipulated data (aggregations, new fields, etc.).

# positions table

1. Data Fetching: We are using MetaApi's RPC for one-time requests to fetch initial data. For real-time updates, we are using MetaApi's Streaming API. This ensures that we always have the most up-to-date data.

2. Data Storage: We are storing the fetched data in MongoDB. This allows us to keep a historical record of the data, which is necessary for comparing metrics over time.

3. Data Usage: We are fetching the stored data from MongoDB as needed. This includes both the current data and historical data for comparison.

4. Real-Time Updates: We are using MongoDB's change streams feature to get real-time updates when the data changes. We are also using the stream method of the Panel Tabulator widget to update the front-end table in real-time.

5. Data Visualization: We are using Panel HoloViz for interactive data visualization. This allows us to present the data in a user-friendly way and update the visualizations in real-time.

6. Comparison Metrics: We are calculating certain metrics, such as the profit difference since yesterday or last week, based on the historical data stored in MongoDB. These metrics are updated each time new data is fetched.

This approach ensures that we always have the most up-to-date data, both for the current state and for historical comparisons. It also allows us to present the data in a user-friendly way and update the visualizations in real-time.