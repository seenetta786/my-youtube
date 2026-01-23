import argparse
from clickup_client import ClickUpClient

def update_task(task_id, name=None, description=None):
    """
    Updates a task in ClickUp.
    """
    client = ClickUpClient()
    endpoint = f"task/{task_id}"
    data = {}
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    
    if not data:
        print("No fields to update.")
        return None

    return client._request("PUT", endpoint, data=data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a task in ClickUp.")
    parser.add_argument("task_id", help="The ID of the task to update.")
    parser.add_argument("-n", "--name", help="The new name of the task.")
    parser.add_argument("-d", "--description", help="The new description of the task.")
    args = parser.parse_args()

    task = update_task(args.task_id, args.name, args.description)
    if task:
        print(f"Task updated successfully! ID: {task['id']}")
    else:
        print("Failed to update task.")
