import pickle
from Player import Player

DATA_FILE = "data/players.p"

class PlayerList:
    def __init__(self, bot):
        self.bot = bot

        try:
            player_data = pickle.load(open(DATA_FILE, 'rb'))
        except Exception as exc:
            print("Failed to load data file")
            print(str(exc))
            player_data = {}
        self.player_list = player_data
        self.save_data()

    def save_data(self):
        pickle.dump(self.player_list, open(DATA_FILE, "wb"))

    def get_player_by_id(self, player_id):
        if player_id not in self.player_list:
            self.player_list[player_id] = Player(player_id)
        return self.player_list[player_id]
