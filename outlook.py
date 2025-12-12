"""
send_outlook_smtp.py
Simple: send plain text or HTML email via Office365 SMTP.
Note: If your account has MFA, you may need an app password or enable SMTP AUTH.
"""

import os
import smtplib
from email.message import EmailMessage
from typing import Optional

SMTP_SERVER = os.getenv("OUTLOOK_SMTP", "smtp.office365.com")
SMTP_PORT = int(os.getenv("OUTLOOK_SMTP_PORT", 587))
SMTP_USER = os.getenv("OUTLOOK_EMAIL", "orina.guha@jhsassociates.in")           # e.g. "you@yourdomain.com"
SMTP_PASS = os.getenv("OUTLOOK_PASSWORD", "Z/353995261212ur")       # app password or account password if allowed

def send_mail(
    subject: str,
    body: str,
    to: str,
    html: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    attachments: Optional[list] = None,
):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    msg["Subject"] = subject

    # plain text
    msg.set_content(body)

    # optional HTML
    if html:
        msg.add_alternative(html, subtype="html")

    # attachments: list of file paths
    if attachments:
        for path in attachments:
            path = str(path)
            with open(path, "rb") as f:
                data = f.read()
            import mimetypes
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            filename = os.path.basename(path)
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    recipients = [r.strip() for r in (to or "").split(",") if r.strip()]
    if cc:
        recipients += [r.strip() for r in cc.split(",") if r.strip()]
    if bcc:
        recipients += [r.strip() for r in bcc.split(",") if r.strip()]

    # connect and send
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()      # TLS
        smtp.ehlo()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg, from_addr=SMTP_USER, to_addrs=recipients)

if __name__ == "__main__":
    # quick test (set environment variables first)
    send_mail(
        subject="Test from Python (Office365 SMTP)",
        body="Hello — this is a test email sent via smtp.office365.com",
        html="<p>Hello — <b>this is a test</b> sent via <i>smtp.office365.com</i></p>",
        to="vasu.gadde@jhsassociates.in",
        attachments=None,
    )
    print("Sent (or raised).")
