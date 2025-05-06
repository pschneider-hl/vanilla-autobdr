from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

class ContactCreate(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    title: str
    company: str
    website: str
    persona: str

    def with_id(self):
        if not self.id:
            self.id = str(uuid4())
        return self

