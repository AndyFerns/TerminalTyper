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

def wpm_calculator(prompt_text: str, user_text: str, elapsed_time) -> float:
    """
    Standard calculation for Words Per Minute (WPM)
    """
    #Standardize "words" to 5 characters, including spaces
    num_chars = len(user_text)
    typed_words = num_chars / 5 
    
    # avoid zero division if elapsed time is 0 (edgecase)
    if elapsed_time == 0:
        return 0
    
    minutes = elapsed_time / 60
    wpm = typed_words / minutes
    return wpm
    
def acc_calculator(prompt_text: str, user_text: str) -> float:
    """
    Calculates typing accuracy
    """
    correct = 0
    # iterate through the shorter string (between prompt and user)
    for i in range(min(len(prompt_text), len(user_text))):
        if user_text[i] == prompt_text[i]:
            correct += 1
        
    # Avoid division by 0 (edgecase)
    if len(user_text) == 0:
        return 100.0
    
    accuracy = (correct / len(user_text)) * 100
    return accuracy

