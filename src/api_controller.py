"""Patient API Controller"""

from flask import Flask, jsonify, request
from patient_db import PatientDB


class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/", methods=["GET"])(self.home)
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)


    """
    TODO:
    Implement the following methods,
    use the self.patient_db object to interact with the database.

    Every method in this class should return a JSON response with status code
    Status code should be 200 if the operation was successful,
    Status code should be 400 if there was a client error,
    """

    def create_patient(self):
        try:
            data = request.json
            required_fields = ['patient_name', 'patient_gender', 'patient_age']
            if all(field in data for field in required_fields):
                # patient = self.patient_db.insert_patient(data)
                patient_id = self.patient_db.insert_patient(data)
                if patient_id:
                    return jsonify({"message": "Patient created successfully", "patient_id": str(patient_id)}), 200
                else:
                    return jsonify({"message": "Failed to create patient"}), 400
            else: 
                return jsonify({"message": "Missing required fields"}), 400
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    def get_patients(self):
        patients = self.patient_db.select_all_patients()
        if patients:
            return jsonify(patients), 200
        else:
            return jsonify({"message": "Patient not found"}), 400

    def get_patient(self, patient_id):
        patient = self.patient_db.select_patient(patient_id)
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"message": "Patient not found"}), 400

    def update_patient(self, patient_id):
        try:
            data = request.json
            if data:
                patient = self.patient_db.update_patient(patient_id, data)
                if patient:
                    return jsonify({"message": "Patient updated successfully"}), 200
                else:
                    return jsonify({"message": "Failed to update patient"}), 400
            else:
                return jsonify({"message": "No data provided"}), 400
        except Exception as e:
            return jsonify({"message": str(e)}), 400

    def delete_patient(self, patient_id):
        patient = self.patient_db.delete_patient(patient_id)
        if patient:
            return jsonify({"message": "Patient deleted successfully"}), 200
        else:
            return jsonify({"message": "Failed to delete patient"}), 400

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run(debug=True)

    def home(self):
        return jsonify({"message": "Welcomem to the Patient API"}), 200


PatientAPIController()
