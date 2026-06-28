import os
import random

def run_poem_game():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== COLLABORATIVE POEM GENERATOR ===")
    
    player_input = input("Enter player names separated by commas: ")
    players = [name.strip() for name in player_input.split(",") if name.strip()]
    
    if not players:
        print("No players entered. Exiting.")
        return

    remaining_players = list(players)
    poem_lines = []
    
    while remaining_players:
        current_player = random.choice(remaining_players)
        remaining_players.remove(current_player)
        
        print(f"\nTurn: {current_player.upper()}")
        line = input("Write your line and press Enter: ")
        poem_lines.append(line)

if __name__ == "__main__":
    run_poem_game()