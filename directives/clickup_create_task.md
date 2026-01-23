# Directive: Create ClickUp Task

This directive instructs the agent to create a new task in ClickUp.

## Command

Use the `clickup_create_task.py` script to create a new task.

### Arguments

- `list_id`: The ID of the list where the task will be created.
- `name`: The name of the task.
- `--description` (optional): A description for the task.

### Example

```bash
.venv/bin/python3 execution/clickup_create_task.py "123456789" "My New Task" --description "This is a task created from the command line."
```
