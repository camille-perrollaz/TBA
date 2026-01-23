# Import modules

from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog


from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item, Beamer
from actions import charger_beamer, utiliser_beamer
from character import Character
from quest import Quest

class Game:
    DEBUG = False
    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.exit_prompted = False
    
    # Setup the game
    def setup(self, player_name=None):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, D, U)", Actions.go, 1)
        self.commands["go"] = go
        look = Command("look", " : observer la pièce", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : vérifier l'inventaire", Actions.check, 0)
        self.commands["check"] = check
        self.commands["charger"] = Command("charger", " : charger le beamer", charger_beamer, 0)
        self.commands["beamer"]  = Command("beamer", " : utiliser le beamer", utiliser_beamer, 0)
        self.commands["talk"] = Command("talk", " <personnage> : parler à un personnage", Actions.talk,1)
        self.commands["read"] = Command("read", " <item> : lire un objet dans votre inventaire", Actions.read, 1) 
        self.commands["quests"] = Command("quests", " : afficher la liste des quêtes", Actions.quests, 0)
        self.commands["quest"] = Command("quest", " <titre> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["activate"] = Command("activate", " <titre> : activer une quête", Actions.activate, 1)
        self.commands["rewards"] = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
         

        
        # Setup rooms

        vestibule = Room("Vestibule", "un vestibule sombre et poussiéreux, ses murs sont couverts de toiles d’araignée. Plus tôt, tu errais dans la forêt quand un grand manoir a attiré ton regard. Par curiosité, tu y es entré… et la porte s’est refermée brusquement derrière toi. L’air y est lourd et stagnant, et déjà tu sens que cet endroit cache des secrets mystérieux.", image="vestibule.png")
        self.rooms.append(vestibule)
        archives = Room("Les Archives", "les archives, plongées dans la pénombre. Les livres jonchent son sol dans un désordre total, et une odeur d’humidité imprègne l’air.", image="archives.png")
        self.rooms.append(archives)
        salle_oeil = Room("Salle de l’Œil", "la salle d'oeil avec un immense porche menaçant. La porte entrouverte laisse juste assez d’espace pour apercevoir un œil qui t’observe dans l’ombre.", image="salle_oeil.png")
        self.rooms.append(salle_oeil)
        laboratoire = Room("Laboratoire", "un laboratoire en désordre. Des fioles brisées jonchent le sol, où se mêlent des résidus de potions et des matières non identifiées. Une forte odeur de produits chimiques flotte encore dans l’air.", image="laboratoire.png")
        self.rooms.append(laboratoire)
        chapelle = Room("Chapelle", "une vieille chapelle en bois, usée et marquée par le temps. Elle abrite en son centre un coffre mystérieux.", image="chapelle.png")
        self.rooms.append(chapelle)
        chambre = Room("Une chambre", "une chambre figée dans le temps. Un vieux piano poussiéreux trône dans un coin, tandis que des meubles usés sont recouverts de larges toiles d’araignées.", image="chambre.png")
        self.rooms.append(chambre)
        salon_depeceur = Room("Salon ", "un salon opressant. Les fauteuils rouges absorbent la lumière, et les ornements de bronze projettent des ombres tremblantes.", image="salon_depeceur.png")
        self.rooms.append(salon_depeceur)
        crypte = Room("Crypte", "une crypte humide éclairée par des lanternes. Le sol est jonché de débris et de pierres tombées.", image="crypte.png")
        self.rooms.append(crypte)
        cellule = Room("Cellule du Silence", "une cellule minuscule avec une large porte verrouillée d'une grille en fer. Un filet de brume venant de l’extérieur la traverse.", image="cellule.png")
        self.rooms.append(cellule)
        beamer = Beamer()
                

        #Setup objets
        
        vestibule.inventory["note"] = Item("Note", "Elle semble avoir été laissée pour le visiteur. Lis là.", 0.1, text ="Tu es désormais prisonnier de mon manoir. Si tu veux en ressortir vivant, il te faudra percer les énigmes qu’il renferme. Rien n’est laissé au hasard : chaque pièce compte, chaque rencontre a un sens. Explore le manoir dans son intégralité… Et lorsque tu posséderas l’objet que je garde secret, trouve le chemin vers la Cellule du Silence")
        archives.inventory["fiole_a"] = Item("Fiole d'acide sulfurique (fiole_a)", "combiné avec d'autres fioles, cela pourrait faire des ravages.", 0.1)
        salle_oeil.inventory["fiole_v"] = Item("Fiole de potion vide (fiole_v)", "Oh, elle semble ne rien contenir ; les araignées en ont fait leur maison.", 0.2)
        laboratoire.inventory["alambic"] = Item("Alambic", "Outil permettant de faire des potions.", 20, portable=False)
        chapelle.inventory["tabernacle"] = Item("Tabernacle", "Il semble hermétiquement fermé.", 20, portable=False)
        chambre.inventory["coffre"] = Item("Coffre", "Il est fermé d’un cadenas en aluminium, trop abîmé pour être utilisé.", 2, portable=False)
        salle_oeil.inventory["bague"] = Item("Bague", "Elle semble être là depuis un moment... Quelqu’un l’a peut-être égarée.", 0.5)
        chapelle.inventory["beamer"] = beamer 
        
        #--- NPC ---
        sorcier = Character("Sorcier maléfique","Le sorcier maléfique se tient dans l’ombre...",crypte,["Seul celui qui retrouvera ma bague pourra prétendre à la récompense que je réserve."],mobile=False)
        chimiste = Character("Chimiste maudit","Le chimiste semble avoir un message pour toi.",laboratoire,["Prisonnier, disparais avant que je ne t’empoisonne. Tu n’es pas le bienvenu en ces lieux."],mobile=False)
        ame_perdue = Character("Ame perdue","Une silhouette translucide flotte lentement, prisonnière du manoir.", vestibule,["Où suis-je… ?","Je cherche la sortie depuis si longtemps…","Toi aussi, tu es piégé ici ?", "Fais attention, ce manoir est effrayant"], mobile=True)
        ombre_sanguinaire = Character("Ombre Sanguinaire","Une silhouette noire flottante, aux yeux rouges qui brûlent comme du charbon, siffle des menaces glaciales. Son rire résonne dans les murs comme un écho de cauchemar.",laboratoire,["Je sens ton cœur battre… si vite… si faible…","Tu ne devrais pas être ici…","Regarde derrière toi… mais il n'y a rien… ou si ?","Ton souffle devient court… tu le sens ?"],mobile=True)


        crypte.characters[sorcier.name] = sorcier
        laboratoire.characters[chimiste.name] = chimiste
        vestibule.characters[ame_perdue.name] = ame_perdue
        laboratoire.characters[ombre_sanguinaire.name] = ombre_sanguinaire



        
        # Create exits for rooms

        vestibule.exits = {"U": chambre, "D": crypte, "E": archives, "O": salon_depeceur}
        archives.exits = {"O": vestibule, "N": laboratoire}
        salle_oeil.exits = {"O": laboratoire}
        laboratoire.exits = {"U": chapelle, "S" : archives, "E": salle_oeil}
        chapelle.exits = {"D": laboratoire, "O": chambre}
        chambre.exits = {"D": vestibule, "E": chapelle}
        salon_depeceur.exits = {"E": vestibule}
        crypte.exits = {"U": vestibule, "E": cellule}
        cellule.exits = {"O": crypte}

        # Setup player and starting room

        if player_name !="":
            self.player = Player(player_name)
        else:           
            self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = vestibule
        self._setup_quests()  



        
        # Commande pour consulter l'historique
        history_cmd = Command("history", " : afficher l'historique des pièces visitées", Actions.show_history, 0)
        self.commands["history"] = history_cmd

        # Commande pour revenir en arrière
        back_cmd = Command("back", " : revenir en arrière", Actions.go_back, 0)
        self.commands["back"] = back_cmd

    
    def _setup_quests(self):
        """Initialize all quests."""

        exploration_quest = Quest(
            title="Grand Explorateur",
            description="Explorez tous les lieux de ce manoir mystérieux.",
            objectives=["Visiter Vestibule" , "Visiter Les Archives", "Visiter Salle de l’Œil", "Visiter Laboratoire", "Visiter Chapelle","Visiter Une chambre", "Visiter Salon ", "Visiter Crypte", "Visiter Cellule du Silence"], reward="Titre de Grand Explorateur")
        
        item_quest = Quest(
            title="La Bague Perdue",
            description="Retrouvez la bague perdue du magicien.",
            objectives=["prendre bague"],
            reward="L'accès à l’énigme du sorcier"
        )

        interaction_quest = Quest(
            title="L'Énigme du Magicien",
            description="Rapportez la bague au magicien, puis résolvez son énigme.",
            objectives=["donner bague", "résoudre énigme"],
            reward="Fiole de sang"
        )
        

        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(exploration_quest)
        self.player.quest_manager.add_quest(item_quest)
        self.player.quest_manager.add_quest(interaction_quest)


    # Play the game # Rajouté 
    def play(self):
        self.setup()
        self.print_welcome()

        while not self.finished:
            self.process_command(input("> "))

    # reset du prompt si on quitte la cellule
            if self.player.current_room.name != "Cellule du Silence":
                self.exit_prompted = False

            if self.loose():
                self.finished = True
                continue

            if self.win():
                print("\n🏆 Bravo ! Vous avez gagné !\n")
                self.finished = True
                continue


            # Déplacement des PNJ (à chaque tour)
            for room in self.rooms:
                for character in list(room.characters.values()):  # list() crée une copie
                    character.move()

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
    
    def win(self):
        player = self.player

    # conditions de base
        in_cellule = player.current_room.name == "Cellule du Silence"
        has_blood = "sang_coagule" in player.inventory

    # condition : Grand Explorateur terminé
        explore_quest = player.quest_manager.get_quest_by_title("Grand Explorateur")
        explore_done = explore_quest is not None and explore_quest.is_completed

    # si une condition manque -> pas de proposition
        if not (in_cellule and has_blood and explore_done):
            return False

    # éviter de reposer la question en boucle
        if getattr(self, "exit_prompted", False):
            return False
        self.exit_prompted = True

        rep = self.ask(
            "\nVous avez réuni les conditions pour quitter le manoir.\n"
            "Voulez-vous poser la fiole sur le socle et déverrouiller la porte finale ? (oui/non) > "
        ).strip().lower()

        if rep in ("oui", "o", "yes", "y"):
            print("\n🔓 La porte s’ouvre lentement...\n")
            print("🌟 FIN PARFAITE 🌟")
            print(
                "Vous quittez le manoir après avoir percé tous ses secrets.\n"
                "Votre nom restera gravé dans ces murs.\n"
                "🏆 Titre obtenu : Grand Survivant Du Manoir \n"
            )
            return True

        print("\nVous reculez lentement. La porte reste scellée. Revenez si vous changer d'avis.\n")
        return False


    def loose(self):
        player = self.player

        if hasattr(player, "riddle_attempts_left"):
            if not player.riddle_solved and player.riddle_attempts_left <= 0:
                print("\n💀 Le sorcier rit. Trois erreurs. Le manoir se referme sur toi.")
                print("💀 Tu as perdu.\n")
                return True

        return False
    
    def ask(self, message: str) -> str:
    # GUI -> ne jamais bloquer
        if getattr(self, "gui_root", None) is not None:
            try:
                from tkinter import simpledialog
                res = simpledialog.askstring(
                    "Question",
                    message,
                    parent=self.gui_root
                )
                return (res or "").strip().lower()
            except Exception:
                return ""
    # CLI
        return input(message).strip().lower()



class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""
        pass

class GameGUI(tk.Tk):
    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()
        self.game.gui_root = self

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)
        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False) # Keep requested size        
        self.canvas = tk.Canvas(image_frame,width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)
        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))
        # Command buttons
        tk.Button(buttons_frame, image=self._btn_help, command=lambda: self._send_command("help"), bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)
        # Quit button        
        tk.Button(buttons_frame, image=self._btn_quit, command=lambda: self._send_command("quit"),bd=0).grid(row=2, column=0, sticky="ew", pady=(8,2))
        # L2 Terminal output area (Text + Scrollbar)        
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # ✅ Déplacement des PNJ à chaque commande (mode GUI)
        for room in self.game.rooms:
            for character in list(room.characters.values()):
                character.move()

        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()
    
def main():

    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()

if __name__ == "__main__":
    main()