# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, D, U)", Actions.go, 1)
        self.commands["go"] = go
        
        # Setup rooms

        vestibule = Room("Vestibule", "un vestibule sombre et poussiéreux, ses murs sont couverts de toiles d’araignée. Plus tôt, tu errais dans la forêt quand un grand manoir a attiré ton regard. Par curiosité, tu y es entré… et la porte s’est refermée brusquement derrière toi. L’air y est lourd et stagnant, et déjà tu sens que cet endroit cache des secrets mystérieux.")
        self.rooms.append(vestibule)
        archives = Room("Les Archives", "une bibliothèque plongée dans la pénombre. Les livres jonchent son sol dans un désordre total, et une odeur d’humidité imprègne l’air.")
        self.rooms.append(archives)
        salle_oeil = Room("Salle de l’Œil", "une salle avec un immense porche menaçant. La porte entrouverte laisse juste assez d’espace pour apercevoir un œil qui t’observe dans l’ombre.")
        self.rooms.append(salle_oeil)
        laboratoire = Room("Laboratoire", "un laboratoire en désordre. Des fioles brisées jonchent le sol, où se mêlent des résidus de potions et des matières non identifiées. Une forte odeur de produits chimiques flotte encore dans l’air.")
        self.rooms.append(laboratoire)
        chapelle = Room("Chapelle", "une vieille chapelle en bois, usée et marquée par le temps. Elle abrite en son centre un coffre mystérieux.")
        self.rooms.append(chapelle)
        chambre = Room("Une chambre", "une chambre figée dans le temps. Un vieux piano poussiéreux trône dans un coin, tandis que des meubles usés sont recouverts de larges toiles d’araignées.")
        self.rooms.append(chambre)
        salon_depeceur = Room("Salon ", "un salon plongé dans la pénombre. Les fauteuils rouges absorbent la lumière, et les ornements de bronze projettent des ombres tremblantes.")
        self.rooms.append(salon_depeceur)
        crypte = Room("Crypte", "un souterrain humide éclairé par des lanternes. Le sol est jonché de débris et de pierres tombées.")
        self.rooms.append(crypte)
        cellule = Room("Cellule du Silence", "une pièce minuscule avec une large porte d'échappatoire verrouillée. Un filet de brume venant de l’extérieur la traverse.")
        self.rooms.append(cellule)


        
        # Create exits for rooms

        vestibule.exits = {"U": chambre, "D": crypte, "E": archives, "O": salon_depeceur}
        archives.exits = {"O": vestibule, "N": salle_oeil, "U":laboratoire}
        salle_oeil.exits = {"S": archives, "E": laboratoire}
        laboratoire.exits = {"O": salle_oeil, "U": chapelle, "D" : archives}
        chapelle.exits = {"D": laboratoire, "O": chambre}
        chambre.exits = {"D": vestibule, "E": chapelle}
        salon_depeceur.exits = {"E": vestibule}
        crypte.exits = {"U": vestibule, "E": cellule}
        cellule.exits = {"O": crypte}

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = vestibule


        
        # Commande pour consulter l'historique
        history_cmd = Command("history", " : afficher l'historique des pièces visitées", Actions.show_history, 0)
        self.commands["history"] = history_cmd

        # Commande pour revenir en arrière
        back_cmd = Command("back", " : revenir en arrière", Actions.go_back, 0)
        self.commands["back"] = back_cmd


    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

        # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words (ignore extra spaces)
        list_of_words = command_string.split()
        if not list_of_words:
            return

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(f"\nVous êtes dans {self.player.current_room.description}\n\n{self.player.current_room.get_exit_string()}\n")
def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
