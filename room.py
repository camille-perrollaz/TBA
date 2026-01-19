# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description, image=None):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters={}
        self.image = image


    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: "
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string


    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"{self.description}\n\n{self.get_exit_string()}\n"

    # Ajouter un inventaire aux lieux
    def get_inventory(self):
        if not self.inventory and not self.characters:
            return "Il n'y a rien ici"
        text = ""
    
        # Items
        if self.inventory:
            text += "On voit:\n"
            for item in self.inventory.values():
                text+= f"    - {item}\n"

        # PNJ
        if self.characters:  
            for character in self.characters.values():
                text += f"    - {character.name} : {character.description}\n"

        return text
