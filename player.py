class Player():
    def __init__(self, name, max_weight=10):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        # poids maximum que le joueur peut porter
        self.max_weight = 10

    def _short_description(self, room):
        desc = room.get_long_description()
        if "." in desc:
            return desc.split(".")[0] + "."
        return desc    

    def move(self, direction):
        direction = direction.upper()
        next_room = self.current_room.exits.get(direction)
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Ajouter la pièce actuelle dans l’historique
        if self.current_room is not None:
            self.history.append(self.current_room)

        # Passer à la nouvelle pièce
        self.current_room = next_room

        # Afficher description complète
        print(f"\nVous êtes dans {self.current_room.description}\n\n{self.current_room.get_exit_string()}\n")
        # Afficher l’historique 
        print(self.get_history())
        return True


    def get_history(self):
        if not self.history:
            return "\nVous n'avez encore visité aucune pièce.\n"

        result = "\nVous avez déja visité les pièces suivantes :\n"
        for room in self.history:
            result += f"    - {self._short_description(room)}\n"
        return result

    def back(self):
        if not self.history:
            print("\nVous ne pouvez pas revenir en arrière, aucun déplacement précédent.\n")
            return False

        # Revenir à la dernière salle visitée
        self.current_room = self.history.pop()

        print(f"\nVous êtes dans {self.current_room.description}\n\n{self.current_room.get_exit_string()}\n")
        print(self.get_history())
        return True


    def add_item(self, item):
        self.inventory.append(item)

    # Ajouter un inventaire au joueur
    def get_inventory(self):
        if not self.inventory:
            return "Votre inventaire est vide."

        text = "Vous disposez des items suivants :\n"
        for item in self.inventory.values():
            text += f"- {item}\n"
        return text

    
    def charger_beamer(self):
        if "beamer" not in self.inventory:
            return "Tu n'as pas de beamer."
        return self.inventory["beamer"].charge(self.current_room)

    def use_beamer(self):
        if "beamer" not in self.inventory:
            return "Tu n'as pas de beamer."
        room = self.inventory["beamer"].fire()
        if room is None:
            return "Le beamer n'est pas chargé."

        if self.current_room is not None:
            self.history.append(self.current_room)
            
        self.current_room = room

        msg = f"Tu es téléporté dans {room.name}.\n\n"
        msg += f"{self.current_room.description}\n\n"
        msg += self.current_room.get_exit_string() + "\n"
        msg += self.get_history()
    
        return msg
