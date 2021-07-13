'''
    This file configures the games map
'''
import math

#################################

class gamemap():
    '''
        gamemap holds all information about the map and relative position calculations
    '''
    def __init__(self):
        self.height = 0
        self.width = 0

        self.start = 0
        self.end = 0
        self.need_item = False
        
        self.rooms = dict()
        self.dead_rooms = []

        self.config_catagories = ["gamemap"]
        self.config_component_required = ["dims","start","end"]
        self.movement_directions = ['n','s','e','w']
    '''
        Configuration management
    '''
    def load_config(self,config):
        '''
            Return state of configuration load attempt
        '''
        good_config = True
        indent = "    "
        
        if not all(item in config["gamemap"].keys() for item in self.config_component_required):
            print("Error :: Failed to find all required gamemap components {}".format(self.config_component_required))
            good_config = False
        else:
            print("\nLoading Gamemap design info ....")
            # configure board layout
            N = int(config["gamemap"]["dims"].split(',')[0].strip())
            M = int(config["gamemap"]["dims"].split(',')[1].strip())
            self._build_board(N,M)
            print("{}Board created".format(indent))

            # identify start and end rooms
            self._set_objective(int(config["gamemap"]["start"]), int(config["gamemap"]["end"]))
            print("{}Start and End rooms loaded".format(indent))

            # store dead rooms where player cannot go
            if "dead_rooms" in config["gamemap"]:
                self._set_dead_rooms(config["gamemap"]["dead_rooms"])
                print("{}Dead Rooms loaded".format(indent))

            # store the goal / item the player needs to be able to win
            if "goal" in config["gamemap"]:
                self._add_goal(config["gamemap"]["goal"])
                print("{}Game Map Goal loaded".format(indent))

            return good_config

    def _build_board(self, width, height):
        self.width = width
        self.height = height

    def _set_objective(self, start, end):
        self.start = start
        self.end = end

    def _set_dead_rooms(self, dead_rooms):
        self.dead_rooms = [int(room) for room in dead_rooms.strip().split(',')]

    def _add_goal(self,goal):
        goal_loc = int(goal.split(',')[0].strip())
        goal_name = goal.split(',')[1].strip()
        self.add_to_room(goal_loc,["item", goal_name])

        self.need_item = goal_name
        return

    '''
        Map position translations
    '''
    def room_to_cords(self, room):
        x = math.floor(room / self.width)
        y = room - (self.width * x)
        return [x, y]

    def cords_to_room(self, cords):
        room = self.width * cords[1] + cords[0]
        return room

    '''
        Movement
    '''
    def move_if_possible(self, current_pos, direction):
        new_pos = self._move(current_pos, direction)

        if self._is_move_possible(new_pos):
            return new_pos
        else:
            return current_pos

    def _move(self, current_pos, direction):
        if direction == "n":
            return [current_pos[0],current_pos[1] - 1]
        elif direction == "s":
            return [current_pos[0],current_pos[1] + 1]
        elif direction == "e":
            return [current_pos[0] + 1,current_pos[1]]
        elif direction == "w":
            return [current_pos[0] - 1,current_pos[1]]

    def _is_move_possible(self, pos):
        if self.cords_to_room(pos) in self.dead_rooms:
            return False
        elif pos[0] < 0 or pos[0] > (self.width - 1) or pos[1] < 0 or pos[1] > (self.height - 1):
            return False
        else:
            return True

    '''
        Manage Room Inventory
    '''
    def add_to_room (self,room,thing):
        if not room in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(thing)

    def remove_from_room(self,room,thing):
        self.rooms[room].remove(thing)
        if len(self.rooms[room]) == 0:
            del self.rooms[room]

    def is_monster_in_room(self, room):
        if room in self.rooms:
            for thing in self.rooms[room]:
                if thing[0] == "monster":
                    return True, thing[1]
        return False, False

    '''
        Display Map
    '''
    def print_map(self):
        print('-'*(self.width*4+1))
        for i in range(self.height):
            if not i == 0:
                print('----'*(self.width) + '-')
            print('|   '*(self.width+1))
            print('|   '*(self.width+1))
        print('-'*(self.width*4+1))

        return