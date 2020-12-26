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
        res = f"""<h2 class="titre_item">{self.titre}</h2>\n"""

        return res

class Section:
    
    def __init__(self):
        self.liste_items = []
        self.liste_items_ignores = []
        self.dict_etat_items = {}
        self.dict_tous_items = {}
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
        res = f"""<h1 class="debut_de_section">{self.nom}</h1>\n"""
        it:Item
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

    def write_csv(self):
        """on va sauver le contenu du CV dans des CSV avant de sauver en JSON"""
        with open("sections/infos_personnelles.csv",'w',encoding='utf8') as file:
            for key in self.qui_je_suis.keys():
                file.write(f"{key};{self.qui_je_suis[key]}\n")

        date_ref = os.path.getmtime("CV.json")
        for sec in self.liste_sections : #type: Section
            fichier = f"sections/{titre_to_nom_de_fichier(sec.nom)}.csv"
            # if fichier not in os.listdir("sections") or os.path.getmtime(fichier)>date_ref:
            
            with open(f"sections/{titre_to_nom_de_fichier(sec.nom)}.csv", 'w', encoding='utf8') as file :
                file.write(f"{sec.nom}\n")#TODO 
                file.write("ignore;numero;titre;organisme;description;date_debut;date_fin;logo;url\n")
                print(sec.nb_items, len(sec.dict_tous_items))
                for i in range(sec.nb_items):
                    try: #Problème ICI # TODO # WIP
                        it = sec.dict_tous_items[i]
                        if sec.dict_etat_items[i] == "ignore":
                            file.write(f"oui;{it.numero};{it.titre};{it.organisme};{it.description};{it.date_debut};{it.date_fin};{it.logo};{it.url}\n")
                        else : 
                            file.write(f"non;{it.numero};{it.titre};{it.organisme};{it.description};{it.date_debut};{it.date_fin};{it.logo};{it.url}\n")
                    except:
                        pass

    def load_csv(self):
        liste_des_sections = os.listdir("sections")
        date_ref = os.path.getmtime("CV.json")

        if os.path.getmtime("sections/infos_personnelles.csv") > date_ref :
            # alors les infos perso ont été modifiées
            with open("sections/infos_personnelles.csv",'r',encoding='utf8') as file:
                liste_infos_perso = file.readlines()
                for ligne in liste_infos_perso:
                    # on va remplacer la valeur dans self.qui_je_suis
                    ligne = ligne[:-1]
                    key, value = ligne.split(";")
                    self.qui_je_suis[key] = value

        for sec in liste_des_sections:
            chemin_fichier = "sections/"+sec
            if os.path.getmtime(chemin_fichier) > date_ref :
                print("modifié : ", sec)
                # alors le CSV a été modifié
                with open(chemin_fichier, 'r', encoding='utf8') as file:
                    liste_lignes_section = file.readlines()

                trouve=False
                sec:Section
                for sec in self.liste_sections:
                    if sec.nom == liste_lignes_section[0][:-1]:
                        trouve=True
                        # on a alors la section qui a été modifiée
                        # on va alors reconstruire la section de 0
                        sec.liste_items = []
                        sec.liste_items_ignores = []
                        sec.dict_etat_items = {}
                        sec.dict_tous_items = {}
                        sec.nb_items = 0

                        for ligne_it in liste_lignes_section[2:]:#WIP
                            if ligne_it and len(ligne_it)>1:
                                print("ici",sec.nb_items)
                                # on parcourt les items de la section
                                ligne_it = ligne_it[:-1]
                                ignore,no,titre,organisme,description,date_debut,date_fin,logo,url = ligne_it.split(";")
                                if ignore == 'oui':
                                    # on ajoute à la liste des ignores
                                    sec.liste_items_ignores.append(Item(sec.nb_items,titre,organisme,description,date_debut,date_fin,logo,url))
                                    sec.dict_etat_items[sec.nb_items] = "ignore"
                                    sec.dict_tous_items[sec.nb_items] = sec.liste_items_ignores[-1]
                                    
                                else:#WIP
                                    sec.liste_items.append(Item(sec.nb_items,titre,organisme,description,date_debut,date_fin,logo,url))
                                    sec.dict_etat_items[sec.nb_items] = "dedans"
                                    sec.dict_tous_items[sec.nb_items] = sec.liste_items[-1]
                                sec.nb_items += 1
                        break

                if not trouve:
                    # alors c'est une nouvelle section 
                    pass
                    

        # ATTENTION EN LISANT LES LIGNES COMMENTEES 
        # ON NE VEUT PAS LES DETRUIRE EN SAUVANT LE FICHIER A LA FIN .....


        #TODO :
        # on doit pouvoir ajouter une section en ajoutant un CSV


    def html_header(self,nom_image:str,format='full'):
        res = ""
        if format == 'full':
            res += "<header>\n"
            res += f"""  <img src = "images/{nom_image}" id="profile_picture" />\n"""
            res += """  <section id="header_sauf_photo">\n"""
            res += f"""    <h1 id="header_nom">{self.qui_je_suis['nom']} </h1>\n"""
            res += f"""    <h2>Né le {self.qui_je_suis['date_naissance']}</h2>\n"""
            res += f"""    <p>{self.qui_je_suis['motto']}</p>\n"""
            res += """  </section>\n"""
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
            # file.write("<h1> CV </h1>\n")
            file.write("""<section id="toutes_les_sections">\n""")
            sec:Section
            for sec in self.liste_sections:
                file.write(sec.to_html())
            file.write("</section>")
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