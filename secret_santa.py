from dotenv import load_dotenv
import os
import random
import smtplib
import ssl
from email.message import EmailMessage

load_dotenv()

SENDER_EMAIL = "yourgmail@gmail.com"

PASSWORD = os.getenv("password")
if not PASSWORD:
    print("ERROR: Please add 'password' in your .env file (App Password).")
    exit(1)

participants = [
    ["Jenisha", "jenishashereyl@gmail.com"],
    ["Jen", "jenshereyl@gmail.com"],
]

if len(participants) < 2:
    print("Need at least 2 participants!")
    exit(1)

names = [p[0] for p in participants]
emails = {p[0]: p[1] for p in participants}

recipients = names[:]
random.shuffle(recipients)

while any(a == b for a, b in zip(names, recipients)):
    random.shuffle(recipients)

pairs = list(zip(names, recipients))

def send_email(sender, receiver, recipient):
    body_text = f"""Hi! Your Secret Santa recipient is: {recipient}! 🎁
Spend ₹500–₹1500, and have fun choosing the gift!"""

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "Your Secret Santa Assignment! 🎅"
    msg.set_content(body_text, charset="utf-8")

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender, PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {receiver} (recipient: {recipient})")
        return True
    except smtplib.SMTPAuthenticationError:
        print(f" SMTP Authentication error for {receiver}")
        return False
    except Exception as e:
        print(f"Failed to send email to {receiver}: {e}")
        return False

successes = 0
failures = []

for giver, recipient in pairs:
    receiver_email = emails[giver]
    if send_email(SENDER_EMAIL, receiver_email, recipient):
        successes += 1
    else:
        failures.append(receiver_email)

print(f"\nAll done! {successes} emails sent, {len(failures)} failures.")
if failures:
    print("Failed to send emails to:")
    for f in failures:
        print(" -", f)
