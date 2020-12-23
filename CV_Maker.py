# import json
import jsonpickle

def titre_to_nom_de_fichier(titre:str):
    titre = titre.replace(" ", "_")
    titre = titre.replace("é","e")
    titre = titre.replace("è","e")
    titre = titre.replace("ù","u")
    titre = titre.replace("à","a")
    return titre

def header_html(titre='CV'):
    res = f"""<!DOCTYPE html>
    <meta charset="utf-8" />
    <html lang="en">
    <head>
      <title>{titre}</title>
    </head>
    """
    return res

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

    def afficher(self):
        print(self.titre)
        print(self.organisme)
        print(self.date_debut)
        print(self.date_fin)
        
    def modifier(self):
        for carac in [self.titre,self.organisme,self.date_debut,self.date_fin,self.logo,self.url]:
            print(carac)
            while True:
                a = input("Remplacement :\n")
                if a:
                    carac = a
                    break
                else:
                    break

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

    def afficher(self):
        print(self.nom)
        for i, item in enumerate(self.liste_items):
            print(f"{i} {item.nom}")

    def afficher_items(self):
        for i, item in enumerate(self.liste_items) :
            print(f"{i} {item.titre}")

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

    def to_html(self, format='normal'):
        with open("CV.html", 'w', encoding='utf8') as file:
            # file.write("""<!DOCTYPE html\n PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n""")
            file.write(header_html())
            file.write("<body>\n")
            file.write("<h1> CV </h1>\n")
            for sec in self.liste_sections:
                file.write(f"<h2>{sec.nom}</h2>\n")
            file.write("</body>\n</html>")

def mainloop(cv:CV, lieu='main', no_sec=-1, no_it=-1, new=False,modify=False):
    if lieu ==  'main':
        while True :
            key = input("q, s : new section, l: liste sec°, m: modify,p : to html: ")
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
            elif key[0].lower() == 'p':
                cv.to_html()
    
    elif lieu == 'section':
        if not modify:
        while True : #TODO
            key = input("q : quitter section, s : new item : ")
            if not key :
                pass
            elif key[0].lower() == 'q' :
                return
            elif key[0].lower() == 's' :    
                    mainloop(cv, 'item',no_sec=no_sec, new=1)
                elif key[0].lower() == 'l':
                    print(cv.liste_sections[no_sec].liste_items)
                elif key[0].lower() == 'm':
                    cv.liste_sections[no_sec].afficher_items()
                    while True : 
                        no_item = input("Quel numéro d'item ? " )
                        if not no_item:
                            pass
                        elif int(no_item) < cv.nb_sections[no_sec].nb_items and int(no_item) >= 0 :
                            mainloop(cv, lieu='item',no_sec=no_sec,no_it=int(no_item), modify=True)
                            break
                        elif no_item[0].lower() == 'q':
                            break
                    
    
    elif lieu == 'item':
        if new:
            cv.liste_sections[no_sec].ajouter_item()
            return

        if modify:
            cv.liste_sections[no_sec].liste_items[no_item].modifier()
        # while True :
        #     key = input("q : quitter item")

        #     if not key:
        #         pass
        #     elif key[0] == 'q':
        #         return

            
        


def main():
    try :
        mon_cv = load_JSON('CV.json')

    except:
        print("n'a pas réussi à le charger")
        mon_cv = CV()
        mainloop(mon_cv)
        sauvegarde_JSON(mon_cv,'CV_1.json')
    else:
        mainloop(mon_cv)
        sauvegarde_JSON(mon_cv)


main()