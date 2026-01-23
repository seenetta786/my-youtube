#!/bin/bash

# Define paths
WORKSPACE_DIR="/media/seanetta/RXX/ai/YouTube Workspace(DOE)"
PYTHON_EXEC="$WORKSPACE_DIR/.venv/bin/python"
SCRIPT_PATH="$WORKSPACE_DIR/execution/recurring_rcb_poll.py"
LOG_PATH="$WORKSPACE_DIR/.tmp/recurring_poll.log"

# Remove legacy cron entry if it exists
(crontab -l 2>/dev/null | grep -vF "$SCRIPT_PATH") | crontab -
echo "Removed any legacy cron entries for $SCRIPT_PATH."

# Systemd User Configuration
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
SERVICE_NAME="rcb-poll.service"
TIMER_NAME="rcb-poll.timer"

mkdir -p "$SYSTEMD_USER_DIR"

# Create Service File
cat <<EOF > "$SYSTEMD_USER_DIR/$SERVICE_NAME"
[Unit]
Description=Daily RCB WhatsApp Poll
After=network.target

[Service]
Type=oneshot
WorkingDirectory=$WORKSPACE_DIR
ExecStart="$PYTHON_EXEC" "$SCRIPT_PATH"
StandardOutput=append:$LOG_PATH
StandardError=append:$LOG_PATH

[Install]
WantedBy=default.target
EOF

# Create Timer File (5:30 PM)
cat <<EOF > "$SYSTEMD_USER_DIR/$TIMER_NAME"
[Unit]
Description=Daily RCB WhatsApp Poll Timer

[Timer]
OnCalendar=Mon..Thu,Sat,Sun *-*-* 18:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Reload and Start
systemctl --user daemon-reload
systemctl --user enable "$TIMER_NAME"
systemctl --user start "$TIMER_NAME"

echo "Systemd timer '$TIMER_NAME' configured and started (Daily at 5:30 PM)."
echo "Missed polls will be sent automatically upon system startup (Persistent=true)."
