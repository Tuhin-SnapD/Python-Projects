"""
Enhanced Word Guess Game (Lingo)

A feature-rich word guessing game with improved feedback,
statistics tracking, and better user experience.
"""

import random
import os
import sys
from typing import List, Set

WORDS_FILE = os.path.join(os.path.dirname(__file__), 'doc', 'words.txt')


def load_words() -> List[str]:
    try:
        with open(WORDS_FILE, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
        # Only 4-letter words with no repeated letters
        return [word for word in data if len(word) == 4 and len(set(word)) == 4]
    except Exception as e:
        print(f"❌ Error loading words: {e}")
        return []


def get_random_word(words: List[str]) -> str:
    return random.choice(words) if words else "game"


def feedback(guess: str, word: str) -> str:
    result = []
    for i, char in enumerate(guess):
        if i < len(word) and char == word[i]:
            result.append(f"[{char}]")
        elif char in word:
            result.append(f"({char})")
        else:
            result.append(char)
    return ''.join(result)


def play_game(words: List[str]):
    word = get_random_word(words)
    attempts = 0
    guessed = False
    print("Welcome to Lingo! Guess the 4-letter word (no repeated letters). Type 'revl' to reveal the word.")
    while not guessed:
        guess = input("Guess the word: ").strip().lower()
        if guess == 'revl':
            print(f"The word was: {word}")
            word = get_random_word(words)
            print("New word selected!")
            continue
        if len(guess) != 4 or len(set(guess)) != 4:
            print("❌ Please enter a 4-letter word with no repeated letters.")
            continue
        attempts += 1
        if guess == word:
            print(f"🎉 Correct! The word was: {word}. Attempts: {attempts}")
            guessed = True
        else:
            print(feedback(guess, word))
    return attempts


def main():
    words = load_words()
    if not words:
        print("No valid words loaded. Exiting.")
        return
    stats = {'games_played': 0, 'total_attempts': 0, 'best': None}
    while True:
        attempts = play_game(words)
        stats['games_played'] += 1
        stats['total_attempts'] += attempts
        if stats['best'] is None or attempts < stats['best']:
            stats['best'] = attempts
        print(f"\n📊 Games played: {stats['games_played']}, Avg attempts: {stats['total_attempts']/stats['games_played']:.2f}, Best: {stats['best']}")
        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing Lingo!")
            break


if __name__ == "__main__":
    main()