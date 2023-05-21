import matplotlib.pyplot as plt
gender_counts = {
    "Male": 20,
    "Female": 15,
    "Others": 5
}

plt.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%')

plt.title("Appointments by Gender")

plt.show()

