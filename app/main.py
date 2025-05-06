from fastapi import FastAPI, BackgroundTasks
from .schemas import ContactCreate
from .email_service import send_initial_email

app = FastAPI()

@app.post("/contacts/")
async def create_contact(contact: ContactCreate, tasks: BackgroundTasks):
    tasks.add_task(send_initial_email, contact)
    return {"message": "Email generation started"}
from .csv_importer import load_contacts_from_csv

@app.get("/upload-csv/")
async def upload_csv(background_tasks: BackgroundTasks):
    contacts = load_contacts_from_csv("contacts.csv")  # or another path

    for contact in contacts:
        background_tasks.add_task(send_initial_email, contact)

    return {"message": f"Queued {len(contacts)} contacts from CSV"}
