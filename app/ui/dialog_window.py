# Settings dialog window
# TidyBit Settings


import copy
from PySide6.QtCore import Qt, QSignalBlocker, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QTableWidget, QHeaderView, QTabWidget, QWidget,
                                QLabel, QTableWidgetItem, QPushButton, QAbstractItemView, QMessageBox)
from app.config import save_settings, get_defaults


class SettingsDialog(QDialog):
    settings_applied = Signal(dict)

    def __init__(self, data, parent=None):
        super().__init__()

        self.setWindowTitle("TidyBit - Settings")
        self.resize(600, 700)

        # Dialog window - Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Class Variable
        self.data = data
        self.current_category = None

        # Tab Widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Tab 1: Manage Rules
        self.tab_manage = QWidget()
        self.setup_manage_tab()
        self.tabs.addTab(self.tab_manage, "Manage Rules")

        # Tab 2: About
        self.tab_about = QTabWidget()
        self.setup_about_tab()
        self.tabs.addTab(self.tab_about, "About")


    def setup_manage_tab(self):

        tab_layout = QHBoxLayout()
        self.tab_manage.setLayout(tab_layout)

        # Left Layout
        left_layout = QVBoxLayout()
        

        # Left Table widget to display categories
        self.left_table = QTableWidget()
        self.left_table.setColumnCount(1)
        self.left_table.setHorizontalHeaderLabels(["Categories"])

        # Set ID to Table
        self.left_table.setObjectName("SettingsTable")

        # Hide the numbers
        self.left_table.verticalHeader().hide()

        # Header expands to fill the empty space
        left_header = self.left_table.horizontalHeader()
        left_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        # Selection Behavior: Select the whole row, not just one cell
        self.left_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.left_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Real Data
        categories = self.get_categories()
        
        with QSignalBlocker(self.left_table):
            self.left_table.setRowCount(len(categories))

            for row, category in enumerate(categories):
                item = QTableWidgetItem(category)
                item.setData(Qt.ItemDataRole.UserRole, category)
                self.left_table.setItem(row, 0, item)

        # display extension data in right table when category changes 
        self.left_table.currentItemChanged.connect(self.update_right_panel)

        # update dictionary key, if a category is renamed
        self.left_table.itemChanged.connect(self.on_category_rename)

        # Add left table widget to letft layout
        left_layout.addWidget(self.left_table)

        # Left - Buttons
        lft_btn_layout =  QHBoxLayout()
        lft_btn_add = QPushButton("Add")
        lft_btn_del = QPushButton("Delete")

        # Set ID to Buttons
        lft_btn_add.setObjectName("dialogButton")
        lft_btn_del.setObjectName("dialogButton")

        # Button function
        lft_btn_add.clicked.connect(self.add_category)
        lft_btn_del.clicked.connect(self.del_category)

        # Add left button widgets to left btn layout
        lft_btn_layout.addWidget(lft_btn_add)
        lft_btn_layout.addWidget(lft_btn_del) 

        # Add left button layout to left layout
        left_layout.addLayout(lft_btn_layout)



        # Right Pane - Table (Extension and It's Description)

        # Right Layout
        right_layout = QVBoxLayout()

        # Table
        self.right_table = QTableWidget()
        self.right_table.setColumnCount(2)
        self.right_table.setHorizontalHeaderLabels(["Extension", "Description"])

        # Set ID to Table
        self.right_table.setObjectName("SettingsTable")

        # Header expands to fill the empty space
        header = self.right_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # Selection Behavior: Select the whole row, not just one cell
        self.right_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.right_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Hide numbers
        self.right_table.verticalHeader().hide()


        # Add right_table widget to right_layout
        right_layout.addWidget(self.right_table)

        # Update extension if an extension is renamed
        self.right_table.itemChanged.connect(self.on_extension_rename)

        # Buttons
        rt_btn_layout = QHBoxLayout()
        rt_btn_add = QPushButton("Add")
        rt_btn_del = QPushButton("Delete")

        # Set ID to Buttons
        rt_btn_add.setObjectName("dialogButton")
        rt_btn_del.setObjectName("dialogButton")

        # Button function
        rt_btn_add.clicked.connect(self.add_extension)
        rt_btn_del.clicked.connect(self.del_extension)

        # Add button widgets to btn layout
        rt_btn_layout.addWidget(rt_btn_add)
        rt_btn_layout.addWidget(rt_btn_del)

        # Add btn layout to right_layout
        right_layout.addLayout(rt_btn_layout)


        # Add left and right layouts to the main layout
        tab_layout.addLayout(left_layout, 1)
        tab_layout.addLayout(right_layout, 2)


    def setup_about_tab(self):

        tab_layout = QVBoxLayout()
        self.tab_about.setLayout(tab_layout)

        # Title
        label_title = QLabel("TidyBit")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_title = QFont()
        font_title.setPointSize(24)
        font_title.setBold(True)
        label_title.setFont(font_title)
        tab_layout.addWidget(label_title)

        # Labels
        label_desc = QLabel("A simple file organizer.")
        label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tab_layout.addWidget(label_desc)


        label_version = QLabel("Version 1.3")
        label_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tab_layout.addWidget(label_version)
        tab_layout.addStretch()


        tab_layout.addSpacing(40)


        # Restore Settings Button
        reset_btn = QPushButton("Restore to default settings")
        reset_btn.setFlat(True)
        reset_btn.clicked.connect(self.restore_defaults)

        tab_layout.addWidget(reset_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        tab_layout.addStretch()



    # Class functions

    
    # Function to get categories from the hard-coded rule-system in the table.
    def get_categories(self):
        return list(self.data.keys())
    
    
    # Function to display extensions info for a selected category
    def update_right_panel(self, current, previous):
        # gets current and previous row numbers and it's text
        if current == None:
            with QSignalBlocker(self.right_table):
                self.right_table.setRowCount(0)
            self.current_category = None
            return

        category = current.data(Qt.ItemDataRole.UserRole)
        self.current_category = category

        # Stop UI Signals
        with QSignalBlocker(self.right_table):

            # Clear table
            self.right_table.setRowCount(0)

            if category in self.data:
                extensions_dict = self.data[category]

                self.right_table.setRowCount(len(extensions_dict))
                
                for row, (extn, des) in enumerate(list(extensions_dict.items())):
                    # Extension
                    item_extn = QTableWidgetItem(extn)
                    item_extn.setData(Qt.ItemDataRole.UserRole, extn)
                    self.right_table.setItem(row, 0, item_extn)

                    # Description
                    item_des = QTableWidgetItem(des)
                    self.right_table.setItem(row, 1, item_des)



    # Function to add a category
    def add_category(self):
        # If same name exist
        new_name = "New Category"
        counter = 1
        while new_name in self.data:
            new_name = f"New Category {counter}"
            counter += 1
        
        # Update data
        self.data[new_name] = {}

        # Stop UI Signals
        with QSignalBlocker(self.left_table):
        
            row = self.left_table.rowCount()
            self.left_table.insertRow(row)
            item = QTableWidgetItem(new_name)
            item.setData(Qt.ItemDataRole.UserRole, new_name)
            self.left_table.setItem(row, 0, item)

        # Edit cell
        self.left_table.setCurrentCell(row, 0)
        self.left_table.editItem(item)


    # Function to delete a category
    def del_category(self):
        selected_row = self.left_table.currentRow()

        if selected_row < 0:
            QMessageBox.information(self, "Select Category", "Select a category to delete.")
            return
        
        item = self.left_table.item(selected_row, 0)

        if item == None:
            self.left_table.removeRow(selected_row)
            return
        
        category = item.text()

        # Confirm delete
        confirm = QMessageBox.question(
            self,
            "Delete Category",
            f"Delete '{category}' and all it's extensions?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.No:
            return
        
        # Delete category from data
        if category in self.data:
            del self.data[category]

        # delete from UI
        self.left_table.removeRow(selected_row)


    # Function to add extension and description
    def add_extension(self):
        if not self.current_category:
            QMessageBox.information(self, "Select Category", "Select a category to add extension.")
            return
        
        new_extn_name = "Extension"
        counter = 1
        extensions_dict = self.data[self.current_category]
        
        while new_extn_name in extensions_dict:
            new_extn_name = f"Extension {counter}"
            counter += 1
        
        self.data[self.current_category][new_extn_name] = "Description"

        # Stop UI Signals
        with QSignalBlocker(self.right_table):

            row = self.right_table.rowCount()
            self.right_table.insertRow(row)

            item_ext = QTableWidgetItem(new_extn_name)
            # Set UserRole, to rename it
            item_ext.setData(Qt.ItemDataRole.UserRole, new_extn_name)
            self.right_table.setItem(row, 0, item_ext)

            item_des = QTableWidgetItem("Description")
            self.right_table.setItem(row, 1, item_des)

        # Edit cells
        self.right_table.setCurrentCell(row, 0)
        self.right_table.editItem(item_ext)



    # Function to delete extension and description
    def del_extension(self):
        if not self.current_category:
            QMessageBox.information(self, "Select Category", "Select a category and choose an extension to delete.")
            return
        
        selected_row = self.right_table.currentRow()

        if selected_row < 0:
            QMessageBox.information(self, "Select Extension", "Select an extension to delete.")
            return
        
        item_extn = self.right_table.item(selected_row, 0)

        if not item_extn:
            return
        
        chosen_extn = item_extn.text()

        # delete extension from data
        if chosen_extn in self.data[self.current_category]:
            del self.data[self.current_category][chosen_extn]

        # delete in UI
        self.right_table.removeRow(selected_row)


    # Function to update data when a category is renamed
    def on_category_rename(self, item):
        
        new_name = item.text().strip()
        old_name = item.data(Qt.ItemDataRole.UserRole)

        if not new_name:
            with QSignalBlocker(self.left_table):
                item.setText(old_name)

            QMessageBox.information(self,
                                    "Empty Category", 
                                    "Category name can not be empty. \nPlease enter a name." )

            QTimer.singleShot(0, lambda: self.left_table.editItem(item))
            return
        
        if new_name in self.data and new_name != old_name:
            with QSignalBlocker(self.left_table):
                item.setText(old_name)

            QMessageBox.information(self,
                                    "Duplicate category",
                                    f"'{new_name}' already exist. \nPlease enter a new category name.")

            QTimer.singleShot(0, lambda: self.left_table.editItem(item))
            return
        
        if new_name == old_name:
            return
        
        # Update new name to data
        if old_name in self.data:
            self.data[new_name] = self.data.pop(old_name)

            # update the hidden user role to new name
            with QSignalBlocker(self.left_table):
                item.setData(Qt.ItemDataRole.UserRole, new_name)

            # Update self.current_category to new name
            if self.current_category == old_name:
                self.current_category = new_name


    # Function to update data on extension rename
    def on_extension_rename(self, item):

            # If category is not selected, ignore
            if not self.current_category:
                return
            
            row = item.row()
            col = item.column()

            new_text = item.text().strip()

            item_extn = self.right_table.item(row, 0)

            if item_extn == None:
                return
            
            old_extn = item_extn.data(Qt.ItemDataRole.UserRole)


            if col == 0:
                # Ignore empty extensions
                if not new_text:
                    with QSignalBlocker(self.right_table):
                        item.setText(old_extn)
                    QMessageBox.information(self,
                        "Extension name is empty", 
                        "Extension name can not be empty. \nPlease enter a name." )

                    QTimer.singleShot(0, lambda: self.right_table.editItem(item))
                    return
                
                # If user enters the same name
                if new_text == old_extn:
                    return
                

                # If extension already exist
                for category in self.data:
                    if new_text.lower() in self.data[category]:
                        with QSignalBlocker(self.right_table):
                            item.setText(old_extn)
                        QMessageBox.information(self,
                                                "Duplicate Extension",
                                                f"'{new_text}' already exist in category: '{category}'.\nEnter a new extension name.")
                        QTimer.singleShot(0, lambda: self.right_table.editItem(item))
                        return

                        
                # If user tries renaming an extension in a category
                category_dict = self.data[self.current_category]

                if old_extn in category_dict:
                    
                    # If it is extension, make it lowercase
                    if new_text.startswith("."):
                        new_text = new_text.lower()

                    # replace the extension and swap description
                    desc_value = category_dict.pop(old_extn)
                    category_dict[new_text] = desc_value

                    # Update the hidden user role
                    with QSignalBlocker(self.right_table):
                        item.setData(Qt.ItemDataRole.UserRole, new_text)

            elif col == 1:
                category_dict = self.data[self.current_category]

                # replace the old description with new one 
                if old_extn in category_dict:
                    category_dict[old_extn] = new_text



    # Function to reset settings
    def restore_defaults(self):

        confirm = QMessageBox.warning(
            self,
            "Reset Settings",
            "Reset to default settings? \nThis will DELETE all custom extensions and categories.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.No:
            return
        
        # Overrite Memory
        self.data = copy.deepcopy(get_defaults())

        # Refresh UI
        with QSignalBlocker(self.left_table), QSignalBlocker(self.right_table):

            self.left_table.setRowCount(0)
            self.right_table.setRowCount(0)
            self.current_category = None

            categories = self.get_categories()
            self.left_table.setRowCount(len(categories))
            for row, category in enumerate(categories):
                item = QTableWidgetItem(category)
                item.setData(Qt.ItemDataRole.UserRole, category)
                self.left_table.setItem(row, 0, item)

        # Save settings
        save_settings(self.data)
        self.settings_applied.emit(self.data) 

        # Notify reset complete
        QMessageBox.information(
            self,
            "Success",
            "Default settings restored."
        )





    # On Close
    def closeEvent(self, event):

        reply = QMessageBox.question(
            self, 
            "Save Settings?", 
            "Do you wish to save these settings?",
            QMessageBox.StandardButton.Save |  QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
        
        if reply == QMessageBox.StandardButton.Save:
            save_settings(self.data)
            self.settings_applied.emit(self.data)
            event.accept()

        elif reply == QMessageBox.StandardButton.Discard:
            event.accept()

        else:
            event.ignore()
            

    


        



            

        





    

        
        












 




        


