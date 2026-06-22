from pydantic import BaseModel

class Donor(BaseModel):

    donor_id: str
    name: str
    age: int
    gender: str
    blood_group: str
    weight: float
    city: str