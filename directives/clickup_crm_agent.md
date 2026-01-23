# ClickUp CRM Agent SOP

This directive handles all interactions with the ClickUp CRM using the Universal Tool approach.

## Inputs
- **Request**: Natural language request (e.g., "Add a lead", "Check status of Project X").
- **Context**: `.tmp/crm_map.json` (The hierarchy map).

## Tools
- `execution/clickup_universal.py`: Main API bridge.
- `execution/clickup_discover.py`: Hierarchy crawler.

## Process

### 1. Identify Target
Read `.tmp/crm_map.json` to find the correct Space, Folder, and List IDs based on the user's request.
- If the map doesn't exist, run `python execution/clickup_discover.py`.
- Resolve names to IDs (e.g., "Template creative agency space" -> `space_id`).

### 2. Format API Call
Refer to [ClickUp API Documentation](https://clickup.com/api/) to determine the endpoint and method.
- **Example (Create Task)**: 
  - Endpoint: `list/{list_id}/task`
  - Method: `POST`
  - Data: `{"name": "...", "description": "..."}`

### 3. Execute
Call `python execution/clickup_universal.py <endpoint> <method> '<json_data>'`.

### 4. Handle Response
- If successful, confirm to the user.
- If a custom field is needed but not in the map, use `clickup_universal.py` to fetch list-specific custom fields.

## Common Endpoints
- **Get Tasks**: `list/{list_id}/task` (GET)
- **Create Task**: `list/{list_id}/task` (POST)
- **Update Task**: `task/{task_id}` (PUT)
- **Add Comment**: `task/{task_id}/comment` (POST)
