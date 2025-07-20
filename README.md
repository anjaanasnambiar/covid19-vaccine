# COVID-19 Vaccination Scheduler

A desktop application built with Python and Tkinter for managing COVID-19 vaccination appointments across multiple healthcare centers.

## Background

This application was developed during the COVID-19 pandemic period as an academic project when vaccination programs were being rolled out globally. It was created to demonstrate practical software development skills while addressing a real-world challenge of managing vaccination appointments efficiently during a critical public health initiative.

## Features

### Appointment Scheduling

* Interactive calendar for date selection (up to 30 days in advance)
* Multiple vaccination centers with different capacities and hours
* Time slot management with availability checking
* Real-time slot availability updates
* Input validation for personal information

## User Appointment Management

* Search appointments by email address
* View personal appointment details
* Cancel scheduled appointments
* User-friendly confirmation dialogs

## Admin Dashboard

* View all appointments with filtering options
* Statistics display (total appointments, center distribution)
* Date range filtering (30 days past to 60 days future)
* Center-specific filtering
* Export functionality for reports
* Admin-level appointment cancellation

## Data Management

* CSV-based data storage
* Automatic data persistence
* Export reports to CSV format
* Appointment capacity management per center

## Project Structure

```
vaccination-scheduler/
├── main.py              # Main application entry point and GUI
├── data_manager.py      # Data handling and CSV operations
├── validator.py         # Input validation utilities
├── requirements.txt     # Python dependencies
├── appointments.csv     # Data storage file (created automatically)
└── README.md           # This file
```

## License
This project is open source and available under the MIT License.
