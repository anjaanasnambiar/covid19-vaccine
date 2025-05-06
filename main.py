#!/usr/bin/env python3
import sys
import _tkinter
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import datetime
from data_manager import DataManager
from validator import InputValidator

class VaccinationScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("COVID-19 Vaccination Scheduler")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        self.data_manager = DataManager()
        self.validator = InputValidator()
        self.tab_control = ttk.Notebook(root)
        
        self.schedule_tab = ttk.Frame(self.tab_control)
        self.view_tab = ttk.Frame(self.tab_control)
        self.admin_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.schedule_tab, text="Schedule Appointment")
        self.tab_control.add(self.view_tab, text="View your Appointment")
        self.tab_control.add(self.admin_tab, text="All Appointments")
        
        self.tab_control.pack(expand=1, fill="both")
        
        self.setup_schedule_tab()
        self.setup_view_tab()
        self.setup_admin_tab()
        
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        self.data_manager.save_appointments()
        self.root.destroy()
        
    def setup_schedule_tab(self):
        frame = ttk.Frame(self.schedule_tab, padding=20)
        frame.pack(fill="both", expand=True)
        
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Select Date:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        
        today = datetime.date.today()
        self.cal = Calendar(left_frame, selectmode="day", year=today.year, month=today.month, day=today.day,
                          mindate=today, maxdate=today + datetime.timedelta(days=30))
        self.cal.pack(fill="x", pady=(0, 15))
        
        ttk.Label(left_frame, text="Select Vaccination Center:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        
        self.center_var = tk.StringVar()
        center_frame = ttk.Frame(left_frame)
        center_frame.pack(fill="x", pady=(0, 15))
        
        for center in self.data_manager.centers:
            ttk.Radiobutton(center_frame, text=center, value=center, variable=self.center_var).pack(anchor="w")
        
        self.center_var.set(list(self.data_manager.centers.keys())[0])  
        self.center_details = ttk.LabelFrame(left_frame, text="Center Details", padding=10)
        self.center_details.pack(fill="x")
        
        self.center_info_label = ttk.Label(self.center_details, text="", wraplength=300)
        self.center_info_label.pack(fill="x")
        
        self.update_center_details()
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10, 0))
        
        ttk.Label(right_frame, text="Select Time:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))

        self.time_var = tk.StringVar()
        self.time_slots_frame = ttk.Frame(right_frame)
        self.time_slots_frame.pack(fill="x", pady=(0, 15))
        
        self.time_buttons = []
        for i, time in enumerate(self.data_manager.time_slots):
            rb = ttk.Radiobutton(self.time_slots_frame, text=time, value=time, variable=self.time_var)
            rb.grid(row=i//3, column=i%3, sticky="w", padx=5, pady=2)
            self.time_buttons.append(rb)
        
        self.time_var.set(self.data_manager.time_slots[0])  
        
        info_frame = ttk.LabelFrame(right_frame, text="Personal Information", padding=10)
        info_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(info_frame, text="Full Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Phone:").grid(row=1, column=0, sticky="w", pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, sticky="w", pady=5)
        
        submit_button = ttk.Button(right_frame, text="Schedule Appointment", command=self.schedule_appointment)
        submit_button.pack(anchor="e", pady=(15, 0))
        
        self.center_var.trace_add("write", lambda *args: self.update_center_details())
        self.cal.bind("<<CalendarSelected>>", lambda event: self.update_available_slots())
        self.center_var.trace_add("write", lambda *args: self.update_available_slots())
    
    def update_center_details(self):
        center_name = self.center_var.get()
        if center_name in self.data_manager.centers:
            center = self.data_manager.centers[center_name]
            info_text = f"Hours: {center['hours']}\nDaily Capacity: {center['capacity']} appointments"
            self.center_info_label.config(text=info_text)
    
    def update_available_slots(self, *args):
        selected_date = self.cal.get_date()
        selected_center = self.center_var.get()
        
        for i, button in enumerate(self.time_buttons):
            button.config(state="normal")
            
        for i, time in enumerate(self.data_manager.time_slots):
            if not self.data_manager.is_slot_available(selected_date, time, selected_center):
                self.time_buttons[i].config(state="disabled")
    
    def schedule_appointment(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        
        is_valid, errors = self.validator.validate_appointment_form(name, phone, email)
        if not is_valid:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        selected_date = self.cal.get_date()
        selected_time = self.time_var.get()
        selected_center = self.center_var.get()
        
        if not self.data_manager.is_slot_available(selected_date, selected_time, selected_center):
            messagebox.showerror("Error", "This time slot is no longer available. Please select another.")
            self.update_available_slots()
            return
        
        self.data_manager.add_appointment(selected_date, selected_time, selected_center, name, phone, email)
        confirmation = f"Appointment scheduled!\n\nDate: {selected_date}\nTime: {selected_time}\nCenter: {selected_center}"
        messagebox.showinfo("Success", confirmation)
        
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        
        self.update_available_slots()
    
    def setup_view_tab(self):
        frame = ttk.Frame(self.view_tab, padding=20)
        frame.pack(fill="both", expand=True)

        search_frame = ttk.LabelFrame(frame, text="Search Appointments", padding=10)
        search_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(search_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5)
        self.search_email = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_email, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(search_frame, text="Search", command=self.search_appointments).grid(row=0, column=2, padx=5, pady=5)
        
        self.results_frame = ttk.LabelFrame(frame, text="Your Appointments", padding=10)
        self.results_frame.pack(fill="both", expand=True)
        
        columns = ("Date", "Time", "Center", "Name", "Phone", "Email")
        self.appointments_tree = ttk.Treeview(self.results_frame, columns=columns, show="headings")
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        cancel_frame = ttk.Frame(frame)
        cancel_frame.pack(fill="x", pady=(10, 0))
        ttk.Button(cancel_frame, text="Cancel Selected Appointment", 
                  command=self.cancel_appointment).pack(side="right")
    
    def search_appointments(self):
        search_email = self.search_email.get().strip().lower()
        
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        if not search_email:
            messagebox.showinfo("Info", "Please enter an email to search.")
            return
        
        appointments = self.data_manager.get_appointments_by_email(search_email)
        
        if not appointments:
            messagebox.showinfo("Info", "No appointments found for this email.")
            return
            
        for appt in appointments:
            date, time, center, data = appt
            self.appointments_tree.insert("", "end", values=(date, time, center, 
                                                       data["name"], data["phone"], data["email"]))
    
    def cancel_appointment(self):
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an appointment to cancel.")
            return
        
        values = self.appointments_tree.item(selected_item, "values")
        date, time, center, name, phone, email = values
        
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to cancel this appointment?\n\n"
                                      f"Date: {date}\nTime: {time}\nCenter: {center}")
        if not confirm:
            return
        
        success = self.data_manager.cancel_appointment(date, time, center, email)
        
        if success:
            self.appointments_tree.delete(selected_item)
            messagebox.showinfo("Success", "Appointment has been cancelled.")
        else:
            messagebox.showerror("Error", "Failed to cancel appointment.")
    
    def setup_admin_tab(self):
        frame = ttk.Frame(self.admin_tab, padding=20)
        frame.pack(fill="both", expand=True)
        
        filter_frame = ttk.LabelFrame(frame, text="Filters", padding=10)
        filter_frame.pack(side="left", fill="y", padx=(0, 10))
        
        ttk.Label(filter_frame, text="Select Date:").pack(anchor="w", pady=(0, 5))

        today = datetime.date.today()
        self.admin_cal = Calendar(filter_frame, selectmode="day", year=today.year, month=today.month, day=today.day,
                                mindate=today - datetime.timedelta(days=30),
                                maxdate=today + datetime.timedelta(days=60))
        self.admin_cal.pack(fill="x", pady=(0, 15))
        
        ttk.Label(filter_frame, text="Center:").pack(anchor="w", pady=(0, 5))
        self.admin_center_var = tk.StringVar(value="All Centers")
        centers = ["All Centers"] + list(self.data_manager.centers.keys())
        ttk.Combobox(filter_frame, textvariable=self.admin_center_var, values=centers, state="readonly").pack(fill="x")
        
        ttk.Button(filter_frame, text="Apply Filters", command=self.refresh_admin_view).pack(pady=(15, 0))
        
        content_frame = ttk.Frame(frame)
        content_frame.pack(side="right", fill="both", expand=True)
        
        stats_frame = ttk.LabelFrame(content_frame, text="Statistics", padding=10)
        stats_frame.pack(fill="x", pady=(0, 10))
        
        self.total_appointments_var = tk.StringVar(value="Total Appointments: 0")
        ttk.Label(stats_frame, textvariable=self.total_appointments_var).grid(row=0, column=0, padx=10)
        
        self.center_distribution_var = tk.StringVar(value="")
        ttk.Label(stats_frame, textvariable=self.center_distribution_var).grid(row=0, column=1, padx=10)
        
        appointments_frame = ttk.LabelFrame(content_frame, text="Appointments", padding=10)
        appointments_frame.pack(fill="both", expand=True)
        
        columns = ("Date", "Time", "Center", "Name", "Phone", "Email")
        self.admin_tree = ttk.Treeview(appointments_frame, columns=columns, show="headings")
        
        for col in columns:
            self.admin_tree.heading(col, text=col)
            self.admin_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(appointments_frame, orient="vertical", command=self.admin_tree.yview)
        self.admin_tree.configure(yscrollcommand=scrollbar.set)
        
        self.admin_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Export Report", command=self.export_report).pack(side="left", padx=(0, 10))
        ttk.Button(buttons_frame, text="Cancel Selected", command=self.admin_cancel_appointment).pack(side="left")
        

        self.refresh_admin_view()
        
        self.admin_cal.bind("<<CalendarSelected>>", lambda event: self.refresh_admin_view())
        self.admin_center_var.trace_add("write", lambda *args: self.refresh_admin_view())
    
    def refresh_admin_view(self, *args):
        selected_date = self.admin_cal.get_date()
        selected_center = self.admin_center_var.get()
        
        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)
        
        center = None if selected_center == "All Centers" else selected_center
        appointments = self.data_manager.get_filtered_appointments(selected_date, center)
        
        for appt in appointments:
            date, time, center, data = appt
            self.admin_tree.insert("", "end", values=(date, time, center, 
                                                 data["name"], data["phone"], data["email"]))
        
        self.total_appointments_var.set(f"Total Appointments: {len(appointments)}")
        
        if selected_center == "All Centers":
            center_counts = {}
            for _, _, center, _ in appointments:
                center_counts[center] = center_counts.get(center, 0) + 1
            
            distribution = ", ".join(f"{center}: {count}" for center, count in center_counts.items())
            self.center_distribution_var.set(f"Distribution: {distribution}")
        else:
            self.center_distribution_var.set("")
    
    def admin_cancel_appointment(self):
        selected_item = self.admin_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an appointment to cancel.")
            return
        
        values = self.admin_tree.item(selected_item, "values")
        date, time, center, name, phone, email = values
        
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to cancel this appointment?\n\n"
                                      f"Date: {date}\nTime: {time}\nCenter: {center}\nName: {name}")
        if not confirm:
            return
        
        success = self.data_manager.cancel_appointment(date, time, center, email)
        
        if success:
            self.admin_tree.delete(selected_item)
            messagebox.showinfo("Success", "Appointment has been cancelled.")
            
            self.refresh_admin_view()
        else:
            messagebox.showerror("Error", "Failed to cancel appointment.")
    
    def export_report(self):
        from tkinter import filedialog
        selected_date = self.admin_cal.get_date()
        selected_center = self.admin_center_var.get()
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"vaccination_report_{selected_date}.csv"
        )
        
        if not filename:
            return
        
        center = None if selected_center == "All Centers" else selected_center
        success = self.data_manager.export_report(filename, selected_date, center)

def main():
    root = tk.Tk()
    app = VaccinationScheduler(root)
    root.mainloop()

if __name__ == "__main__":
    main()