# Directive: Update ClickUp Task

This directive instructs the agent to update a task in ClickUp.

## Command

Use the `clickup_update_task.py` script to update a task.

### Arguments

- `task_id`: The ID of the task to update.
- `--name` (optional): The new name of the task.
- `--description` (optional): The new description of the task.

### Example

```bash
.venv/bin/python3 execution/clickup_update_task.py "987654321" --name "My Updated Task Name"
```
