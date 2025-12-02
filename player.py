class Player():
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []

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