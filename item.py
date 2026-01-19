class Item:
    def __init__(self, name, description, weight, portable=True, text=None): # Rajouté
        self.name = name
        self.description = description
        self.weight = weight
        self.portable = portable
        self.text = text
    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"


class Beamer(Item):
    def __init__(self):
        super().__init__("Beamer", "Permet de revenir sur ces pas. (dans la pièce de chargement du beamer)", 1)
        self.charged_room = None

    def charge(self, room):
        self.charged_room = room
        return "Beamer chargé !"

    def fire(self):
        if self.charged_room:
            return self.charged_room
        return None


