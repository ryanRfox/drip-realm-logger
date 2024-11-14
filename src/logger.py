import requests
from typing import Dict, List
from datetime import datetime
import pandas as pd
from .config import config
from database.models import LogEntry
from database.database import get_session
import json

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
            timestamp = datetime.strptime(log.get('timestamp'), '%a, %d %b %Y %H:%M:%S GMT')
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
                    event_type=log.get('type'),
                    guild_id=log.get('guild_id'),
                    receiver=str(log.get('receiver')),
                    sender=str(log.get('sender')) if log.get('sender') else None,
                    activity=log.get('data', {}).get('activity'),
                    amount=log.get('data', {}).get('amount'),
                    receiver_balance=log.get('data', {}).get('receiverBalance'),
                    sender_balance=log.get('data', {}).get('senderBalance'),
                    raw_data=log
                )
                session.add(log_entry)
        session.commit()

def sync_realm_logs(realm_id: str, api_base_url: str, api_token: str) -> None:
    """Fetch and store logs for a realm"""
    logs = fetch_realm_logs(realm_id, api_base_url, api_token)
    store_logs(logs)

def get_logs_as_dataframe(realm_id: str = None) -> 'pd.DataFrame':
    with get_session() as session:
        query = session.query(LogEntry)
        if realm_id:
            query = query.filter(LogEntry.realm_id == realm_id)
        
        # Convert SQLAlchemy results to pandas DataFrame
        df = pd.read_sql(query.statement, session.bind)
        
        # Drop the raw_data column as we don't need it for display
        if 'raw_data' in df.columns:
            df = df.drop(['raw_data'], axis=1)
        
        return df

# Get logs for a specific realm
sync_realm_logs(
        config.DRIP_ACCOUNT_ID, 
        config.DRIP_API_BASE_URL, 
        config.DRIP_API_KEY
)

# Display settings for pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', True)

# Get all logs
df = get_logs_as_dataframe()

# Convert DataFrame to JSON records
print("\nFull Data as JSON:")
json_records = df.to_dict(orient='records')
print(json.dumps(json_records, indent=2, default=str))

# Analysis with more detailed output
print("\nActivities Types Summary:")
print(df.groupby('activity').size().to_string())

print("\nRealm Summary:")
print(df.groupby('realm_id').size().to_string())

# Daily Event Summary
print("\nDaily Event Summary:")
daily_counts = df['timestamp'].dt.date.value_counts().sort_index()
print(daily_counts.to_string())