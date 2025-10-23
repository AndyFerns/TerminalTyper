import time
from core import WORDS, generate_prompt, acc_calculator, wpm_calculator

def countdown():
    """
    Displays a 3-second countdown timer.
    """
    input("\nPress Enter when you are ready to start...")
    
    for i in range(3, 0, -1):
        print(f"\rStarting in {i}...", end="", flush=True)
        time.sleep(1) # Wait for one second
        
    print("\rSTART!\t")

def main():
    """
    Main function for core logic
    """
    
    # Prompt generation
    prompt = generate_prompt(WORDS, num_words=10)
    print("\n--- Terminal Typer Test ---")
    print("\nType the following text:")
    print(f"{prompt}")
    
    # add countdown before test start
    countdown()
    
    # Test loop
    start_time = time.time()
    user_input = input("Start typing: \n")
    end_time = time.time()
    
    # Result calc
    elapsed_time = end_time - start_time
    wpm = wpm_calculator(prompt, user_input, elapsed_time)
    acc = acc_calculator(prompt, user_input)
    
    # Result display
    print("\n--- Results ---")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"Your WPM: {wpm:.2f} wpm")
    print(f"Accuracy: {acc:.2f}%")
    
if __name__ == '__main__':
    main()