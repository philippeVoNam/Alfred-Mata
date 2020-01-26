 # * author : Philippe Vo 
 # * date : Jan-25-2020 17:38:18
 
# * Imports
# 3rd Party Imports
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
# User Imports
from ui_mod import MainWindow

# * Template
# class ClassName():
#     """
#     description : What is it 
#     features    : What it can do
#     """
#     def __init__(self):
#         """ init. """

#     def func_name(self, inputs):
#         """
#         feature : what does it do 
#         :input [type] name: what is it 
#         :input [type] name:
#         :input [type] name:
#         :return [type] name: what is it
#         """

# * Code

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Setting Stylesheet 
    style = """
        QCheckBox:indicator{
            border : 1px solid white;
            border-radius: 2px; }
        QCheckBox:indicator:checked{
            background-color: white; }
            """
    app.setStyleSheet(style)

    window = MainWindow()
    window.show()

    app.exec_()
