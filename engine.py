'''
    This file is used to control the games flow.
    To use, execute start_engine()
'''
import os

#################################

INDENT = "    "

def print_help_info(player_actions):
    '''
        Print out all the actions the player can take
    '''
    print("\nIn this wild and crazy world you can do the following :")
    print("{}help".format(INDENT))
    for act in player_actions:
        print("{}{}".format(INDENT,act))

    return

def inspect_room(room):
    '''
        Look around the room for anything stored in the room inventory
    '''
    if room in game_map.rooms:
        print("This room contains:")
        
        for thing in game_map.rooms[room]:
            if thing[0] == "monster":
                print("{}{} - {}".format(INDENT,thing[0],thing[1].name))
            else:
                print("{}{} - {}".format(INDENT,thing[0],thing[1]))
    else:
        print("You found nothing interesting in this room.")
    return

def pickup_item(room, thing_to_pickup):
    '''
        Attempt to pick up an item
    '''
    if room in game_map.rooms:
        thing_found = False
        
        for thing in game_map.rooms[room]:
            if thing[0] == thing_to_pickup:
                game_player.add_item(thing[1])
                game_map.remove_from_room(room,thing)
                thing_found = True
                print("You picked up {}".format(thing[1]))
                break

        if not thing_found:
            print("Could not find {} in the room.".format(thing_to_pickup))
    else:
        print("There is no item to pickup in this room.")
    return

def attempt_move(player_pos, move_dir):
    '''
        See if the user's movement choice is allowed
        Return new position if allowed, else return False
    '''
    player_pos_new = game_map.move_if_possible(player_pos,move_dir)
    if player_pos_new == player_pos:
        return False
    else:
        return player_pos_new

def move_player(user_in):
    '''
        Attempt to move the player and resolve any issues with monsters or blocked paths
    '''
    move_type = user_in.split(' ')[0].strip()
    move_dir = user_in.split(' ')[1].strip()

    did_player_die = False

    is_monster, baddie = game_map.is_monster_in_room(game_map.cords_to_room(game_player.position))
    if is_monster:
        if move_type not in baddie.win_condition:
            did_player_die = True
            baddie.death_scene()
        else:
            print("Your quick action has allowed you evade the {}".format(baddie.name))

    if not did_player_die:
        if move_dir in game_map.movement_directions:
            position_new = attempt_move(game_player.position, move_dir)
            if position_new:
                game_player.set_player_position(position_new)
                print("You successfully make your way out of the room by going {}".format(move_dir))
            else:
                print("The path this direction is blocked.")
                if is_monster:
                    did_player_die = True
                    print("Your error in navigation has allowed {} to catch you.".format(baddie.name))
                    print(baddie.bad_stuff)
        else:
            print("The direction specified is not recognized : {}".format(move_dir))

    return did_player_die

def attacking():
    '''
        Resolve player conflict if attacking
    '''
    did_player_die = False
    
    room = game_map.cords_to_room(game_player.position)
    is_monster, baddie = game_map.is_monster_in_room(room)
    
    if is_monster:
        if "attack" not in baddie.win_condition:
            did_player_die = True
            print("The {} seems confused by the futility of your actions ...".format(baddie.name))
            baddie.death_scene()
    
        else:
            print("You stand your ground and pummel the {} into submission.".format(baddie.name))
            game_map.remove_from_room(room, ["monster", baddie])
    else:
        print("In a fit of insanity, you swing wildly at the air. Luckily nobody saw you.")

    return did_player_die

def implemented_actions():
    '''
        List of options available in take_action()
    '''
    return ['inspect room' , 'pickup item', 'read map', 'attack']

def take_action(action):
    '''
        Resolve player actions.
        Keep implemented_actions up to date with conditions implemented
    '''
    did_player_die = False

    room = game_map.cords_to_room(game_player.position)

    if action == 'inspect room':
        inspect_room(room)

    elif "pickup item" in action:
        pickup_item(room, action.split(' ')[1].strip())

    elif action == 'read map':
        game_map.print_map()

    elif action == "attack":
        did_player_die = attacking()

    return did_player_die

def get_user_input():
    '''
        Get input from the user and act on it
        Return status of if they died or not
    '''
    did_player_die = False

    print("\nWhat do you want to do?")
    user_in = input('>').lower().strip()

    if "help" in user_in:
        print_help_info(game_player.get_actions())

    elif user_in in game_player.player_actions:
        did_player_die = take_action(user_in)

    elif user_in.split(' ')[0] in game_player.nav_actions and len(user_in.split(' ')) == 2:
        did_player_die = move_player(user_in)

    else:
        print("I'm sorry. I do not understand that command.")

    return did_player_die

def play_round():
    '''
        Play a round in the game world
    '''
    game_over = get_user_input()

    return game_over

def did_player_win():
    '''
        Check victory conditions and return if player has won or not
    '''
    if game_map.cords_to_room(game_player.position) == game_map.end:
        if not game_map.need_item:
            return True
        else:
            if game_map.need_item in game_player.inventory:
                return True
            else:
                print("You see the way out but need to recover the {} first.".format(game_map.need_item))
                return False
    return False

def present_text(text_file):
    '''
        Read out game text file
    '''
    with open(text_file, 'r') as f:
        for line in f:
            print(line.strip())
    return

def play_intro(g_design):
    '''
        Read out introduction before first round begins
    '''
    print("\n\n--- Your Adventure begins ---")
    if "intro" in g_design:
        if os.path.isfile(g_design["intro"]):
            present_text(g_design["intro"])
        else:
            print("Warning :: Intro text file not found.")
    return

def play_outro(g_design):
    '''
        Play the outro information when the player has won
    '''
    print()
    if "escape" in g_design:
        if os.path.isfile(g_design["escape"]):
            present_text(g_design["escape"])

        else:
            print("Warning :: Escape text file not found.")
            print("Congratulations! You were able escaped this terrible place.")
    else:
        print("Congratulations! You were able escaped this terrible place.")

    return

'''
    MAIN JUMPING IN POINT
'''
def start_game(g_player, g_map, g_design):
    '''
        Main function to be called to start the game engine

    '''
    global game_player
    game_player = g_player

    global game_map
    game_map = g_map

    play_intro(g_design)

    # Set the player to starting position and still alive
    player_won = False
    player_dead = False
    game_player.set_player_position(game_map.room_to_cords(game_map.start))

    while not player_dead and not player_won:
        player_dead = play_round()

        if not player_dead:
            player_won = did_player_win()

    if player_won:
        play_outro(g_design)

    return