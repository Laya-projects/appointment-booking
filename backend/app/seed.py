from datetime import datetime, timedelta
from .database import SessionLocal, engine, Base
from . import models

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear existing data (safe to re-run while building)
db.query(models.Appointment).delete()
db.query(models.Slot).delete()
db.query(models.Doctor).delete()
db.commit()

doctors = [
    models.Doctor(name="Dr. Anjali Rao", specialization="Cardiology",
                  qualifications="MBBS, MD (Cardiology)", achievements="15 years experience, AIIMS trained"),
    models.Doctor(name="Dr. Karthik Menon", specialization="Dermatology",
                  qualifications="MBBS, MD (Dermatology)", achievements="Published researcher, 10 years practice"),
    models.Doctor(name="Dr. Priya Nair", specialization="Pediatrics",
                  qualifications="MBBS, DCH", achievements="Child health specialist, 12 years experience"),
]
db.add_all(doctors)
db.commit()
for d in doctors:
    db.refresh(d)

# Generate 2-hour slots for the next 3 days, per doctor: 9-11, 2-4, 5-7
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
blocks = [(9, 11), (14, 16), (17, 19)]

slots = []
for day_offset in range(3):
    day = today + timedelta(days=day_offset + 1)  # start from tomorrow
    for doctor in doctors:
        for start_hour, end_hour in blocks:
            slots.append(models.Slot(
                doctor_id=doctor.id,
                start_time=day.replace(hour=start_hour),
                end_time=day.replace(hour=end_hour),
                is_booked=False,
            ))

db.add_all(slots)
db.commit()
db.close()

print(f"Seeded {len(doctors)} doctors and {len(slots)} slots.")