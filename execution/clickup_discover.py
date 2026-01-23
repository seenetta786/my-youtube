import os
import json
from clickup_universal import clickup_request

def discover_hierarchy():
    print("Discovering ClickUp Hierarchy...")
    
    # 1. Get Teams (Workspaces)
    teams = clickup_request("team")["teams"]
    hierarchy = []
    
    for team in teams:
        team_data = {
            "id": team["id"],
            "name": team["name"],
            "spaces": []
        }
        
        # 2. Get Spaces
        spaces = clickup_request(f"team/{team['id']}/space")["spaces"]
        for space in spaces:
            space_data = {
                "id": space["id"],
                "name": space["name"],
                "folders": [],
                "lists": [] # Folderless lists
            }
            
            # 3. Get Folders
            folders = clickup_request(f"space/{space['id']}/folder")["folders"]
            for folder in folders:
                folder_data = {
                    "id": folder["id"],
                    "name": folder["name"],
                    "lists": []
                }
                
                # 4. Get Lists in Folders
                lists = clickup_request(f"folder/{folder['id']}/list")["lists"]
                for lst in lists:
                    folder_data["lists"].append({"id": lst["id"], "name": lst["name"]})
                
                space_data["folders"].append(folder_data)
            
            # 5. Get Folderless Lists
            lists = clickup_request(f"space/{space['id']}/list")["lists"]
            for lst in lists:
                space_data["lists"].append({"id": lst["id"], "name": lst["name"]})
            
            team_data["spaces"].append(space_data)
        
        hierarchy.append(team_data)
    
    # Save to .tmp
    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/crm_map.json", "w") as f:
        json.dump(hierarchy, f, indent=2)
    
    print("Discovery complete! Saved to .tmp/crm_map.json")

if __name__ == "__main__":
    discover_hierarchy()
