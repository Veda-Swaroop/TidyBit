# UI MAIN WINDOW


# imports
import shutil
import copy
from pathlib import Path

from app.config import load_settings
from app.logic import fetch_files, categorize_files, label_files, create_category_table
from app.ui.styles import STYLESHEET
from app.ui.dialog_window import SettingsDialog
from app.utils.helper_function import resource_path


from PySide6.QtWidgets import (QMainWindow, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QProgressBar,
                                 QWidget, QFileDialog, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QFont




# Worker Thread class
class FileMoverWorker(QThread):
    def __init__(self, src_pth, dst_pth, category_dict):
        super().__init__()

        self.src_path = Path(src_pth)
        self.dst_path = Path(dst_pth)
        self.category_dict = category_dict
        self.is_running = True 

    # Define Signal Variables
    log_signal = Signal(str)
    progress_signal = Signal(int)
    finished_signal = Signal(dict)

    # FileMoverWorker.start() runs this run() method 
    def run(self):

        error_count = 0
        moved_count = 0
        total_files = len(self.category_dict)

        for i, (filename, category) in enumerate(self.category_dict.items(), start=1):
            if not self.is_running:
                break

            src_file = self.src_path / filename
            dst_folder = self.dst_path / category
            dst_file = dst_folder / filename

            try:
                dst_folder.mkdir(parents=True, exist_ok=True)
                # Handling duplicate filenames
                if dst_file.exists():
                    stem = dst_file.stem
                    suffix = dst_file.suffix
                    counter = 1
                    while dst_file.exists():
                        dst_file = dst_folder / f"{stem}_{counter}{suffix}"
                        counter += 1
                    self.log_signal.emit(f"[info] Renamed dulplicate to: {dst_file.name}")

                # Move Files
                shutil.move(str(src_file), str(dst_file))
                moved_count += 1

            except PermissionError:
                error_count += 1
                self.log_signal.emit(f"[error] ACCESS DENIED: {filename}")
            except Exception as e:
                error_count += 1
                self.log_signal.emit(f"[error] Failed {filename}: {e}")

            # Update ProgressBar to UI
            percent = int(i / total_files) * 100
            self.progress_signal.emit(percent)
        # Update stats to UI
        stats = {"moved": moved_count, "errors": error_count}
        self.finished_signal.emit(stats)

    # Stop method to stop the worker
    def stop(self):
        self.is_running = False

# App UI
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # App Data
        self.data = load_settings() 

        # UI window
        self.setObjectName("MainWindow")
        self.setWindowTitle("TidyBit - a simple file organizer")
        self.resize(800, 700)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Defining Layouts
        root_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        content_layout = QGridLayout()

        # Set root_layout as central widget
        central_widget.setLayout(root_layout)


        # Settings Button
        self.settings_btn = QPushButton()
        settings_icon_path = resource_path("assets/settings_icon.svg")
        self.settings_btn.setIcon(QIcon(settings_icon_path))
        self.settings_btn.setFixedSize(35, 35)
        self.settings_btn.setFlat(True)
        self.settings_btn.setToolTip("Configure Extensions")
        self.settings_btn.clicked.connect(self.open_settings)

        # Title Label
        title_label = QLabel("TidyBit")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: grey;")

        # Version Label
        ver_label = QLabel("v1.3")
        ver_font = QFont()
        ver_font.setPointSize(10)
        ver_font.setBold(True)
        ver_label.setFont(ver_font)
        ver_label.setStyleSheet("color: grey;")



        # Add settings button and title label to header layout
        header_layout.addWidget(self.settings_btn)
        header_layout.addSpacing(10)
        header_layout.addWidget(title_label)
        header_layout.addWidget(ver_label)
        header_layout.addStretch()
        
        # Content Layout
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setColumnStretch(1, 1)


        # Labels
        self.label_1 = QLabel("Source Folder Path ")
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.label_1, 0, 0)

        self.label_2 = QLabel("Target Folder Path ")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.label_2, 1, 0)

        # Entries or Line Edits
        self.entry_1 = QLineEdit()
        self.entry_1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_1.setPlaceholderText("Select Source Folder")
        self.entry_1.textChanged.connect(self.reset_state)
        content_layout.addWidget(self.entry_1, 0, 1)

        self.entry_2 = QLineEdit()
        self.entry_2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_2.setPlaceholderText("Select Target Folder")
        self.entry_2.textChanged.connect(self.reset_state)
        content_layout.addWidget(self.entry_2, 1, 1)

        # Buttons
        self.btn_1 = QPushButton("Browse")
        self.btn_1.setFixedSize(100, 40)
        self.btn_1.clicked.connect(self.browse_source)
        content_layout.addWidget(self.btn_1, 0, 2)

        self.btn_2 = QPushButton("Browse")
        self.btn_2.setFixedSize(100, 40)
        self.btn_2.clicked.connect(self.browse_target)
        content_layout.addWidget(self.btn_2, 1, 2)

        # Log Box 
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        content_layout.addWidget(self.log_box, 2, 0, 1, 3)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        content_layout.addWidget(self.progress_bar, 3, 0, 1, 3)

        # Action Button
        self.btn_3 = QPushButton("Start")
        self.btn_3.setFixedHeight(60)
        self.btn_3.clicked.connect(self.action_btn)
        content_layout.addWidget(self.btn_3, 4, 1)

        
        root_layout.addLayout(header_layout)
        root_layout.addLayout(content_layout)

        # State Variable
        self.btn_3_state = 0
        # Variable to count execution flow cycle of action buttion
        self.flow_cycle = 0


    # class methods
    def browse_source(self):
        home_dir = str(Path.home())
        source_dir = QFileDialog.getExistingDirectory(self, "Select a folder", home_dir)
        if source_dir:
            # delete placeholder text
            self.entry_1.clear()
            # insert source path
            self.entry_1.setText(source_dir)
            # log the path in log_box
            if self.btn_3_state > 0:
                self.log_box.clear()
            self.log_box.append(f"📂 Source: {source_dir}\n")


    def browse_target(self):
        home_dir = str(Path.home())
        target_dir = QFileDialog.getExistingDirectory(self, "Select a folder", home_dir)
        if target_dir:
            # delete placeholder text
            self.entry_2.clear()
            # insert target path
            self.entry_2.setText(target_dir)
            # log the path in log_box
            if self.btn_3_state > 0:
                self.log_box.clear()
            self.log_box.append(f"📂 Target: {target_dir}\n")


    def reset_state(self):
        self.btn_3_state = 0
        self.btn_3.setText("Start")

    # Open settings - dialog window
    def open_settings(self):
        dialog = SettingsDialog(
            data = copy.deepcopy(self.data),
            parent = self
        )
        dialog.settings_applied.connect(self.apply_settings)
        dialog.exec()
    
    # Update app with new_data
    def apply_settings(self, new_data):
        self.data = new_data
        


    # Action Button
    def action_btn(self):

        self.src_pth = self.entry_1.text()
        self.dst_pth = self.entry_2.text()
        
        # Start(state=0) -> Fetch(state=1) -> Organize(state=2) -> Move(state=3)
        

        # state 0, Start
        if self.btn_3_state == 0:

            # if execution flow completes a cycle, clear log_box
            if self.flow_cycle > 0:
                self.log_box.clear()
            self.progress_bar.setValue(0)
            
            # Confirm both paths are selected
            if self.src_pth == "" or self.dst_pth == "":
                QMessageBox.warning(self, "Warning", "Please select both source and target folder paths!")
                return

            # Validate Source and Target paths.
            src_p = Path(self.src_pth)
            dst_p = Path(self.dst_pth)

            if not src_p.exists():
                QMessageBox.warning(self, "Invalid Source folder path", f"{self.src_pth} does not exist.")
                return
            if not dst_p.exists():
                QMessageBox.warning(self, "Invalid Target folder path", f"{self.dst_pth} does not exist.")
                return

            # if source and target paths are same, stop. It throws error.
            if src_p.resolve() == dst_p.resolve():
                QMessageBox.critical(self, "Error", "Source and Target can't be the same folder.\nPlease select a different Target folder.")
                return

            # If both paths are confirmed and valid, Ready to fetch.
            self.log_box.append(f"✅ Source and Target paths are valid. Ready to Fetch Files.\n")

            # Change the state variable and button to Fetch.
            self.btn_3.setText("Fetch Files")
            self.btn_3_state = 1


        # state 1, Fetch files
        elif self.btn_3_state == 1:
        
            # Prepare log_box before file fetch
            self.log_box.append(f"⏳ Fetching files from: {self.src_pth}\n")

            # Fetch files from source path and display them in log_box
            try:
                self.files = fetch_files(self.src_pth)
            except Exception as e:
                self.log_box.append(f"❌ Error occured while fetching files. {e}\n")
                return

            # If source folder is empty
            if not self.files:
                self.log_box.append("ℹ️ No files found in source folder!\n")
                return

            for index, file in enumerate(self.files, start=1):
                self.log_box.append(f"{index}. {file}")

            self.log_box.append("")
           
            # Change the state variable and button to Fetch.
            self.btn_3.setText("Organize Files")
            self.btn_3_state = 2


        # state 2, Organize files
        elif self.btn_3_state == 2:

            # organize files into categories based on file extension
            self.category_list, group_dict = categorize_files(self.files, self.data)

            # If group_dict is empty
            if not group_dict:
                self.log_box.append("ℹ️ No categorizable files found.")
                return

            # display file category and total file count in each category.
            self.log_box.append(f"⏳ Organizing files into categories\n")
            formatted_table = create_category_table(group_dict)
            self.log_box.insertHtml(formatted_table)

            # Auto-scroll to bottom of log_box
            scrollbar = self.log_box.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

            # Change state variable and the button to Move.
            self.btn_3.setText("Move Files")
            self.btn_3_state = 3


        # state 3, Move files 
        elif self.btn_3_state == 3:

            # Assign a category to each file
            try:
                category_dict = label_files(self.files, self.category_list)
            except ValueError as e:
                self.log_box.append(f"❌ Error: {e}\n")
                return

            if not category_dict:
                self.log_box.append("ℹ️ No files found to Move.\n")
                return

            # Disable Button in UI
            self.btn_3.setEnabled(False)
            self.btn_3.setText("...Moving Files...")

            # Setup Thread
            self.worker = FileMoverWorker(self.src_pth, self.dst_pth, category_dict)

            # Connect to Signals from Worker
            self.worker.log_signal.connect(self.update_log)
            self.worker.progress_signal.connect(self.update_progress)
            self.worker.finished_signal.connect(self.on_move_finished)

            # Start worker
            self.worker.start()

    # Slot methods called by worker thread
    def update_log(self, text):
        self.log_box.append(text)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_move_finished(self, stats):
        moved = stats["moved"]
        errors = stats["errors"]

        if errors == 0:
            # If files moved successfully, display that in log_box
            QMessageBox.information(self, "Success", "Files are organized and moved to Target Folder")
            self.log_box.append(f"✅ Files moved to {self.dst_pth}\n")
            
        else:
            # If errors occured while moving, display info in log box
            QMessageBox.warning(self, "Completed with Errors", f"Moved {moved} files, Failed {errors}")
            self.log_box.append(f"⚠️ {errors} errors occured.\n")

        ## Reset the button to Start and state variable=0.
        self.btn_3.setEnabled(True)
        self.reset_state()
        self.flow_cycle += 1



