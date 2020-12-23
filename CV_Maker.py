# import json
import jsonpickle


def sauvegarde_JSON(cv, nom_fichier="CV.json"):
    # jsonstr = json.dumps(cv.__dict__)
    jsonstr = jsonpickle.encode(cv, indent=4)
    with open(nom_fichier, 'w', encoding='utf8') as file:
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
        self.nb_items = 0
        self.nouveau()

    def nouveau(self):
        self.nom = input("Nom de la section : ")
        # self.liste_items.append(Item())


    def ajouter_item(self):
        self.liste_items.append(Item())
        self.nb_items += 1

    def __repr__(self) -> str:
        return f"[Section {self.nom} "+" ".join((repr(i) for i in self.liste_items))+"]"

class CV:

    def __init__(self):
        self.liste_sections = []
        self.nb_sections = 0
        # self.nouvelle_section()

    def nouvelle_section(self):
        self.liste_sections.append(Section())
        self.nb_sections += 1

    def afficher_sections(self):
        for i, sec in enumerate(self.liste_sections) :
            print(f"{i} {sec.nom}")


def mainloop(cv:CV, lieu='main', no_sec=-1, no_item=-1, new=0):
    if lieu ==  'main':
        while True :
            key = input("q, s : new section, l: liste sec°, m: modify: ")
            if not key :
                pass
            elif key[0].lower() == 'q' :
                return
            elif key[0].lower() == 's' :
                cv.nouvelle_section()
                print("là")
                mainloop(cv, lieu='section', no_sec=cv.nb_sections-1)
            elif key[0].lower() == 'l':
                cv.afficher_sections()
            elif key[0].lower() == 'm':
                cv.afficher_sections()
                while True : # ne va pas du tout
                    no_sec = input("Quel numéro de section ? " )
                    if not no_sec:
                        pass
                    elif int(no_sec) < cv.nb_sections and int(no_sec) >= 0 :
                        mainloop(cv,'section',no_sec=no_sec)
                        break
                    elif no_sec[0].lower() == 'q':
                        break
    
    elif lieu == 'section':
        while True : #TODO
            key = input("q : quitter section, s : new item : ")
            if not key :
                pass
            elif key[0].lower() == 'q' :
                return
            elif key[0].lower() == 's' :    
                
                mainloop(cv, 'item',no_sec=no_sec, new=1)
    
    elif lieu == 'item':
        if new:
            cv.liste_sections[no_sec].ajouter_item()
        while True :
            key = input("q : quitter item")

            if not key:
                pass
            elif key[0] == 'q':
                return

            
        


def main():
    try :
        mon_cv = load_JSON('CV_1.json')

    except:
        print("n'a pas réussi à le charger")
        mon_cv = CV()
        mainloop(mon_cv)
        sauvegarde_JSON(mon_cv,'CV.json')
    else:
        mainloop(mon_cv)
        sauvegarde_JSON(mon_cv)


main()