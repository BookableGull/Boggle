#Tulane University, CMPS 1500, Spring 2023
#
#STUDENTS MUST FILL IN BELOW
#
#Student name: Ivo Tomasovich
#Student email address: itomasovich@tulane.edu
#
#Collaborators:
#Professor Toups
#Garrett Gilliom
import BoggleFunctions
# NOTE: you must write your own code. You may discuss the assignment with
#       professors, TAs, other students, or family members. But you MUST
#       list anyone you collaborated with in the space above.

# ALSO NOTE: You must add comments which explain how your solution works.
#            If you do not do this, your solution will not receive credit.

from BoggleFunctions import BoggleBoardGenerator
from BoggleWordlist import BoggleWordlist


class GameBoard():
    """ an instance of a boggle board, for use by BoggleGame """
    def __init__(self, game_size=4):
        self.edge_length = game_size # boards are always square
        self.board_letters = BoggleBoardGenerator(game_size) # don't change this line
        # Students may set their own board for testing below, but any custom
        # board below here must be commented out before submitting for grading
        self.board_letters = [['H', 'B', 'W', 'O'],
                              ['T', 'G', 'I', 'C'],
                              ['W', 'G', 'E', 'R'],
                              ['B', 'T', 'S', 'U']]

    def __len__(self):
        """ the length of a GameBoard will be the length of one edge """
        return self.edge_length

    def __str__(self): ### TODO STEP 1: make the game board printable
        """ Convert our GameBoard object to a string for printing"""
        board = ''  # used for the board
        amount = 0  # used to count how far along we are in counting the length of the board
        for item in self.board_letters:  # for every letter in the board, add 1 to amount
            for letter in item:
                amount += 1
                if amount != len(item):  # if amount isn't the length of the item, add to str board the letter and a tab space
                    board += letter + "\t"
                else:  # if it is, set amount back to 0 for the next line. Instead of a tab space, add a new line
                    amount = 0
                    board += letter + "\n"
        return board  # return the board

class BoggleGame():
    """ This class will contain everything needed to play a game of Boggle."""
    def __init__(self, game_size=4):
        """ Create a new game object."""
        # default board size is 4x4
        self.gameboard = GameBoard(game_size) # GameBoard object
        self.wordlist = BoggleWordlist().words # all valid words
        self.words_already_used = [] # begin with empty list
        self.score = 0 # score begins at zero

    def compute_word_score(self, word):
        """ given a word, return a number corresponding to the score for that word"""
        if len(word) == 3 or len(word) == 4:  # if the len of the word is equal to one of these conditions, return the respective points.
            return 1
        elif len(word) < 3:
            return 0
        elif len(word) == 5:
            return 2
        elif len(word) == 6:
            return 3
        elif len(word) == 7:
            return 5
        elif len(word) >= 8:
            return 11
      # TODO STEP 2: compute score according to rules on handout

    def is_valid_guess(self, word):
        word = word.upper()  # used to not make any errors
        points = 0  # used to track if the first 3 conditions are met, to see if it's even worth doing recursion
        rowcounter = 0  # used to track rows initially
        columncounter = 1  # used to track columns initially
        rowcounter2 = 0  # used to track rows in recursion
        columncounter2 = 0 # used to track columns in recursion
        rowlist = [] # used to store the rows of the chosen letter
        columnlist = []  # used to store the columns of the chosen letter
        lettercounter = 0 # used to track which letter we're on
        baserowlist = [] # used to store the rows of the chosen letter as a base
        checks = BoggleWordlist.get_file_lines(self, "ospd.txt") # used to check if the word is in the file
        """ returns True if word is a valid guess, False if not"""
        if len(word.upper()) >= 3: # if the word is greater than or equal to 3, add 1 to points
            points += 1
        check = GameBoard() # used to open the gameboard class for use later
        if word.lower() in checks: # if the word is in the file, add 1 to points
            points += 1
        if word.lower() not in self.words_already_used: # if the word is not in the list of words already used, add 1 to points
            points += 1
        if points == 3: # if points is equal to 3...
                letter = BoggleGame.find_letter_on_board(self, word[lettercounter]) # used to find the letter on the board. Uses word and the lettercounter to find the letter we want to check
                lettercounter += 1 # used to track the letter we're on
                if letter is False: # if the letter is not on the board,
                    return False # return false
                for entry in range(len(letter)):  # gives a list of the rows and columns of the letter, and adds them to the rowlist and columnlist
                    if columncounter < len(letter):
                        rowlist.append(int(letter[rowcounter]))
                        columnlist.append(int(letter[columncounter]))
                        rowcounter += 2
                        columncounter += 2
                    for item in rowlist: # for every item in rowlist, do the following...
                        recursivesearch = BoggleGame.check_string_starting_at(self, word, check.board_letters, int(rowlist[0]), int(columnlist[0]))  # perform recursion on the initial set of row and column of both lists
                        if lettercounter == 1: # if lettercounter is one, set baserowlist and baserowcolumn to the current rowlist and columnlist for future reference
                            baserowlist = rowlist
                            basecolumnlist = columnlist
                        for number in baserowlist:  # for every number in baserowlist, add to rowcounter2 and columncounter2 so we can move on to the next item in those lists
                            rowcounter2 += 1
                            columncounter2 += 1
                if recursivesearch is True:  # if after all the recursion, we reach the empty basecase, and it's true, return true so we can give points
                    return True
                else:
                    return False
        else:
            return False  # if points is not equal to 3, return false
        #return False

    def find_letter_on_board(self, letter):
        """ returns a list of (row,column) for each location on the
        gameboard where the letter can be found. (Empty list returned if
        the letter cannot be found"""
        rowcounter = 0  # used to track rows
        columncounter = 0 # used to track columns
        finallist = [] # used to store the final list of rows and columns
        gamerows = GameBoard() # used to open the gameboard class for use later
        for line in gamerows.board_letters: # for every line in the gameboard
            for item in line: # for every item in the line aka the letters
                if item == letter: # if the item is equal to the letter we're looking for
                    myTuple = (int(rowcounter - 1), int(columncounter - 1))  # make a tuple of the row and column
                    finallist += myTuple  # add the tuple to the finallist (and make it simply a list)
                if columncounter == len(line):  # if the columncounter is equal to 4, reset it to 0
                    columncounter = 0
                columncounter += 1  # add one to columncounter
            rowcounter += 1  # add one to row counter
        if len(finallist) == 0: # if there's nothing in the finallist, return false
            return False
        return finallist # return the finallist

    def is_in_bounds(self, row, col):
        """ returns True if row and column are both in-bounds on the current
        gameboard. Or, returns False if either row or col are less than 0, or
        if row or col are greater than or equal to the length of one edge of
        the gameboard. """
        rowcounter = 0 # used to track rows
        columncounter = 0 # used to track columns
        gamerows = GameBoard() # used to open the gameboard class for use later
        gameactualrows = gamerows.board_letters # used to store the actual rows of the gameboard
        amountofrows = len(gameactualrows) # used to store the amount of rows in the gameboard
        if row < 0 or col < 0: # if the row or column is less than 0, return false
            return False 
        else: 
            if row >= amountofrows or col >= amountofrows: # if the row or column is greater than or equal to the amount of rows, return false
                return False
            elif row >= gamerows.edge_length or col >= gamerows.edge_length: # if the row or column is greater than or equal to the edge length, return false
                return False
            else: # if none of the above are true, return true
                return True
                

    def check_string_starting_at(self, string, board, row, col):
        """ checks to see if a string can be found starting at position
        (row, col) on the board given as a parameter. If it can be found
        there (according to the Boggle rules), return True. If it can't,
        return False.
        """
        slicedstring = string # used to store the sliced string
        lettercheck = BoggleGame # used to open the BoggleGame class for use later
        Falsecounter = 0 # used to track the amount of false statements
        Truecounter = 0 # used to track the amount of true statements
        copiedboard = board # used to store a copy of the board
        if string == "": # Base case. If the string is empty, return true
            return True
        check1 = lettercheck.is_in_bounds(self, row - 1, col - 1)  # for the following 8 checks, use the is_in_bounds function to check if the row and column are in bounds
        # for each of the 8 possible letters around the current letter, if any are false, add one to false counter.
        # Else, check if the first letter of string is equal to the letter on that board.
        # If it is, add one to true counter, set the new row and col to the current check conditions, and use copied board to call the remove letter fucntion to store a copied board with the letter removed
        # We will use this new board from now on.
        if check1 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row - 1][col - 1]:
                newrow = row - 1
                newcol = col - 1
                Truecounter += 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        check2 = lettercheck.is_in_bounds(self, row - 1, col)
        if check2 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row - 1][col]:
                newrow = row - 1
                newcol = col
                Truecounter += 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        check3 = lettercheck.is_in_bounds(self, row - 1, col + 1)
        if check3 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row - 1][col + 1]:
                newrow = row - 1
                newcol = col + 1
                Truecounter += 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        check4 = lettercheck.is_in_bounds(self, row, col + 1)
        if check4 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row][col + 1]:
                Truecounter += 1
                newrow = row
                newcol = col + 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        check5 = lettercheck.is_in_bounds(self, row + 1, col + 1)
        if check5 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row + 1][col + 1]:
                newrow = row + 1
                newcol = col + 1
                Truecounter += 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        check6 = lettercheck.is_in_bounds(self, row + 1, col)
        if check6 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row + 1][col]:
                newrow = row + 1
                newcol = col
                Truecounter += 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        check7 = lettercheck.is_in_bounds(self, row + 1, col - 1)
        if check7 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row + 1][col - 1]:
                newrow = row + 1
                newcol = col - 1
                Truecounter += 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        check8 = lettercheck.is_in_bounds(self, row, col - 1)
        if check8 is False:
            Falsecounter += 1
        else:
            if string[0] == board[row][col - 1]:
                newrow = row
                newcol = col - 1
                Truecounter += 1
                copiedboard = BoggleFunctions.remove_letter(board, newrow, newcol)
        if Truecounter == 0:  # if none of the checks were true, return false
            return False
        else: # if any of the checks were true, slice the string and call the function again. Repeat until either truecounter is 0, or the string is empty
            return lettercheck.check_string_starting_at(self, (slicedstring[1:]), copiedboard, newrow, newcol)



        return True # TODO: write helper function to be used in is_valid_guess

    # Students: there is no need to change anything below here
    def play_game(self):
        print("Game board:\n")
        print(self.gameboard)
        print(f"Current score is: {self.score}")
        
        guessedword = input("Guess a word: ").upper()
        # guessedword will be upper case since the letters on the board are upper case
        
        while (guessedword != 'Q'):
            if self.is_valid_guess(guessedword):
                print(f"Correct! You get {self.compute_word_score(guessedword)} points.")
                self.score += self.compute_word_score(guessedword)
                self.words_already_used.append(guessedword.lower())
            print(self.gameboard)
            print(f"Current score: {self.score} Correct words: {self.words_already_used}")
            guessedword = input("Guess a word (type q when finished): ").upper()
        print(f"Done, final score: {self.score}")
        
if __name__ == '__main__': # your program will begin execution here
    game = BoggleGame()
    game.play_game()
