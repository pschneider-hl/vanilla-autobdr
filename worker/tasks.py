from celery import Celery
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from app.email_service import send_initial_email, send_log
from app.schemas import ContactCreate

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("worker", broker=redis_url)

# === TASK: Initial email trigger ===
@celery.task
def send_initial_email_task(contact_data):
    send_initial_email(contact_data, attempt=1)


# === TASK: Retry if no reply ===
RETRY_WAIT_SECONDS = 180
MAX_ATTEMPTS = 4

@celery.task
def retry_unsuccessful_emails():
    now = datetime.utcnow()
    for contact_id, attempts in send_log.items():
        last_attempt = attempts[-1]
        attempt_number = len(attempts) + 1

        if attempt_number > MAX_ATTEMPTS:
            continue  # Max reached
        if last_attempt["status"] == "replied":
            continue  # No follow-up needed
        if now - last_attempt["timestamp"] >= timedelta(seconds=RETRY_WAIT_SECONDS):

            print(f"[Retry Attempt #{attempt_number}] for contact ID: {contact_id}")

            # TEMP CONTACT INFO — replace with DB lookups in future
            fake_contact = ContactCreate(
                id=contact_id,
                name="Retry Placeholder",
                email="test@example.com",
                title="Director of Support",
                company="Fake Co",
                website="https://fake.com",
                persona="support"
            )
            send_initial_email(fake_contact, attempt=attempt_number)


