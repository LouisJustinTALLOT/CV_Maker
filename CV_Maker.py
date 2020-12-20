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
class Section:
    
    def __init__(self,nom):
        self.nom=nom

class CV:

main()