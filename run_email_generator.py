import pandas as pd
from dotenv import load_dotenv
import os
import openai
from app.schemas import ContactCreate
from app.email_prompts import get_prompt
from app.email_service import send_email

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_email(contact: ContactCreate, attempt: int = 1):
    prompt = get_prompt(contact, attempt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def run_from_csv(path="contacts.csv"):
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        name = f"{row['First Name']} {row['Last Name']}"
        email = row['Email']
        title = row['Title']
        company = row['Company']
        website = row['Website']
        persona = row.get('Persona', 'success').lower()

        contact = ContactCreate(
            name=name,
            email=email,
            title=title,
            company=company,
            website=website,
            persona=persona
        )

        email_text = generate_email(contact, attempt=1)

        # Extract subject line from HTML
        subject_line = "Follow-up from Higher Logic"
        if "<b>Subject:</b>" in email_text:
            subject_line = email_text.split("<b>Subject:</b>")[1].split("<br>")[0].strip()

        send_email(email, subject_line, email_text)
        print(f"✅ Sent to {email}")
        print("=" * 60 + "\n")

if __name__ == "__main__":
    run_from_csv()


