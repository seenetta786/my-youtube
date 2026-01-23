# Directive: WhatsApp Messenger Wrapper

This directive handles all interactions with WhatsApp Messenger using the `execution/whatsapp_messenger.py` script.

## Command Patterns
- "Send a WhatsApp message to [Contact Name]: [Message]"
- "List my WhatsApp contacts"

## Workflow

### 1. Send Message
To send a message, call the messenger script:
`python execution/whatsapp_messenger.py --to "[Contact Name]" --msg "[Message]"`

### 2. Search Contacts
To find a contact's ID or verify their name:
`python execution/whatsapp_messenger.py --get-contacts`

### 3. Handle Errors
- If a contact is not found, the script will return an error JSON. Ask the user for the correct name or the phone number.
- Ensure `GREENAPI_ID_INSTANCE` and `GREENAPI_API_TOKEN` are present in `.env`.

## Reliability and Scheduling
The recurring RCB poll is managed via a **systemd timer** for maximum reliability.

- **Service**: `rcb-poll.service`
- **Timer**: `rcb-poll.timer` (Daily at 17:30)
- **Features**: 
    - **Persistence**: If the system is down during the scheduled time, the poll will trigger immediately upon the next boot.
    - **Isolation**: Runs in a dedicated environment with automatic logging to `.tmp/recurring_poll.log`.

### Check Status
To check the status of the timer:
`systemctl --user status rcb-poll.timer`

To list all active timers:
`systemctl --user list-timers`
