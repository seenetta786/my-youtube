# Directive: Process Replies

**Command:** `process replies from <email>`

**Description:** Checks for and processes replies from a client.

**Workflow:**

1.  **Extract client email:** The client's email address is extracted from the command.
2.  **Check for new emails:** The `execution/check_emails.py` script is called with the client's email address to check for new unread emails.
3.  **Process and summarize:** If new emails are found, their content is summarized.
4.  **Present summary:** The summary of the email is presented to the user.
5.  **Suggest next steps:** The user is prompted to decide on the next steps, such as:
    *   Creating a client file to track the conversation.
    *   Replying to the client.
    *   Ignoring the email.
