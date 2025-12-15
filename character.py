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


def create_npcs(vestibule, laboratoire,crypte):
 #--- NPC ---
    sorcier = Character("Sorcier maléfique","Le sorcier maléfique se tient dans l’ombre...",crypte,["Seul celui qui retrouvera ma bague pourra prétendre à la récompense que je réserve."],mobile=False)
    chimiste = Character("Chimiste maudit","Le chimiste semble avoir un message pour toi.",laboratoire,["Prisonnier, le maître de maison, par sa mystérieuse générosité, t'accorde une potion. Pour t'aider à t’échapper, tu devras retrouver les ingrédients et utiliser l’alambic."],mobile=False)
    ame_perdue = Character("Ame perdue","Une silhouette translucide flotte lentement, prisonnière du manoir.", vestibule,["Où suis-je… ?","Je cherche la sortie depuis si longtemps…","Toi aussi, tu es piégé ici ?", "Fais attention, ce manoir est effrayant"], mobile=True)
    ombre_sanguinaire = Character("Ombre Sanguinaire","Une silhouette noire flottante, aux yeux rouges qui brûlent comme du charbon, siffle des menaces glaciales. Son rire résonne dans les murs comme un écho de cauchemar.",laboratoire,["Je sens ton cœur battre… si vite… si faible…","Tu ne devrais pas être ici…","Regarde derrière toi… mais il n'y a rien… ou si ?","Ton souffle devient court… tu le sens ?"],mobile=True)


    crypte.characters[sorcier.name] = sorcier
    laboratoire.characters[chimiste.name] = chimiste
    vestibule.characters["ame_perdue"] = ame_perdue
    laboratoire.characters["ombre_sanguinaire"] = ombre_sanguinaire

