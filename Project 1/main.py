import game  
import sys
import pygame
import threading
import copy
import random 


# Function to show the rules of the game
def show_rules():
    rules_running = True
    back_button = game.Button((0, 255, 0), 145, screen_height - 100, 80, 40, 'Back')

    rules_text = [
        "2 player game on a 6×6 board with 1×4 extensions on each side.",
        "Stacks may move as many spaces as there are pieces in the stack.",
        "Players can move a stack orthogonally, and if their piece is on top of the stack.",
        "The game ends when a player doesn’t have any piece on top of any stack.",
        "Each stack, of 5 pieces maximum, when landing on another stack, merges with it. If the new stack contains more than five pieces, then pieces are removed from the bottom to bring it down to five. If a player's own piece is removed, they are kept outside the board to use later. If the piece is of the opponent, they are removed.",
        "A player doesn’t need to move the complete stack. But if he doesn’t, he must only take as many pieces of the same as positions moved."
    ]

    font = pygame.font.SysFont('Tahoma', 20)
    max_width = screen_width - 100  

    split_rules_text = []
    for line in rules_text:
        words = line.split(' ')
        split_line = ''
        for word in words:
            test_line = split_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                split_line = test_line
            else:
                split_rules_text.append(split_line)
                split_line = word + ' '
        split_rules_text.append(split_line)

    while rules_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pygame.mouse.get_pos()):
                    rules_running = False

        screen.fill((0, 0, 0))
        for i, line in enumerate(split_rules_text):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, 50 + i * 30))
        back_button.draw(g.DISPLAY)
        pygame.display.update()

# Function to convert a string to a tuple of integers 
# used to convert the input of the player to the coordinates of the board        
def string_to_tuple(s):
    return tuple(map(int, s))

# Function to run the game loop    
def pygame_loop():
    global game_running  
    while game_running:  
        
        g.draw_board()  

        
        pygame.display.update()

g = game.Game()

t = 0
s = 0

pygame.init()
pygame.display.set_caption('Focus')

screen = pygame.display.set_mode((800, 600))

screen.fill((0, 0, 0))
pygame.display.flip()

screen_width, screen_height = screen.get_size()  

# Create buttons for the main menu
start_button = game.Button((0, 255, 0), screen_width // 2, screen_height // 2 - 120, 100, 50, 'Start Game')
rules_button = game.Button((0, 255, 0), screen_width // 2, screen_height // 2, 100, 50, 'Rules')
quit_button = game.Button((0, 255, 0), screen_width // 2, screen_height // 2 + 120, 100, 50, 'Quit')

game_started = False
game_running = True  

# Function to run the game
def run_game():
    game_running = True
    game_started = False

    quit_game = False

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(pygame.mouse.get_pos()):
                    game_started = True
                elif rules_button.isOver(pygame.mouse.get_pos()):
                    show_rules()
                elif quit_button.isOver(pygame.mouse.get_pos()):
                    game_running = False
                    pygame.quit()
                    sys.exit()


        if not game_started:
            screen.fill((0, 0, 0))
            start_button.draw(g.DISPLAY)
            rules_button.draw(g.DISPLAY)
            quit_button.draw(g.DISPLAY)
            pygame.display.update()  
        else:
            drawing_thread = threading.Thread(target=g.draw_board).start()

            print("Welcome to the Focus game, a game of strategy and skill")
            print("If you want to forfeit the game, press Q when asked for a move")
            print("What type of game do you want to play? (1: Player vs Player, 2: Player vs AI, 3: Dumb_AI vs Smart_AI, 4: Smart_AI vs Smarter_AI)")
            game_type = (input())
            while not (game_type=="1" or game_type=="2" or game_type=="3" or game_type=="4"):
                print("Please input a valid game type")
                print("What type of game do you want to play? (1: Player vs Player, 2: Player vs AI, 3: Dumb_AI vs Smart_AI, 4: Smart_AI vs Smarter_AI)")
                game_type = (input())
            if game_type == "2":
                print("What difficulty do you want to play? (1: Easy, 2: Medium, 3: Hard)")
                difficulty = (input())
                while not (difficulty == "1" or difficulty == "2" or difficulty == "3"):
                    print("Invalid input. Please input a valid difficulty.")
                    difficulty = (input())

            # Player vs Player
            if game_type == "1":
                while g.winner == -1:
                    g.print_board() 
                    print(f"Player {g.player} turn!")
                    if((g.player == 1 and g.saved1 > 0) or (g.player == 2 and g.saved2 > 0)):
                        print("Do you want to use a saved piece? (y/n)")
                        t = input()
                        if t.upper() == 'Q':
                            g.winner = 1 if g.player == 2 else 2
                            print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                            game_running = False
                            break
                        elif t.upper() == 'Y':
                            print("To what position do you want to add the saved piece? Write the two coordenates without spaces, for example: 11")
                            s = input()
                            if s.upper() == 'Q':
                                g.winner = 1 if g.player == 2 else 2
                                print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                                game_running = False
                                break
                            if len(s) != 2 or not s.isdigit():
                                print("Invalid input. Please enter exactly two numerical characters.")
                                continue
                            r = string_to_tuple(s)
                            if g.board[r[0]][r[1]] == 'x':
                                print("You can't add a saved piece to that position")
                                continue
                            if g.player == 1:
                                g.board[r[0]][r[1]].append(1)
                                g.saved1 -= 1
                                g.player = 3 - g.player
                            elif g.player == 2:
                                g.board[r[0]][r[1]].append(2)
                                g.saved2 -= 1
                                g.player = 3 - g.player
                            else:
                                print("You don't have that amount of saved pieces")
                                continue
                            g.print_board()
                            g.player_winner()
                        elif t.upper() == 'N':
                            print("Insert your move with the coordenates of the source and destination with no spaces, for example: 11 12")
                            print("Source:")
                            a = input()
                            if a.upper() == 'Q':
                                g.winner = 1 if g.player == 2 else 2
                                print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                                game_running = False
                                break
                            if len(a) != 2 or not a.isdigit():
                                print("Invalid input. Please enter exactly two numerical characters.")
                                continue
                            b = string_to_tuple(a)
                            if(not g.is_players_stack(b)):
                                print("You can't move a stack that is not yours")
                                continue
                            print("Destination:")
                            c = input()
                            if c.upper() == 'Q':
                                g.winner = 1 if g.player == 2 else 2
                                print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                                game_running = False
                                break
                            if len(c) != 2 or not c.isdigit():
                                print("Invalid input. Please enter exactly two numerical characters.")
                                continue
                            d = string_to_tuple(c)
                            if(not g.is_move_orthogonal_and_inbounds(b, d)):
                                print("You can't move to that position, try again!")
                                continue
                            g.move(b, d)
                    else:
                        print("Insert your move with the coordenates of the source and destination with no spaces, for example: 11 12")
                        print("Source:")
                        a = input()
                        if a.upper() == 'Q':
                            g.winner = 1 if g.player == 2 else 2
                            print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                            game_running = False
                            break
                        if len(a) != 2 or not a.isdigit():
                            print("Invalid input. Please enter exactly two numerical characters.")
                            continue
                        b = string_to_tuple(a)
                        if(not g.is_players_stack(b)):
                            print("You can't move a stack that is not yours")
                            continue
                        print("Destination:")
                        c = input()
                        if c.upper() == 'Q':
                            g.winner = 1 if g.player == 2 else 2
                            print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                            game_running = False
                            break
                        if len(c) != 2 or not c.isdigit():
                            print("Invalid input. Please enter exactly two numerical characters.")
                            continue
                        d = string_to_tuple(c)
                        if(not g.is_move_orthogonal_and_inbounds(b, d)):
                            print("You can't move to that position, try again!")
                            continue
                        g.move(b, d)
                if a.upper() != 'Q' and c.upper() != 'Q' and s.upper() != 'Q' and t.upper() != 'Q':
                    g.print_board()
                    g.player_winner()

                else:
                    quit_game = True
                
            # Player vs AI
            elif game_type == "2":
                while g.winner == -1:
                    g.print_board()
                    print(f"Player {g.player} turn!")
                    if(g.player == 1 and g.saved1 > 0):
                        print("Do you want to use a saved piece? (y/n)")
                        t = input()
                        if t.upper() == 'Q':
                            g.winner = 1 if g.player == 2 else 2
                            print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                            game_running = False
                            break
                        elif t.upper() == 'Y':
                            print("To what position do you want to add the saved piece? Write the two coordenates without spaces, for example: 11")
                            s = input()
                            if s.upper() == 'Q':
                                g.winner = 1 if g.player == 2 else 2
                                print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                                game_running = False
                                break
                            if len(s) != 2 or not s.isdigit():
                                print("Invalid input. Please enter exactly two numerical characters.")
                                continue
                            r = string_to_tuple(s)
                            if g.board[r[0]][r[1]] == 'x':
                                print("You can't add a saved piece to that position")
                                continue
                            if g.player == 1:
                                g.board[r[0]][r[1]].append(1)
                                g.saved1 -= 1
                                g.player = 3 - g.player
                            g.print_board()
                            g.player_winner()
                        elif t.upper() == 'N':
                            print("Insert your move with the coordenates of the source and destination with no spaces, for example: 11 12")
                            print("Source:")
                            a = input()
                            if a.upper() == 'Q':
                                g.winner = 1 if g.player == 2 else 2
                                print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                                game_running = False
                                break
                            if len(a) != 2 or not a.isdigit():
                                print("Invalid input. Please enter exactly two numerical characters.")
                                continue
                            b = string_to_tuple(a)
                            if(not g.is_players_stack(b)):
                                print("You can't move a stack that is not yours")
                                continue
                            print("Destination:")
                            c = input()
                            if c.upper() == 'Q':
                                g.winner = 1 if g.player == 2 else 2
                                print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                                game_running = False
                                break
                            if len(c) != 2 or not c.isdigit():
                                print("Invalid input. Please enter exactly two numerical characters.")
                                continue
                            d = string_to_tuple(c)
                            if(not g.is_move_orthogonal_and_inbounds(b, d)):
                                print("You can't move to that position, try again!")
                                continue
                            g.move(b, d)
                    elif g.player == 1:
                        print("Insert your move with the coordenates of the source and destination with no spaces, for example: 11 12")
                        print("Source:")
                        a = input()
                        if a.upper() == 'Q':
                            g.winner = 1 if g.player == 2 else 2
                            print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                            game_running = False
                            break
                        if len(a) != 2 or not a.isdigit():
                            print("Invalid input. Please enter exactly two numerical characters.")
                            continue
                        b = string_to_tuple(a)
                        if(not g.is_players_stack(b)):
                            print("You can't move a stack that is not yours")
                            continue
                        print("Destination:")
                        c = input()
                        if c.upper() == 'Q':
                            g.winner = 1 if g.player == 2 else 2
                            print(f"Player {g.winner} is the winner! Player {g.player} has forfeited the game.")
                            game_running = False
                            break
                        if len(c) != 2 or not c.isdigit():
                            print("Invalid input. Please enter exactly two numerical characters.")
                            continue
                        d = string_to_tuple(c)
                        if(not g.is_move_orthogonal_and_inbounds(b, d)):
                            print("You can't move to that position, try again!")
                            continue
                        g.move(b, d)

                    else:
                        if difficulty == "1":
                            g.make_random_move()
                        elif difficulty == "2":
                            g.make_best_move(3)
                        elif difficulty == "3":
                            g.make_best_move(8)

                if a.upper() != 'Q' and c.upper() != 'Q' and s.upper() != 'Q' and t.upper() != 'Q':
                    g.print_board()
                    g.player_winner()

                else:
                    quit_game = True

            # Dumb_AI vs Smart_AI
            elif game_type == "3":
                g.print_board()
                while g.winner == -1: 
                    print(f"Player {g.player} turn!")
                    
                    if g.player == 1:
                        g.make_random_move()
                    else:
                        g.make_best_move(1)

            # Smart_AI vs Smarter_AI
            elif game_type == "4":
                g.print_board()
                while g.winner == -1: 
                    print(f"Player {g.player} turn!")
                    
                    if g.player == 1:
                        g.make_best_move(3)
                    else:
                        g.make_best_move(8)

            # Check if the game has a winner
            if (g.winner != -1 ) and quit_game == False:
                print(f"Player {g.winner} wins the game")
                game_running = False
                break


run_game()