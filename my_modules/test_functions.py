from bot_game_functions import *
import random
from time import sleep
from IPython.display import clear_output

#test free for all function
def test_ffa():
    
    # initialize bots to compete
    bots =  [TeleportBot(character = 1078), ExploreBot(character = 1200), FastBot(character = 1300),
             WanderBot(character = 1500), TeleportBot(character = 8982), DiagonalBot(character = 5000), 
             FastBot(character = 3596), WanderBot(character = 4200)]
    
    #check initial bots length
    assert len(bots) == 8
    
    #call free_for_all
    free_for_all(bots, grid_size = 5)
    
    #asssert ending bots length
    assert len(bots) == 1
    
    #assert grid size matches ffa grid size
    assert bots[0].grid_size == 5

    
# test for team deathmatch function
def test_tdm():
    
    # initialize bots to compete
    bots =  [TeleportBot(character = 3000), TeleportBot(character = 8982), FastBot(character = 3000),
             WanderBot(character = 8982), ExploreBot(character = 3000), DiagonalBot(character = 8982)]
    
    #check initial bots length
    assert len(bots) == 6
    
    #call free_for_all
    final_score = team_deathmatch(bots, points_to_win = 7, grid_size = 5)
    
    #asssert ending bots length
    assert len(bots) == 6
    
    #assert grid size matches ffa grid size
    assert bots[0].grid_size == 5
    
    # assert different teams are assigned correctly
    assert bots[0].team == 'red'
    assert bots[1].team == 'blue'
    
    # check that one of teams score is 7 points
    assert max(final_score) == 7
    

# test diagonal bot class and bot type function
def test_diagonal_bot():
    
    #initialize diagonal bot
    dbot = DiagonalBot()
    
    #check if diagonal bot is bot diagonal and explore bot class
    assert isinstance(dbot, DiagonalBot)
    assert isinstance(dbot, ExploreBot)

    dbot = [dbot]
    
    #test bot_type function
    assert bot_type(dbot) == 'diagonal bot'

    
def test_fast_bot():
    
    #initialize diagonal bot
    fbot = FastBot()
    
    #check if fast bot is both fast and wander bot class
    assert isinstance(fbot, FastBot)
    assert isinstance(fbot, WanderBot)

    fbot = [fbot]
    
    #test bot_type function
    assert bot_type(fbot) == 'fast bot'

 
 # test for check positions and assign teams functions 
def test_check_positions():
    
    # initialize bots
    bots = [DiagonalBot(character = 1078), TeleportBot(character = 1078), WanderBot(character = 1078),
        WanderBot(character = 1127),DiagonalBot(character = 1078), TeleportBot(character = 1078)]
    
    # initialize bots as red/blue teams
    assign_teams(bots, teams = [1,1,1,0,0,0])
    
    # create list with team labels to verify
    team_labels = []
    for bot in bots:
        team_labels.append(bot.team)
        
    # verify team labels are correct according [1,1,1,0,0,0]
    assert team_labels == ['red', 'red', 'red', 'blue', 'blue', 'blue']
    
    #assign bots positions that can be compared with check_position
    for bot in bots:
        if isinstance(bot, DiagonalBot):
            bot.position = [1,1]
        elif isinstance(bot, TeleportBot):
            bot.position = [2,2]
        elif isinstance(bot, WanderBot):
            bot.position = [3,3]
    
    # get pairs of positions that match
    ffa_pairs = check_positions(bots, 'ffa')
    tdm_pairs = check_positions(bots, 'tdm')
            
        
    # check that position pair lists are the correct length
    assert len(ffa_pairs) == 3
    assert len(tdm_pairs) == 3

    
    
# test battle function
def test_battle():
    
    #initialize paired bots, which would come from check positions function
    battle_bots = [[DiagonalBot(), TeleportBot()], [ExploreBot(), WanderBot()], [FastBot(), TeleportBot()]]
    
    # create list of losing bots - should have one bot from each pair passed in
    losing_bots = battle(battle_bots, win_probability = 0.75)
    
    # check that losing bots list is same length as battle_bots
    
    assert len(losing_bots) == len(battle_bots) == 3
    

# test destroy bot function
def test_destroy_bot():
    
    # initialize bots list
    bots = [DiagonalBot(character = 1078), TeleportBot(character = 1078), WanderBot(character = 1078),
            WanderBot(character = 1127),DiagonalBot(character = 1078), TeleportBot(character = 1078)]
    orig_len = len(bots)
    
    # choose bots from bots list to destroy
    bots_to_destroy = [bots[3], bots[5], bots[0]]
    destroy_len = len(bots_to_destroy)
    
    # destroy marked bots by removing them from bots list
    destroy_bot(bots, bots_to_destroy)
    new_bots_len = len(bots)
    
    
    # check that length of original list - list of bots to destroy = new remaining bots list
    assert orig_len - destroy_len == new_bots_len
    
    