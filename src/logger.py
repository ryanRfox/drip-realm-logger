import requests
from typing import Dict, List
from datetime import datetime
import pandas as pd
from .config import config
from database.models import LogEntry
from database.database import get_session

def fetch_realm_logs(realm_id: str, api_base_url: str, api_token: str) -> List[Dict]:
    """Fetch logs from the API for a specific realm"""
    headers = {"Authorization": f"Bearer {api_token}"}
    url = f"{api_base_url}/api/v4/realms/{realm_id}/export_logs"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def store_logs(logs: List[Dict]) -> None:
    """Store logs in the database"""
    with get_session() as session:
        for log in logs:
            # Convert RFC 2822 timestamp to datetime object
            timestamp = datetime.strptime(log.get('timestamp'), '%a, %d %b %Y %H:%M:%S GMT')
            
            # Use guild_id as realm_id if realm_id is not present
            realm_id = log.get('realm_id') or log.get('guild_id')
            
            if not realm_id:
                raise ValueError(f"Log entry missing required realm_id/guild_id: {log}")
            
            existing_record = session.query(LogEntry).filter_by(
                realm_id=realm_id, 
                timestamp=timestamp
            ).first()
            
            if not existing_record:
                log_entry = LogEntry(
                    realm_id=realm_id,
                    timestamp=timestamp,
                    event_type=log.get('type'),  # Changed from 'event_type' to 'type'
                    data=log
                )
                session.add(log_entry)
        session.commit()

def sync_realm_logs(realm_id: str, api_base_url: str, api_token: str) -> None:
    """Fetch and store logs for a realm"""
    logs = fetch_realm_logs(realm_id, api_base_url, api_token)
    store_logs(logs)

def get_logs_as_dataframe(realm_id: str = None) -> 'pd.DataFrame':
    """
    Fetch logs from database and return as a pandas DataFrame.
    Optionally filter by realm_id.
    
    Returns:
        pd.DataFrame with columns: realm_id, timestamp, event_type, data
    """
    with get_session() as session:
        query = session.query(LogEntry)
        if realm_id:
            query = query.filter(LogEntry.realm_id == realm_id)
        
        # Convert SQLAlchemy results to pandas DataFrame
        df = pd.read_sql(query.statement, session.bind)
        
        # Convert timestamp strings to datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df

# Get logs for a specific realm
sync_realm_logs(
        config.DRIP_ACCOUNT_ID, 
        config.DRIP_API_BASE_URL, 
        config.DRIP_API_KEY
)

# Get all logs
df = get_logs_as_dataframe()

# Basic analysis examples:
print(df.head())  # View first 5 rows
print(df.info())  # Get column info and data types
print(df.describe())  # Get basic statistics

# Filter and analyze
print(df.groupby('event_type').count())  # Count events by type
print(df.groupby('realm_id').size())  # Count events by realm

# Time-based analysis
print(df.set_index('timestamp').resample('1D').count())  # Daily event counts