import pickle

DATA_FILE = "data/interfaces.p"

class InterfaceList:
    def __init__(self, bot):
        self.bot = bot

        try:
            interface_data = pickle.load(open(DATA_FILE, 'rb'))
        except Exception as exc:
            print("Failed to load data file")
            print(str(exc))
            interface_data = {}
        self.interface_list = interface_data
        self.save_data()

    def save_data(self):
        pickle.dump(self.interface_list, open(DATA_FILE, "wb"))
