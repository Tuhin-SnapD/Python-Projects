"""
Enhanced Tic Tac Toe Game

A feature-rich implementation with AI difficulty levels,
statistics tracking, and improved gameplay mechanics.
"""

import random
import sys
from typing import List, Optional
from enum import Enum


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


def print_board(board: List[str]):
    print()
    print(f" {board[7]} | {board[8]} | {board[9]}")
    print("-----------")
    print(f" {board[4]} | {board[5]} | {board[6]}")
    print("-----------")
    print(f" {board[1]} | {board[2]} | {board[3]}")
    print()


def input_player_letter() -> List[str]:
    letter = ''
    while letter not in ['X', 'O']:
        letter = input('Do you want to be X or O? ').upper()
    return ['X', 'O'] if letter == 'X' else ['O', 'X']


def who_goes_first() -> str:
    return 'computer' if random.randint(0, 1) == 0 else 'player'


def play_again() -> bool:
    return input('Do you want to play again? (yes or no) ').lower().startswith('y')


def make_move(board: List[str], letter: str, move: int):
    board[move] = letter


def is_winner(bo: List[str], le: str) -> bool:
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[9] == le and bo[5] == le and bo[1] == le))


def get_board_copy(board: List[str]) -> List[str]:
    return board[:]


def is_space_free(board: List[str], move: int) -> bool:
    return board[move] == ' '


def get_player_move(board: List[str]) -> int:
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not is_space_free(board, int(move)):
        move = input('What is your next move? (1-9) ')
    return int(move)


def choose_random_move_from_list(board: List[str], moves_list: List[int]) -> Optional[int]:
    possible_moves = [i for i in moves_list if is_space_free(board, i)]
    return random.choice(possible_moves) if possible_moves else None


def get_computer_move(board: List[str], computer_letter: str, difficulty: Difficulty) -> int:
    player_letter = 'O' if computer_letter == 'X' else 'X'

    # HARD: Minimax algorithm
    if difficulty == Difficulty.HARD:
        def minimax(board, depth, is_maximizing):
            if is_winner(board, computer_letter):
                return 10 - depth
            if is_winner(board, player_letter):
                return depth - 10
            if is_board_full(board):
                return 0
            if is_maximizing:
                best_score = -float('inf')
                for i in range(1, 10):
                    if is_space_free(board, i):
                        board[i] = computer_letter
                        score = minimax(board, depth + 1, False)
                        board[i] = ' '
                        best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for i in range(1, 10):
                    if is_space_free(board, i):
                        board[i] = player_letter
                        score = minimax(board, depth + 1, True)
                        board[i] = ' '
                        best_score = min(score, best_score)
                return best_score
        best_score = -float('inf')
        best_move = None
        for i in range(1, 10):
            if is_space_free(board, i):
                board[i] = computer_letter
                score = minimax(board, 0, False)
                board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    # MEDIUM: Block player win, else random
    if difficulty == Difficulty.MEDIUM:
        for i in range(1, 10):
            copy = get_board_copy(board)
            if is_space_free(copy, i):
                make_move(copy, computer_letter, i)
                if is_winner(copy, computer_letter):
                    return i
        for i in range(1, 10):
            copy = get_board_copy(board)
            if is_space_free(copy, i):
                make_move(copy, player_letter, i)
                if is_winner(copy, player_letter):
                    return i
        move = choose_random_move_from_list(board, [1, 3, 7, 9])
        if move:
            return move
        if is_space_free(board, 5):
            return 5
        return choose_random_move_from_list(board, [2, 4, 6, 8])

    # EASY: Random move
    return choose_random_move_from_list(board, list(range(1, 10)))


def is_board_full(board: List[str]) -> bool:
    return all(space != ' ' for space in board[1:])


def print_stats(stats):
    print("\n📊 GAME STATISTICS")
    print("=" * 30)
    print(f"Games played: {stats['games_played']}")
    print(f"Player wins: {stats['player_wins']}")
    print(f"Computer wins: {stats['computer_wins']}")
    print(f"Ties: {stats['ties']}")
    print("=" * 30)


def main():
    print('Welcome to Enhanced Tic Tac Toe!')
    stats = {'games_played': 0, 'player_wins': 0, 'computer_wins': 0, 'ties': 0}
    difficulty = Difficulty.MEDIUM
    
    while True:
        the_board = [' '] * 10
        player_letter, computer_letter = input_player_letter()
        
        # Difficulty selection
        print("\nSelect AI difficulty:")
        print("1. Easy\n2. Medium\n3. Hard")
        diff_choice = input("Enter difficulty (1-3, default 2): ").strip()
        if diff_choice == '1':
            difficulty = Difficulty.EASY
        elif diff_choice == '3':
            difficulty = Difficulty.HARD
        else:
            difficulty = Difficulty.MEDIUM
        
        turn = who_goes_first()
        print('The ' + turn + ' will go first.')
        game_is_playing = True
        
        while game_is_playing:
            if turn == 'player':
                print_board(the_board)
                move = get_player_move(the_board)
                make_move(the_board, player_letter, move)
                if is_winner(the_board, player_letter):
                    print_board(the_board)
                    print('Hooray! You have won the game!')
                    stats['player_wins'] += 1
                    game_is_playing = False
                elif is_board_full(the_board):
                    print_board(the_board)
                    print('The game is a tie!')
                    stats['ties'] += 1
                    break
                else:
                    turn = 'computer'
            else:
                move = get_computer_move(the_board, computer_letter, difficulty)
                make_move(the_board, computer_letter, move)
                if is_winner(the_board, computer_letter):
                    print_board(the_board)
                    print('The computer has beaten you! You lose.')
                    stats['computer_wins'] += 1
                    game_is_playing = False
                elif is_board_full(the_board):
                    print_board(the_board)
                    print('The game is a tie!')
                    stats['ties'] += 1
                    break
                else:
                    turn = 'player'
        stats['games_played'] += 1
        print_stats(stats)
        if not play_again():
            break


if __name__ == "__main__":
    main()