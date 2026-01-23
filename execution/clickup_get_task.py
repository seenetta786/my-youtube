import argparse
import json
from clickup_client import ClickUpClient

def get_task(task_id):
    """
    Gets a task from ClickUp.
    """
    client = ClickUpClient()
    endpoint = f"task/{task_id}"
    return client._request("GET", endpoint)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a task from ClickUp.")
    parser.add_argument("task_id", help="The ID of the task to get.")
    args = parser.parse_args()

    task = get_task(args.task_id)
    if task:
        print(json.dumps(task, indent=2))
    else:
        print("Failed to get task.")
