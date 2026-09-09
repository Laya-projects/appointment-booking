from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, update
from datetime import datetime
from . import models, schemas
from .database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. GET available slots
@router.get("/slots", response_model=list[schemas.SlotOut])
def get_slots(db: Session = Depends(get_db)):
    slots = (
        db.query(models.Slot, models.Doctor)
        .join(models.Doctor, models.Slot.doctor_id == models.Doctor.id)
        .filter(models.Slot.is_booked == False, models.Slot.start_time > datetime.utcnow())
        .order_by(models.Slot.start_time)
        .all()
    )
    return [
        schemas.SlotOut(
            id=s.id, doctor_id=s.doctor_id, doctor_name=d.name,
            specialization=d.specialization, start_time=s.start_time,
            end_time=s.end_time, is_booked=s.is_booked
        )
        for s, d in slots
    ]

# 2. POST book a slot — THE concurrency-critical one
@router.post("/appointments", response_model=schemas.AppointmentOut)
def book_slot(req: schemas.BookRequest, db: Session = Depends(get_db)):
    result = db.execute(
        update(models.Slot)
        .where(models.Slot.id == req.slot_id, models.Slot.is_booked == False)
        .values(is_booked=True)
    )
    if result.rowcount == 0:
        db.rollback()
        raise HTTPException(status_code=409, detail="Slot is no longer available")

    appointment = models.Appointment(
        slot_id=req.slot_id, patient_name=req.patient_name.strip(), status="booked"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    slot = db.query(models.Slot).filter(models.Slot.id == req.slot_id).first()
    doctor = db.query(models.Doctor).filter(models.Doctor.id == slot.doctor_id).first()
    return schemas.AppointmentOut(
        id=appointment.id, slot_id=slot.id, doctor_name=doctor.name,
        start_time=slot.start_time, end_time=slot.end_time,
        patient_name=appointment.patient_name, status=appointment.status,
    )

# 3. GET a patient's appointments
@router.get("/appointments", response_model=list[schemas.AppointmentOut])
def get_appointments(patient_name: str, db: Session = Depends(get_db)):
    rows = (
        db.query(models.Appointment, models.Slot, models.Doctor)
        .join(models.Slot, models.Appointment.slot_id == models.Slot.id)
        .join(models.Doctor, models.Slot.doctor_id == models.Doctor.id)
        .filter(models.Appointment.patient_name == patient_name)
        .order_by(models.Slot.start_time.desc())
        .all()
    )
    return [
        schemas.AppointmentOut(
            id=a.id, slot_id=s.id, doctor_name=d.name,
            start_time=s.start_time, end_time=s.end_time,
            patient_name=a.patient_name, status=a.status,
        )
        for a, s, d in rows
    ]

# 4. Cancel an appointment
@router.patch("/appointments/{appointment_id}/cancel", response_model=schemas.AppointmentOut)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appointment.status == "cancelled":
        raise HTTPException(status_code=400, detail="Appointment already cancelled")

    appointment.status = "cancelled"
    slot = db.query(models.Slot).filter(models.Slot.id == appointment.slot_id).first()
    slot.is_booked = False
    db.commit()
    db.refresh(appointment)

    doctor = db.query(models.Doctor).filter(models.Doctor.id == slot.doctor_id).first()
    return schemas.AppointmentOut(
        id=appointment.id, slot_id=slot.id, doctor_name=doctor.name,
        start_time=slot.start_time, end_time=slot.end_time,
        patient_name=appointment.patient_name, status=appointment.status,
    )