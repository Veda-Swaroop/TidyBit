# Get Resource_path 

from pathlib import Path
import sys, os

def resource_path(relative_path: str) -> str:

    if getattr(sys, 'frozen', False):   
        base_path = Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent))
            
    elif "SNAP" in os.environ:
        base_path = Path(os.environ["SNAP"])

    else:
        base_path = Path(__file__).resolve().parent.parent.parent
    
    return str(base_path / relative_path)








