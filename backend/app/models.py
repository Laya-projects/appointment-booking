from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func
from .database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    qualifications = Column(String, nullable=False)
    achievements = Column(Text, nullable=True)

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False, nullable=False)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    patient_name = Column(String, nullable=False)
    status = Column(String, default="booked", nullable=False)  # "booked" or "cancelled"
    created_at = Column(DateTime, server_default=func.now(), nullable=False)