from enum import Enum

class InterfaceType(Enum):
    # True/False refers to whether the Interface has pages
    ACTIONS = False
    LIMITS = True
    CATEGORIES = True
    ASSIGNMENTS = True
    TASKS = True
    VERIFICATION = False

class Interface:
    def __init__(self, interface_type: InterfaceType, message_id, player_id=None, task_id=None):
        self.interface_type = interface_type
        self.message_id = message_id

        self.page = 0 if bool(interface_type) else None
        self.player_id = player_id
        self.task_id = task_id
