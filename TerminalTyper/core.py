import random
import time
from pathlib import Path

WORD_LIST_PATH = Path(__file__).parent / "words.txt"

def load_words() -> list[str]:
    """
    Loads a list of words from the words.txt file
    """
    with open(WORD_LIST_PATH, "r") as f:
        return f.read().splitlines()
    
def generate_prompt(words_list: list[str], num_words: int = 20) -> str:
    """
    Generates a random prompt from the word list
    """
    typewords = random.choices(words_list, k=num_words)
    return " ".join(typewords)


# Load the words into a global constant so the file only has to be read once
WORDS = load_words()