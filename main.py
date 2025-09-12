#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
)
import os
import logging
from datetime import datetime
import pandas as pd
from ui import BaseWindow


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

# import utils functions
from utils import download_zip_file, extract_zip_file, generate_excel

# Global temporary directory - create in current working directory
TEMP_DIR = os.path.join(os.getcwd(), "tmp")
os.makedirs(TEMP_DIR, exist_ok=True)

CURRENT_DATE = datetime.now().strftime("%Y%m%d")


class AppraisalDataTransformer(BaseWindow):
    def __init__(self, zip_file_name, extracted_dir):
        title = "Grayson Appraisal Data Transformer"
        title_label_text = "Appraisal Data Transformer"
        about_dict = {
            "title": "About",
            "text": "Grayson Appraisal Data Transformer\n\n"
            "A simple tool for processing appraisal data.\n\n"
            "Built with PyQt5",
        }
        super().__init__(
            title=title, title_label_text=title_label_text, about_dict=about_dict
        )
        self.zip_file_name = zip_file_name
        self.extracted_dir = extracted_dir

    def on_start_clicked(self):
        """Handle start button click"""
        msg = "Processing started..."
        logger.info(msg)
        self.statusBar().showMessage(msg)

        if not os.path.exists(self.extracted_dir):
            msg = "No extracted directory found. Extracting now..."
            logger.info(msg)
            self.statusBar().showMessage(msg)

            if not os.path.exists(zip_file_name):
                try:
                    url = "https://maps.graysonappraisal.org/export/Preliminary_Export.zip?_gl=1*j3nrwp*_ga*MTgwNzM4NTg1OC4xNzU1MjgyOTI5*_ga_1WRCW1XD2M*czE3NTc0NzgzMTgkbzkkZzAkdDE3NTc0NzgzMTgkajYwJGwwJGgw"
                    # Download the zip file
                    download_zip_file(url, save_path=zip_file_name)
                    msg = f"Downloaded zip file to: {zip_file_name}"
                    logger.info(msg)
                    self.statusBar().showMessage(msg)
                except Exception as e:
                    msg = f"Failed to download and extract zip: {e}"
                    logger.error(msg)
                    self.statusBar().showMessage(msg)
                    return
            else:
                msg = f"Zip file already exists at: {zip_file_name}"
                logger.info(msg)
                self.statusBar().showMessage(msg)

            try:
                # Extract the zip file
                extract_zip_file(
                    zip_file_name, extracted_dir=extracted_dir, cleanup=False
                )
                msg = f"Extracted zip file to: {extracted_dir}"
                logger.info(msg)
                self.statusBar().showMessage(msg)
            except Exception as e:
                err_msg = f"Failed to download and extract zip: {e}"
                logger.error(err_msg)
                QMessageBox.critical(self, "Error", err_msg)
                return

        else:
            msg = "Extracted directory found. Proceeding to generate Excel."
            logger.info(msg)
            self.statusBar().showMessage(msg)

        msg = f"Extracted Files dir: {self.extracted_dir}"
        logger.info(msg)
        self.statusBar().showMessage(msg)

        # Find the file ending with _APPRAISAL_INFO.TXT
        appraisal_info_file = None
        for file in os.listdir(extracted_dir):
            if file.endswith("_APPRAISAL_INFO.TXT"):
                appraisal_info_file = os.path.join(extracted_dir, file)
                break

        if appraisal_info_file:
            msg = f"Found appraisal info file: {appraisal_info_file}"
            self.statusBar().showMessage(msg)
            logger.info(msg)
        else:
            msg = (
                "No file ending with '_APPRAISAL_INFO.TXT' found in extracted directory"
            )
            logger.error(msg)
            self.statusBar().showMessage(msg)
            raise FileNotFoundError(msg)

        # read using pandas
        excel_path = os.path.join(os.getcwd(), f"Appraisal_Data_{CURRENT_DATE}.xlsx")
        generate_excel(appraisal_info_file, excel_path, chunk_size=10000)

        msg = f"Excel file generated at: {excel_path}"
        logger.info(msg)
        self.statusBar().showMessage(msg)

        success_msg = "Processing completed successfully!"
        logger.info(success_msg)
        self.statusBar().showMessage(success_msg)
        QMessageBox.information(self, "Info", success_msg)


if __name__ == "__main__":
    logger.info("Application started")
    zip_file_name = os.path.join(TEMP_DIR, f"Preliminary_Export_{CURRENT_DATE}.zip")
    extracted_dir = os.path.join(TEMP_DIR, f"Preliminary_Export_{CURRENT_DATE}")

    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Grayson Appraisal Transformer")
    app.setApplicationVersion("1.0")

    window = AppraisalDataTransformer(zip_file_name, extracted_dir)
    window.show()

    sys.exit(app.exec_())
