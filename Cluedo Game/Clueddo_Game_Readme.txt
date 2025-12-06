Overview:
---------
This program is a digital implementation of the classic board game Cluedo (Clue). The game involves a mix of human and AI players attempting to solve a murder mystery by deducing the suspect, weapon, and room involved in the crime. Players take turns making suggestions and accusations to determine the solution hidden within the envelope.

How to run the Cluedo game:
---------------------------

1. Install Python:
   - Ensure that Python is installed on your system. You can download and install Python from python.org.

2. Install Required Libraries:
   - The game uses the random, time, tkinter, collections, and tabulate modules.
   - tkinter and random are included by default with Python.
   - Install the tabulate library using pip: pip install tabulate

3. Prepare the Source Code:
   - Copy the provided Python code and save it to a file named Cluedo_Game.py.
   - Save the file in a directory where you can easily navigate, such as your Desktop or a specific project folder.

4. Navigate to the Source Code Directory:
   - Open your terminal or command prompt.
   - Change to the directory where Cluedo_Game.py is saved. For example: cd Desktop

5. Run the Game Script:
   - Execute the script using Python: python Cluedo_Game.py

6. Game Setup:
   - A pop-up will appear asking for the number of players (between 3 and 6). Enter the desired number.
   - The first player is always a human player, and the rest are AI players.

7. Human Player's Turn:
   - You’ll see your cards and options for suspects, weapons, and rooms displayed dynamically.
   - Use the dropdown menus in the pop-up windows to make your choices.
   - Decide whether to make an accusation or continue suggesting.

8. Global Clue Sheet:
   - After your turn, the game will display the global suggestion counts in the console. 
   - These counts show how often each suspect, weapon, and room has been suggested by all players so far.

9. AI Players' Turns:
   - AI players will make suggestions, refutations, and deductions automatically.
   - The game will display AI players' actions and decisions in the console.

10. Game Loop:
   - Players will take turns suggesting and refuting until one player correctly deduces the solution or everyone is eliminated.

11. End Game:
    - When only one active player remains or someone makes the correct accusation, the game ends.
    - The solution is revealed, and the winner (if any) is announced.

12. Exiting the Game:
    - Once the game ends, the script terminates automatically.

Steps for navigating to the source code directory:
--------------------------------------------------

1. Open the Command Prompt:
   - Press Win + R on your keyboard to open the Run dialog box.
   - Type cmd and press Enter.

2. Change the Drive (if necessary):
   - If your Cluedo_Game.py file is located on a drive other than C:, type the drive letter followed by a colon and press Enter.

3. Navigate to the Desktop:
   - If the file is on your Desktop, type: cd Desktop

4. Navigate to the Project Directory:
   - The project is in a folder named Vandana_Pathania_Project2_SourceCode on the Desktop, type: cd Vandana_Pathania_Project2_SourceCode

5. Verify the File is Present:
   - To ensure Cluedo_Game.py is in the directory, type: dir
   - Look for Cluedo_Game.py in the listed files.

6. Run the Python Script:
   - Type the following command to run the game: python Cluedo_Game.py

Prerequisites required to execute the code:
-------------------------------------------

1. Python 3.x

2. Libraries:
   - tkinter (for GUI prompts)
   - random (for randomness)
   - time (for delays between turns)
   - collections (for data structures like defaultdict)
   - tabulate (for formatted clue sheet display)

Code Structure:
---------------

1. Player Class: Represents a player in the game (human or AI).

Attributes:
- name: The player's name.
- is_human: Indicates if the player is human.
- cards: The player's hand of cards.
- known_cards: Cards the player has seen or deduced.
- private_clue_sheet: Tracks the player's knowledge of suspects, weapons, and rooms.
- suggestion_counts: Tracks how often each suspect, weapon, and room has been suggested by the player.
- previous_suggestions: Keeps track of unique suggestions made by the player.

Key Methods:
- add_known_card(card): Updates the player's known cards and clue sheet.
- get_matching_cards(suggestion): Returns cards in the player's hand that match the suggestion.
- get_suggestion(suspects, weapons, rooms, global_suggestion_counts): AI generates a suggestion based on rules and randomness.
- update_clue_sheet(suggestion, refuted_card): Updates the private clue sheet based on refutations.
- deduce_solution(suspects, weapons, rooms): Attempts to deduce the solution if enough information is available.

2. CluedoGame Class: Manages the overall gameplay, including player turns, suggestions, and the game loop.

Attributes:
- suspects, weapons, rooms: Lists of all possible suspects, weapons, and rooms.
- solution: The mystery solution (randomly generated).
- players: List of Player objects participating in the game.
- global_suggestion_counts: Tracks how often each suspect, weapon, and room is suggested by all players.

Key Methods:
- setup_players(player_names): Dynamically sets up human and AI players.
- assign_cards(): Distributes cards to players and excludes solution cards.
- refute_suggestion(suggestion, suggesting_player): Handles refutations of suggestions.
- handle_turn(player): Handles a player’s turn (human or AI).
- manual_turn(player): Processes a human player's turn, including suggestions and accusations.
- ai_turn(player): Processes an AI player’s turn, including suggestions, deductions, and accusations.
- make_accusation(player, accusation): Allows a player to make an accusation.
- display_global_suggestion_counts(): Displays the global clue sheet after turns.
- show_clue_sheet(player): Displays a player’s private clue sheet.
- game_loop(): The main game loop where players take turns.
- end_game(): Ends the game, reveals the solution, and announces the winner.

Known Limitations:
------------------

1. Single Human Player:
   - Currently supports only one human player (always "Miss Scarlett").

2. AI Deduction:
   - AI uses simple rule-based logic and does not employ advanced reasoning techniques.

3. GUI Dependency:
   - The game relies on tkinter for human player interactions, which may not work in environments without GUI support.

Future Improvements:
--------------------

1. Add support for multiple human players.
2. Implement advanced AI strategies for deduction.
3. Create a web-based or graphical version of the game.
4. Enhance the clue sheet for better tracking of suggestions and refutations.






