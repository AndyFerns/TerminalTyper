import time
from core import WORDS, generate_prompt, acc_calculator, wpm_calculator

def main():
    """
    Main function for core logic
    """
    
    # Prompt generation
    prompt = generate_prompt(WORDS, num_words=10)
    print("\n--- Terminal Typer Test ---")
    print("\nType the following text:")
    print(f"{prompt}")
    print("\nPress ENTER when you are ready to start...\n")
    input()
    
    # Test loop
    start_time = time.time()
    user_input = input("Start typing: ")
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