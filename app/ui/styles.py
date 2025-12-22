# App UI Style

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

    QPushButton#dialogButton {
    background-color: transparent;
    border: none;
    font-weight: bold;
    color: white;
    font-size: 12pt;
    padding: 0px;      
    min-width: 30px; 
    max-width: 70px;   
    
    }
    QPushButton#dialogButton:hover {
        background-color: #2580c4;
        color: white;
    }
    QPushButton#dialogButton:pressed {
    background-color: #145374;  
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
    }
    

    QTableWidget#SettingsTable {
        border: 2px solid grey;       /* The Outer Border */          
        gridline-color: #444;         /* Inner Grid Lines */
        background-color: #2b2b2b;    /* Dark Background */
        color: white;                 
    }
    QHeaderView::section {
        background-color: #333;       
        color: white;
        border: 1px solid #555;
        padding: 0px;
        font-weight: bold;
    }
    QTableWidget::item:selected {
        background-color: #3d8ec9;    /* TidyBit Blue */
        color: white;
    }

    QTableWidget#SettingsTable QLineEdit {
        color: white;
        background-color: #2b2b2b; /* Match the table background */
    
        /* CRITICAL: Remove borders/padding so text aligns perfectly with the cell */
        border: none;
        padding: 0px;
        margin: 0px;
        
        /* Optional: Make selection visible while editing */
        selection-background-color: #3d8ec9;
        selection-color: white;
    }

    """