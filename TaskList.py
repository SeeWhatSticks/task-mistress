import pickle

DATA_FILE = "data/tasks.p"

class TaskList:
    def __init__(self, bot):
        self.bot = bot

        try:
            task_data = pickle.load(open(DATA_FILE, 'rb'))
        except Exception as exc:
            print("Failed to load data file")
            print(str(exc))
            task_data = {}
        self.task_list = task_data
        self.save_data()

    def save_data(self):
        pickle.dump(self.task_list, open(DATA_FILE, "wb"))
