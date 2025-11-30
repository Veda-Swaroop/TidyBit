# Project File

import os
import sys
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox
from file_ext import file_extensions
from PIL import ImageTk, Image



def main():
    ctk.set_appearance_mode("system")
    app_gui = App()

    app_gui.mainloop()

# Helper function for executable
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS #type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def fetch_files(src):
    unfiltered_files = os.listdir(src)
    files = [file for file in unfiltered_files if file != "desktop.ini" and not file.startswith(".")]
    return files


def categorize_files(files):
    bag = []
    grouped_dict = {}

    ## splitting each file into it's name and extension.
    for file in files:
        filename, extension = os.path.splitext(file)

    ## Categorize each extension.
        if extension == "":
            if filename in {"README", "LICENSE", "Makefile", "Dockerfile"}:
                bag.append("documents")
            else:
                bag.append("folder")
        else:
            extn_category = identify_extension(extension)
            bag.append(extn_category)   # bag contains the category name of each extension.

    # Group similar category of extensions and display the count of each extension.
    for item in set(bag):
        grouped_dict[item] = bag.count(item)

    return bag, grouped_dict

# Label each file based on it's extension.
def label_files(files, bag):
    label_dict = {}
    if len(files) == len(bag):
        for file in range(len(files)):
            label_dict[files[file]] = bag[file]

    else:
        raise ValueError("Mismatch error in labelling files")

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



# GUI
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Program Window Setup
        self.title("TidyBit - a simple file organizer")
        self.geometry("600x500")

        # Icon and font for Windows
        if os.name == "nt":
            log_font = ("Lucida Console", 12)
            try:
                icon_path = resource_path(os.path.join("assets", "images", "app_icon.ico"))
                self.iconbitmap(icon_path)
            except Exception:
                    pass
        # Icon and font for Linux
        else:
            log_font = ("Monospace", 12)
            try:
                icon_path = resource_path(os.path.join("assets", "images", "app_logo.png"))
                img = Image.open(icon_path)
                self.icon_image = ImageTk.PhotoImage(img)
                self.iconphoto(False, self.icon_image)
            except Exception:
                pass

        # Grid Configuration
        self.grid_rowconfigure(2, weight=1) # Row 2 expands
        self.grid_columnconfigure(1, weight=1) # Column 1 expands

        # Labels
        self.label_1 = ctk.CTkLabel(self, text="Source Folder Path")
        self.label_1.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.label_2 = ctk.CTkLabel(self, text="Target Folder Path")
        self.label_2.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Entries
        self.entry_1 = ctk.CTkEntry(self, placeholder_text="select source folder")
        self.entry_1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.entry_2 = ctk.CTkEntry(self, placeholder_text="select target folder")
        self.entry_2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Browse - Buttons
        self.btn_1 = ctk.CTkButton(self, text="Browse", width=100, hover_color="green", command=self.browse_source)
        self.btn_1.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.btn_2 = ctk.CTkButton(self, text="Browse", width=100, hover_color="green", command=self.browse_target)
        self.btn_2.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Text box
        self.textbox = ctk.CTkTextbox(self, font=log_font)
        self.textbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        #self.textbox.tag_config("title", justify="center")

        # Action Button
        self.btn_3 = ctk.CTkButton(self, text="Start", height=50, hover_color="green", command=self.action_btn)
        self.btn_3.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        # State Variable
        self.btn_3_state = 0
        # Variable to count execution flow cycle of action buttion
        self.flow_cycle = 0

    # class methods
    def browse_source(self):
        source_dir = filedialog.askdirectory()
        if source_dir:
            # delete placeholder text
            self.entry_1.delete(0, "end")
            # insert source path
            self.entry_1.insert(0, source_dir)
            # log the path in textbox
            self.textbox.insert("end", f"[dir] Source: {source_dir}\n")
            self.textbox.insert("end", "\n")
            self.btn_3_state = 0



    def browse_target(self):
        target_dir = filedialog.askdirectory()
        if target_dir:
            # delete placeholder text
            self.entry_2.delete(0, "end")
            # insert target path
            self.entry_2.insert(0, target_dir)
            # log the path in textbox
            self.textbox.insert("end", f"[dir] Target: {target_dir}\n")
            self.textbox.insert("end", "\n")
            self.btn_3_state = 0


    def action_btn(self):
        self.src_pth = self.entry_1.get()
        self.dst_pth = self.entry_2.get()
        

        # Start(state=0) -> Fetch(state=1) -> Organize(state=2) -> Move(state=3)

        if self.btn_3_state == 0:
            # state = 0, Button = start

            # if execution flow completes a cycle, clear textbox
            if self.flow_cycle > 0:
                self.textbox.delete("0.0", "end")
            
            # Confirm both paths are selected
            if self.src_pth == "" or self.dst_pth == "":
                messagebox.showwarning("Warning", "Please select both source and target folder paths!")
                return

            # Validate Source and Target paths.
            if not os.path.exists(self.src_pth):
                messagebox.showwarning("Invalid Source folder path", f"{self.src_pth} does not exist.")
                return
            if not os.path.exists(self.dst_pth):
                messagebox.showwarning("Invalid Target folder path", f"{self.dst_pth} does not exist.")
                return

            # if source and target paths are same, stop. It throws error.
            if os.path.abspath(self.src_pth) == os.path.abspath(self.dst_pth):
                messagebox.showerror("Error", "Source and Target can't be the same folder.\nPlease select a different Target folder.")
                return

            # If both paths are confirmed and valid, Ready to fetch.
            self.textbox.insert("end", f"[ok] Source and Target paths are valid. Ready to Fetch Files.\n")

            # Change the button to Fetch and state variable.
            self.btn_3.configure(text="Fetch Files")
            self.btn_3_state = 1


        elif self.btn_3_state == 1:
            # state = 1, Button = Fetch
        
            # Prepare textbox before file fetch
            self.textbox.insert("end", "\n")
            self.textbox.insert("end", f"[...] Fetching files from: {self.src_pth}\n")
            self.textbox.insert("end", "\n")

            # Fetch files from source path and display them in textbox
            try:
                self.files = fetch_files(self.src_pth)
            except Exception as e:
                self.textbox.insert("end", f"[error] Error occured while fetching files. {e}\n")
                self.textbox.see("end")
                return
            # If source folder is empty
            if not self.files:
                self.textbox.insert("end", "[info] No files found in source folder!\n\n")
                return

            for index, file in enumerate(self.files, start=1):
                self.textbox.insert("end", f"{index}. {file}\n")

            # Scroll the textbox
            self.textbox.see("end")
 
            # Change the button to Fetch and state variable.
            self.btn_3.configure(text="Organize Files")
            self.btn_3_state = 2

        elif self.btn_3_state == 2:
            # state = 2, Button = Organize 

            # Organize files

            # organize files into categories based on file extension
            self.category_list, group_dict = categorize_files(self.files)

            # display file category and total file count in each category.
            found_files = ""
            max_len = max(len(key) for key, value in group_dict.items())
            for key, value in group_dict.items():
                
                found_files+= f"{key:<{max_len}} : {value:>5}\n"

            # If source path contains only folders.
            if len(group_dict) == 1 and "folder" in group_dict:
                self.textbox.insert("end", f"\n")
                self.textbox.insert("end", f"{'Category':<{max_len}}   {'Count':>5}\n")
                self.textbox.insert("end", f"{'_'* (max_len + 10)}\n")
                self.textbox.insert("end", f"\n{found_files}")
                self.textbox.insert("end", f"[info] No files found to Organize!\n")
                self.textbox.see("end")
                return

            # If path contains files, organize them.
            self.textbox.insert("end", f"\n")
            self.textbox.insert("end", f"[...] Organizing files into categories\n")
            self.textbox.insert("end", f"\n")
            self.textbox.insert("end", f"{'Category':<{max_len}}   {'Count':>5}\n")
            self.textbox.insert("end", f"{'_'* (max_len + 10)}\n")
            self.textbox.insert("end", f"\n{found_files}")
            
            # Scroll the textbox
            self.textbox.see("end")

            # Change the button to Move and state variable=3.
            self.btn_3.configure(text="Move Files")
            self.btn_3_state = 3

        elif self.btn_3_state == 3:
            # state = 3, Button = Move 

            # Label each file to a category
            try:
                category_dict = label_files(self.files, self.category_list)
            except ValueError as e:
                self.textbox.insert("end", f"[error] {e}\n")
                return

            if not category_dict:
                self.textbox.insert("end", "[info] No files found to Move.\n")
                return

            # Moving Files to Target Folder
            error_count = 0
            folder_count = 0

            for file, label in category_dict.items():
                if label == "folder":
                    folder_count += 1
                    self.textbox.insert("end", f"\n[info] Skipped moving Folder: {file}\n")
                    continue
                src = os.path.join(self.src_pth, file)
                dst_folder = os.path.join(self.dst_pth, label)
                dst = os.path.join(dst_folder, file)
                try:
                    os.makedirs(dst_folder, exist_ok=True)
                    shutil.move(src, dst)
                except PermissionError:
                    error_count += 1
                    self.textbox.insert("end", f"[error] ACCESS DENIED. Can't move file: {file}.\n")
                    continue
                
                except Exception as e:
                    error_count += 1
                    self.textbox.insert("end", f"[error] Error while moving file: {file}.\n{e}\n")
                    self.textbox.see("end")
                    
            total_files = len(self.files) - folder_count

            if error_count == 0:
                # If files moved successfully, display that in textbox
                messagebox.showinfo("Success", "Files are organized and moved to Target Folder")
                self.textbox.insert("end", f"\n")
                self.textbox.insert("end", f"[ok] Files moved to {self.dst_pth}\n")
                self.textbox.see("end")
            else:
                if error_count < total_files:
                    # If errors occured while moving files
                    messagebox.showwarning("Warning", f"Failed to move {error_count} files.\n Please check the log for details.")
                    self.textbox.insert("end", f"\n")
                    self.textbox.insert("end", f"[warn] Error occured while moving {error_count} files out of {total_files}.\n")
                    self.textbox.see("end")
                else:
                    # If errors occured on all files
                    messagebox.showwarning("Error", f"Failed to move files.\n Please check the log for details.")
                    self.textbox.insert("end", f"\n")
                    self.textbox.insert("end", f"[error] Failed to move files to Target folder.\n")
                    self.textbox.see("end")



            ## Reset the button to Start and state variable=0.
            self.btn_3.configure(text="Start")
            self.btn_3_state = 0
            self.flow_cycle += 1





if __name__ == "__main__":
    main()
