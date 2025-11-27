# Testing dictionary iteration

file_extensions = {
    "documents": {
        ".doc": "Microsoft Word",
        ".docx": "Microsoft Word (XML)",
        ".pdf": "Portable Document Format",
        ".txt": "Plain Text",
        ".rtf": "Rich Text Format",
        ".odt": "OpenDocument Text"
    },
    "spreadsheets": {
        ".xls": "Microsoft Excel",
        ".xlsx": "Microsoft Excel (XML)",
        ".csv": "Comma-Separated Values",
        ".ods": "OpenDocument Spreadsheet"
    },
    "presentations": {
        ".ppt": "Microsoft PowerPoint",
        ".pptx": "Microsoft PowerPoint (XML)",
        ".odp": "OpenDocument Presentation"
    },
    "archives": {
        ".zip": "ZIP Archive",
        ".rar": "RAR Archive",
        ".7z": "7-Zip Archive",
        ".tar": "Unix Archive",
        ".gz": "Gzip Compressed Archive"
    },
    "code": {
        ".py": "Python Script",
        ".js": "JavaScript",
        ".html": "HyperText Markup Language",
        ".htm": "HyperText Markup Language",
        ".css": "Cascading Style Sheets",
        ".java": "Java Source Code",
        ".c": "C Source Code",
        ".cpp": "C++ Source Code"
    },
    "system": {
        ".exe": "Windows Executable",
        ".dll": "Dynamic Link Library",
        ".sys": "System File",
        ".bat": "Batch File",
        ".sh": "Shell Script"
    },
    "data": {
        ".json": "JavaScript Object Notation",
        ".xml": "Extensible Markup Language",
        ".sql": "SQL Script",
        ".db": "Database File",
        ".sqlite": "SQLite Database"
    },
    "images": {
        ".jpg": "JPEG Image",
        ".jpeg": "JPEG Image",
        ".png": "Portable Network Graphics",
        ".gif": "Graphics Interchange Format",
        ".bmp": "Bitmap Image",
        ".tiff": "Tagged Image File Format",
        ".tif": "Tagged Image File Format",
        ".webp": "Web Picture Format",
        ".svg": "Scalable Vector Graphics",
        ".heic": "High Efficiency Image Format",
        ".heif": "High Efficiency Image Format",
        ".raw": "Raw Image Format",
        ".ico": "Icon File"
    },
    "audio": {
        ".mp3": "MPEG Audio Layer III",
        ".wav": "Waveform Audio File",
        ".aac": "Advanced Audio Coding",
        ".flac": "Free Lossless Audio Codec",
        ".ogg": "Ogg Vorbis",
        ".wma": "Windows Media Audio",
        ".m4a": "MPEG-4 Audio",
        ".aiff": "Audio Interchange File Format",
        ".alac": "Apple Lossless Audio Codec",
        ".opus": "Opus Audio Codec"
    },
    "video": {
        ".mp4": "MPEG-4 Video",
        ".avi": "Audio Video Interleave",
        ".mov": "QuickTime Movie",
        ".wmv": "Windows Media Video",
        ".mkv": "Matroska Video",
        ".flv": "Flash Video",
        ".webm": "Web Media",
        ".3gp": "3GPP Multimedia",
        ".m4v": "MPEG-4 Video",
        ".ts": "Transport Stream"
    }
}


def main():
    ...



# def identify_extension(b):
#     # b = unknown extension
#     for category, category_dict in file_extensions.items():
#         for extn, extn_info in category_dict.items():
#             if extn == b:
#                 return extn, extn_info, category
    
#     return f"Extension not found"
           



if __name__ == "__main__":
    main()