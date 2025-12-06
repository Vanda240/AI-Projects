import random
import time
import tkinter as tk
from tkinter import simpledialog
from collections import defaultdict
from tabulate import tabulate


class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.cards = []
        self.known_cards = set()
        self.active = True
        self.private_clue_sheet = defaultdict(lambda: "Unknown")  # Keeps track of suspects, weapons, and rooms
        self.refutation_history = []
        self.previous_suggestions = set()  # Track unique suggestions
        self.suggestion_counts = {"suspects": defaultdict(int), "weapons": defaultdict(int), "rooms": defaultdict(int)}

    def add_known_card(self, card):
       
        self.known_cards.add(card)
        self.private_clue_sheet[card] = "Seen"

    def get_matching_cards(self, suggestion):
        return [card for card in suggestion if card.lower() in (c.lower() for c in self.cards)]

    def update_clue_sheet(self, suggestion, refuted_card=None):
        """Update the private clue sheet dynamically."""
        for card in suggestion:
            
            if card not in self.known_cards and card != refuted_card:
                self.private_clue_sheet[card] = "Maybe in Envelope"
    
    def get_suggestion(self, suspects, weapons, rooms, global_suggestion_counts):
        """Generate a suggestion using rule-based deductions with randomness."""
        unknown_suspects = [s for s in suspects if s not in self.known_cards]
        unknown_weapons = [w for w in weapons if w not in self.known_cards]
        unknown_rooms = [r for r in rooms if r not in self.known_cards]

        # Generate all possible combinations
        all_combinations = [
           (suspect, weapon, room)
           for suspect in (unknown_suspects or suspects)
           for weapon in (unknown_weapons or weapons)
           for room in (unknown_rooms or rooms)
        ]

        # Filter out previously made suggestions
        valid_combinations = [combo for combo in all_combinations if combo not in self.previous_suggestions]

        if not valid_combinations:
           # If no new combinations are left, allow repeats
           valid_combinations = all_combinations

        # Choose a random combination and save it
        suggestion = random.choice(valid_combinations)
        self.previous_suggestions.add(suggestion)

        # Increment suggestion counts
        self.suggestion_counts["suspects"][suggestion[0]] += 1
        self.suggestion_counts["weapons"][suggestion[1]] += 1
        self.suggestion_counts["rooms"][suggestion[2]] += 1

        # Increment global counts for the game
        global_suggestion_counts["suspects"][suggestion[0]] += 1
        global_suggestion_counts["weapons"][suggestion[1]] += 1
        global_suggestion_counts["rooms"][suggestion[2]] += 1

        return suggestion

    def deduce_solution(self, suspects, weapons, rooms):
        """Try to deduce the solution based on known cards."""
        unknown_suspects = [s for s in suspects if s not in self.known_cards]
        unknown_weapons = [w for w in weapons if w not in self.known_cards]
        unknown_rooms = [r for r in rooms if r not in self.known_cards]

        # If only one option is left for each category, deduce the solution
        suspect = unknown_suspects[0] if len(unknown_suspects) == 1 else None
        weapon = unknown_weapons[0] if len(unknown_weapons) == 1 else None
        room = unknown_rooms[0] if len(unknown_rooms) == 1 else None

        # Return the deduced solution if it's complete
        if suspect and weapon and room:
            return {"suspect": suspect, "weapon": weapon, "room": room}
        return None

class CluedoGame:
    def __init__(self, player_names, suspects, weapons, rooms):
        self.suspects = suspects
        self.weapons = weapons
        self.rooms = rooms
        self.solution = {
            "suspect": random.choice(suspects),
            "weapon": random.choice(weapons),
            "room": random.choice(rooms)
        }
        self.players = []
        self.current_turn = 0

        # Global counts for all suggestions
        self.global_suggestion_counts = {
            "suspects": defaultdict(int),
            "weapons": defaultdict(int),
            "rooms": defaultdict(int)
        }

        # Dynamically set up players
        self.setup_players(player_names)

        # Assign cards after players are created
        self.assign_cards()

    def setup_players(self, player_names):
        """Dynamically ask how many players will participate and create them."""
        root = tk.Tk()
        root.withdraw()
        num_players = simpledialog.askinteger("Player Setup", "Enter the number of players (3-6):", minvalue=3, maxvalue=6)
        root.destroy()

        if num_players > len(player_names):
            raise ValueError("Not enough player names available for the selected number of players!")

        for i in range(num_players):
            if i == 0:
                # First player is always human
                self.players.append(Player(player_names[i], is_human=True))
            else:
                # Remaining players are AI
                self.players.append(Player(player_names[i], is_human=False))

    def assign_cards(self):
        """Distribute cards to players after setting aside the solution."""
        remaining_cards = (
            [s for s in self.suspects if s != self.solution["suspect"]] +
            [w for w in self.weapons if w != self.solution["weapon"]] +
            [r for r in self.rooms if r != self.solution["room"]]
        )
        random.shuffle(remaining_cards)
        for i, card in enumerate(remaining_cards):
            self.players[i % len(self.players)].cards.append(card)
            self.players[i % len(self.players)].add_known_card(card)
        
    def refute_suggestion(self, suggestion, suggesting_player):
        """Find a player to refute the suggestion and return the refuted card."""
        for player in self.players:
            
            if player == suggesting_player:
                continue
            matching_cards = player.get_matching_cards(suggestion)
            if matching_cards:
                refuted_card = random.choice(matching_cards)
                suggesting_player.add_known_card(refuted_card)
                suggesting_player.update_clue_sheet(suggestion, refuted_card)

                if suggesting_player.is_human:
                   
                   print(f"{player.name} was refuted: {refuted_card}.")
                
                return player.name, refuted_card
        
        return None, None

    def get_selection(self, options, prompt):
        
            """Show a dropdown menu for the manual player to select an option."""
            root = tk.Tk()
            root.title(prompt)

            # Set a larger window size
            root.geometry("400x300")  # Width x Height in pixels

            # Variable to store the selected option
            selected_option = tk.StringVar(root)
            selected_option.set(options[0])  # Default to the first option

            # Create a larger label
            tk.Label(root, text=prompt, font=("Helvetica", 14), wraplength=380).pack(pady=10)

            # Create dropdown menu
            
            dropdown = tk.OptionMenu(root, selected_option, *options)
            dropdown.config(font=("Helvetica", 12), width=20)  # Adjust font and width
            dropdown.pack(pady=20)

            # Add a button to confirm the selection
            def confirm_selection():
                root.quit()
                root.destroy()

            tk.Button(root, text="OK", font=("Helvetica", 12), command=confirm_selection, width=10).pack(pady=10)

            # Run the Tkinter loop
            root.mainloop()

            # Return the selected option
            return selected_option.get()

    def handle_turn(self, player):
        """Handle a player's turn."""
        print("\n" + "-" * 30)
        #print(f"{player.name}'s turn!")


        if not player.active:
            print(f"{player.name} is eliminated and skips their turn.")
            return

        if player.is_human:
            self.manual_turn(player)
        else:
            self.ai_turn(player)
              
    def display_global_suggestion_counts(self):
        """Display the total counts of all suspects, weapons, and rooms suggested so far."""
        print("\n--- Global Suggestion Counts ---")
        print("Suspects:")
        for suspect, count in self.global_suggestion_counts["suspects"].items():
            print(f"  {suspect}: {count} times")

        print("Weapons:")
        for weapon, count in self.global_suggestion_counts["weapons"].items():
            print(f"  {weapon}: {count} times")

        print("Rooms:")
        for room, count in self.global_suggestion_counts["rooms"].items():
            print(f"  {room}: {count} times")

    def manual_turn(self, player):
        """Handle the manual player's turn."""
        print(f"Your cards: {', '.join(player.cards)}")
         
        # Dynamically filter out seen cards and cards in hand from options
        suspects = [s for s in self.suspects if player.private_clue_sheet[s] in ["Maybe in Envelope", "Unknown"]]
        weapons = [w for w in self.weapons if player.private_clue_sheet[w] in ["Maybe in Envelope", "Unknown"]]
        rooms = [r for r in self.rooms if player.private_clue_sheet[r] in ["Maybe in Envelope", "Unknown"]]

        # Fallback to all options if the filtered list is empty
        if not suspects:
            suspects = self.suspects
            print("All suspects have been seen. Falling back to all suspects.")
        if not weapons:
            weapons = self.weapons
            print("All weapons have been seen. Falling back to all weapons.")
        if not rooms:
            rooms = self.rooms
            print("All rooms have been seen. Falling back to all rooms.")

        suspect = self.get_selection(suspects, "Choose a suspect:")
        weapon = self.get_selection(weapons, "Choose a weapon:")
        room = self.get_selection(rooms, "Choose a room:")

        suggestion = (suspect, weapon, room)
        print(f"You suggest: {suggestion}")

        # Process the suggestion
        refuted_by, refuted_card = self.refute_suggestion(suggestion, player)        
       
        if refuted_card:
           pass
        else:
           print("No one could refute your suggestion.")

        self.show_clue_sheet(player)

        accuse = input("Do you want to make an accusation? (yes/no): ").strip().lower()
        if accuse == "yes":
           accusation = {
            "suspect": self.get_selection(self.suspects, "Accuse: Choose a suspect:"),
            "weapon": self.get_selection(self.weapons, "Accuse: Choose a weapon:"),
            "room": self.get_selection(self.rooms, "Accuse: Choose a room:")
           }
           self.make_accusation(player, accusation)            

    def ai_turn(self, player):
        """Handle AI player actions using hybrid logic."""
        if not player.active:
            print(f"{player.name} is eliminated and skips their turn.")
            return

        print(f"{player.name}'s turn! Thinking...")

        # Rule-based deductions for suggestion
        suggestion = player.get_suggestion(self.suspects, self.weapons, self.rooms, self.global_suggestion_counts)
        print(f"{player.name} suggests: {suggestion}")

        # Process the suggestion
        refuted_by, refuted_card = self.refute_suggestion(suggestion, player)
        if refuted_card:
            print(f"{refuted_by} refuted {player.name}'s suggestion.")
            player.add_known_card(refuted_card)
        else:
            print(f"No one refuted {player.name}'s suggestion.")

        # Deduce and accuse if confident
        deduced_solution = player.deduce_solution(self.suspects, self.weapons, self.rooms)
        if deduced_solution:
           print(f"{player.name} deduces: {deduced_solution}")
           self.make_accusation(player, deduced_solution)
        elif self.risk_based_accusation(player):
           # Make a risky accusation
           accusation = {
               "suspect": random.choice([s for s in self.suspects if s not in player.known_cards]),
               "weapon": random.choice([w for w in self.weapons if w not in player.known_cards]),
               "room": random.choice([r for r in self.rooms if r not in player.known_cards]),
           }
           self.make_accusation(player, accusation)

    def make_accusation(self, player, accusation=None):
        """Allow a player to make an accusation."""
        if accusation is None:  # For human players, prompt for input
           print(f"{player.name}, make an accusation!")
           suspect = self.get_selection(self.suspects, "Accuse: Choose a suspect:")
           weapon = self.get_selection(self.weapons, "Accuse: Choose a weapon:")
           room = self.get_selection(self.rooms, "Accuse: Choose a room:")

           accusation = {"suspect": suspect, "weapon": weapon, "room": room}
        print(f"{player.name} accuses: {accusation}")

        if accusation == self.solution:
            print(f"🎉 {player.name} wins! The solution was: {self.solution}")
            exit()
        else:
            print(f"❌ {player.name}'s accusation was incorrect!")
            player.active = False
            print(f"{player.name} is eliminated. They can no longer suggest or accuse but can still refute suggestions.")

    def show_clue_sheet(self, player):
        """Display the current player's private clue sheet."""
        print(f"\n--- {player.name}'s Clue Sheet ---")
        table = [[key, value] for key, value in player.private_clue_sheet.items()]
        print(tabulate(table, headers=["Card", "Status"], tablefmt="grid"))

    def risk_based_accusation(self, player):
        """Decide if the AI should make a risky accusation."""
        # 10% chance of making a risky accusation
        return random.random() < 0.1

    def should_accuse(self, player):
        """Determine if the AI should accuse based on confidence."""
        possible_suspects = [s for s in self.suspects if s not in player.known_cards]
        possible_weapons = [w for w in self.weapons if w not in player.known_cards]
        possible_rooms = [r for r in self.rooms if r not in player.known_cards]      
        return len(possible_suspects) == 1 and len(possible_weapons) == 1 and len(possible_rooms) == 1

    def game_loop(self):
        """Run the main game loop."""
        while len([player for player in self.players if player.active]) > 1:
            for i, player in enumerate(self.players):  # Use enumerate to get the index
                if player.active:
                    self.handle_turn(player)
                    time.sleep(3)  # Pause between turns

            # Display global suggestion counts at the end of the last player's turn
            self.display_global_suggestion_counts()

        # End the game when there's only one or no active player left
        self.end_game()
    
    def end_game(self):
        """End the game and reveal the solution."""
        print("\n--- Game Over ---")

        # Check if a winner exists
        active_players = [player for player in self.players if player.active]

        if len(active_players) == 1:
           final_player = active_players[0]
           print(f"Only {final_player.name} remains active.")

           if final_player.is_human:
              print(f"{final_player.name}, you must make a final accusation to win.")

              # Allow manual player to input their final accusation
              suspect = self.get_selection(self.suspects, "Accuse: Choose a suspect:")
              weapon = self.get_selection(self.weapons, "Accuse: Choose a weapon:")
              room = self.get_selection(self.rooms, "Accuse: Choose a room:")
              accusation = {"suspect": suspect, "weapon": weapon, "room": room}

              print(f"{final_player.name} accuses: {accusation}")

              if accusation == self.solution:
                  print(f"🎉 {final_player.name} wins! The solution was: {self.solution}")
              else:
                  print(f"❌ {final_player.name}'s accusation was incorrect!")
                  print("No one wins the game!")
                  print("The solution was:", self.solution)
           else:

               # Generate an automatic accusation
               possible_suspects = [s for s in self.suspects if s not in final_player.known_cards]
               possible_weapons = [w for w in self.weapons if w not in final_player.known_cards]
               possible_rooms = [r for r in self.rooms if r not in final_player.known_cards]


               # Choose random options for the accusation if knowledge is incomplete
               suspect = possible_suspects[0] if possible_suspects else random.choice(self.suspects)
               weapon = possible_weapons[0] if possible_weapons else random.choice(self.weapons)
               room = possible_rooms[0] if possible_rooms else random.choice(self.rooms)

               accusation = {"suspect": suspect, "weapon": weapon, "room": room}
               print(f"{final_player.name} accuses: {accusation}")

               if accusation == self.solution:
                  print(f"🎉 {final_player.name} wins! The solution was: {self.solution}")
               else:
                  print(f"❌ {final_player.name}'s accusation was incorrect!")
                  print("No one wins the game!")
                  print("The solution was:", self.solution)
        else:
           print("❌ All players have been eliminated! No one solved the mystery.")
           print("The solution was:", self.solution)

        exit()

# Game setup
player_names = ["Miss Scarlett", "Professor Plum", "Mrs. Peacock", "Colonel Mustard", "Reverend Green", "Dr. Orchid"]
suspects = ["Miss Scarlett", "Professor Plum", "Mrs. Peacock", "Colonel Mustard", "Reverend Green", "Dr. Orchid"]
weapons = ["Knife", "Candlestick", "Revolver", "Rope", "Lead Pipe", "Wrench"]
rooms = ["Study", "Hall", "Lounge", "Library", "Billiard Room", "Dining Room", "Kitchen", "Ballroom", "Conservatory"]


game = CluedoGame(player_names, suspects, weapons, rooms)
game.game_loop()  