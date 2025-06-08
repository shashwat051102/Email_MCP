# Email MCP Server

A Python-based server for sending and previewing emails using Gmail, built with [FastMCP](https://github.com/ContextualAI/fastmcp). This project provides a simple API for sending emails and listing recent inbox messages, with environment-based configuration for security.

---

## Features

- **Send Emails**: Easily send HTML emails via Gmail SMTP.
- **List Recent Emails**: Preview the latest emails in your Gmail inbox.
- **Input Validation**: Ensures all email addresses and fields are valid.
- **Environment Variable Support**: Keeps sensitive credentials out of your codebase.
- **FastMCP Integration**: Exposes tools as API endpoints for easy integration.

---

## Requirements

- Python 3.8+
- Gmail account (with App Password if 2FA is enabled)
- [FastMCP](https://github.com/ContextualAI/fastmcp)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies:

```sh
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root with the following:

```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

- **EMAIL_ADDRESS**: Your Gmail address.
- **EMAIL_PASSWORD**: [App Password](https://support.google.com/accounts/answer/185833?hl=en) (required if 2FA is enabled).

---

## Usage

### Start the Server

```sh
python Email_MCP_Server.py
```

The server will expose tools via FastMCP.

---

### Tools

#### 1. `send_email`

Send an email using Gmail SMTP.

**Parameters:**
- `recipient_email` (str): Recipient's email address.
- `subject` (str): Email subject.
- `body` (str): Email body (HTML supported).

**Returns:**  
Success message or error details.

#### 2. `list_recent_emails`

List the most recent emails in your inbox.

**Parameters:**
- `limit` (int, optional): Number of emails to preview (default: 5).

**Returns:**  
A formatted string with subject and sender for each email.

---

## Example

```python
from mcp.client import MCPClient

client = MCPClient("http://localhost:8000")
print(client.send_email("to@example.com", "Test Subject", "<b>Hello!</b>"))
print(client.list_recent_emails(limit=3))
```

---

## Security Notes

- Use an App Password for Gmail if 2FA is enabled.
- Never commit your `.env` file or credentials to version control.
- For production, consider using OAuth2 for Gmail access.

---

## Troubleshooting

- **Authentication failed**: Check your email and app password.
- **Less secure app access**: Ensure your Google account allows SMTP/IMAP access.
- **Firewall issues**: Make sure ports 465 (SMTP) and 993 (IMAP) are open.

---

## License

MIT License

---

**Author:** Shashwat SIngh
