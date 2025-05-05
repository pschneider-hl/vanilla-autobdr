# app/csv_importer.py

import pandas as pd
from .schemas import ContactCreate

def load_contacts_from_csv(file_path: str):
    df = pd.read_csv(file_path)

    contacts = []
    for _, row in df.iterrows():
        first_name = row.get('First Name', '').strip()
        last_name = row.get('Last Name', '').strip()
        email = row.get('Email', '').strip()
        title = row.get('Title', '').strip()
        company = row.get('Company', '').strip()
        website = row.get('Website', '').strip()

        if not email or not title:
            continue

        full_name = f"{first_name} {last_name}".strip()

        # Guess persona if not provided
        persona = str(row.get("Persona", "")).lower()
        if persona not in ["success", "marketing", "advocacy", "support"]:
            if "marketing" in title.lower():
                persona = "marketing"
            elif "advocacy" in title.lower():
                persona = "advocacy"
            elif "support" in title.lower():
                persona = "support"
            else:
                persona = "success"

        contact = ContactCreate(
            name=full_name,
            email=email,
            title=title,
            company=company,
            website=website,
            persona=persona
        )
        contacts.append(contact)

    return contacts

