import random

from time import sleep
from IPython.display import clear_output

#bot functions

def add_lists(list1,list2):
    """sum each element of two lists
    
     copied from artificial agents homework
     original author: Jacob Hohn
     renamed variables
    
    Parameters
    -----------
    list1 - list of ints or floats
        used in this project to add ints together
    list2 - list of ints or floats
        used in this project to add ints together
    
    Returns
    ----------
    summed_list - list of ints or floats
        contains summation of each element input lists
    """
    summed_list = []
    
    for int1,int2 in zip(list1,list2):
        summed_list.append(int1 + int2)
    
    return summed_list


def check_bounds(position,size):
    """validate that position is valid for given size
    
        copied from artificial agents homework
        original author: Jacob Hohn
        renamed variables
    
    Parameters
    -----------
    position - list of ints
        corresponds to coordinates on a grid
    size - int
        number representing grid bounds
    
    Returns
    --------
    
    """
    # assume coordinates are not in bounds
    in_bounds = False
    
    # check if either of the coordinates are out of bounds 
    # if so return that it's out of bounds
    for element in position:
        if element < 0 or element >= size:
            return in_bounds
    
    # if function did not return, coordinates are in bounds
    in_bounds = True
    
    return in_bounds


class Bot():
    """
    base class containing elements for manipulating artificial agents on a grid
    
    refactored from Bot class in artificial agents homework 
    Author of original code: Jacob Hohn
    added starting position and team attributes for use in this project
    
    Attributes
    -----------
    character - integer
        used to represent bot on a grid
    position - list of [int, int]
        coordinates for location on a grid
    starting_position - list of [int,int]
        point where bot started on grid
    team - int
        only used in certain game modes
        red(1)/blue(0)
    moves - list of list of [int, int]
        possible moves bot can take on a grid
    grid_size - None or int 
        defines boundaries set that limiits bot's position
    """
    def __init__(self, character = 8982):
        """Constructor for Bot Class"""
        
        self.character = chr(character)
        self.position = [0,0]
        self.starting_position = [0,0]
        self.team = None
        self.moves = [[-1,0], [1,0], [0,1], [0,-1]]
        self.grid_size = None

        
        
class WanderBot(Bot):
    """bot that moves in random cardinal coordinate directions
       inherits WanderBot class
       
    Copied from WanderBot class in artificial agents homework 
    Author of original code: Jacob Hohn
    added functionality and condition for when board is run
    
    Attributes
    -----------
    character - integer
        used to represent bot on a grid
    position - list of [int, int]
        coordinates for location on a grid
    starting_position - list of [int,int]
        point where bot started on grid
    moves - list of list of [int, int]
        possible moves bot can take on a grid
    grid_size - None or int 
        defines boundaries set that limiits bot's position
    """
    
    def __init__(self,character = 8982): 
        """construct for WanderBot Class
           calls super from Bot"""
        super().__init__(character)
    
    def wander(self):
        """choose random move from moves list and make sure it is valid on the grid"""
        
        #used for checking that bot has a valid move
        has_new_pos = False
        
        while not has_new_pos:
            #choose a random move
            move = random.choice(self.moves)
            
            # change bot's position
            new_pos = add_lists(self.position, move)
            
            # check that position change was valid
            has_new_pos = check_bounds(new_pos, self.grid_size)
        
        return new_pos
    
    def move(self):
        """move WanderBot on a grid"""
        
        # move via wander method
        self.position = self.wander()       

        
        
class ExploreBot(Bot):
    """bot that tends to move in the same direction it was last moving
       inherits Bot class
    
       copied from homework
       original author: Jacob Hohn
    
    Attributes
    -----------
    character - integer
        used to represent bot on a grid
    position - list of [int, int]
        coordinates for location on a grid
    starting_position - list of [int,int]
        point where bot started on grid
    moves - list of list of [int, int]
        possible moves bot can take on a grid
    grid_size - None or int 
        defines boundaries set that limiits bot's position
    move_prob - float
        probability that the bot moves in the same direction it was just moving"""
    
    def __init__(self,character = 8982, move_prob = 0.75):
        """constructor for ExploreBot class
           calls super from Bot class"""
        
        super().__init__(character)
        self.move_prob = move_prob
        self.last_move = None
    
    def biased_choice(self):
        """high percentage chance to move in the same direction previously moving
           small percentage bot chooses new direction to move"""
        
        move = None
        
        #set move as the same move just taken
        if self.last_move != None:
            if random.random() < self.move_prob:
                move = self.last_move
                
        # low chance to select new move entirely
        if move == None:
            move = random.choice(self.moves)
            
        return move
            
    
    def explore(self):
        """move mostly biasedly around the grid"""
        
        has_new_pos = False
        
        while not has_new_pos:
            #set move to last valid move (most likely)
            move = self.biased_choice()
            
            #change position
            new_pos = add_lists(self.position, move)
            
            #check if move just made is valid within the grid
            has_new_pos = check_bounds(new_pos, self.grid_size)
            
            #set move just performed as last move for future use
            self.last_move = move
        
        return new_pos
    
    def move(self):
        """move ExploreBot on a grid"""
        
        # move via explore method
        self.position = self.explore()
        
        
class TeleportBot(WanderBot):
    """bot that moves in random cardinal coordinate directions and sometimes teleports
       to a random location on the grid
       inherits WanderBot class
       
    Copied from TeleportBot class in artificial agents homework 
    Author of original code: Jacob Hohn
    added functionality and condition for when board is run
    
    Attributes
    -----------
    character - integer
        used to represent bot on a grid
    position - list of [int, int]
        coordinates for location on a grid
    starting_position - list of [int,int]
        point where bot started on grid
    moves - list of list of [int, int]
        possible moves bot can take on a grid
    grid_size - None or int, optional
        defines boundaries set that limiits bot's position
    tele_prob - float, optional
        defines how often Teleport Bot will move to a random location on the grid
        """
    
    def __init__(self, character = 8982, tele_prob = 0.3 ):
        """constructor for Teleport Bot"""
        
        super().__init__(character)
        self.tele_prob = tele_prob
    
    def teleport(self):
        """move to a random location on the grid"""
        
        #initialize list for new location
        randlst = []
        
        #choose two random valid coordinates for bot to teleport to
        randlst.append(random.choice(range(self.grid_size)))
        randlst.append(random.choice(range(self.grid_size)))
        
        return randlst
    
    def move(self):
        """move Teleport Bot on a grid"""
        
        # most of the time - move randomly, sometimes teleport to new location
        if random.random() < self.tele_prob:
            self.position = self.teleport()
        else:
            self.position = self.wander()

            
class DiagonalBot(ExploreBot):
    """bot that tends to move in the same direction it was last moving
       can only move diagonally
       
       inherits ExploreBot class
    
       refactored from ExploreBot class to have a different move scheme
       original author: Jacob Hohn
       consider for grading
    
    Attributes
    -----------
    character - integer
        used to represent bot on a grid
    position - list of [int, int]
        coordinates for location on a grid
    starting_position - list of [int,int]
        point where bot started on grid
    moves - list of list of [int, int]
        possible moves bot can take on a grid
    grid_size - None or int 
        defines boundaries set that limiits bot's position
    diag_prob - float, optional
        probability that bot chooses to move diagonally on a grid
    move_prob - float, optional
        probability that the bot moves in the same direction it was just moving
        """
    
    def __init__(self, character = 8982, diag_prob = 0.8, move_prob = 0.75):
        """constructor for DiagonalBot class"""
        
        super().__init__(character,move_prob)
        self.diag_moves = [[1,1], [1,-1], [-1,1], [-1,-1]]
        self.diag_prob = diag_prob
    
    def diagonal_biased_choice(self):
        """high percentage chance to move in same direction bot was already moving
        
        refactored from biased_choice method in ExploreBot
        changed available move list to diagonal moves
        Original Author: Jacob Hohn
        """
        
        
        #only changed moves to choose from
        move = None
        if self.last_move != None:
            if random.random() < self.move_prob:
                move = self.last_move
        if move == None:
            move = random.choice(self.diag_moves)
            
        return move
        
    
    def diagonal_explore(self):
        """move mostly biasedly around the grid
        
        refactored from explore method in artificial agents homework
        change biased_choice method to diagonal_biased_choice method
        original author: Jacob Hohn
        """
        
        has_new_pos = False
        
        #only changed biased choice
        while not has_new_pos:
            move = self.diagonal_biased_choice()
            new_pos = add_lists(self.position, move)
            has_new_pos = check_bounds(new_pos, self.grid_size)
            self.last_move = move
        
        return new_pos
        
    def move(self):
        """move Diagonal Bot on a grid"""
        
        # high chance to continue in same direction already moving
        if random.random() < self.diag_prob:
            self.position = self.diagonal_explore()
            
        else:
            self.position = self.explore()
 

class FastBot(WanderBot):
    """bot that moves in random cardinal coordinate directions
       moves two times the speed of other bots
       inherits WanderBot class
       
    Refactored from WanderBot class in artificial agents homework 
    Author of original code: Jacob Hohn
    changed moves list to reflect theme of the bot
    consider for grading
    
    Attributes
    -----------
    character - integer
        used to represent bot on a grid
    position - list of [int, int]
        coordinates for location on a grid
    starting_position - list of [int,int]
        point where bot started on grid
    moves - list of list of [int, int]
        possible moves bot can take on a grid
    grid_size - None or int 
        defines boundaries set that limiits bot's position
    """
    def __init__(self, character = 8982):
        """constructor for FastBot class"""
        
        super().__init__(character)
        self.moves = [[2,0],[0,2],[-2,0],[0,-2]]
        
    #inherits wander and move from WanderBot
    


#----------------------------------------------------------------

#game functions

def choose_bots(num_bots, game_mode):
    """allow user to choose what bots compete
    
    Parameters
    ------------
    num_bots : string
        defines how many bots are competing, convert to int in function
    game_mode : string
        defines what game user is playing (ffa or tdm)
        
    Returns
    -------------
    bots : list of Bot() type
        all the bots competing in the game"""
    
    # initialize empty bots list
    bots = []
    
    # set team deathmatch bots to 6 bots (3v3)
    if game_mode == 'tdm':
        num_bots = 6
    
    #convert num_bots to integer
    else:
        num_bots = int(num_bots)
        
    #loop while len(bots) < #  of bots
    while len(bots) < len(range(num_bots)):
                
        temp_type = input('Please pick a bot type:\n' \
                          'A) WanderBot\nB) ExploreBot' \
                          '\nC) TeleportBot\nD) DiagonalBot'\
                          '\nE) FastBot')
            
        #give bot random symbol
        temp_char = int(random.random()*10000)
               
        # create bots list to play
        if str.lower(temp_type) == 'a':
            bots.append(WanderBot(character = temp_char))
               
        if str.lower(temp_type) == 'b':
            bots.append(ExploreBot(character = temp_char))
             
        if str.lower(temp_type) == 'c':
            bots.append(TeleportBot(character = temp_char))
                
        if str.lower(temp_type) == 'd':
            bots.append(DiagonalBot(character = temp_char))
            
        if str.lower(temp_type) == 'e':
            bots.append(FastBot(character = temp_char))
    
    return bots

    

def assign_teams(bots, teams = [1,0,1,0,1,0]):
    """assign bots 'randomly' to two teams. 
       
       Parameters
       -----------
       bots - list of Bot()
           assign .team attribute 'red' or 'blue'
       teams = list of ints
           red(1)/blue(0), should be same length as bots list
           default = [1,0,1,0,1,0]
       """
    
    # check that bots list and teams list have the same length to properly attach labels
    if len(bots) == len(teams):
        
        # loop through both bots list and teams list if they are the same length
        for bot,team in zip(bots,teams):
            if team == 1:
                bot.team = 'red'
                
            elif team == 0:
                bot.team = 'blue'
            
            else:
                #teams statement not correct
                pass
            
    else:
        # if length of lists were not the same, you will get an error later with no teams attached
        raise IndexError('Bots and teams list not the same length')
        
        
        
def game_starting_position(bots, game_mode):
    """set each bots starting position based on game mode
    
    Parameters
    -------------
    bots : list of Bot() type
        assign each bot different positions
    game_mode : string
        depending on game mode assign bots to different positions
    """    
    
    if game_mode == 'ffa':
        
        # initialize options for starting position from one of the bot's grid size
        # it does not matter which bot since they have the same grid size
        pos_options = range(bots[0].grid_size)
        
        # in free for all give every bot a random starting position in the grid 
        for bot in bots:
            bot.position = [random.choice(pos_options),random.choice(pos_options)]
                   
    
    if game_mode == 'tdm':
        # in free for all give all members of the same team the same starting position
        # teams start on opposite ends of the grid
        
        # loop through individual bots
        for bot in bots:
            
            # if bot is on the red team, assign them to the bottom middle point of the grid
            # also initialize bot's starting position for respawn purposes
            if bot.team == 'red':
                bot.position = [bot.grid_size-1,bot.grid_size//2]
                bot.starting_position = bot.position
                
            # assign blue team bots to the top middle point of the grid
            # also initialize bot's starting position for respawn purposes
            else:
                bot.position = [0, bot.grid_size//2]
                bot.starting_position = bot.position              
        
            

def check_positions(bots, game_mode):
    """create list of pairs of bots that share the same positions.
    
    Parameters
    ------------
    bots : list of Bot() type
        loop through bots list and compare positions
    game_mode : string 
        decide whether to take team into account or not
        
    Returns
    ------------
    pos_pairs : list of [Bot,Bot]
        """
    
    # initialize list to hold pairs of bots sharing positions
    pos_pairs = []
    
    # initialize list of bots to skip so pairs do not get added twice
    bots_to_skip = []
    
    if game_mode == 'ffa':
        
        for bot1 in bots:
            
            # check that bot is not already paired up
            if bot1 not in bots_to_skip:
                
                for bot2 in bots:
                    
                    # avoiding comparisons of bots with the same reference
                    if bot1 != bot2:
                        if bot1.position == bot2.position:
                            
                            # append pair of bots to list for use later
                            pos_pairs.append([bot1,bot2])
                            # append second bot so loop skips further comparisons with it
                            bots_to_skip.append(bot2)
                            
    elif game_mode == 'tdm':
        
        for bot1 in bots:
            
            # check that bot is not already paired up
            if bot1 not in bots_to_skip:
                
                for bot2 in bots:
                    
                    # avoiding comparisons of bots on the same team
                    # no friendly fire
                    if bot1.team != bot2.team:
                        
                        if bot1.position == bot2.position:
                            
                            # append pair of bots to list for use later
                            pos_pairs.append([bot1,bot2])
                            # append second bot so loop skips further comparisons with it
                            bots_to_skip.append(bot2)
    
    return pos_pairs


def battle(battle_bots, win_probability = 0.5):
    """Make bots that share position engage in combat. Losers are destroyed or respawn.
    
    Parameters
    -----------
    battle_bots : list of [Bot,Bot]
        list of bots that share same position on grid
    win_probability : float, optional
        probability that bot1 wins, default = 0.5
    
    Returns
    ----------
    losing_bots : list of Bot() type
        list of losers from each fight
       """
    
    # initialize list of losing bots
    losing_bots = []
    
    # loop through pairs of bots 
    for bot_pair in battle_bots:
        
        # check to see if bot1 wins
        if random.random() < win_probability:
            # append bot2 to losers list if bot1 wins
            losing_bots.append(bot_pair[1])
            
        else:
            # append bot1 to losers list if bot1 wins
            losing_bots.append(bot_pair[0])
        
        
    return losing_bots
            

    
def destroy_bot(bots, bots_to_destroy):
    """remove losing bots from bots list
    
    Parameters
    -----------
    bots : list of Bot() type
        contains all bots currently competing
    bots_to_destroy : list of Bot() type
        contains list of losing bots to remove from bots
    """
    # loop through competing bots list
    for competing_bot in bots:
        
        #check if competing_bot lost in battle
        if competing_bot in bots_to_destroy:
            #remove competing bot from bots list
            bots.remove(competing_bot)
            
            
def respawn(bots, bots_to_respawn):
    """reset losing bots to their starting positions
    
    Parameters
    -----------
    bots : list of Bot() type
        contains all bots currently competing
    bots_to_respawn : list of Bot() type
        contains list of losing bots to respawn to starting position
        
    """
    #loop through competing bots list
    for competing_bot in bots:
        
        #check if competing bot lost in battle
        if competing_bot in bots_to_respawn:
            #reset position to starting position
            competing_bot.position = competing_bot.starting_position
            
            

def bot_type(bot):
    """returns the type of bot being passed in
    
    Parameters
    -----------
    bot - Bot() type
        one of five types of Bot()
        wander, explore, teleport, diagonal, fast
    
    Returns
    ---------
    type_of_bot - string
        string containing type of bot, or returns nothing if parameter passed in
        is not an instance of any bot
        """
    
    #check the type of bot and save it as a string
    # check for diagonal, fast, and teleport first since they are derived from
    # wander and explore bots
    if isinstance(bot[0], DiagonalBot):
        type_of_bot = 'diagonal bot'
        
    elif isinstance(bot[0], FastBot):
        type_of_bot = 'fast bot'
    
    elif isinstance(bot[0], TeleportBot):
        type_of_bot = 'teleport bot'
        
    elif isinstance(bot[0],WanderBot):
        type_of_bot = 'wander bot'
        
    elif isinstance(bot[0], ExploreBot):
        type_of_bot = 'explore bot'
        
    else:
        # not a bot
        pass
    
    return type_of_bot



def update_score(bots_to_respawn, score):
    """update team deathmatch score to reflect battles
    
    Parameters
    -----------
    bots_to_respawn : list of Bot() type
        check team to decide who gets points
    score : list of ints
        0th index = red team score, 1st index = blue team score
        
    Returns
    --------
    updated_scored : list of ints
        0th index = red team score, 1st index = blue team score
    """
    #initialize updated score with current score
    updated_score = score
    
    #loop through bots that lost in battle
    for respawning_bot in bots_to_respawn:
        
        #if losing bot is on red team, add a point to the blue team
        if respawning_bot.team == 'red':
            updated_score[1] += 1
            
        # if losing bot is on blue team, add a point to the red team
        elif respawning_bot.team == 'blue':
            updated_score[0] += 1
    return updated_score



def display_winner(bots, game_mode, score = None):
    """Congratulate winning bot(s) of game
    
    Parameters
    ----------
    bot : list of Bot() 
        contains only one bot crowned the winner
    game_mode : string
        string literal to represent ffa or tdm
    score : list of ints
        used if game mode was team deathmatch
    """
    
    if game_mode == 'ffa':
        
        # check what kind of bot it is and save the type as a string
        winner = bot_type(bots)
    
        print('Congratulations to ' + winner + ' for coming in first place. Please play again soon!')
    
    elif game_mode == 'tdm':
        
        if score[0] > score[1]:
            winning_team = 'red'
            losing_team = 'blue'
            
        else:
            winning_team = 'blue'
            losing_team = 'red'
        
        print('Congratulations to the ' + winning_team + ' team for beating the ' + losing_team + ' team with a '\
              'final score of ' + str(score[0]) + ' to ' + str(score[1]) + '. See you next time!')
        
        

def free_for_all(bots, grid_size = 5, sleep_time = 0.3, game_mode = 'ffa'):
    """X bots enter. Last one standing wins
    
    refactored from play_board function in artificial agents homework 
    Author of original code: Professor Ellis
    added functionality and condition for when board is run
    consider this function for grading
    
    Parameters
    ------------
    bots : Bot() type or list of Bot() type
        if input only contains one bot, then it automatically wins
    grid_size : int, optional
        Board size. default = 5x5
    sleep_time : float, optional
        Amount of time to pause between turns. default = 0.3        
    
    """
    # If input is a single bot, put it in a list so that procedures work
    if not isinstance(bots, list):
        bots = [bots]
        
    # Update each bot to know about the grid_size they are on
    for bot in bots:
        bot.grid_size = grid_size    
    
    # Set each bots starting position
    game_starting_position(bots,game_mode)
    
    # run game until one bot remains
    while len(bots) > 1:
        
        
        # Create the grid - code taken from homework
        grid_list = [['.'] * grid_size for ncols in range(grid_size)]
        
        # add the bots to the grid
        for bot in bots:
            grid_list[bot.position[0]][bot.position[1]] = bot.character
            
        # add divider for better viewability in terminal
        print('---------------------------')
            
        # check if any of the bots share a position - if so battle!
        battle_bots = check_positions(bots,game_mode)
        bots_to_destroy = battle(battle_bots)
        
        # remove the losers of each battle
        destroy_bot(bots, bots_to_destroy)
        
        
        # Clear the previous iteration, print the new grid (as a string), and wait
        clear_output(True)
        print('\n'.join([' '.join(lst) for lst in grid_list]))
        sleep(sleep_time)

        # Update bot position(s) for next turn
        for bot in bots:
            bot.move()
    
    #check what kind of bot won and congratulate winner
    display_winner(bots,game_mode)
    
    
        
def team_deathmatch(bots, points_to_win = 5, grid_size = 5, sleep_time = 0.3, game_mode = 'tdm'):
    """Two teams of three bots each compete. 
       First team to X points wins
    
    refactored from play_board function in artificial agents homework 
    Author of original code: Professor Ellis
    added functionality and condition for when board is run
    consider this function for grading
    
    Parameters
    ------------
    bots : Bot() type or list of Bot() type
        if input only contains one bot, then it automatically wins
    points_to_win : int, optional
        bots score points by winning in battle against enemy team
    grid_size : int, optional
        Board size. default = 5x5
    sleep_time : float, optional
        Amount of time to pause between turns. default = 0.3    
        
    Returns
    ---------
    score : list of ints
        used for testing to ensure one team reaches points_to_win
        function runs as long as either team's score is less than 
        points to win
    
    """
    # If input is a single bot, put it in a list so that procedures work
    if not isinstance(bots, list):
        bots = [bots]
        
    # Update each bot to know about the grid_size they are on
    for bot in bots:
        bot.grid_size = grid_size    
    
    # Assign teams to each bot via user input
    assign_teams(bots)
    
    # Set each bots starting position
    game_starting_position(bots, game_mode)
    
    # initialize scoring parameters for each team
    # 0th index = points for red team, 1st index = points for blue team
    score = [0,0]
    
    
    # run game until one team has enough points to win
    while not (score[0] >= points_to_win or score[1] >= points_to_win):
        
        
        # Create the grid - code taken from homework
        grid_list = [['.'] * grid_size for ncols in range(grid_size)]
        
        # add the bots to the grid
        for bot in bots:
            grid_list[bot.position[0]][bot.position[1]] = bot.character
        
        print('Score:\nRed Team: ' + str(score[0]) + '\nBlueTeam: ' + str(score[1]))
        # check if any of the bots share a position - if so battle!
        battle_bots = check_positions(bots, game_mode)
        bots_to_respawn = battle(battle_bots)
        
        # respawn the losers of each battle to their starting positions
        respawn(bots, bots_to_respawn)
        # update score to reflect battles
        score = update_score(bots_to_respawn, score)
        
        
        # Clear the previous iteration, print the new grid (as a string), and wait
        clear_output(True)
        print('\n'.join([' '.join(lst) for lst in grid_list]))
        sleep(sleep_time)

        # Update bot position(s) for next turn
        for bot in bots:
            bot.move()
    
    #check what kind of bot won and congratulate winner
    display_winner(bots, game_mode, score)
    
    # used for testing
    return score
