from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()


class AppointmentType(enum.Enum):
    NEW_PATIENT = "NEW_PATIENT"
    FOLLOW_UP = "FOLLOW_UP"


class Doctor(db.Model):
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)


class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, unique=True
    )

    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)


class Appointment(db.Model):
    __tablename__ = "appointments"

    appointment_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, unique=True
    )

    appointment_datetime = db.Column(db.DateTime, nullable=False)
    kind = db.Column(db.Enum(AppointmentType), nullable=False)
    doctor_id = db.Column(
        db.Integer, db.ForeignKey("doctors.doctor_id"), nullable=False
    )
    patient_id = db.Column(
        db.Integer, db.ForeignKey("patients.patient_id"), nullable=False
    )
