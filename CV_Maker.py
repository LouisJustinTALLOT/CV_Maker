# import json
import jsonpickle

def main():
    try :
        mon_cv = load_JSON('CV_1.json')
        print('here')
        print(mon_cv.liste_sections)
    except:
        print("là")
        mon_cv = CV()
        sauvegarde_JSON(mon_cv)

def sauvegarde_JSON(cv):
    # jsonstr = json.dumps(cv.__dict__)
    jsonstr = jsonpickle.encode(cv, indent=4)
    with open("CV.json", 'w', encoding='utf8') as file:
        file.write(jsonstr)

def load_JSON(fichier):
    with open(fichier, 'r', encoding='utf8') as file :
        fichier = file.readlines()
        jsonstr = "\n".join(fichier)

    return jsonpickle.decode(jsonstr)


class Item:
    def __init__(self):
        self.nouveau()


    def nouveau(self):
        self.titre = input("Titre: ")
        self.organisme = input("Organisme : ")
        self.date_debut = input("Date de début (JJ/MM/AAAA) : ")
        self.date_fin = input("Date de fin ou in progress : ")
        self.logo = input("Nom du fichier logo : ")
        self.url = input("Url éventuelle : ")

    def __repr__(self):
        return f"Item {self.titre}"

class Section:
    
    def __init__(self):
        self.liste_items = []
        self.nouveau()

    def nouveau(self):
        self.nom = input("Nom de la section : ")
        self.liste_items.append(Item())


    def ajouter_item(self):
        self.liste_items.append(Item())

    def __repr__(self) -> str:
        return f"[Section {self.nom} "+" ".join((repr(i) for i in self.liste_items))+"]"

class CV:

main()