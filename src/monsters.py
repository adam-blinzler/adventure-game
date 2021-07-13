'''
    This file builds monsters to be used and stored elsewhere
'''
import random

#################################
class monster:
    '''
        Generic monster class for all
    '''
    def __init__(self, name, win_condition, bad_stuff):
        self.name = name
        self.win_condition = win_condition
        self.bad_stuff = bad_stuff
        self.is_sleeping = False
    '''
        Status modifiers
    '''
    def set_to_sleep(self):
        self.is_sleeping = True
        self.name = "sleeping " + self.name
        self._change_to_sneak()

    def _change_to_sneak(self):
        if "run" in self.win_condition:
            self.win_condition.remove("run")
        
        if "sneak" not in self.win_condition:
            self.win_condition.append("sneak")
    '''
        Print out special death text
    '''
    def death_scene(self):
        print(self.bad_stuff)

def monster_builds(monster_file):
    '''
        Retrieve a list of all the monster builds available.
    '''
    builds = []
    with open(monster_file, 'r') as f:
        for line in f:
            if line[0] != '#' and len(line.split(',')) > 0:
                monster = []
                monster = [part.strip() for part in line.split(',')]
                #make win condition into list
                monster[1] = monster[1].split('-')
                builds.append(monster)
    
    return builds

def get_randos(monster_file, num=1):
    '''
        Retrieve a random monster
    '''
    all_monsters = monster_builds(monster_file)
    randos = []
    for _ in range(num):
        rando_build = random.choice(all_monsters)
        rando = monster(*rando_build)
        if random.choice([True, False]):
            rando.set_to_sleep()
        randos.append(rando)
        
    return randos