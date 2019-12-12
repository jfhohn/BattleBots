import sys
sys.path.append('..')

from my_modules.bot_game_functions import add_lists, check_bounds, WanderBot, ExploreBot, TeleportBot, \
                                          DiagonalBot, FastBot, choose_bots, assign_teams, game_starting_position, \
                                          check_positions, battle, destroy_bot, respawn,  bot_type, update_score, \
                                          display_winner, free_for_all, team_deathmatch

import random
from time import sleep
from IPython.display import clear_output


#display welcoming statement
print('Hello! Welcome to BattleBots! We hope you enjoy your stay.\n')


# initialize variable to continue playing game 
done_playing = False

while not done_playing:
    
    # ask user what type of game they'd like to play
    game_mode = input('What game mode would you like to play?' \
                      '\nA) Free for all\nB) Team Deathmatch')
    
    if str.lower(game_mode) == 'a':
        
        # set game mode
        game_mode = 'ffa'
        
        # ask for number of bots on board
        num_bots = input('How many bots would you like on the board?\n')
        
        # get user input for bots to play
        bots = choose_bots(num_bots, game_mode)
        
        # get grid size from user
        grid_size = input('Now select an integer for grid_size (N x N): ')
        
        # play the game
        print('Enjoy the game!')
        free_for_all(bots, grid_size = int(grid_size))
    
    elif str.lower(game_mode) == 'b':
        
        #set game mode
        game_mode = 'tdm'
        
        print('Choose six bots you would like to compete:\n')
        
        # set number of bots to 6 for 3v3
        num_bots = 6
        
        #get user input for bots to play
        bots = choose_bots(num_bots, game_mode)
        
        # get grid size from user
        grid_size = input('Now select an integer for grid_size (N x N): ')
        
        # get points to win from user
        points_to_win = input('What score would you like to set to win?: ')
        
        # play the game!
        print('Enjoy the game!')
        team_deathmatch(bots, grid_size = int(grid_size), points_to_win = int(points_to_win))
        
    # user inputted wrong key - check if they would still like to play
    else:
        print('That is not an option.\n')
        play = input('Would you like to continue playing?\n' \
                     'A) Yes\nB) No')
        
        if str.lower(play) == 'a':
            done_playing = False
            
        else:
            print('Okay, goodbye!')
            done_playing = True
            break
            
    playing = input('Would you like to play again?\n' \
                    'A) Yes\nB) No')
    
    if str.lower(playing) == 'a':
        done_playing = False
        
    else:
        print('Okay, thanks for stopping by!')
        done_playing = True