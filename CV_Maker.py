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


class Section:
    
    def __init__(self,nom):
        self.nom=nom

class CV:

main()