 # * author : Philippe Vo 
 # * date : Jan-25-2020 17:32:16
 
# * Imports
# 3rd Party Imports
# User Imports

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
class Board():
    """
    description : Board to contain the tasks
    features    : Contains the tasks 
    """
    def __init__(self):
        self.progress = 0
        self.tasks = []

class BoardController():
    """
    description : Controls the various function of the board
    """ 
    def __init__(self):
        pass

    def load_tasks(self, board, tasks):
        """[load all the tasks into the board]
        
        Arguments:
            tasks {[type]} -- [description]
        """
        for task in tasks:
            self.add_task(board, task)

    def add_task(self, board, task):
        board.tasks.append(task)

    def delete_task(self, board, task):
        try:
            board.tasks.remove(task) # removes from the list of tasks -> "task" if it exists
        except ValueError as e:
            print(e)
            print("Task does not exist")

    def set_progress(self, board, progressPercentage):
        board.progress = progressPercentage

    