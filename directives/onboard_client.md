# Directive: Onboard Client

**Command:** `onboard client <email>`

**Description:** Onboards a new client by sending them a welcome email.

**Workflow:**

1.  **Extract client email:** The client's email address is extracted from the command.
2.  **Read email template:** The content of `/directives/email_templates/onboarding_email.md` is read.
3.  **Get company info:** The user is prompted to provide a list of bullet points about the company.
4.  **Populate template:** The placeholders in the email template are replaced with the following information:
    *   `[CLIENT_NAME]`: The part of the email address before the `@`.
    *   `[COMPANY_INFO]`: The bullet points provided by the user.
    *   `[CALENDAR_LINK]`: A placeholder link: `https://app.cal.com/srinu-reddy-h8wwzb`
5.  **Send email:** The `execution/send_email.py` script is called with the recipient's email, a subject line, and the populated email body.