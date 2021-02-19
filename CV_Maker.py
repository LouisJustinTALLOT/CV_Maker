import os
import pdfkit
from weasyprint import HTML, CSS
import mdpdf.cli as cli
from click.testing  import CliRunner, Result

def titre_to_nom_de_fichier(titre:str):
    titre = titre.replace(" ", "_")
    titre = titre.replace("é", "e")
    titre = titre.replace("è", "e")
    titre = titre.replace("ù", "u")
    titre = titre.replace("à", "a")
    titre = titre.replace("ç", "c")
    titre = titre.replace("ô", "o")
    titre = titre.replace("ï", "i")
    return titre

def html_head(titre='CV', style_CV='full'):
    res = f"""<!DOCTYPE html>
    <meta charset="utf-8" />
    <html lang="en">
    <link rel="icon" href="favicon.png" />
    <link rel="stylesheet" href="{style_CV}.css" />
    <head>
      <title>{titre}</title>
    </head>
    """
    return res

class Item:
    def __init__(self, num,t=None,org=None, des=None, dd=None, df=None, logo=None,url=None,ignore=False):
        
        self.numero = num
        if t or org or des:
            self.titre = t
            self.organisme = org
            self.description = des
            self.date_debut = dd
            self.date_fin = df
            self.logo = logo
            self.url =url
            self.ignore = ignore
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
        self.ignore=False

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
        res = """<div class="titre_org_logo">\n"""
        res += """<div class="titre_et_org_item">\n"""
        res += f"""    <h2 class="titre_item">{self.titre}</h2>\n"""
        res += """     <div class="div_org_dates">\n """
        res += f"""      <h3 class="organisme_item">{self.organisme}</h3>\n"""
        if self.date_debut:
            if not self.organisme:
                if self.date_fin:
                    res += f"""      <h3 class="dates_item">{self.date_debut} - {self.date_fin}</h3>\n"""
                else:
                    res += f"""      <h3 class="dates_item">{self.date_debut} </h3>\n"""
            else:
                if self.date_fin:
                    res += f"""      <h3 class="dates_item">{self.date_debut} - {self.date_fin}</h3>\n"""
                else:
                    res += f"""      <h3 class="dates_item">{self.date_debut} </h3>\n"""
        res += """    </div>\n"""
        res += """</div>\n"""
        res += """<div class="div_logo_item">\n"""
        if self.logo:
            res += f"""   <div class="conteneur_logo_item"> <img src="images/{self.logo}" class="logo_item" /></div>\n"""
        res += """</div>\n"""
        res += """</div>\n"""

                    
        res += """<div class="description_et_url_item">\n"""
        res += f"""    <p class="description_item">{self.description}\n"""
        if self.url:   
            res += f"""    <br /><a class="url_item" href="{self.url}" target="_blank">{self.url}</a>"""
        res += """    </p>\n"""
        res += """</div>\n"""
        
        
        return res

    def to_markdown(self):
        res = ""
        if self.titre:
            res += f"""## {self.titre}\n\n"""
        if self.organisme:
            res += f"""### {self.organisme} """
        if self.date_debut:
            if self.date_fin:
                res += f"""{self.date_debut} - {self.date_fin}\n\n"""
            else:
                res += f"""{self.date_debut} \n\n"""
        desc = self.description.replace("<br/>", "\n\n")
        res += f"""{desc}\n\n"""
        if self.url:   
            res += f"""[{self.url}]({self.url})\n\n"""

        return res

class Section:
    
    def __init__(self):
        self.liste_items = []
        self.nb_items = 0
        self.ignore = False
        self.type = 0
        self.numero = 0

    def nouveau(self):
        self.nom = input("Nom de la section : ")


    def ajouter_item(self):
        self.liste_items.append(Item(self.nb_items))
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
            if not it.ignore :
                res += """<div class="item">\n"""
                res += it.to_html()
                res += """</div>\n"""
        return res

    def to_markdown(self):
        res = f"# {self.nom}\n\n"

        it:Item
        for it in self.liste_items :
            if not it.ignore :
                res += it.to_markdown()

        return res

class CV:

    def __init__(self, new=False):
        self.liste_sections = []
        self.nb_sections = 0
        self.qui_je_suis = {}
        self.nouveau = new

        if self.nouveau:
            self.qui_je_suis["nom"] = input("Votre nom: ")
            self.qui_je_suis["date_naissance"] = input("Votre date de naissance: ")
            self.qui_je_suis["motto"] = input("Votre motto")

    def nouvelle_section(self):
        self.liste_sections.append(Section())
        self.liste_sections[-1].nouveau()
        self.nb_sections += 1

    def afficher_sections(self):
        for i, sec in enumerate(self.liste_sections) :
            print(f"{i} {sec.nom}")

    def save(self):
        """on va sauver le contenu du CV dans des CSV"""
        with open("sections/infos_personnelles.csv",'w',encoding='utf8') as file:
            for key, valeur in self.qui_je_suis.items():
                file.write(f"{key};{valeur}\n")

        sec:Section
        for sec in self.liste_sections :
            
            with open(f"sections/{titre_to_nom_de_fichier(sec.nom)}.csv", 'w', encoding='utf8') as file :
                file.write(f"{sec.nom};{sec.ignore};{sec.type};{sec.numero}\n")
                file.write("ignore;numero;titre;organisme;description;date_debut;date_fin;logo;url\n")
                it : Item
                for j, it in enumerate(sec.liste_items):
                    if it.ignore:
                        file.write(f"oui;{it.numero};{it.titre};{it.organisme};{it.description};{it.date_debut};{it.date_fin};{it.logo};{it.url}\n")
                    else : 
                        file.write(f"non;{it.numero};{it.titre};{it.organisme};{it.description};{it.date_debut};{it.date_fin};{it.logo};{it.url}\n")

    def load(self):
        """Charge un CV à partir des fichiers CSV"""
        if self.nouveau:
            return
        
        # on va charger le CV à partir des fichiers CSV
        with open("sections/infos_personnelles.csv",'r',encoding='utf8') as file:
            liste_infos_perso = file.readlines()
            for ligne in liste_infos_perso:
                # on va écrire la valeur dans self.qui_je_suis
                ligne = ligne[:-1]
                key, value = ligne.split(";")
                self.qui_je_suis[key] = value

        # on doit ajouter toutes les sections maintenant
        for fichier in os.listdir("sections"):
            if fichier != "infos_personnelles.csv":
                with open(f"sections/{fichier}",'r',encoding='utf8') as file:
                    lignes_fichier = file.readlines()
                sec = Section()
                ligne_titre = lignes_fichier[0][:-1]
                sec.nom, sec.ignore, sec.type, sec.numero = ligne_titre.split(";")[:4]
                sec.numero = int(sec.numero)
                if sec.ignore == 'True':
                    sec.ignore = True
                else: 
                    sec.ignore = False
                for ligne_it in lignes_fichier[2:]:
                        if ligne_it and len(ligne_it)>1:
                            # on parcourt les items de la section
                            ligne_it = ligne_it[:-1]
                            ignore,no,titre,organisme,description,date_debut,date_fin,logo,url = ligne_it.split(";")
                            if ignore == 'oui':
                                # on l'ajoute avec ignore=True
                                sec.liste_items.append(Item(sec.nb_items,titre,organisme,description,date_debut,date_fin,logo,url,True))
                                
                            else:
                                sec.liste_items.append(Item(sec.nb_items,titre,organisme,description,date_debut,date_fin,logo,url,False))
                            sec.nb_items += 1

                self.liste_sections.append(sec)


    def html_header(self,nom_image:str,style_CV='full'):
        res = ""
        if style_CV == 'full':
            res += "<header>\n"
            res += """ <div class="header_profile">\n"""
            res += """  <div class="header_picture">\n"""
            res += f"""  <img src = "images/{nom_image}" id="profile_picture" />\n"""
            res += """  </div>\n"""
            res += """  <div class="header_sauf_photo">\n"""
            res += f"""    <h1 id="header_nom">{self.qui_je_suis['nom']} </h1>\n"""
            res += f"""    <h2>Né le {self.qui_je_suis['date_naissance']}</h2>\n"""
            res += f"""    <img src="images/logo_mail.png" class="logo_social_media"/> <a href="mailto:{self.qui_je_suis['mail']}" target="_blank">{self.qui_je_suis['mail']}</a>\n"""
            res += f"""    <img src="images/logo_github.png" class="logo_social_media"/> <a href="{self.qui_je_suis['github']}" target="_blank">{self.qui_je_suis['nom_github']}</a>\n"""
            res += f"""    <br />\n    <img src="images/logo_linkedin.png" class="logo_social_media"/> <a href="{self.qui_je_suis['linkedin']}" target="_blank">{self.qui_je_suis['linkedin']}</a>\n"""
            res += f"""    <p>{self.qui_je_suis['motto']}</p>\n"""
            res += """  </div>\n"""
            res += """ </div>\n"""
            res += "</header>\n"
            return res
        elif style_CV == 'onepager':
            return self.html_header(nom_image) # à changer pour les autres styles
        return self.html_header(nom_image)

    def html_footer(self):
        res = "<footer>\n"
        res += """    <p>Ce CV est le produit du projet """
        res += f"""<a href="https://github.com/LouisJustinTALLOT/CV_Maker" target="_blank"><img src="images/logo_github.png" class="logo_social_media"/>LouisJustinTALLOT/CV_Maker</a>"""
        res += """ utilisant le pack d'icônes gratuit <a href="https://streamlineicons.com/" target="_blank">Streamline.</a> """
        res += "</footer>\n"
        return res

    def markdown_header(self):
        res = f"# {self.qui_je_suis['nom']}\n\n"
        res += f"## Né le {self.qui_je_suis['date_naissance']}\n\n"
        res += f"""Mail : [{self.qui_je_suis['mail']}      ](mailto:{self.qui_je_suis['mail']}) | """
        res += f"""Linkedin : [{self.qui_je_suis['linkedin']}  ]({self.qui_je_suis['linkedin']}) | """
        res += f"""Github : [{self.qui_je_suis['nom_github']}]({self.qui_je_suis['github']})\n\n"""
        res += f"""\n\n{self.qui_je_suis['motto']}\n\n"""
        res += "-------------------------------------------\n\n"
        
        return res

    def markdown_footer(self):
        res = "-------------------------------------------\n"
        res += """Ce CV est le produit du projet """
        res += f"""[LouisJustinTALLOT/CV_Maker](https://github.com/LouisJustinTALLOT/CV_Maker)"""
        res += """ utilisant le pack d'icônes gratuit [Streamline](https://streamlineicons.com/)."""
        
        return res

    def to_html(self, style_CV='full'):
        with open("CV.html", 'w', encoding='utf8') as file:
            file.write(html_head())
            file.write("<body>\n")
            file.write("""<div id="main">\n""")
            file.write(self.html_header("photo_lj.jpg"))
            file.write("""<section id="toutes_les_sections">\n""")
            
            self.liste_sections.sort(key=lambda x: x.numero)
            sec:Section
            for sec in self.liste_sections:
                if not sec.ignore:
                    file.write(f"""<section id="{titre_to_nom_de_fichier(sec.nom)}"> \n""")
                    file.write(sec.to_html())
                    file.write(f"""</section> \n""")

            file.write("</section>\n")
            file.write("</div>\n")
            file.write(self.html_footer())
            file.write("</body>\n</html>")

    def to_markdown(self, style_CV='full'):
        with open("CV_md.md", 'w', encoding='utf8') as file:
            file.write(self.markdown_header())
            self.liste_sections.sort(key=lambda x: x.numero)
            sec:Section
            for sec in self.liste_sections:
                if not sec.ignore:
                    file.write(sec.to_markdown())

            file.write(self.markdown_footer())  


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
                cv.to_markdown()

            elif key[0].lower() == 'r':
                if os.path.exists("CV.pdf"):
                    os.remove("CV.pdf")
                if os.path.exists("CV2.pdf"):
                    os.remove("CV2.pdf")
                
                cv.to_html()
                options = {"enable-local-file-access": ""}
                pdfkit.from_file('CV.html', 'CV.pdf', options=options)
                HTML('CV.html').write_pdf('CV2.pdf')

                cv.to_markdown()
                
                if os.path.exists("CV_md.pdf"):
                    os.remove("CV_md.pdf")
                runner = CliRunner()
                Result = runner.invoke(cli.cli, ["-o", "CV_md.pdf", "CV_md.md"])
                


    elif lieu == 'section':
        if not modify:
            while True :
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
    if "infos_personnelles.csv" not in os.listdir("sections"):
        cv = CV(new=True)
        mainloop(cv)
        cv.save()
    else:
        mon_cv = CV()
        mon_cv.load()
        mainloop(mon_cv)
        mon_cv.save()

if __name__ == "__main__":
    main()