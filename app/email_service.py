import openai
import os
import sqlite3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from datetime import datetime
from .email_prompts import get_prompt

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
DB_PATH = "autobdr.db"

def log_email(contact, subject, message, attempt):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.utcnow().isoformat()

    # Log the email to email_logs
    cursor.execute("""
        INSERT INTO email_logs (contact_id, email, persona, subject, message, attempt, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        contact.id,
        contact.email,
        contact.persona,
        subject,
        message,
        attempt,
        timestamp
    ))

    # Check if this subject/message combo already exists in message_variants
    cursor.execute("""
        SELECT id FROM message_variants
        WHERE persona = ? AND subject = ? AND body = ?
    """, (contact.persona, subject, message))
    variant = cursor.fetchone()

    if variant:
        # Update send count
        cursor.execute("""
            UPDATE message_variants
            SET total_sent = total_sent + 1
            WHERE id = ?
        """, (variant[0],))
    else:
        # Insert new variant
        cursor.execute("""
            INSERT INTO message_variants (persona, subject, body, total_sent)
            VALUES (?, ?, ?, 1)
        """, (contact.persona, subject, message))

    conn.commit()
    conn.close()

def send_initial_email(contact, attempt=1):
    contact = contact.with_id()
    prompt = get_prompt(contact, attempt)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        text = response["choices"][0]["message"]["content"]
        subject = "Let’s connect"

        # Try to extract a subject line if GPT gave us one
        if "Subject:" in text:
            lines = text.splitlines()
            for line in lines:
                if line.lower().startswith("subject:"):
                    subject = line.split(":", 1)[1].strip()
                    break

        # Send the email using SendGrid
        message = Mail(
            from_email="yourname@yourdomain.com",  # Replace with your SendGrid sender
            to_emails=contact.email,
            subject=subject,
            plain_text_content=text
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)

        # Log the email and subject line to DB
        log_email(contact, subject, text, attempt)

        print(f"[Email Sent] {contact.email} (Attempt #{attempt})")

    except Exception as e:
        print(f"[Error Sending Email to {contact.email}]: {e}")
