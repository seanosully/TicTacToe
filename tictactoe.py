
# Description: An implementation of the game Tic-Tac-Toe
# with a computer player that uses minimax with or without
# alpha-beta pruning to compute its moves.

from hashlib import new
import sys
import math

# Prints the given board to standard output
def printBoard(board):
    for i in range(len(board)): #rows
        for j in range(len(board[0])-1): #columns
            print("%s," %board[i][j],end="")
        print("%s" %board[i][len(board[0])-1])

# Returns the winner and the evaluation of the
# board given as a parameter, i.e., returns
# 1,'X' or -1,'O' when there is a winner
# 0,'No one' for a tie and 0,'?' otherwise
def TerminalTest(board):
    # Check each row
    for i in range(len(board)):
        if(board[i][0] == board[i][1] and
           board[i][0] == board[i][2]):
            if(board[i][0] == 'X'):
                return 1,'X'
            elif(board[i][0] == 'O'):
                return -1,'O'
    # Check each column
    for j in range(len(board[0])):
        if(board[0][j] == board[1][j] and
           board[0][j] == board[2][j]):
            if(board[0][j] == 'X'):
                return 1,'X'
            elif(board[0][j] == 'O'):
                return -1,'O'

    # Check each diagonal
    if(board[0][0] == board[1][1] and
       board[0][0] == board[2][2]): 
        if (board[0][0] == 'X'):
            return 1,'X'
        elif (board[0][0] == 'O'):
            return -1,'O'

    if(board[0][2] == board[1][1] and
       board[0][2] == board[2][0]):
        if (board[0][2] == 'X'):
            return 1,'X'
        elif (board[0][2] == 'O'):
            return -1,'O'

    for i in range(len(board)):
        for j in range(len(board[0])):
            if (board[i][j] == '-'):
                return 0,'?'

    return 0,'No one'

# Returns the best move for X, the value of that move, and the number of search nodes generated.
def MaxValue(current, prune, alpha, beta):
    global numNodes
    besti = 0
    bestj = 0

    score, winner = TerminalTest(current)

    #Check if board game is over
    if winner != '?': 
        return score, (3, 3), numNodes

    v = -math.inf

    for i in range(3):
        for j in range(3):
            if current[i][j] == '-':
                current[i][j] = 'X'
                numNodes = numNodes + 1
                value, _, _ = MinValue(current, prune, alpha, beta) # Get value of move

                if value > v:
                    v = value
                    besti = i # Best move
                    bestj = j
                current[i][j] = "-" # Undo move
                if prune:
                    if v >= beta:
                        return v, besti, bestj
                    alpha = max(v, alpha)
                
                    
    return v, (besti, bestj), numNodes
    

# Returns the best move for O, the value of that move, and the number of search nodes generated.
def MinValue(current, prune, alpha, beta):
    global numNodes
    besti = 0
    bestj = 0
    score, winner = TerminalTest(current)

    #Check if board game is over
    if winner != '?':
        return score, (3, 3), numNodes

    v = math.inf

    for i in range(3):
         for j in range(3):
            if current[i][j] == '-':
                current[i][j] = 'O'
                numNodes = numNodes + 1
                value, _, _ = MaxValue(current, prune, alpha, beta)
                
                if value < v:
                    v = value
                    besti = i
                    bestj = j
                current[i][j] = "-"

                if prune:
                    if v <= alpha:
                        return v, besti, bestj
                    beta = min(v, beta)
                
    return v, (besti, bestj), numNodes


# Returns the best move for O and the number of search nodes generated.
# board describes the state of the board
# prune is a boolean that indicates if alpha-beta
# pruning should be used.
def MinimaxDecision(board, prune):
    global numNodes
    numNodes = 1
    # makes a copy of the given board to pass to MinValue
    nextBoard = [row[:] for row in board]

    # MinValue returns three values (the nextmove, the minimax value, and nodes gneerated)
    # Can use _ to ignore values
    v, nextMove, numNodes = MinValue(nextBoard, prune, -1*float("inf"), float("inf"))

    # If game not over, play best move
    if nextMove[0] != 3 and nextMove[1] != 3:
        nextBoard[nextMove[0]][nextMove[1]] = 'O'
    return nextBoard, numNodes


# Main program
##########################
def main():
    if len(sys.argv) != 2:
        print('Usage: python3 tictactoe.py [prune|noprune]')
    else:
        cmd = str(sys.argv[1])
        
        if(cmd != "prune" and cmd != "noprune"):
            print('Usage: python3 tictactoe.py [prune|noprune]')
            sys.exit()

        prune = str(sys.argv[1]) == "prune" 

        board = [['-','-','-'],
                 ['-','-','-'],
                 ['-','-','-']]

        winner = '?'
        while(winner is '?'):
            printBoard(board)
            usrMove = str(input('Please enter your move in the format 0,0: '))
            move = (int(usrMove[0]),int(usrMove[2]))
            if(board[move[0]][move[1]] != '-'):
                print("Illegal Move! Please choose an open space.")
                continue
            board[move[0]][move[1]] = 'X'

            board,numNodes = MinimaxDecision(board, prune)
            print(numNodes)

            score,winner = TerminalTest(board)
            if winner != '?':
                break

        printBoard(board)
        print(winner+' wins!')
           
#Executes the main program.
if __name__ == "__main__":
    main()
