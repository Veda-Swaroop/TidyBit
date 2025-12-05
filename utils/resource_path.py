# Get Resource_path 
from pathlib import Path
import sys

def resource_path(relative_path: str) -> str:
    """
    Return absolute path to resource.
    Works both in development and when bundled with PyInstaller.
    """
    base_path = getattr(sys, "_MEIPASS", Path(__file__).parent.parent)
    return str((Path(base_path) / relative_path).resolve())
