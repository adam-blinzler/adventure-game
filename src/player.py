'''
    This file controls the player and their status
'''

#################################
class player:
    def __init__(self):
        self.nav_actions = []
        self.player_actions = []
        
        self.position = [0,0]
        
        self.inventory = []
        self.has_map = True
        
        self.config_catagories = ["nav", "player"]
        self.movement_directions = []

        self._indent = "    "
    '''
        Configuration management
    '''
    def load_config(self,config):
        '''
            Return state of configuration load attempt
        '''
        good_config = True
   
        print("\nLoading Player actions ....")
        if "actions" in config["nav"]:
            self._add_nav_actions(config["nav"]["actions"])
        else:
            good_config = False
            print("Error :: Failed to load player navigation options")

        if "actions" in config["player"]:
            self._add_player_actions(config["player"]["actions"])
        else:
            good_config = False
            print("Error :: Failed to load player actions")

        return good_config

    def load_movement(self,dirs):
        self.movement_directions = dirs

    def _add_nav_actions(self,actions):
        self.nav_actions = actions
        print("{}Player navigation options loaded".format(self._indent))
        for nav in self._make_nav_pretty():
            print("{}{}".format(self._indent*2,nav))
        
    def _add_player_actions(self,actions):
        self.player_actions = actions
        print("{}Player actions loaded".format(self._indent))
        for act in self.player_actions:
            print("{}{}".format(self._indent*2,act))
    
    '''
        Manipulate player variables
    '''
    def add_item(self,item_name):
        self.inventory.append(item_name)

    def set_player_position(self,pos):
        self.position = pos

    '''
        Print out player actions with movement
    '''
    def get_actions(self):
        actions = self._make_nav_pretty()
        actions.extend(self.player_actions)
        return actions
        
    def _make_nav_pretty(self):
        nav_pretty = []
        for act in self.nav_actions:
            nav_pretty.append("{} <{}>".format(act,','.join(self.movement_directions)))
        
        return nav_pretty