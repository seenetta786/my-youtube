import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ClickUpClient:
    def __init__(self):
        self.api_key = os.getenv("CLICKUP_API_KEY")
        if not self.api_key:
            raise ValueError("CLICKUP_API_KEY not found in .env file")
        self.base_url = "https://api.clickup.com/api/v2/"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"ClickUp API Http Error: {errh}")
            print(f"Status Code: {errh.response.status_code}")
            print(f"Response Body: {errh.response.text}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")
        return None

    def get_teams(self):
        """Get all teams (workspaces)"""
        return self._request("GET", "team")

    def get_spaces(self, team_id):
        """Get spaces for a team"""
        return self._request("GET", f"team/{team_id}/space")

    def get_folders(self, space_id):
        """Get folders in a space"""
        return self._request("GET", f"space/{space_id}/folder")

    def get_lists(self, folder_id):
        """Get lists in a folder"""
        return self._request("GET", f"folder/{folder_id}/list")

    def get_tasks(self, list_id):
        """Get tasks in a list"""
        return self._request("GET", f"list/{list_id}/task")

if __name__ == '__main__':
    # Example usage:
    client = ClickUpClient()
    teams = client.get_teams()
    if teams and teams.get('teams'):
        for team in teams['teams']:
            print(f"Team: {team['name']} (ID: {team['id']})")
    else:
        print("Could not retrieve teams. Check your API key and permissions.")

