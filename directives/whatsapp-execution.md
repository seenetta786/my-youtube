# WhatsApp Service Execution Plan

This directive outlines the operation and maintenance of automated WhatsApp services using Green API and GitHub Actions.

## Services Overview

### 1. ShYlpA Daily Compliment
Sends a random compliment to brighten the recipient's day.
- **Recipient**: `919481546119@c.us` (ShYlpA)
- **Schedule**: Daily at 05:35 IST (00:05 UTC)
- **Status**: [TEMPORARY] Increased to every 30 minutes for Jan 29.
- **Script**: [shylpa_compliment.py](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/execution/shylpa_compliment.py)
- **Workflow**: [shylpa_compliment.yml](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/.github/workflows/shylpa_compliment.yml)

### 2. RCB 2.0 Recurring Poll
Sends a daily poll for team coordination.
- **Recipient**: `120363419563262981@g.us` (RCB 2.0 Group)
- **Schedule**: Monday to Thursday at 18:05 IST (12:35 UTC)
- **Script**: [recurring_rcb_poll.py](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/execution/recurring_rcb_poll.py)
- **Workflow**: [whatsapp_poll.yml](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/.github/workflows/whatsapp_poll.yml)

### 3. Payment Reminder (RCB 2.0)
Sends a beautified payment reminder message.
- **Recipient**: `120363419563262981@g.us` (RCB 2.0 Group)
- **Schedule**: Mon, Wed, Fri at 08:00 IST (02:30 UTC)
- **Script**: [payment_reminder.py](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/execution/payment_reminder.py)
- **Workflow**: [payment_reminder.yml](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/.github/workflows/payment_reminder.yml)

## Technical Architecture

- **Layer 1 (Directive)**: This document.
- **Layer 2 (Orchestration)**: GitHub Actions workflows schedule the execution.
- **Layer 3 (Execution)**: Python scripts using the `WhatsAppWrapper` in [whatsapp_messenger.py](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/execution/whatsapp_messenger.py).
- **API Provider**: [Green API](https://green-api.com/)

## Operational Procedures

### Credentials Management
Secrets are stored in GitHub Repository Secrets:
- `GREENAPI_ID_INSTANCE`: Instance ID from Green API console.
- `GREENAPI_API_TOKEN`: API Token from Green API console.

> [!IMPORTANT]
> Never hardcode these credentials. They must be accessed via environment variables.

### Recovery and Support
If a service fails:
1. Check **GitHub Actions** tab for logs.
2. Verify Green API instance status at [console.green-api.com](https://console.green-api.com/).
3. Use **Workflow Dispatch** (manual trigger) in the Actions tab to re-run a missed message.
4. Run [check_status.py](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/execution/check_status.py) locally to verify API connectivity.

## Maintenance Notes

### Reverting Temporary Schedules
To revert the ShYlpA compliment service to its original daily schedule (Jan 30 onwards):
- **File**: [.github/workflows/shylpa_compliment.yml](file:///media/seanetta/RXX/ai/YouTube%20Workspace(DOE)/.github/workflows/shylpa_compliment.yml)
- **Original Cron**: `5 0 * * *` (05:35 IST)
- **Status Change**: Remove the `[TEMPORARY]` notice in this directive.
