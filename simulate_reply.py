import sqlite3
from datetime import datetime

DB_PATH = "autobdr.db"

def mark_email_as_replied(email_address):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Find the most recent email sent to this address
    cursor.execute("""
        SELECT id, subject, message
        FROM email_logs
        WHERE email = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (email_address,))
    result = cursor.fetchone()

    if not result:
        print(f"No emails found for {email_address}")
        return

    email_log_id, subject, message = result

    # Update the log to show it was replied to
    cursor.execute("""
        UPDATE email_logs
        SET outcome = 'replied'
        WHERE id = ?
    """, (email_log_id,))

    # Update the message variant reply count
    cursor.execute("""
        UPDATE message_variants
        SET total_replies = total_replies + 1
        WHERE subject = ? AND body = ?
    """, (subject, message))

    conn.commit()
    conn.close()
    print(f"✅ Marked as replied: {email_address}")

if __name__ == "__main__":
    # 👇 Replace with any test email you've used
    mark_email_as_replied("prschneider9933@gmail.com")
