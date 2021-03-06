import os
import sys
import time

import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from bs4 import BeautifulSoup

os.system("pyuic5 MainWindow.ui > MainWindow.py")
import MainWindow


def scrap_main_page():
    url = "https://www.worldometers.info/coronavirus/"

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    # get table part from html
    table = soup.find("table", id="main_table_countries_today")
    # add border for show in browser like looking original
    table["border"] = "1"
    # delete this attr else just showing blank page
    del table.attrs["style"]
    # write table to file for read again with browser
    with open("table.html", "w") as f:
        f.write(str(table))

# pip install PyQtWebEngine

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.update_label()
        scrap_main_page()
        self.loadPage()
        self.ui.export_pdf_btn.clicked.connect(self.export_pdf)

        self.showMaximized()

    def update_label(self):
        curr_time = time.strftime("%H:%M:%S %d/%m/%Y")
        self.ui.label.setText("Worldometer Covid-19 ( {} )".format(curr_time))

    def loadPage(self):
        """load local file to browser"""
        current_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(current_dir, "table.html")
        url = QUrl.fromLocalFile(filename)
        self.ui.browser.load(url)

    def export_pdf(self):
        filename = "table_{}.pdf".format(time.strftime("%Y%m%d-%H%M%S"))
        print(filename)
        self.ui.browser.page().printToPdf(filename)
        QtWidgets.QMessageBox.information(self, "PDF Saved !", filename + " saved to disk.")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Window()
    app.exec_()
