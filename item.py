class Item:
    def __init__(self, name, description, weight, portable=True):
        self.name = name
        self.description = description
        self.weight = weight
        self.portable = portable  # Indique si l'objet peut être pris

    def __str__(self):
        
        return f"{self.name} : {self.description} ({self.weight} kg)"
