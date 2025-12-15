# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        input_direction = list_of_words[1].strip().upper()
        direction_map = {
        "N": "N", "NORD": "N",
        "S": "S", "SUD": "S",
        "E": "E", "EST": "E",
        "O": "O", "OUEST": "O",
        "U": "U", "UP": "U", "HAUT": "U",
        "D": "D", "DOWN": "D", "BAS": "D"
        }

        direction = direction_map.get(input_direction)
        if not direction:
            print(f"\nCommande '{list_of_words[1]}' non reconnue.\n")
            return False

        next_room = player.current_room.exits.get(direction)
        if not next_room:
            print("\nIl n'y a pas de porte dans cette direction !\n")
            return False

        return player.move(direction)


    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    def show_history(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        print(game.player.get_history())
        return True
    
    def go_back(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        return game.player.back()

    # Observer l’environnement
    def look(game, list_of_words, number_of_parameters):
        room = game.player.current_room  
        print(room.get_inventory()) 

    # Prendre
    def take(game, list_of_words, number_of_parameters):
        if len(list_of_words) < 2:
            print("Vous devez préciser quel objet prendre.")
            return

        item_name = list_of_words[1].lower()
        room = game.player.current_room
        player = game.player

        if item_name not in room.inventory:
            print(f"L'objet '{item_name}' n'est pas dans la pièce.")
            return

        item = room.inventory[item_name]

        current_weight = sum(i.weight for i in player.inventory.values())
        if current_weight + item.weight > player.max_weight:
            print(f"Vous ne pouvez pas prendre '{item_name}' (poids trop élevé).")
            return

        player.inventory[item_name] = room.inventory.pop(item_name)
        print(f"Vous avez pris l'objet '{item_name}'.")

    # Reposer un item    
    def drop(game, list_of_words, number_of_parameters):
        if len(list_of_words) < 2:
            print("Vous devez préciser quel objet déposer.")
            return

        item_name = list_of_words[1].lower()
        player = game.player
        room = player.current_room

        if item_name not in player.inventory:
            print(f"L'objet '{item_name}' n'est pas dans l'inventaire.")
            return

        room.inventory[item_name] = player.inventory.pop(item_name)
        print(f"Vous avez déposé l'objet '{item_name}'.")
    
    # Vérifier son inventaire

    def check(game, list_of_words, number_of_parameters):
        inv = game.player.inventory
        if not inv:
            print("Votre inventaire est vide.")
            return
        print("Vous disposez des items suivants :")
        for item in inv.values():
            print(f"    - {item}")


    def talk(game, list_of_words, number_of_parameters):
    # Vérifier le nombre de paramètres
        if len(list_of_words) != number_of_parameters + 1:
            print(f"\nLa commande '{list_of_words[0]}' prend {number_of_parameters} paramètre(s).\n")
            return False

    # Nom saisi par le joueur
        name_input = list_of_words[1].lower()
        room = game.player.current_room

    # Chercher le personnage dans la salle
        for character in room.characters.values():
            if name_input in character.name.lower():  # permet "chimiste" pour "Chimiste maudit"
                character.get_msg()
                return True

        print("Il n'y a personne de ce nom ici.")
        return False

    def read(game, list_of_words, number_of_parameters):
        if len(list_of_words) != 2:
            print("La commande 'read' prend 1 seul paramètre.")
            return False

        item_name = list_of_words[1].lower()
        if item_name not in game.player.inventory:
            print(f"Vous n'avez pas '{item_name}' dans votre inventaire.")
            return False

        print(game.player.inventory[item_name].text)
        return True


# options beamer
def charger_beamer(game, words, n):
    print(game.player.charger_beamer())

def utiliser_beamer(game, words, n):
    print(game.player.use_beamer())

