# Get Resource_path 

from pathlib import Path
import sys

def resource_path(relative_path: str) -> str:

    if getattr(sys, 'frozen', False) and hasattr(sys, "_MEIPASS"):   
        base_path = Path(sys._MEIPASS) # type: ignore

    else:
        base_path = Path(__file__).resolve().parent.parent.parent

    
    return str(base_path / relative_path)








