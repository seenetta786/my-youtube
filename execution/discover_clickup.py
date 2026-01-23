import json
from clickup_client import ClickUpClient

def discover():
    """
    Discovers the structure of the ClickUp workspace.
    """
    client = ClickUpClient()
    
    print("Discovering ClickUp Workspace...")
    
    teams = client.get_teams()
    if not teams or not teams.get('teams'):
        print("Could not retrieve teams.")
        return

    for team in teams['teams']:
        print(f"\nTeam: {team['name']} (ID: {team['id']})")
        spaces = client.get_spaces(team['id'])
        if not spaces or not spaces.get('spaces'):
            print("  No spaces found in this team.")
            continue

        for space in spaces['spaces']:
            print(f"  Space: {space['name']} (ID: {space['id']})")
            folders = client.get_folders(space['id'])
            if not folders or not folders.get('folders'):
                print("    No folders found in this space.")
                # Check for lists directly in the space
                # ClickUp API to get lists in a space is not straightforward,
                # lists can exist without folders.
                # For now, we only check for lists in folders.
                continue

            for folder in folders['folders']:
                print(f"    Folder: {folder['name']} (ID: {folder['id']})")
                lists = client.get_lists(folder['id'])
                if not lists or not lists.get('lists'):
                    print("      No lists found in this folder.")
                    continue
                
                for lst in lists['lists']:
                    print(f"      List: {lst['name']} (ID: {lst['id']})")


if __name__ == "__main__":
    discover()
