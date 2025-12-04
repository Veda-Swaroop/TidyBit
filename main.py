# TidyBit with PySide6 UI

import sys
from pathlib import Path
import shutil
from file_ext import file_extensions
from PySide6.QtWidgets import (QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QGridLayout, QProgressBar,
                                 QWidget, QFileDialog, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon


# Helper Function
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS) #type: ignore
    except Exception:
        base_path = Path.cwd()

    return str((base_path / relative_path).resolve())

def fetch_files(src):
    unfiltered_files = Path(src)
    files = [p.name for p in unfiltered_files.iterdir() if p.is_file() and not p.name.startswith(".")]
    return files


def categorize_files(files):
    bag = []
    grouped_dict = {}

    ## splitting each file into it's name and extension.
    for file in files:
        p = Path(file)
        filename = p.stem
        extension = p.suffix

    ## Categorize each extension.
        if extension == "":
            if filename in {"README", "LICENSE", "Makefile", "Dockerfile"}:
                bag.append("documents")
    
        extn_category = identify_extension(extension)
        bag.append(extn_category)   # bag contains the category name of each extension.

    # Group similar category of extensions and display the count of each extension.
    for item in set(bag):
        grouped_dict[item] = bag.count(item)

    return bag, grouped_dict

# Label each file based on it's extension.
def label_files(files, bag):
    label_dict = {}
    if len(files) != len(bag):
        raise ValueError("Mismatch error in labelling files")
        
    label_dict = dict(zip(files, bag))    

    return label_dict   

# Identify file extension
def identify_extension(b):
    b = b.lower()
    # b = unknown extension
    for category, category_dict in file_extensions.items():
        # if b is in category_dict, extension category is found
        if b in category_dict:
            return category

    return f"others"   # If not found, retun others to prevent program crash.

# Html Table that displays file category and count for QTextEdit
def create_category_table(group_dict):
    """
    Takes a dictionary {'Images': 5, 'Docs': 2} and returns 
    a formatted string that aligns perfectly in QTextEdit.
    """
    # We define the style colors here (Grey text for names, White for counts)
    row_html = ""
    for key, value in group_dict.items():
        row_html += f"""
        <tr>
            <td style="padding-right: 30px; color: #ffffff;">{key}</td>
            <td style="text-align: right; color: #ffffff; font-weight: bold;">{value}</td>
        </tr>
        """
    
    # Wrap it in a table structure
    full_html = f"""
    <br>
    <table cellspacing="0" cellpadding="3">
        <tr>
            <th style="text-align: left; color: #888888; border-bottom: 1px solid #555;">Category</th>
            <th style="text-align: right; color: #888888; border-bottom: 1px solid #555;">Count</th>
        </tr>
        {row_html}
    </table>
    <br>
    """
    return full_html

# App Stylesheet

STYLESHEET = """
    QWidget {
        background-color: #2E2E2E;
        color: white;
        font-size: 10pt; 
    }

    QLineEdit {
        background-color: #2E2E2E;
        border: 2px solid grey;
        border-radius: 10px;
        color: white;
        padding: 10px;
    }

    QTextEdit {
        background-color: #2E2E2E;
        border: 2px solid grey;
        border-radius: 10px;
        color: white;
        padding: 10px;
        }

    QScrollBar:vertical{
        border: 2px solid #888888;
        border-radius: 11px;
        background: #2E2E2E;
        width: 22px;
        margin: 0px 0px 0px 0px;
        }
    QScrollBar::handle:vertical {
        background-color: #1F6AA5;
        min-height: 30px;
        border-radius: 6px;
        margin: 3px 3px 3px 3px;
        }
    QScrollBar::handle:vertical:hover {
        background-color: #2980b9;
        }
    QScrollBar::handle:vertical:pressed {
        background-color: #145374;
        }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;   
        border: none;
        background: none;
        }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        border: none;
        background: none;
        }
    QscrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
        }

    QTextEdit QWidget {
        background-color: transparent;
    }

    QPushButton {
        background-color: #1F6AA5;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 12pt;
        padding: 10px;                
    }
    QPushButton:hover{
        background-color: #2580c4;
        color: white;
    }
    QPushButton:pressed {
        background-color: #145374;  
    }
    QPushButton:disabled {
        background-color: #555555;
        color: #aaaaaa;
    }

    QProgressBar {
        background: #2E2E2E;
        border: 2px solid grey;
        border-radius: 10px;
        color: white;
        font: bold 10pt;
        padding: 10px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #4CAF50;
        border-radius: 10px;
    }"""

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

        # UI window
        self.setObjectName("MainWindow")
        self.setWindowTitle("TidyBit - a simple file organizer")
        self.resize(800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout Manager
        main_layout = QGridLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        central_widget.setLayout(main_layout)
        main_layout.setColumnStretch(1, 1)


        # Labels
        self.label_1 = QLabel("Source Folder Path ")
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_1, 0, 0)

        self.label_2 = QLabel("Target Folder Path ")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_2, 1, 0)

        # Entries or Line Edits
        self.entry_1 = QLineEdit()
        self.entry_1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_1.setPlaceholderText("Select Source Folder")
        self.entry_1.textChanged.connect(self.reset_state)
        main_layout.addWidget(self.entry_1, 0, 1)

        self.entry_2 = QLineEdit()
        self.entry_2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_2.setPlaceholderText("Select Target Folder")
        self.entry_2.textChanged.connect(self.reset_state)
        main_layout.addWidget(self.entry_2, 1, 1)

        # Buttons
        self.btn_1 = QPushButton("Browse")
        self.btn_1.setFixedSize(100, 40)
        self.btn_1.clicked.connect(self.browse_source)
        main_layout.addWidget(self.btn_1, 0, 2)

        self.btn_2 = QPushButton("Browse")
        self.btn_2.setFixedSize(100, 40)
        self.btn_2.clicked.connect(self.browse_target)
        main_layout.addWidget(self.btn_2, 1, 2)

        # Log Box 
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        main_layout.addWidget(self.log_box, 2, 0, 1, 3)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar, 3, 0, 1, 3)

        # Action Button
        self.btn_3 = QPushButton("Start")
        self.btn_3.setFixedHeight(60)
        self.btn_3.clicked.connect(self.action_btn)
        main_layout.addWidget(self.btn_3, 4, 1)


        # State Variable
        self.btn_3_state = 0
        # Variable to count execution flow cycle of action buttion
        self.flow_cycle = 0


    # class methods
    def browse_source(self):
        source_dir = QFileDialog.getExistingDirectory(self, "Select a folder", "")
        if source_dir:
            # delete placeholder text
            self.entry_1.clear()
            # insert source path
            self.entry_1.setText(source_dir)
            # log the path in log_box
            if self.btn_3_state > 0:
                self.log_box.clear()
            self.log_box.append(f"[dir] Source: {source_dir}\n")


    def browse_target(self):
        target_dir = QFileDialog.getExistingDirectory(self, "Select a folder", "")
        if target_dir:
            # delete placeholder text
            self.entry_2.clear()
            # insert target path
            self.entry_2.setText(target_dir)
            # log the path in log_box
            if self.btn_3_state > 0:
                self.log_box.clear()
            self.log_box.append(f"[dir] Target: {target_dir}\n")


    def reset_state(self):
        self.btn_3_state = 0
        self.btn_3.setText("Start")


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
            self.log_box.append(f"[o.k] Source and Target paths are valid. Ready to Fetch Files.\n")

            # Change the state variable and button to Fetch.
            self.btn_3.setText("Fetch Files")
            self.btn_3_state = 1


        # state 1, Fetch files
        elif self.btn_3_state == 1:
        
            # Prepare log_box before file fetch
            self.log_box.append(f"[...] Fetching files from: {self.src_pth}\n")

            # Fetch files from source path and display them in log_box
            try:
                self.files = fetch_files(self.src_pth)
            except Exception as e:
                self.log_box.append(f"[error] Error occured while fetching files. {e}\n")
                return

            # If source folder is empty
            if not self.files:
                self.log_box.append("[info] No files found in source folder!\n")
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
            self.category_list, group_dict = categorize_files(self.files)

            # If group_dict is empty
            if not group_dict:
                self.log_box.append("[info] No categorizable files found.")
                return

            # display file category and total file count in each category.
            self.log_box.append(f"[...] Organizing files into categories\n")
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
                self.log_box.append(f"[error] {e}\n")
                return

            if not category_dict:
                self.log_box.append("[info] No files found to Move.\n")
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
            self.log_box.append(f"[o.k] Files moved to {self.dst_pth}\n")
            
        else:
            # If errors occured while moving, display info in log box
            QMessageBox.information(self, "Completed with Errors", f"Moved {moved} files, Failed {errors}")
            self.log_box.append(f"[warn] {errors} errors occured.\n")

        ## Reset the button to Start and state variable=0.
        self.btn_3.setEnabled(True)
        self.reset_state()
        self.flow_cycle += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    try:
        icon_path = resource_path("assets/images/app_logo.png")
        if Path(icon_path).exists():
            app.setWindowIcon(QIcon(icon_path))
    except:
        pass

    window = App()
    window.show()
    sys.exit(app.exec())





