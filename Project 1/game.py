import sys
import pygame
import threading
import copy
import random

# OFFICIAL BOARD
initial_board = [["x", "x", [], [], [], [], "x", "x"], 
         ["x", [1], [1], [2], [2], [1], [1], "x"],
         [[], [2], [2], [1], [1], [2], [2], []],
         [[], [1], [1], [2], [2], [1], [1], []],
         [[], [2], [2], [1], [1], [2], [2], []],
         [[], [1], [1], [2], [2], [1], [1], []],
         ["x", [2], [2], [1], [1], [2], [2], "x"],
         ["x", "x", [], [], [], [], "x", "x"]
         ]


# BOARD FOR TESTS

# initial_board = [["x", "x", [], [], [], [], "x", "x"], 
#          ["x", [], [], [], [], [], [], "x"],
#          [[], [], [], [], [], [], [], []],
#          [[2], [], [], [], [], [], [], []],
#          [[], [], [], [], [], [], [2,1,1,1,1], []],
#          [[], [], [], [], [], [1], [], []],
#          ["x", [], [], [], [], [], [], "x"],
#          ["x", "x", [], [], [], [], "x", "x"]
#          ]

# button class for the UI menu
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width + 110
        self.height = height + 20
        self.text = text
        self.font = pygame.font.SysFont(None, 50)  

    def draw(self, win, outline=None):
        
        if outline:
            pygame.draw.rect(win, outline, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 0)
        
        pygame.draw.rect(win, self.color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('Tahoma', 36)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x - text.get_width()//2, self.y - text.get_height()//2))

    def isOver(self, pos):
        
        if self.x - self.width // 2 < pos[0] < self.x + self.width // 2:
            if self.y - self.height // 2 < pos[1] < self.y + self.height // 2:
                return True
        return False

# class for the game
class Game:

    def __init__(self):
        self.DISPLAY = pygame.display.set_mode((800, 600))
        self.player = 1
        self.winner = -1
        self.saved1 = 0 #saved pieces player 1
        self.saved2 = 0 #saved pieces player 2
        self.removed1 = 0 #removed pieces player 1
        self.removed2 = 0 #removed pieces player 2
        self.board = initial_board
        self.max_depth = 1

    # function to print the board in the terminal
    def print_board(self):
        for row in self.board:
            print(row)

        if self.player==1:
            print("you have " + str(self.saved1) + " saved pieces to use")
        else:
            print("you have " + str(self.saved2) + " saved pieces to use")

        return 
    
    # function to draw the board in the UI
    def draw_board(self):
        
        GRID_SIZE = 85
        OFFSET = 50  
        
        DISPLAY = pygame.display.set_mode((GRID_SIZE * len(self.board[0]) + OFFSET, GRID_SIZE * len(self.board) + OFFSET))

        
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)

        
        font = pygame.font.SysFont('Arial', 25)

        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            for y in range(len(self.board)):
                for x in range(len(self.board[0])):
                    rect = pygame.Rect(x * GRID_SIZE + OFFSET, y * GRID_SIZE + OFFSET, GRID_SIZE, GRID_SIZE)

                    
                    if x == 0:
                        row_text = font.render(str(y), True, WHITE)
                        text_width, text_height = font.size(str(y))
                        DISPLAY.blit(row_text, ((OFFSET - text_width) // 2, y * GRID_SIZE + OFFSET + (GRID_SIZE - text_height) // 2))
                        pygame.display.update()

                    
                    if y == 0:
                        col_text = font.render(str(x), True, WHITE)
                        text_width, text_height = font.size(str(x))
                        DISPLAY.blit(col_text, (x * GRID_SIZE + OFFSET + (GRID_SIZE - text_width) // 2, (OFFSET - text_height) // 2))
                        pygame.display.update()

                    
                    if self.board[y][x] == "x":
                        pygame.draw.rect(DISPLAY, WHITE, rect)
                    else:
                        pygame.draw.rect(DISPLAY, BLACK, rect)
                        pygame.draw.rect(DISPLAY, WHITE, rect, 1)  

                        
                        for i in range(len(self.board[y][x])):
                            
                            size = GRID_SIZE - i * GRID_SIZE / len(self.board[y][x])
                            radius = size // 2

                            
                            center_x = x * GRID_SIZE + OFFSET + GRID_SIZE // 2
                            center_y = y * GRID_SIZE + OFFSET + GRID_SIZE // 2

                            
                            if self.board[y][x][i] == 1:
                                pygame.draw.circle(DISPLAY, RED, (center_x, center_y), radius)
                                pygame.draw.circle(DISPLAY, BLACK, (center_x, center_y), radius, 1)
                            elif self.board[y][x][i] == 2:
                                pygame.draw.circle(DISPLAY, BLUE, (center_x, center_y), radius)
                                pygame.draw.circle(DISPLAY, BLACK, (center_x, center_y), radius, 1)

            
            pygame.display.update()

    # function to check if the stack is the player's
    def is_players_stack(self, position):

        if position[0] >= 8 or position[1] >= 8:
            return False
        
        if self.board[position[0]][position[1]] == []:
            return False

        
        return self.board[position[0]][position[1]][-1] == self.player

    # function to check if the move is orthogonal and in bounds
    def is_move_orthogonal_and_inbounds(self, source, destination):

        # check if the moves in not outside the board
        if destination[0] >= 8 or destination[1] >= 8 or destination[0]<=0 or destination[1] <=0:
            return False

        # check if it is not a forbidden position
        if self.board[destination[0]][destination[1]] == 'x':
            return False
        
        num = len(self.board[source[0]][source[1]])
        # check if the move has less than or equal pieces 
        if destination[0] == source[0] and destination[1] <= source[1] + num :
            return True
    
        if destination[0] <= source[0] + num and destination[1] == source[1]:
            return True
        

        return False
    
    # function to merge the stacks correctly according to game rules
    def stack_merge(self, source, sourcepos, dest, destpos):

        sourcesize = len(source)
        #distance of the movement
        coordinatedistance = abs(sourcepos[0] - destpos[0]) + abs(sourcepos[1] - destpos[1])
        #when we add a saved piece
        if sourcepos == destpos:
            dest.append(self.player)
        elif sourcesize > coordinatedistance:
            dest = dest + source[-coordinatedistance:]
            source = source[:-coordinatedistance]
        else:
            dest = dest + source
            source = []
        #pieces removed
        temp = dest[:-5]
        # check if we have to save some player's piece and increment the removed pieces of the opponent
        for position in temp:
            if position == self.player:
                if self.player == 1:
                    self.saved1 += 1

                else:
                    self.saved2 += 1
                
            else:
                if self.player == 1:
                    self.removed2 += 1

                else:
                    self.removed1 += 1
        
        #stack in the dest
        dest = dest[-5:]

        return (source,dest)

    # function to move the pieces used both in player and AI
    def move(self, source, dest):
        #the movement is to add a saved piece 
        if source == dest and self.board[source[0]][source[1]] != "x":
            if self.player == 1:
                if self.saved1 > 0:
                    self.saved1 -= 1
                    (a,b) = self.stack_merge([1], source, self.board[dest[0]][dest[1]], dest)
            else:
                if self.saved2 > 0:
                    self.saved2 -= 1
                    (a,b) = self.stack_merge([2], source, self.board[dest[0]][dest[1]], dest)
            
            self.board[dest[0]][dest[1]] = b
            self.player = 3 - self.player
            return True
        #movement of pieces inside the board
        else:
            (a,b) = self.stack_merge(self.board[source[0]][source[1]], source, self.board[dest[0]][dest[1]], dest)

            if self.is_players_stack(source) and self.is_move_orthogonal_and_inbounds(source, dest):
                self.board[dest[0]][dest[1]] = b
                self.board[source[0]][source[1]] = a
                self.player = 3 - self.player
                return True

        return False
    
    # function to check if there is a winner or not
    def player_winner(self):

        player1 = 0
        player2 = 0

        for row in self.board:
            for position in row:
                if (position != []):
                    if position[-1] == 1:
                        player1 += 1
                        if player2 != 0:
                            self.winner = -1
                            return False
                    if position[-1] == 2:
                        player2 += 1
                        if player1 != 0:
                            self.winner = -1
                            return False

        if player1 == 0:
            self.winner = 2
            return 2
        
        if player2 == 0:
            self.winner = 1
            return 1

    # function to check a certain move in a temporary board so that the original board is not affected
    # used in the minimax algorithm to check the best move
    def check_move(self, board, source, dest):
        temp_saved1 = self.saved1
        copy1 = copy.deepcopy(self.saved1) #temporary saved pieces of player 1
        temp_saved2 = self.saved2
        copy2 = copy.deepcopy(self.saved2) # temporary saved pieces of player 2
        #the movement is to add a saved piece
        if source == dest and board[source[0]][source[1]] != "x":
            if self.player == 1:
                if temp_saved1 > 0:
                    temp_saved1 -= 1
                    (a,b) = self.stack_merge([1], source, board[dest[0]][dest[1]], dest)
                    self.saved1 = copy1

            else:
                if temp_saved2 > 0:
                    temp_saved2 -= 1
                    (a,b) = self.stack_merge([2], source, board[dest[0]][dest[1]], dest)
                    self.saved2 = copy2
            
            board[dest[0]][dest[1]] = b
            return board
        
        else:
            (a,b) = self.stack_merge(board[source[0]][source[1]], source, board[dest[0]][dest[1]], dest)
            if self.player == 1:
                self.saved1 = copy1
            else:
                self.saved2 = copy2

            if self.is_players_stack(source) and self.is_move_orthogonal_and_inbounds(source, dest):
                board[dest[0]][dest[1]] = b
                board[source[0]][source[1]] = a
                return board

        return False
    
    # function to evaluate the board and award points to the player
    # used in the minimax algorithm
    def evaluate_board(self, board):
        player_score = 0
        opponent_score = 0
        counter = 0 # counter to help make the AI choose to have two stacks instead of 1 if they make the same points

        for row in board:
            for position in row:
                if position:
                    if position[-1] == self.player: #when the stack is player's
                        counter+=1
                        player_score += 2 * len(position) #number of points is 2 times the stack size
                        if self.player == 1:
                            player_score += self.removed2 * 3
                        else:
                            player_score += self.removed1 * 3
                    elif position[-1] == 3-self.player: # if the stack is opponent's
                        opponent_score += 2 * len(position)
                        if self.player == 1:
                            opponent_score += self.removed1 * 3
                        else:
                            opponent_score += self.removed2 * 3

        final_score = player_score - opponent_score + counter
        return final_score
    
    # function to check all the available moves for the player even using the saved pieces
    def get_avail_moves(self):
        pos = [] # positions of the player's stacks
        savedpos = [] # all positions
        moves = [] #list of possible moves

        for i in range(8):
            for j in range(8):
                if self.is_players_stack((i,j)):
                    pos.append((i,j)) # player's stack
                savedpos.append((i,j)) # all positions 

        for position in pos: # iterate over every player's stack
            new = 1
            length = len(self.board[position[0]][position[1]]) #size of the stack we are evaluating
            while new!=length + 1 : #check all possible moves with that stack
                if (self.is_move_orthogonal_and_inbounds((position[0],position[1]), (position[0],position[1] +new))):
                    moves.append((position, (position[0], position[1] + new )))

                if (self.is_move_orthogonal_and_inbounds((position[0],position[1]), (position[0],position[1] -new))):
                    moves.append((position, (position[0], position[1] - new )))

                if (self.is_move_orthogonal_and_inbounds((position[0],position[1]), (position[0] + new,position[1]))):
                    moves.append((position, (position[0] + new, position[1])))

                if (self.is_move_orthogonal_and_inbounds((position[0],position[1]), (position[0] - new,position[1]))):
                    moves.append((position, (position[0] - new, position[1])))

                new += 1

        #check all possibilities to play a saved piece
        if self.player==1 and self.saved1>0 or self.player==2 and self.saved2>0: #check if the player has saved pieces
            for position in savedpos: # for all positions on the board
                if self.board[position[0]][position[1]] != 'x': #checks if the position is not forbidden
                    moves.append((position, position)) #all possibilities to play a saved piece
                
        return moves
    
    # function to make a random move for the AI
    def make_random_move(self):

        moves = self.get_avail_moves() #get all avail moves

        total = len(moves)

        rand = random.randint(0, total - 1) #choose a random from all availables

        self.move(moves[rand][0], moves[rand][1])

        return         

    # function to make the best move for the AI using the minimax algorithm
    def minimax(self, depth, alpha, beta, is_maximizing_player):
        moves = [] #list to save moves for maximizing
        moves2 = [] # list to save moves for minimizing

        if depth == 0 or self.winner != -1: #if no more depth or winner found
            temp_board = copy.deepcopy(self.board)
            return self.evaluate_board(temp_board), None
        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.get_avail_moves(): #iterate over all possible moves
                temp_board = copy.deepcopy(self.board)
                temp_board = self.check_move(temp_board, move[0], move[1]) #make the move using a temp board, so that the final board is not affected
                self.player_winner()
                eval = self.evaluate_board(temp_board) #get the score of the temp board used to make the move
                if eval == max_eval or self.winner == self.player: #if score is equal than what we already had
                    moves.append(move) #append to the moves
                if eval > max_eval or self.winner == self.player: #if the score is bigger than what we already had
                    moves.clear() #clear the least profitable moves
                    moves.append(move) #append the new move 
                    max_eval = eval #update the score
                alpha = max(alpha, eval)
                if beta <= alpha: #alpha beta cuts
                    break
                _, _ = self.minimax(depth - 1, alpha, beta, False) #call the minimax with less 1 on the depth
            return max_eval, moves
        else:
            min_eval = float('inf')
            for move in self.get_avail_moves():
                temp_board = copy.deepcopy(self.board)
                temp_board = self.check_move(temp_board, move[0], move[1])  
                eval = self.evaluate_board(temp_board)
                if eval==min_eval:
                    moves2.append(move)
                if eval < min_eval:
                    moves2.clear()
                    moves2.append(move)
                    min_eval = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                _, _ = self.minimax(depth - 1, alpha, beta, True)
            return min_eval, moves2

    # function to execute the best move calculated by the minimax algorithm
    def make_best_move(self, max_depth):
        _, moves = self.minimax(max_depth, float('-inf'), float('inf'), True) #call mininimax to get the best moves
        aux = len(moves) #size of the list of the moves to help random choose a valid option
        aux2 = random.randint(0, aux - 1) #choose one move from the list randomly
        if moves is not None:
            self.move(moves[aux2][0], moves[aux2][1]) #apply the move to the index selected 
            self.player_winner() #check if the game is over

