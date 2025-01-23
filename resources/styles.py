class Main_window_Styles:
    # Main form widget styles
    FORM_WIDGET = """
        background: white;
        border-radius: 15px;
        padding: 30px;
    """

    # Title label styles
    TITLE_LABEL = """
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        background: white;
    """

    # Input field styles
    INPUT_FIELD = """
        padding-left: 35px;
        border-radius: 20px;
        background: #F0F0F0;
        margin-bottom: 5px;
    """

    # Login button styles
    LOGIN_BUTTON = """
        QPushButton {
            background-color: #4CAF50; 
            color: white;              
            border: none;             
            padding: 10px 20px;   
            font-size: 16px;      
        }

        QPushButton:hover {
            background-color: #45a049; 
        }

        QPushButton:pressed {
            background-color: #3e8e41; 
        }
    """

    # Link label styles
    LINK_LABEL = """
        color: #777;
        font-size: 12px;
    """



class Dashboard_styles:
    DASHBOARD_BUTTON_STYLE = """
QPushButton {
    background-color: #a7a6a8;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
    color: #333;
    height:60px;
}
QPushButton:hover {
    background-color: #dfdedf;
}
"""

    SAVE_BUTTON_STYLE = """
    QPushButton {
        background-color: #4CAF50; 
        color: white;              
        border: none;             
        padding: 10px 20px;       
        font-size: 16px;          
    }
    QPushButton:hover {
        background-color: #45a049; 
    }
    """

    SIDEBAR_WIDGET_STYLE = """
    QWidget {
        background: qlineargradient(
            x1: 1, y1: 1, x2: 0, y2: 0,
            stop: 0 #d8dbdb, stop: 1 #f5f5f5
        );
    }
    """

    SEARCH_BAR_STYLE = """
    QLineEdit {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 8px;
        font-size: 14px;
        color: #333;
    }
    """

    RESULT_LABEL_STYLE = """
    background: #F9F9F9; border: 1px solid #DDD; padding: 8px; border-radius: 5px;
    font-size: 12px; font-weight: bold;
    """

    NO_RESULTS_LABEL_STYLE = """
    color: #999; font-style: italic;
    """

    WELCOME_LABEL_STYLE = """
    font-size: 20px; font-weight: bold; color: #4CAF50;
    """

    DASHBOARD_UI = [
            "background-color: #ffcccc; font-size: 20px; color: #ff0000; padding: 20px; border-radius: 10px; width: 200px; height: 200px; word-wrap: break-word;",
            "background-color: #ccffcc; font-size: 20px; color: #00ff00; padding: 20px; border-radius: 10px; width: 200px; height: 200px; word-wrap: break-word;",
            "background-color: #ccccff; font-size: 20px; color: #0000ff; padding: 20px; border-radius: 10px; width: 200px; height: 200px; word-wrap: break-word;",
            "background-color: #ffffcc; font-size: 20px; color: #ffff00; padding: 20px; border-radius: 10px; width: 200px; height: 200px; word-wrap: break-word;"
        ]