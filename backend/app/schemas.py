from pydantic import BaseModel
from datetime import datetime

class SlotOut(BaseModel):
    id: int
    doctor_id: int
    doctor_name: str
    specialization: str
    start_time: datetime
    end_time: datetime
    is_booked: bool

    class Config:
        from_attributes = True

class BookRequest(BaseModel):
    slot_id: int
    patient_name: str

class AppointmentOut(BaseModel):
    id: int
    slot_id: int
    doctor_name: str
    start_time: datetime
    end_time: datetime
    patient_name: str
    status: str

    class Config:
        from_attributes = True