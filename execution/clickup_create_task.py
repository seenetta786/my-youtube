import argparse
from clickup_client import ClickUpClient

def create_task(list_id, name, description=None):
    """
    Creates a new task in a ClickUp list.
    """
    client = ClickUpClient()
    endpoint = f"list/{list_id}/task"
    data = {
        "name": name,
        "description": description if description else ""
    }
    return client._request("POST", endpoint, data=data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new task in ClickUp.")
    parser.add_argument("list_id", help="The ID of the list to create the task in.")
    parser.add_argument("name", help="The name of the task.")
    parser.add_argument("-d", "--description", help="The description of the task.")
    args = parser.parse_args()

    task = create_task(args.list_id, args.name, args.description)
    if task:
        print(f"Task created successfully! ID: {task['id']}")
    else:
        print("Failed to create task. Check the console for API error details.")
