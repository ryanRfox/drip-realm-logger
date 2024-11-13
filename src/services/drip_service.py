import requests
from ..config import (
    DRIP_API_BASE_URL,
    DRIP_API_KEY,
    DRIP_ACCOUNT_ID
)

""" Optional query params for export_logs endpoint:
types: string['all', 'transaction', 'tip', 'quest', 'store', 'prize']
days: int
count: int
users: string[] of userIds

Append '?parameter=value' to the endpoint URL to filter the logs. 
  e.g. `/api/v4/realms/:id/export_logs?days=0` will return logs from today.
 """
 
class DripService:
    def __init__(self, use_oauth=False, access_token=None):
        self.base_url = DRIP_API_BASE_URL
        self.account_id = DRIP_ACCOUNT_ID
        
        # Set up authentication headers
        if use_oauth and access_token:
            self.headers = {
                'Authorization': f'Bearer {access_token}',
                'User-Agent': 'Your App Name (www.yourapp.com)',
                'Content-Type': 'application/json'
            }
        else:
            self.headers = {
                'Authorization': f'Basic {DRIP_API_KEY}:',
                'User-Agent': 'Your App Name (www.yourapp.com)',
                'Content-Type': 'application/json'
            }

    def make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json() 