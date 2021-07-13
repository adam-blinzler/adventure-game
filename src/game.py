
'''
    This is the main file for an adventure game.

    Requires python3
'''
import os
import argparse
import random
import math

# Internal files
import engine
import gamemap
import player
import monsters

#################################

INDENT = "    "

def get_all_config_lines(configfile_path):
    '''
        Collect all lines with configuration data from the configfile
    '''
    config = dict()

    with open(configfile_path, 'r') as f:
        for line in f:
            if len(line.strip())== 0 or line[0] == '#':
                #ignore blank or comment lines
                continue
            else:
                category = line.split('-')[0]
                component = line.split('-')[1].split(':')[0].strip()
                design_info = line.split(':')[1].strip()

                if category not in config:
                    config[category] = dict()
                elif component in config[category]:
                    print("Warning :: conflicting parameters - Listed more than 1 time , {}-{}".format(category,component))
                    print("Warning :: using last found parameters - {}".format(line.strip()))

                config[category][component] = design_info

    return config

def populate_monsters(game_map, game_design):
    '''
        Add a random amount of monsters around the map spaces
    '''

    rooms_unavailable = [game_map.start, game_map.end, *game_map.dead_rooms]
    rooms_available = [room for room in list(range(0,game_map.width*game_map.height-1)) if room not in rooms_unavailable]
    
    if len(rooms_available) > 0:
        monsters_to_add = random.randint(1,math.ceil((len(rooms_available))/2))

        rooms =  random.sample(rooms_available, monsters_to_add)
        monster_list = monsters.get_randos(game_design["monsters"],num=monsters_to_add)

        for room, monster in zip(rooms,monster_list):
            game_map.add_to_room(room, ["monster", monster])
        print("{}Monsters Added".format(INDENT))
    else:
        print("Warning :: No rooms available to add monsters.")
    return game_map

def need_monsters(config,game_design):
    '''
        See if monsters need to be added
        Return
                -1    : Error in configfile parameters
                0     : No monsters needed
                1     : Yes monsters needed
    '''
    if "monsters" in config["gamemap"]:
        if "auto" in config["gamemap"]["monsters"]:
            if not "monsters" in game_design:
                return -1
        else:
            return 0
    else:
        return 0
    return 1

def build_game_from_configfile(config):
    '''
        Using the configuration lines, build the gamemap and player classes, and store text info
    '''
    good_config = True

    #load game_design parameters from config
    game_design = dict()
    if "design" in config:
        for key, file in {key : "./game-design/" + loc for key, loc in config["design"].items()}.items():
            if not os.path.isfile(file):
                print("Warning :: design-{} {} file not found.".format(key,file))
            else:
                game_design[key] = file

    #load game map class from config
    game_map = gamemap.gamemap()
    if game_map.load_config({ cat : config[cat] for cat in game_map.config_catagories}):
        need_monster_return = need_monsters(config,game_design)
        if need_monster_return == 1:
            game_map = populate_monsters(game_map, game_design)
        elif need_monster_return == -1:
            print("Error :: Monster parameters incompatible.")
            good_config = False
    
    else:
        print("Error :: Failed to load game map configuration.")
        good_config = False

    #load player class from config
    game_player = player.player()
    game_player.load_movement(game_map.movement_directions)
    if game_player.load_config({ cat : config[cat] for cat in game_player.config_catagories}):
        pass
    else:
        print("Error :: Failed to load player configuration.")
        good_config = False

    return good_config, game_player, game_map, game_design

def cli():
    '''
        Build the command line interface
    '''
    my_parser = argparse.ArgumentParser(description='Welcome to the your text adventure. To begin, add the path to the \
                                        configuration file. See sample file for help.')
    # Only use required positional arguments
    my_parser.add_argument('path', metavar='path', type=str,
                           help='path to text file of the word list')

    args = my_parser.parse_args()

    filepath = os.path.abspath("./game-design/" + args.path)

    if os.path.isfile(filepath):
        return filepath
    else:
        print("Error :: Invalid configuration file path")
        return False

'''
    MAIN
'''
if __name__ == "__main__":

    good_config = True
    configfile_path = cli()

    if configfile_path:
        config = get_all_config_lines(configfile_path)
        if config:
            good_config, game_player, game_map, game_design = build_game_from_configfile(config)
            if good_config:
                engine.start_game(game_player, game_map, game_design)

        else:
            print("Error :: Unable to start adventure game.")
            good_config = False

    else:
        print("Error :: Unable to start adventure game.")
        good_config = False

    print("\n--- Adventure Game Has Ended ---")
    if not good_config:
        print("Errors were found in configuration. Check the log.")