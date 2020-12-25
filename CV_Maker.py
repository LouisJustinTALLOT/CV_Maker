# import json
import jsonpickle
import os

def titre_to_nom_de_fichier(titre:str):
    titre = titre.replace(" ", "_")
    titre = titre.replace("é", "e")
    titre = titre.replace("è", "e")
    titre = titre.replace("ù", "u")
    titre = titre.replace("à", "a")
    titre = titre.replace("ç", "c")
    return titre

def html_head(titre='CV', format='full'):
    res = f"""<!DOCTYPE html>
    <meta charset="utf-8" />
    <html lang="en">
    <link rel="stylesheet" href="{format}.css" />
    <head>
      <title>{titre}</title>
    </head>
    """
    return res


def sauvegarde_JSON(cv, nom_fichier="CV.json"):
    # jsonstr = json.dumps(cv.__dict__)
    cv.write_csv() # on écrit les CSV pour être raccord
    jsonstr = jsonpickle.encode(cv, indent=1) #et on sauve en JSON
    with open(nom_fichier, 'w', encoding='utf8') as file:
        file.write(jsonstr) 

def load_JSON(fichier):
    with open(fichier, 'r', encoding='utf8') as file :
        fichier = file.readlines()
        jsonstr = "\n".join(fichier)
    cv = jsonpickle.decode(jsonstr) # on récupère le CV du JSON
    cv.load_csv() # et on compare avec les CSV 
    return cv


class Item:
    def __init__(self, num,t=None,org=None, des=None, dd=None, df=None, logo=None,url=None):
        
        self.numero = num
        if t:
            self.titre = t
            self.organisme = org
            self.description = des
            self.date_debut = dd
            self.date_fin = df
            self.logo = logo
            self.url =url
        else:
            self.nouveau()


    def nouveau(self):
        self.titre = input("Titre: ")
        self.organisme = input("Organisme : ")
        self.description = input("Description :")
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

    def to_html(self):   # à modifier pour changer ce qu'on affiche
        res = f"<h3>{self.titre}</h3>\n"

        return res

class Section:
    
    def __init__(self):
        self.liste_items = []
        self.liste_items_ignores = []
        self.nb_items = 0
        self.nouveau()

    def nouveau(self):
        self.nom = input("Nom de la section : ")
        # self.liste_items.append(Item())


    def ajouter_item(self, ignore=False):
        if ignore:
            self.liste_items_ignores.append(Item(self.nb_items))
            self.dict_etat_items[self.nb_items] = "ignore"
            self.dict_tous_items[self.nb_items] = self.liste_items_ignores[-1]
            
        else:
            self.liste_items.append(Item(self.nb_items))
            self.dict_etat_items[self.nb_items] = "dedans"
            self.dict_tous_items[self.nb_items] = self.liste_items[-1]
        
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

    def to_html(self):
        res = f"<h2>{self.nom}</h2>\n"
        for it in self.liste_items :
            res += it.to_html()
        return res

class CV:

    def __init__(self):
        self.liste_sections = []
        self.nb_sections = 0
        self.qui_je_suis = {'nom' : "Elmo",
               'date_naissance' : "01/01/1970",
                'motto' : 'Voici ma devise'
        }

        self.qui_je_suis["nom"] = input("Votre nom: ")
        self.qui_je_suis["date_naissance"] = input("Votre date de naissance: ")
        self.qui_je_suis["motto"] = input("Votre motto")
        # self.nouvelle_section()

    def nouvelle_section(self):
        self.liste_sections.append(Section())
        self.nb_sections += 1

    def afficher_sections(self):
        for i, sec in enumerate(self.liste_sections) :
            print(f"{i} {sec.nom}")

    def html_header(self,nom_image:str,format='full'):
        res = ""
        if format == 'full':
            res += "<header>\n"
            res += f"""<img src = "images/{nom_image}" style="height:200px; width:auto" />\n"""
            res += f"""<h1>{self.qui_je_suis['nom']} </h1>\n"""
            res += f"""<h2>Né le {self.qui_je_suis['date_naissance']}</h2>\n"""
            res += f"""<p>{self.qui_je_suis['motto']}</p>\n"""
            res += "</header>\n"
            return res
        else:
            return self.html_header(nom_image) # à changer pour les autres styles

    def to_html(self, format='normal'):
        with open("CV.html", 'w', encoding='utf8') as file:
            # file.write("""<!DOCTYPE html\n PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n""")
            file.write(html_head())
            file.write("<body>\n")
            file.write(self.html_header("photo_elmo.jpg"))
            file.write("<h1> CV </h1>\n")
            for sec in self.liste_sections:
                file.write(sec.to_html())
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
                mainloop(cv, lieu='section', no_sec=cv.nb_sections-1)
            elif key[0].lower() == 'l':
                cv.afficher_sections()
            elif key[0].lower() == 'm':
                cv.afficher_sections()
                while True : # ne va pas du tout
                    no_section = input("Quel numéro de section ? " )
                    if not no_section:
                        pass
                    elif int(no_section) < cv.nb_sections and int(no_section) >= 0 :
                        mainloop(cv, lieu='section',no_sec=int(no_section))
                        break
                    elif no_section[0].lower() == 'q':
                        break
            elif key[0].lower() == 'p':
                cv.to_html()
    
    elif lieu == 'section':
        if not modify:
            while True : #TODO
                key = input("q : quitter section,l: list item s : new item , m odifier item: ")
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
                    
        else:
            # TODO 
            pass

    elif lieu == 'item':
        if new:
            cv.liste_sections[no_sec].ajouter_item()
            return

        if modify:
            cv.liste_sections[no_sec].liste_items[no_it].modifier()
        # while True :
        #     key = input("q : quitter item")

        #     if not key:
        #         pass
        #     elif key[0] == 'q':
        #         return

def main():
    try :
        mon_cv = load_JSON('CV.json')

    except Exception as e:
        print(e)
        print("n'a pas réussi à le charger")
        mon_cv = CV()
        mainloop(mon_cv)
        sauvegarde_JSON(mon_cv,'CV_1.json')
    else:
        mainloop(mon_cv)
        sauvegarde_JSON(mon_cv)


main()