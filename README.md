# Drip Logs to Database

A Python application that fetches, stores, and analyzes Drip API log data.

## Project Structure

```
├── LICENSE            <- MIT License
├── README.md          <- Project documentation
├── data
│   └── database.db    <- SQLite database (gitignored)
│
├── database
│   ├── database.py    <- SQLAlchemy database connection setup
│   └── models.py      <- Database models and schemas
│
├── requirements.txt   <- Project dependencies
│
└── src                <- Source code
    ├── __init__.py            <- Makes src a Python module
    ├── config.py              <- Configuration management
    ├── logger.py              <- Main log processing logic
    └── services               <- External service integrations
        └── drip_service.py    <- Drip API client
```

## Data Flow

The application processes data through several stages:

1. **API Ingestion**
   - Fetches log data from Drip API using Bearer token authentication
   - Endpoint: `/api/v4/realms/{realm_id}/export_logs`
   - Handles pagination and rate limiting

2. **Data Storage**
   - Uses SQLAlchemy ORM with SQLite backend
   - Main table: `log_entries` with the following structure:
     ```
     - id (Primary Key)
     - realm_id
     - timestamp
     - event_type
     - guild_id
     - receiver
     - sender (nullable)
     - activity (nullable)
     - amount (nullable)
     - receiver_balance (nullable)
     - sender_balance (nullable)
     - raw_data (JSON)
     ```

3. **Data Processing**
   - Converts API response to structured database records
   - Handles data type conversions (e.g., timestamps, large integers)
   - Preserves original data in raw_data column
   - Prevents duplicate entries using realm_id + timestamp composite key

4. **Analysis & Display**
   - Loads data from SQLite into pandas DataFrame
   - Provides multiple analysis views:
     - Event type distribution
     - Realm activity summary
     - Daily event counts
   - Outputs formatted JSON and summary statistics

## Usage

1. Set up environment:
   ```
   cp .env.sample .env              # Configure environment variables
   pip install -r requirements.txt  # Install dependencies
   ```

2. Configure .env file:
   ```
   DRIP_API_BASE_URL=<your_api_url>
   HACKATHON_API_KEY=<your_api_key>
   HACKATHON_REALM_ID=<your_realm_id>
   PLAYER_DB_PATH=data/database.db
   ```

3. Run the application:
   ```
   python -m src.logger
   ```

## Output Format

The application generates several reports:
1. Full JSON data dump of all logs
2. Event Types Summary showing distribution of event types
3. Realm Summary showing activity per realm
4. Daily Event Summary showing temporal distribution

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.