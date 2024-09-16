"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""

import uuid
from datetime import datetime
from config import GENDERS, WARD__NUMBERS, ROOM_NUMBERS
from patient_db_config import PATIENT_COLUMN_NAMES
from api_controller import PatientAPIController

class Patient:
    def __init__(self, name, gender, age):
        self.id = str(uuid.uuid4())
        self.gender = gender
        self.age = age
        self.checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.checkout = None
        self.ward = None
        self.room = None

    def update_room_and_ward(self, ward, room):
        if ward in WARD_NUMBERS and room in ROOM_NUMBERS[ward]:
            self.ward = ward
            self.room = room
            return True
        else:
            print("Invalid ward or room number.")
            return False

    def commit_to_database(self):
        api_controller = PatientAPIController()
        patient_data = {
            "patient_id": self.id,
            "patiend_name": self.name,
            "patient_gender": self.gender,
            "patient_age": self.age,
            "patient_checkin": self.checkin,
            "patient_checkout": self.checkout,
            "patient_ward": self.ward,
            "patient_room": self.room
        }
        response = api_controller.create_patient(patient_data)
        if response.status_code == 200:
            print("Patient committed to the database successfully.")
            return True
        else:
            print("Failed to commit patient to the database.")
            return False
    