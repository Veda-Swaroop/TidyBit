# App Logic functions


# imports
from pathlib import Path
from app.config import load_settings

data_file = load_settings()

# Functions
def fetch_files(src):
    unfiltered_files = Path(src)
    files = [p.name for p in unfiltered_files.iterdir() if p.is_file() and not p.name.startswith(".") and not p.name == "desktop.ini"]
    return files


def categorize_files(files, data):
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
    
        extn_category = identify_extension(extension, data)
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
   # b = unknown extension
def identify_extension(b, data):
    if b.startswith("."):
        b = b.lower()
 
    for category, category_dict in data.items():
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