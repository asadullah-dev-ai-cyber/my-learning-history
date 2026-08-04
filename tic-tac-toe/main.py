import os
import random


def clear_screen():
    """Clears the terminal console screen."""
    os.system("cls" if os.name == "nt" else "clear")


class Board:
    def __init__(self):
        # 1-9 mapping directly to grid positions
        self.board_dic = {
            1: " ", 2: " ", 3: " ",
            4: " ", 5: " ", 6: " ",
            7: " ", 8: " ", 9: " "
        }

    def display_board(self):
        """Renders the current state of the board in the console."""
        print(f"\n {self.board_dic[1]} | {self.board_dic[2]} | {self.board_dic[3]} ")
        print("-----------")
        print(f" {self.board_dic[4]} | {self.board_dic[5]} | {self.board_dic[6]} ")
        print("-----------")
        print(f" {self.board_dic[7]} | {self.board_dic[8]} | {self.board_dic[9]} \n")

    def update_board(self, position, mark):
        """Updates board if spot is open. Returns True on success, False if taken."""
        if self.board_dic[position] == " ":
            self.board_dic[position] = mark
            return True
        return False

    def check_win(self, mark):
        """Checks all 8 horizontal, vertical, and diagonal win combinations."""
        win_combinations = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Horizontal Rows
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Vertical Columns
            (1, 5, 9), (3, 5, 7)              # Diagonals
        ]

        for combo in win_combinations:
            if (self.board_dic[combo[0]] == mark and
                    self.board_dic[combo[1]] == mark and
                    self.board_dic[combo[2]] == mark):
                return True
        return False

    def is_full(self):
        """Returns True if no empty spaces remain on the board."""
        return " " not in self.board_dic.values()


def get_ai_move(board):
    """Smart AI logic: Wins if possible, blocks human win, or chooses randomly."""
    available_spots = [key for key, val in board.board_dic.items() if val == " "]

    # 1. Winning Move Check
    for spot in available_spots:
        board.board_dic[spot] = "O"
        if board.check_win("O"):
            board.board_dic[spot] = " "  # Undo test move
            return spot
        board.board_dic[spot] = " "

    # 2. Block Opponent Check
    for spot in available_spots:
        board.board_dic[spot] = "X"
        if board.check_win("X"):
            board.board_dic[spot] = " "  # Undo test move
            return spot
        board.board_dic[spot] = " "

    # 3. Random Choice
    return random.choice(available_spots)


# --- GAME CONTROLLER ---
scores = {"X": 0, "O": 0, "Draws": 0}

clear_screen()
print("=== WELCOME TO CLI TIC TAC TOE ===")
print("1. Single Player (vs Computer AI)")
print("2. 2 Players")
game_mode = input("Choose mode (1 or 2): ").strip()

while True:  # Outer Replay Loop
    board = Board()
    current_player = "X"
    game_is_on = True

    while game_is_on:  # Inner Turn Loop
        clear_screen()
        mode_label = "vs Computer" if game_mode == "1" else "2 Players"
        print(f"=== CLI TIC TAC TOE ({mode_label}) ===")
        print(f"SCOREBOARD | Player X: {scores['X']} | Player O: {scores['O']} | Draws: {scores['Draws']}")
        board.display_board()

        # Handle Turn based on Game Mode
        if game_mode == "1" and current_player == "O":
            print("🤖 Computer (O) is thinking...")
            choice = get_ai_move(board)
        else:
            # Human Input with validation
            try:
                choice = int(input(f"Player {current_player}, choose a position (1-9): "))
            except ValueError:
                input("Invalid input! Please enter a number 1-9. (Press Enter to try again)")
                continue

            if choice < 1 or choice > 9:
                input("Invalid position! Choice must be 1-9. (Press Enter to try again)")
                continue

        # Execute Move
        move_was_successful = board.update_board(choice, current_player)

        if not move_was_successful:
            input("That spot is taken! (Press Enter to try again)")
            continue

        # Win / Draw / Switch Evaluation
        if board.check_win(current_player):
            clear_screen()
            print(f"SCOREBOARD | Player X: {scores['X']} | Player O: {scores['O']} | Draws: {scores['Draws']}")
            board.display_board()
            winner_text = "Computer AI" if (game_mode == "1" and current_player == "O") else f"Player {current_player}"
            print(f"🎉 {winner_text} wins!")
            scores[current_player] += 1
            game_is_on = False

        elif board.is_full():
            clear_screen()
            print(f"SCOREBOARD | Player X: {scores['X']} | Player O: {scores['O']} | Draws: {scores['Draws']}")
            board.display_board()
            print("🤝 It's a draw! No moves left.")
            scores["Draws"] += 1
            game_is_on = False

        else:
            current_player = "O" if current_player == "X" else "X"

    # Replay Prompt
    play_again = input("\nDo you want to play another round? (y/n): ").lower().strip()
    if play_again != "y":
        print("\nThanks for playing! Final Scores:")
        print(f"Player X: {scores['X']} | Player O: {scores['O']} | Draws: {scores['Draws']}")
        break