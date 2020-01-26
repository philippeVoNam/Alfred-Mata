 # * author : Philippe Vo 
 # * date : Jan-25-2020 17:26:20
 
# * Imports
# 3rd Party Imports
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from datetime import date, datetime, timedelta
# User Imports
from task_mod import Task, TaskController
from board_mod import Board, BoardController
from daily import get_data_trello_to_db, get_tasks_valid

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
# * Code
# Subclass QMainWindow to customise your application's main window
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # init data
        mandatoryTasks, optionaltasks, pastduetasks, validTasks = self.init_data()

        # init UI
        self.init_ui(mandatoryTasks, optionaltasks, pastduetasks)

    def init_ui(self, mandatoryTasks, optionaltasks, pastduetasks):
        self.setWindowTitle("Alfred-Mata")

        # Layouts
        mainLayout = QGridLayout()

        # Adding Widgets
        ## Main Window
        
        ## init data
        self.boardController = BoardController()

        self.mandatoryBoard = Board()
        self.boardController.load_tasks(self.mandatoryBoard, mandatoryTasks)

        self.optionalBoard = Board()
        self.boardController.load_tasks(self.optionalBoard, optionaltasks)
        ## init data

        self.mandatoryBoardUI = BoardUI("Mandatory", self.mandatoryBoard)
        self.optionalBoardUI = BoardUI("Optional", self.optionalBoard)

        mandatoryLabel = QLabel("Mandatory")
        optionalLabel = QLabel("Optional")

        mainLayout.addWidget(mandatoryLabel)
        mainLayout.addWidget(self.mandatoryBoardUI)
        mainLayout.addWidget(optionalLabel)
        mainLayout.addWidget(self.optionalBoardUI)

        # Setting Style of the Main Widget
        style = """ 
        background-color: rgb(40, 42, 54);
        color : rgb(255,255,255);
        """
        self.setStyleSheet(style)

        # Setting Layouts
        self.setLayout(mainLayout)

    def init_data(self):
        # Download from trello and update database
        mandatoryTasks, optionaltasks, pastduetasks = get_data_trello_to_db()

        # sort the data
        mandatoryTasks = sorted(mandatoryTasks,key=lambda task: task.dueDate)
        optionaltasks = sorted(optionaltasks,key=lambda task: task.dueDate)
        pastduetasks = sorted(pastduetasks,key=lambda task: task.dueDate)

        validTaskList = get_tasks_valid([mandatoryTasks, optionaltasks, pastduetasks])

        return mandatoryTasks, optionaltasks, pastduetasks, validTaskList

class BoardUI(QWidget):
    """
    description : User Interface of the Board
    """
    def __init__(self, boardName, board):
        super(BoardUI, self).__init__()

        # init components needed 
        self.tasksUI = []
        self.boardName = boardName
        self.board = board

        # init UI
        self.init_ui()

    def init_ui(self):
        # Layouts
        scrollLayout = QGridLayout()
        self.box = QGroupBox()
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.box)
        self.scroll.setWidgetResizable(True)
        
        # Init Widgets
        ## Progress Bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 10)

        ## TaskUI components
        # FIXME : testing UI
        for task in self.board.tasks:
            taskBox = TaskUI(task)
            scrollLayout.addWidget(taskBox.get_box())

        # Adding Widgets
        ## Main Window
        # FIXME : Add the Progress bar for board
        scrollLayout.addWidget(self.progress)

        # Setting Style of the Main Widget
        # style = """ 
        # background-color: rgb(40, 42, 54);
        # color : rgb(255,255,255);
        # """
        # self.setStyleSheet(style)

        # Setting Layouts
        self.box.setLayout(scrollLayout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def get_scroll(self):
        return self.scroll

class TaskUI(QWidget):
    """
    description : User Interface of the Board
    """
    def __init__(self, task):
        super(TaskUI, self).__init__()

        # init data
        self.task = task

        # init UI
        self.init_ui()

    def init_ui(self):
        # Layouts
        mainLayout = QGridLayout()
        self.box = QGroupBox()
        # self.box.setMinimumHeight(100)

        # Init Widgets
        ## Progress Bar
        self.updateButton = QPushButton("+")
        self.groupNameLabel = QLabel(self.task.groupClass)
        self.titleLabel = QLabel(self.task.title)
        self.dueDateLabel = QLabel(self.task.dueDateStr)
        self.progressBar = QProgressBar(self)
        self.percentageExpectedLabel = QLabel(self.task.expectedProgressTxtNormal)

        ## Widget Settings
        self.updateButton.setMaximumSize(35,25)
        # self.progressBar.setGeometry(0, 0, 100, 25)
        self.progressBar.setMaximumSize(200,10)
        self.progressBar.setValue(int(self.task.progress))

        # Adding Widgets
        ## Main Window
        mainLayout.addWidget(self.updateButton,0,0)
        mainLayout.addWidget(self.groupNameLabel,0,1)
        mainLayout.addWidget(self.titleLabel,0,2)
        mainLayout.addWidget(self.dueDateLabel,0,3)
        mainLayout.addWidget(self.progressBar,0,4)
        mainLayout.addWidget(self.percentageExpectedLabel,0,5)

        # Slots
        self.updateButton.clicked.connect(lambda: self.update_task_progress())

        # Setting Style of the Main Widget
        # style = """ 
        # background-color: rgb(40, 42, 54);
        # color : rgb(255,255,255);
        # """
        # self.setStyleSheet(style)

        # Setting Layouts
        mainLayout.setContentsMargins(0,0,0,0)
        self.box.setLayout(mainLayout)

    def get_box(self):
        return self.box

    def update_task_progress(self):
        self.ask_progress()

    def ask_progress(self):
        # FIXME : set the style for this as well 
        progress, okPressed = QInputDialog.getInt(self, "At what progress percentage do you think you are ?","Percentage:", 0, 0, 100, 1)
        if okPressed:
            taskController = TaskController()
            taskController.update_task_progress(self.task, progress)
            self.progressBar.setValue(int(self.task.progress))