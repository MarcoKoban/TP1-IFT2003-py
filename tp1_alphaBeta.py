import sys
from os import system
import platform

direction_map = {
    "hg": (-1, -1),  # Haut gauche
    "h": (-1, 0),    # Haut
    "hd": (-1, 1),   # Haut droit
    "g": (0, -1),    # Gauche
    "d": (0, 1),     # Droite
    "bg": (1, -1),   # Bas gauche
    "b": (1, 0),     # Bas
    "bd": (1, 1)     # Bas droit
}

def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def createBoard(x, y):
    board = [[0 for _ in range(y)] for _ in range(x)]
    return board

def setMiddle(board, x, y):
    mid_x = x // 2
    mid_y = y // 2
    board[mid_x][mid_y] = 1
    return board

def printBoard(board):
    for row in board:
        print(row)

def checkWhereIsOne(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                return [i, j]
    return None

def endGame(board):
    current_position = checkWhereIsOne(board)
    directions = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (-1, 1),
        (1, -1), (1, 1)
    ]
    
    for direction in directions:
        new_position = [current_position[0] + direction[0], current_position[1] + direction[1]]
        if canMove(board, current_position, new_position):
            return False
    return True

def canWinInOneMove(board):
    """
    Vérifie si l'IA peut poser un mur qui empêche le joueur de bouger en un seul coup.
    Retourne le coup gagnant si trouvé, sinon None.
    """
    player_position = checkWhereIsOne(board)
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    
    for move in getAllPossibleMoves(board):
        board[move[0]][move[1]] = 2
        blocked = True
        for direction in directions:
            new_position = [player_position[0] + direction[0], player_position[1] + direction[1]]
            if canMove(board, player_position, new_position):
                blocked = False
                break
        board[move[0]][move[1]] = 0

        if blocked:
            return move
    
    return None


def evaluateBoard(board):
    player_position = checkWhereIsOne(board)
    # print(f"Player is at position: {player_position}\n")  # Affiche la position du joueur

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    blocked_paths = 0
    for idx, direction in enumerate(directions):
        new_position = [player_position[0] + direction[0], player_position[1] + direction[1]]
        if not canMove(board, player_position, new_position):
            # print(f"Path blocked in direction: {directions[idx]} ({direction})")
            blocked_paths += 1
        else:
            # print(f"Can move in direction: {directions[idx]} ({direction})")
            pass
    
    # print(f"\nTotal blocked paths: {blocked_paths}\n")  # Affiche le nombre total de chemins bloqués
    return blocked_paths

def getAllPossibleMoves(board):
    possible_moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                possible_moves.append((i, j))
    return possible_moves

def minimax(board, depth, alpha, beta, isMaximizingPlayer, node_count=[0]):
    node_count[0] += 1  # Compte chaque appel de Minimax

    if depth == 0 or endGame(board):
        return evaluateBoard(board)
    
    if isMaximizingPlayer:
        best_value = -float('inf')
        for move in getAllPossibleMoves(board):
            # Place un mur temporaire
            board[move[0]][move[1]] = 2
            value = minimax(board, depth - 1, alpha, beta, False)
            board[move[0]][move[1]] = 0
            best_value = max(best_value, value)
            alpha = max(alpha, value) #définit la veleur de alpha
            if beta <= alpha: # si bêta est supérieur à alpha alors il est inutile de continuer car il existe déjà une meilleur option pour max
                break
        print(f"Minimax explored {node_count[0]} nodes at depth {depth}")
        return best_value
    else:
        best_value = float('inf')
        player_position = checkWhereIsOne(board)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for direction in directions:
            new_position = [player_position[0] + direction[0], player_position[1] + direction[1]]
            if canMove(board, player_position, new_position):
                # Déplace le joueur temporairement
                board[player_position[0]][player_position[1]] = 0
                board[new_position[0]][new_position[1]] = 1
                value = minimax(board, depth - 1, alpha, beta, True)
                board[new_position[0]][new_position[1]] = 0
                board[player_position[0]][player_position[1]] = 1
                best_value = min(best_value, value)
                beta = min(beta, value) #définit la valeur de beta
                if beta <= alpha: # si bêta est supérieur à alpha alors il est inutile de continuer car il existe déjà une meilleur option pour max
                    # print("break")
                    break
        print(f"Minimax explored {node_count[0]} nodes at depth {depth}")
        return best_value

def aiMove(board, depth=3):
    winning_move = canWinInOneMove(board)
    if winning_move:
        board[winning_move[0]][winning_move[1]] = 2  # Vérifie si l'IA peut gagner en 1 et place le mur si oui
        return

    best_value = -float('inf')
    best_move = None
    alpha = -float('inf')
    beta = float('inf')
    
    for move in getAllPossibleMoves(board):
        # Place un mur temporaire sur toutes les cases possible
        board[move[0]][move[1]] = 2
        # print(move)
        move_value = minimax(board, depth - 1, alpha, beta, False)
        # print(move_value)
        board[move[0]][move[1]] = 0
        if move_value > best_value:
            best_value = move_value
            best_move = move
        alpha = max(alpha, move_value) # Alpha récupère la plus grande valeur
        if beta <= alpha:
            break
    
    if best_move:
        board[best_move[0]][best_move[1]] = 2  # Place le mur à la meilleure position

def canMove(board, current_position, new_position):
    x_current, y_current = current_position
    x_new, y_new = new_position
    if abs(x_new - x_current) <= 1 and abs(y_new - y_current) <= 1:
        if 0 <= x_new < len(board) and 0 <= y_new < len(board[0]):
            if board[x_new][y_new] == 0:
                return True
    return False

def wallMoove(board):
    """
    FONCTION INUTILE (précédement utilisé pour la partie développement du jeu)
    """
    while True:
        # clean()
        printBoard(board)
        wall_turn = input("Wall Turn! Enter '0' to quit, or coordinates 'x y': ")
        if wall_turn == '0':
            return 0
        try:
            x, y = map(int, wall_turn.split())
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                if board[x][y] == 0:
                    board[x][y] = 2
                    return 1
                else:
                    print("There is already something at this position. Try again.")
            else:
                print("Coordinates out of bounds. Try again.")
        except ValueError:
            print("Invalid input. Please enter coordinates in the format 'x y'.")

def playerMoove(board):
    """
    Gestion tour du joueur
    """
    current_position = checkWhereIsOne(board)
    try:
        player_turn = input("Show me your moves! Enter '0' to quit, coordinates 'x y', or direction (e.g., hg, bd): ")
        if player_turn == '0':
            return 0
        if player_turn in direction_map:
            direction = direction_map[player_turn]
            new_position = [current_position[0] + direction[0], current_position[1] + direction[1]]
            if canMove(board, current_position, new_position):
                return new_position
            else:
                print("Invalid move. You cannot move in that direction.")
                return 1
        else:
            try:
                x, y = map(int, player_turn.split())
                return [x, y]
            except ValueError:
                print("Invalid input. Please enter coordinates in the format 'x y' or a direction like 'hg'.")
                return 1
    except (EOFError, KeyboardInterrupt):
        print('Bye')
        exit()

def loopGame(board):
    """
    Main Loop du jeu
    """
    while True:
        # clean()
        printBoard(board)
        if endGame(board):
            print("Game Over! You are trapped!")
            break
        current_position = checkWhereIsOne(board)
        player_move = playerMoove(board)
        if player_move == 0:
            print("Game Over!")
            break
        elif isinstance(player_move, list):
            if canMove(board, current_position, player_move):
                board[current_position[0]][current_position[1]] = 0
                board[player_move[0]][player_move[1]] = 1 #effectue le coup du joueur
                aiMove(board)
            else:
                print("Invalid move. You can only move one square in any direction.")
        else:
            continue

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <x_size> <y_size>")
        return
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    board = createBoard(x, y)
    board = setMiddle(board, x, y)
    loopGame(board)

if __name__ == "__main__":
    main()
