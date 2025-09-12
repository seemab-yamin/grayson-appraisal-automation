#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,

    QAction,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
import os
import logging
from datetime import datetime
import pandas as pd


def setup_logging():
    """Setup logging configuration to write to both file and console"""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Create log filename with date
    date = datetime.now().strftime("%Y%m%d")
    log_filename = os.path.join(logs_dir, f"appraisal_transform_{date}.log")

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    return log_filename


# Setup logging once
log_file = setup_logging()
logger = logging.getLogger(__name__)


class BaseWindow(QMainWindow):
    def __init__(self, title, title_label_text, about_dict):
        super().__init__()
        self.title = title
        self.title_label_text = title_label_text
        self.about_dict = about_dict

        self.initUI()

    def initUI(self):
        """Initialize the user interface"""
        # Set window properties
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 800, 600)  # x, y, width, height
        self.setMinimumSize(QSize(600, 400))

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Add title label
        title_label = QLabel(self.title_label_text)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Add button layout
        button_layout = QHBoxLayout()

        # Create buttons
        self.start_button = QPushButton("Start Processing")
        self.start_button.clicked.connect(self.on_start_clicked)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        # Add buttons to layout
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()  # This pushes the exit button to the right
        button_layout.addWidget(self.exit_button)

        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Add some spacing
        main_layout.addStretch()

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("background-color: #f0f0f0; color: black;")

    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def on_start_clicked(self):
        """Handle start button click"""
        msg = "Processing started..."
        logger.info(msg)
        self.statusBar().showMessage(msg)

        QMessageBox.information(self, "Info", "Processing would start here!")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, self.about_dict["title"], self.about_dict["text"])

    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    logger.info("Application started")
    app = QApplication(sys.argv)
    title = "Base Window"
    title_label_text = "Label Title"
    about_dict = {"title": "About", "text": "A\n\nB\nC"}

    window = BaseWindow(
        title=title, title_label_text=title_label_text, about_dict=about_dict
    )
    window.show()

    sys.exit(app.exec_())
