import sys
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QApplication, QGraphicsBlurEffect, QVBoxLayout, QFrame, QLabel, QPushButton, QMainWindow, QMessageBox, QLineEdit, QStackedWidget, QDialog,QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QColor
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QSize, QEvent, pyqtSignal
from ui_login import Ui_MainWindow as Ui_LoginScreen
from ui_dashboard import Ui_MainWindow as Ui_DashboardScreen
from ui_timetablepg import Ui_MainWindow as Ui_timetable
from ui_studentpg import Ui_MainWindow as Ui_student
from ui_attendancepg import Ui_MainWindow as Ui_attendance
from custom_widgets import HoverCard
import ctypes
import os
import sys

if sys.platform == "win32":
    myappid = 'your.app.id'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Lecture(ctypes.Structure):
    _fields_ = [
        ("faculty_id", ctypes.c_int),
        ("subject", ctypes.c_char * 50),
        ("division", ctypes.c_char * 10),
        ("day", ctypes.c_int),
        ("slot", ctypes.c_int),
    ]

    
class LoginFailedPopup(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) #frameless gg
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 200)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.box = QFrame(self)
        self.box.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 20, 20, 240);
                border-radius: 20px; 
            }
            QLabel {
                color: white;
                border: none;
                background: transparent;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bb5; 
            }
        """)

        box_layout = QVBoxLayout(self.box)
        box_layout.setContentsMargins(20, 30, 20, 20)
        box_layout.setSpacing(15)

        title_label = QLabel("Login Failed")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)

        sub_label = QLabel("Incorrect username or password")
        sub_label.fontMetrics
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font1 = QFont()
        font1.setPointSize(10)
        sub_label.setFont(font1)
        try_again_btn = QPushButton("Try Again")
        try_again_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        try_again_btn.clicked.connect(self.accept) 
        
    
        box_layout.addWidget(title_label)
        box_layout.addWidget(sub_label)
        box_layout.addWidget(try_again_btn)
        main_layout.addWidget(self.box)

class Student(QMainWindow):                                         
    def __init__(self, stack_controller):
        super(). __init__()

        self.stack = stack_controller
        self.ui = Ui_student()
        self.ui.setupUi(self)

        self.ui.back_button.clicked.connect(self.back)

    def back(self):
        self.stack.setCurrentIndex(1)

class Attendance(QMainWindow):
    def __init__(self, stack_controller):
        super(). __init__()

        self.stack = stack_controller
        self.ui = Ui_attendance()
        self.ui.setupUi(self)

        self.ui.back_button.clicked.connect(self.back)

   
    def back(self):
        self.stack.setCurrentIndex(1)

class TimeTable(QMainWindow):
    def __init__(self, stack_controller, c_lib):
        super(). __init__()

        self.stack = stack_controller
        self.ui = Ui_timetable()
        self.ui.setupUi(self)
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
        self.table = QTableWidget(self)
        self.table.setRowCount(5)
        self.table.setColumnCount(5)
        self.table.setGeometry(50, 80, 850, 500)

        
        



# Resize to fill window
        self.table.setGeometry(50, 80, 850, 500)

        self.table.setStyleSheet("""
    QTableWidget {
        background-color: #ffffff;
        gridline-color: #e5e7eb;
        border: none;
        font-size: 15px;
    }

    QHeaderView::section {
        background-color: #1e3a8a;
        color: white;
        font-weight: bold;
        padding: 8px;
        border: none;
    }

    QTableWidget::item {
        padding: 10px;
    }

    QTableWidget::item:selected {
        background-color: #3b82f6;
        color: white;
    }
""")

        self.ui.back_button.clicked.connect(self.back)
        self.table.cellClicked.connect(self.handle_cell_click)
        self.c_lib = c_lib
        
   

    def load_schedule(self, faculty_id):
        lectures_ptr = ctypes.POINTER(Lecture)()
        count = ctypes.c_int()
    

        result = self.c_lib.getFacultySchedule(
            faculty_id,
            ctypes.byref(lectures_ptr),
            ctypes.byref(count)
        )
        print("Faculty ID requested:", faculty_id)
        print("Lecture count returned:", count.value)
       

        if result != 1:
            return

        lectures = lectures_ptr[:count.value]

    # Clear previous data
        self.table.clearContents()

        for lec in lectures:
            row = lec.day - 1
            col = lec.slot - 1

            
            division = lec.division.decode()
            subject = lec.subject.decode()

            text = f"Div {division}"
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item.setData(Qt.ItemDataRole.UserRole, {
               "day": lec.day,
               "slot": lec.slot,
               "division": division
             })

            tooltip = (
               f"<b>Subject:</b> {subject}<br>"
               f"<b>Division:</b> {division}<br>"
               f"<b>Day:</b> {lec.day}<br>"
               f"<b>Slot:</b> {lec.slot}"
             )

            print("Setting tooltip for:", text)   # MUST be inside loop
            item.setToolTip(tooltip)

        
            self.table.setItem(row, col, item)

        self.c_lib.freeSchedule(lectures_ptr)
    def handle_cell_click(self, row, column):
        faculty_id = getattr(self.stack.widget(1), "faculty_id", None)

        if faculty_id is None:
            return

        day = row + 1
        slot = column + 1

        reply = QMessageBox.question(
        self,
        "Confirm Absence",
        f"Mark absence for Day {day}, Slot {slot}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

        if reply != QMessageBox.StandardButton.Yes:
          return


        substitute_id = ctypes.c_int()

        result = self.c_lib.reportAbsence(
            faculty_id,
            day,
            slot,
            ctypes.byref(substitute_id)
        )

        if result == 1:
            name_buffer = ctypes.create_string_buffer(50)

            self.c_lib.getFacultyName(
                substitute_id.value,
                name_buffer
            )

            substitute_name = name_buffer.value.decode()

            QMessageBox.information(
                self,
                "Substitute Assigned",
                f"Substitute Teacher: {substitute_name}"
            )

            self.load_schedule(faculty_id)

        else:
            QMessageBox.warning(
                self,
                "Failed",
                "No substitute available or invalid slot."
            )

    def back(self):
        self.stack.setCurrentIndex(1)

class WelcomeWindow(QMainWindow):
    def __init__(self, stack_controller):
        super(). __init__()
        self.stack = stack_controller


        self.ui = Ui_DashboardScreen()
        self.ui.setupUi(self)

        self.ui.label_welcome.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.label_welcome.setAutoFillBackground(False)
    
        self.opacity_effect = QGraphicsOpacityEffect(self.ui.label_welcome)
        self.ui.label_welcome.setGraphicsEffect(self.opacity_effect)

        self.ui.card_layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ui.card_timetable.clicked.connect(self.timetable_viewer)
        self.ui.card_student.clicked.connect(self.report_absence_dialog)
        self.ui.card_attendance.clicked.connect(self.attendance_viewer)
        
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(1500)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.fade_anim.start()

        self.ui.signout_button.clicked.connect(self.signout)
    def generate_timetable(self):
        result = self.stack.widget(0).c_lib.generateTimetable()

        if result == 1:
            print("Timetable generated successfully")
        else:
            print("Failed to generate timetable")

    def update_name(self, name):
        welcome_html = f"""
                <div style="font-family: 'Cedarville Cursive';">
                <span style='color: #FFFFFF; font-size: 80px; font-weight: bold;'>Welcome </span>
                <span style='color: #FFFFFF; font-size: 80px; font-weight: bold;'>{name}!</span>
            </div>
        """
        self.ui.label_welcome.setText(welcome_html)

    def timetable_viewer(self):
       faculty_id = getattr(self, "faculty_id", None)

       if faculty_id is not None:
           self.stack.widget(2).load_schedule(faculty_id)

       self.stack.setCurrentIndex(2)

    def student_viewer(self):
        self.stack.setCurrentIndex(3)

    def attendance_viewer(self):
        self.stack.setCurrentIndex(4)
    def report_absence_dialog(self):
        from PyQt6.QtWidgets import QInputDialog

        faculty_id = getattr(self, "faculty_id", None)

        if faculty_id is None:
            return

        day, ok1 = QInputDialog.getInt(
            self, "Report Absence", "Enter Day (1-5):", min=1, max=5
        )
        if not ok1:
            return

        slot, ok2 = QInputDialog.getInt(
            self, "Report Absence", "Enter Slot (1-5):", min=1, max=5
        )
        if not ok2:
            return

        result = self.stack.widget(0).c_lib.reportAbsence(
            faculty_id,
            day,
            slot
        )

        if result == 1:
            QMessageBox.information(
                self,
                "Success",
                "Absence reported.\nSubstitute assigned."
            )

        # Refresh timetable
            self.stack.widget(2).load_schedule(faculty_id)

        else:
            QMessageBox.warning(
                self,
                "Failed",
                "No substitute available or invalid slot."
            )

    def signout(self):
        self.stack.widget(0).ui.password_input.clear()
        self.stack.widget(0).ui.username_input.clear()

        self.stack.setCurrentIndex(0)

class AdminDashboard(QMainWindow):
    def __init__(self, stack_controller, c_lib):
        super().__init__()
        self.stack = stack_controller
        self.c_lib = c_lib

        self.setWindowTitle("Admin Dashboard")
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.generate_btn = QPushButton("Generate Timetable")
        self.generate_btn.clicked.connect(self.generate_timetable)

        self.import_faculty_btn = QPushButton("Import Faculty CSV")
        self.import_faculty_btn.clicked.connect(self.import_faculty)
        layout.addWidget(self.import_faculty_btn)

        self.import_req_btn = QPushButton("Import Requirements CSV")
        self.import_req_btn.clicked.connect(self.import_requirements)
        layout.addWidget(self.import_req_btn) 

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)

        layout.addWidget(self.generate_btn)
        layout.addWidget(self.logout_btn)

        container = QFrame()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def generate_timetable(self):
        result = self.c_lib.generateTimetable()

        if result == 1:
            QMessageBox.information(self, "Success", "Timetable Generated!")
        else:
            QMessageBox.warning(self, "Error", "Failed to generate timetable.")
    def import_requirements(self):
       result = self.c_lib.importRequirementCSV()

       if result == 1:
           QMessageBox.information(self, "Success", "Requirements Imported!")
       else:
           QMessageBox.warning(self, "Error", "Import Failed!")
    def import_faculty(self):
       result = self.c_lib.importFacultyCSV()

       if result == 1:
           QMessageBox.information(self, "Success", "Faculty Imported!")
       else:
           QMessageBox.warning(self, "Error", "Faculty Import Failed!")

    def logout(self):
        self.stack.setCurrentIndex(0)

class LoginWindow(QMainWindow):
    def __init__(self, stack_controller):
        super(). __init__()
        self.stack = stack_controller

        self.ui = Ui_LoginScreen()
        self.ui.setupUi(self)
        

        ## super important for exe conversion and dllpath stuff, use wherever dlls are used
        if hasattr(sys, '_MEIPASS'):       
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(os.path.abspath(__file__))

      
        if sys.platform == "win32":
            lib_name = "backend.dll"
        else:
            lib_name = "backend.dylib"

        lib_path = os.path.join(basedir, lib_name)
        self.c_lib = ctypes.CDLL(lib_path)
        self.c_lib.generateTimetable.restype = ctypes.c_int
        self.c_lib.importRequirementCSV.restype = ctypes.c_int
        self.c_lib.importFacultyCSV.restype = ctypes.c_int

# ===== TIMETABLE =====
        self.c_lib.generateTimetable.restype = ctypes.c_int

        self.c_lib.getFacultySchedule.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.POINTER(Lecture)),
            ctypes.POINTER(ctypes.c_int)
      ]
        self.c_lib.getFacultySchedule.restype = ctypes.c_int

        self.c_lib.freeSchedule.argtypes = [
            ctypes.POINTER(Lecture)
       ]
# ===== ADMIN LOGIN =====
        self.c_lib.loginAdmin.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p
        ]
        self.c_lib.loginAdmin.restype = ctypes.c_int
#=====report absence=====


        self.c_lib.reportAbsence.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]
        self.c_lib.reportAbsence.restype = ctypes.c_int
#====get_faculty_name=====
        self.c_lib.getFacultyName.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p
    ]
        self.c_lib.getFacultyName.restype = ctypes.c_int
# ===== FACULTY LOGIN =====
        self.c_lib.loginFaculty.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_int)
        ]
        self.c_lib.loginFaculty.restype = ctypes.c_int
        ##

        self.ui.login_button.clicked.connect(self.authenticate)
        self.ui.show_password_checkbox.toggled.connect(self.toggle_password)

    def authenticate(self):
       username = self.ui.username_input.text()
       password = self.ui.password_input.text()

       user_bytes = username.encode("utf-8")
       pass_bytes = password.encode("utf-8")

    # ===== Check Admin Login =====
       if self.c_lib.loginAdmin(user_bytes, pass_bytes):
           print("Admin login successful")
           self.stack.setCurrentIndex(5)   # Admin dashboard
           return

    # ===== Check Faculty Login =====
       faculty_id = ctypes.c_int()

       result = self.c_lib.loginFaculty(
           user_bytes,
           pass_bytes,
           ctypes.byref(faculty_id)
       )

       if result == 1:
         print("Faculty login successful. ID:", faculty_id.value)

    # Go to Faculty Dashboard (WelcomeWindow)
         self.stack.setCurrentIndex(1)

    # Update welcome name
         self.stack.widget(1).update_name(username)

    # Store faculty ID for later use
         self.stack.widget(1).faculty_id = faculty_id.value

       else:
           error_popup = LoginFailedPopup(self)
           error_popup.exec()
    def toggle_password(self):
        if self.ui.show_password_checkbox.isChecked():
            self.ui.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else: 
            self.ui.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #setting app icon at the top left of everywindow
    app.setWindowIcon(QIcon("icon.ico"))

    font_id1 = QFontDatabase.addApplicationFont("Cedarville_Cursive/Cedarville_Cursive/CedarvilleCursive-Regular.ttf")
    families1 = QFontDatabase.applicationFontFamilies(font_id1)
    if families1:
        cedarville_font = families1[0]
        print(f"Font loaded as: {cedarville_font}")
    else:
        print("Font failed to load. Check the filename!")

    font_id = QFontDatabase.addApplicationFont("Inter/Inter-VariableFont_opsz,wght.ttf")
    families = QFontDatabase.applicationFontFamilies(font_id)
    if families:
        inter_font = families[0]
        print(f"Font loaded as: {inter_font}")
    else:
        print("Font failed to load. Check the filename!")

    app.setStyleSheet("""
        /* Target the Welcome Label specifically */
        QLabel#label_welcome {
            font-family: 'Inter', 'Inter Variable', sans-serif;
            font-size: 42px;
            background: transparent;
            border: none;
        }

        HoverCard {
            background-color: rgba(245, 245, 247, 0.9); 
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 24px;
        }
                      
        HoverCard QLabel {
            font-family: 'Inter', 'Inter Variable', sans-serif;
            font-size: 34px;
            font-weight: 700;
            background: transparent;
        }
        QToolTip {
        background-color: #2c3e50;
        color: white;
        border: 1px solid #1f2937;
        padding: 6px;
         }
    """)

    stack = QStackedWidget()
    stack.setWindowTitle("Faculty Assistant")
    stack.resize(1200,900)
    
    welcome_page = WelcomeWindow(stack)
    login_page = LoginWindow(stack)
    admin_page = AdminDashboard(stack, login_page.c_lib)
    timetable_page = TimeTable(stack, login_page.c_lib)
    student_page = Student(stack)
    attendance_page = Attendance(stack)


    stack.addWidget(login_page)     #Index 0
    stack.addWidget(welcome_page)   #Index 1
    stack.addWidget(timetable_page)      #Index 2
    stack.addWidget(student_page)        #Index 3
    stack.addWidget(attendance_page)     #Index 4
    stack.addWidget(admin_page)  # Index 5

    stack.show()
    sys.exit(app.exec())


# QFrame {
#     background: qlineargradient(
#         x1: 0, y1: 0, x2: 0, y2: 1, 
#         stop: 0 rgba(255, 255, 255, 255), 
#         stop: 0.7 rgba(255, 255, 255, 255),
#         stop: 1 rgba(18, 18, 18, 0)
#     );
#     border-radius: 20px;
# }
