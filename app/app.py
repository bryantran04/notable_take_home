from init import create_app
from flask_migrate import Migrate
from flask import abort, jsonify, request


from models import AppointmentType, Doctor, Patient, Appointment, db
from datetime import datetime


app = create_app()
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return {"status": "Hello"}, 201


@app.route("/doctor", methods=["POST"])
def create_doctor():

    response_body = {}
    error = False
    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        doctor = Doctor(first_name=first_name, last_name=last_name)
        db.session.add(doctor)
        db.session.commit()
        response_body["doctor_id"] = doctor.doctor_id
        response_body["first_name"] = f"First name: {first_name}"
        response_body["last_name"] = f"Last name: {last_name}"
        response_body["msg"] = f"Added new doctor into system"
    except Exception as e:
        error = True
        error_reason = e
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            return {"error": str(error_reason)}
        else:
            return jsonify(response_body)


@app.route("/doctors", methods=["GET"])
def get_all_doctors():
    doctors = Doctor.query.order_by(Doctor.doctor_id).all()

    response_body = {}
    response_body["doctors"] = []

    for doctor in doctors:
        response_body["doctors"].append(
            {
                "doctor_id": doctor.doctor_id,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
            }
        )

    return jsonify(response_body)


@app.route("/patient", methods=["POST"])
def create_patient():
    response_body = {}
    error = False
    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        patient = Patient(first_name=first_name, last_name=last_name)
        db.session.add(patient)
        db.session.commit()
        response_body["patient_id"] = patient.patient_id
        response_body["first_name"] = f"First name: {first_name}"
        response_body["last_name"] = f"Last name: {last_name}"
        response_body["msg"] = f"Added new patient into system"
    except Exception as e:
        error = True
        error_reason = e
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            return {"error": str(error_reason)}
        else:
            return jsonify(response_body)


def validate_appointment(patient_id, doctor_id, date_time_obj, kind):
    patient = Patient.query.filter_by(patient_id=patient_id).all()
    if len(patient) < 1:
        raise Exception("Patient does not exist")

    doctor = Doctor.query.filter_by(doctor_id=doctor_id).all()
    if len(doctor) < 1:
        raise Exception("Doctor does not exist")

    if date_time_obj.minute % 15 != 0:
        raise Exception("Not valid time")

    appointments = Appointment.query.filter_by(
        doctor_id=doctor_id, appointment_datetime=date_time_obj
    ).all()
    if len(appointments) >= 3:
        raise Exception("Doctor has 3 appointments at that time")


@app.route("/appointment", methods=["POST"])
def create_appointment():
    response_body = {}
    error = False
    try:
        patient_id = int(request.json["patient_id"])
        doctor_id = int(request.json["doctor_id"])
        appointment_datetime = request.json["appointment_datetime"]
        kind = request.json["kind"]

        date_time_obj = datetime.strptime(appointment_datetime, "%m/%d/%y %H:%M:%S")

        validate_appointment(patient_id, doctor_id, date_time_obj, kind)

        appointment_type = AppointmentType[kind]

        appointment = Appointment(
            appointment_datetime=date_time_obj,
            kind=appointment_type,
            doctor_id=doctor_id,
            patient_id=patient_id,
        )

        db.session.add(appointment)
        db.session.commit()

        response_body["msg"] = f"Added new appointment into system"
    except Exception as e:
        error = True
        error_reason = e
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            return {"error": str(error_reason)}
        else:
            return jsonify(response_body)


@app.route("/appointments/<doctor_id>", methods=["GET"])
def get_appointments(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    response_body = {}
    response_body["appointments"] = []

    for appointment in appointments:
        patient = Patient.query.filter_by(patient_id=appointment.patient_id).first()
        response_body["appointments"].append(
            {
                "patient_first_name": patient.first_name,
                "patient_last_name": patient.last_name,
                "time": appointment.appointment_datetime,
                "appointment_id": appointment.appointment_id,
                "kind": appointment.kind.value,
            }
        )

    return jsonify(response_body)


@app.route("/appointments/<appointment_id>", methods=["DELETE"])
def delete_appointments(appointment_id):
    appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
    if not appointment:
        return {"status": "Appointment does not exist"}

    Appointment.query.filter_by(appointment_id=appointment_id).delete()
    db.session.commit()
    return {"status": "Deleted Appointment"}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
