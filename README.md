# Faculty Assistant

A desktop application built with Python, PyQt6, and C to support faculty scheduling and timetable management.

## Overview

Faculty Assistant combines a graphical desktop interface with a native C backend. The application provides faculty login, timetable viewing, administrative timetable generation, data-import workflows, and absence reporting.

## Features

- **Faculty authentication:** Login workflow for faculty and administrators.
- **Timetable management:** View faculty schedules in a tabular interface.
- **Timetable generation:** Trigger timetable generation through the C backend.
- **CSV imports:** Import faculty and scheduling requirement data.
- **Absence reporting:** Report a faculty absence and attempt to assign a substitute.
- **Desktop interface:** Multi-screen application built with PyQt6, including custom widgets and interactive UI elements.

## Technologies

- Python
- C
- PyQt6
- `ctypes` for Python-to-C integration
- Qt Designer UI files
- CSV-based data import

## Project Structure

- `main.py` — Main application and interface navigation
- `Database.c` — C source for student and faculty data handling
- `custom_widgets.py` — Custom interactive UI components
- `login.ui` — Login interface
- `dashboard.ui` — Main dashboard interface
- `timetablepg.ui` — Timetable screen
- `studentpg.ui` — Student screen
- `attendancepg.ui` — Attendance screen

## Architecture

The Python application manages the graphical interface and user interactions. Through `ctypes`, it calls functions in a native C library for operations such as authentication, timetable generation, schedule retrieval, and absence reporting.

## Setup

1. Install Python and a compatible version of PyQt6.
2. Compile the C backend into a shared library compatible with your operating system.
3. Ensure the shared library exports the functions used by the Python application.
4. Convert the Qt Designer `.ui` files into Python modules with the appropriate names expected by `main.py`.
5. Configure the required input data files using safe, non-sensitive sample data.
6. Run the application from Python.

Exact build commands and data-file formats will be documented after the build configuration and backend dependencies are verified.

## Security Note

Use sample data for demonstrations. Do not commit real faculty or student records, passwords, or other confidential information.

## Future Improvements

- Document the backend build process for supported operating systems.
- Add sample datasets and reproducible setup instructions.
- Improve automated testing and input validation.
- Document timetable-generation constraints and evaluation.
