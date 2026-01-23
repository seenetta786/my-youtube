# Copilot Instructions for YouTube Workspace (DOE)

## Architecture Overview

This project uses a **3-layer architecture** that separates concerns to maximize reliability:

### Layer 1: Directives (What to do)
- **Location**: `directives/`
- SOPs written in Markdown that define goals, inputs, execution steps, outputs, and error handling
- Natural language instructions for workflows
- Current directives:
  - `onboard_client.md` - Client onboarding workflow with email sending
  - `email_templates/` - Reusable email templates with placeholders

### Layer 2: Orchestration (Decision Making)
- **Your role**: Read directives, decide which tools to call, handle errors, ask for clarification
- Route between intent and execution
- When a directive requires a tool, find the corresponding script in `execution/` and call it with the right inputs

### Layer 3: Execution (Doing the Work)
- **Location**: `execution/`
- Deterministic Python scripts for API calls, data processing, file operations
- Current scripts:
  - `send_email.py` - Sends emails with templated content
- All scripts accept CLI arguments and handle their own error reporting

## Key Principles

### 1. Check for Tools First
Before writing new code, check `execution/` for existing scripts matching the directive. Only create new scripts if none exist.

### 2. Self-Anneal When Things Break
- Read error messages and stack traces
- Fix the script (test thoroughly unless it uses paid tokens—check with user first)
- Update the directive with learnings (API limits, timing, edge cases)
- Example: Hit rate limit → research API → find batch endpoint → rewrite script → test → update directive

### 3. Update Directives as You Learn
Directives are living documents. When you discover API constraints, better approaches, common errors, or timing expectations—update the directive. Directives are the instruction set and must be preserved and improved over time.

## File Organization

**Directory structure:**
- `directives/` - SOP markdown files and templates
- `execution/` - Python scripts (deterministic tools)
- `credentials.json`, `token.json` - Google OAuth credentials (in `.gitignore`)
- `.tmp/` - Intermediate processing files (auto-regenerated, never commit)

**Key principle**: Local files are only for processing. Final deliverables go to cloud services (Google Sheets, Slides, etc.).

## Current Workflows

### Sending Emails
1. Read `directives/onboard_client.md` for the workflow
2. Call `execution/send_email.py` with recipient, subject, body arguments
3. Script handles email sending; currently simulates output (awaiting real OAuth setup)

**Example**:
```bash
python3 execution/send_email.py "client@example.com" "Subject" "Email body text"
```

## Developer Conventions

- **Scripts**: Python 3, use argparse for CLI arguments, handle errors explicitly
- **Email Templates**: Markdown files with placeholders like `[PLACEHOLDER_NAME]`
- **Credentials**: Stored in `credentials.json` and `token.json` (never commit)
- **Dependencies**: Document Python packages as they're added

## Integration Points

- Email templates (`directives/email_templates/`) → `execution/send_email.py`
- Directives reference execution scripts by path and required arguments
- Authentication handled by credentials stored in environment files