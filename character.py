import random
class Character:
    def __init__(self, name, description, room, messages, mobile=True):
        self.name = name
        self.description = description
        self.room = room
        self.messages = messages[:]
        self.mobile = mobile 
     
    def get_msg(self):
        if not self.messages:
            print(f"{self.name} n'a plus rien à dire.")
            return
        msg = self.messages.pop(0)
        print(f"{self.name} dit : \"{msg}\"")
        self.messages.append(msg)

    def move(self): 
        if not self.mobile: 
            return False

        if random.choice([True, False]):
            next_room = random.choice(list(self.room.exits.values()))

            # retirer le PNJ de l'ancienne salle
            for key, value in list(self.room.characters.items()):
                if value == self:
                    del self.room.characters[key]
                    break

            # ajouter le PNJ dans la nouvelle salle
            self.room = next_room
            self.room.characters[self.name.lower()] = self
            return True

        return False



 