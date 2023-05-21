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

appointments = []
for appointment in data:
    patient_details = appointment.get('patientDetails', {})  
    appointment_data = {
        'appointmentId': appointment['appointmentId'],
        'phoneNumber': appointment['phoneNumber'],
        'validPhoneNumber':is_valid_phone(appointment['phoneNumber']),
        'phoneNumberHash':hash_phone_number(appointment['phoneNumber']) ,
        'firstName': patient_details.get('firstName'),
        'lastName': patient_details.get('lastName'),
        'gender': 'male' if patient_details.get('gender') == 'M' else 'female' if patient_details.get('gender') == 'F' else 'others',
        'DOB': patient_details.get('birthDate'),
        'Age': calculate_age(patient_details.get('birthDate')),
        'medicines': appointment['consultationData'].get('medicines')
    }
    appointments.append(appointment_data)

df = pd.DataFrame(appointments)

df['fullName'] = df['firstName'] + ' ' + df['lastName']
    
print(df[['appointmentId',   'phoneNumberHash','firstName', 'lastName', 'gender', 'Age', 'medicines', 'fullName']])




