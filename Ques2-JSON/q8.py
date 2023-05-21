import json
import pandas as pd
import re
import hashlib
import datetime

with open('DataEngineeringQ2.json', 'r') as file:
    data = json.load(file)

def is_valid_phone(num):
    return bool(re.match(r"^(?:\+91|91)?[6-9]\d{9}$", str(num)))

def hash_phone_number(number):
    if is_valid_phone(number):
        number = re.sub(r'^\+91', '', number)
        number_hash = hashlib.sha256(number.encode()).hexdigest()
        return number_hash
    else:
        return None

def calculate_age(dob):
    if dob is None:
        return None
    else:
        dob = datetime.datetime.strptime(dob, "%Y-%m-%dT%H:%M:%S.%fZ")
        today = datetime.datetime.now()
        age = today.year - dob.year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1
        return int(age)

selected_data = []
appointments = []
for appointment in data:
    patient_details = appointment.get('patientDetails', {})  
    medicines = appointment['consultationData']['medicines']
    no_of_medicines = len(medicines)
    no_of_active_medicines = sum(1 for medicine in medicines if medicine.get('IsActive', False))
    no_of_inactive_medicines = no_of_medicines - no_of_active_medicines

    active_medicine_names = [medicine['medicineName'] for medicine in medicines if medicine.get('IsActive', False)]
    medicine_names = ', '.join(active_medicine_names)
    appointment_data = {
        'appointmentId': appointment['appointmentId'],
        'fullName': appointment['patientDetails']['firstName'] + ' ' + appointment['patientDetails']['lastName'],
        'phoneNumber': appointment['phoneNumber'],
        'validPhoneNumber':is_valid_phone(appointment['phoneNumber']),
        'phoneNumberHash':hash_phone_number(appointment['phoneNumber']) ,
        'gender': 'male' if patient_details.get('gender') == 'M' else 'female' if patient_details.get('gender') == 'F' else 'others',
        'DOB': patient_details.get('birthDate'),
        'Age': calculate_age(patient_details.get('birthDate')),
        'noOfMedicines': no_of_medicines,
        'noOfActiveMedicines': no_of_active_medicines,
        'noOfInActiveMedicines': no_of_inactive_medicines,
        'medicineNames' : medicine_names
    }
    appointments.append(appointment_data)
    selected_data.append(appointment_data)

df = pd.DataFrame(selected_data)

    

df.to_csv('output.csv', sep='~', index=False)





