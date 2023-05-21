import re
import json
import datetime

with open('DataEngineeringQ2.json') as file:
    data = json.load(file)

age_sum = 0
gender_count = {'male': 0, 'female': 0, 'other': 0}
valid_phone_numbers = 0
appointment_count = 0
medicine_count = 0
active_medicine_count = 0

for appointment in data:
    gender = appointment['patientDetails'].get('gender')
    birth_date = appointment['patientDetails'].get('birthDate')
    phone_number = appointment['phoneNumber']
    medicines = appointment['consultationData']['medicines']

    def calculate_age(dob):
        if dob is None:
            return None
        else:
            dob = datetime.datetime.strptime(dob, "%Y-%m-%dT%H:%M:%S.%fZ")
            today = datetime.datetime.now()
            age = today.year - dob.year
            if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
                age -= 1
            return age

    age = calculate_age(birth_date)
    if age is not None:
        age_sum += age

    if gender is not None:
        if gender.lower() == 'male':
            gender_count['male'] += 1
        elif gender.lower() == 'female':
            gender_count['female'] += 1
        else:
            gender_count['other'] += 1

    def is_valid_phone_number(number):
        number = re.sub(r'\D', '', number)
        if re.match(r'^((\+|0{0,2})91)?[6-9]\d{9}$', number):
            return True
        else:
            return False

    if is_valid_phone_number(phone_number):
        valid_phone_numbers += 1

    appointment_count += 1
    medicine_count += len(medicines)
    active_medicine_count += sum(1 for medicine in medicines if medicine['isActive'])

average_age = age_sum / appointment_count if appointment_count > 0 else 0

aggregated_data = {
    'Age': average_age,
    'gender': gender_count,
    'validPhoneNumbers': valid_phone_numbers,
    'appointments': appointment_count,
    'medicines': medicine_count,
    'activeMedicines': active_medicine_count
}

with open('aggregated_data.json', 'w') as file:
    json.dump(aggregated_data, file, indent=4)
