class Player:
    def __init__(self, player_id):
        self.player_id = player_id

        self.available = False
        self.limits = []
        self.assignments = {}

        self.last_beg_time = None
        self.last_treat_time = None

        self.credits = 1
