# Tulane CMPS 1500
# Spring 2023
import random
import copy

# STUDENTS: no need to modify any of this
def BoggleBoardGenerator(board_size):
    """ This function will return a boggle board with letters chosen
    in a square grid with dimension board_size"""
    dice = [] # will be a list of 16 dice (letters taken from board game)
    dice.append(['A','A','E','E','G','N'])
    dice.append(['A','B','B','J','O','O'])
    dice.append(['A','C','H','O','P','S'])
    dice.append(['A','F','F','K','P','S'])
    dice.append(['A','O','O','T','T','W'])
    dice.append(['C','I','M','O','T','U'])
    dice.append(['D','E','I','L','R','X'])
    dice.append(['D','E','L','R','V','Y'])
    dice.append(['D','I','S','T','T','Y'])
    dice.append(['E','E','G','H','N','W'])
    dice.append(['E','E','I','N','S','U'])
    dice.append(['E','H','R','T','V','W'])
    dice.append(['E','I','O','S','S','T'])
    dice.append(['E','L','R','T','T','Y'])
    dice.append(['H','I','M','N','U','Q']) # Q is special
    dice.append(['H','L','N','N','R','Z'])
    # if we need more than 16 dice, duplicate one at random
    if board_size>4:
        extras_needed = (board_size**2)-16
        for _ in range(extras_needed):
            dice.append(random.choice(dice))
    random.shuffle(dice) # ordering of dice is randomized when shaking
    return [[random.choice(dice.pop())
            for i in range(board_size)]
             for j in range(board_size)]

def remove_letter(board, row, col):
    """ remove_letter takes as input a board (list of lists), makes a deep copy
    of the board, and then replaces the letter at [row][col] with a space.
    The space won't match any words (since no words in the wordlist contain
    spaces), so this prevents a letter from being used twice while looking up
    a single word on the game board (during is_valid_guess).

    This function returns a copy of the board with one letter removed, but does
    not change the original game board (which should be left untouched so it 
    can continue to be used in the rest of the game."""
    newboard = copy.deepcopy(board)
    newboard[row][col] = ' ' # remove letter by replacing it with ' '
    return newboard
