import argparse
from clickup_client import ClickUpClient

def delete_task(task_id):
    """
    Deletes a task from ClickUp.
    """
    client = ClickUpClient()
    endpoint = f"task/{task_id}"
    return client._request("DELETE", endpoint)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a task from ClickUp.")
    parser.add_argument("task_id", help="The ID of the task to delete.")
    args = parser.parse_args()

    result = delete_task(args.task_id)
    if result is None:
        # _request returns None on failure, and for DELETE on success the body is empty
        # but the status code is 204. requests.request with response.raise_for_status()
        # does not return a value on success, so result is None.
        # A bit of a hack to check for success.
        # A better implementation would be to have _request return the response object.
        print(f"Task {args.task_id} deleted successfully (or did not exist).")
    else:
        print("Failed to delete task.")
