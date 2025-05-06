import os
import csv

class DataManager:
    
    def __init__(self, data_file="appointments.csv"):
        self.data_file = data_file
        self.appointments = {}
        
        self.centers = {
            "Nearest Government Hospital": {
                "capacity": 50,
                "hours": "8:00 AM - 5:00 PM"
            },
            "Nearest Government Clinic": {
                "capacity": 30,
                "hours": "9:00 AM - 4:00 PM"
            },
            "Nearest COVID-19 Vaccination Camp": {
                "capacity": 40,
                "hours": "8:30 AM - 2:00 PM"
            }
        }
        
        self.time_slots = ["08:00", "09:00", "10:00", "11:00", "12:00", 
                          "13:00", "14:00", "15:00", "16:00"]
        
        self.load_appointments()
    
    def load_appointments(self):
        appointments = {}
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    if len(row) >= 6: 
                        date, time, center, name, phone, email = row[:6]
                        key = f"{date}_{time}_{center}"
                        
                        if key not in appointments:
                            appointments[key] = []
                        appointments[key].append({
                            "name": name,
                            "phone": phone,
                            "email": email
                        })
        
        self.appointments = appointments
        return appointments
    
    def save_appointments(self):
        with open(self.data_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Center", "Name", "Phone", "Email"])
            
            for key, people in self.appointments.items():
                date, time, center = key.split("_")
                for person in people:
                    writer.writerow([date, time, center, person["name"], 
                                   person["phone"], person["email"]])
    
    def add_appointment(self, date, time, center, name, phone, email):
        key = f"{date}_{time}_{center}"
        
        if key not in self.appointments:
            self.appointments[key] = []
        
        self.appointments[key].append({
            "name": name,
            "phone": phone,
            "email": email
        })
        
        self.save_appointments()
        
    def cancel_appointment(self, date, time, center, email):
        key = f"{date}_{time}_{center}"
        if key in self.appointments:
            for i, person in enumerate(self.appointments[key]):
                if person["email"] == email:
                    self.appointments[key].pop(i)
                    if not self.appointments[key]:  
                        del self.appointments[key]
                    self.save_appointments()
                    return True
        return False
    
    def get_appointments_by_email(self, email):
        results = []
        for key, people in self.appointments.items():
            date, time, center = key.split("_")
            for person in people:
                if person["email"].lower() == email.lower():
                    results.append((date, time, center, person))
        return results
    
    def get_filtered_appointments(self, date=None, center=None):
        results = []
        for key, people in self.appointments.items():
            key_date, key_time, key_center = key.split("_")
            
            if (date is None or key_date == date) and (center is None or key_center == center):
                for person in people:
                    results.append((key_date, key_time, key_center, person))
        
        results.sort(key=lambda x: (x[0], x[1]))
        return results
    
    def is_slot_available(self, date, time, center):
        key = f"{date}_{time}_{center}"
        center_capacity = self.centers[center]["capacity"] // len(self.time_slots)
        
        if key in self.appointments and len(self.appointments[key]) >= center_capacity:
            return False
        return True
    
    def export_report(self, filename, date=None, center=None):
        appointments = self.get_filtered_appointments(date, center)
        
        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Center", "Name", "Phone", "Email"])
                
                for date, time, center, person in appointments:
                    writer.writerow([date, time, center, person["name"], 
                                   person["phone"], person["email"]])
            return True
        except:
            return False