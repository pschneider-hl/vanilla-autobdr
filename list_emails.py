import sqlite3

DB_PATH = "autobdr.db"

def list_emails():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, subject, attempt, outcome, timestamp FROM email_logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    print("\n📬 Logged Emails:")
    for row in rows:
        print(f"ID: {row[0]} | Email: {row[1]} | Subject: {row[2]} | Attempt: {row[3]} | Outcome: {row[4]} | Sent: {row[5]}")

if __name__ == "__main__":
    list_emails()
