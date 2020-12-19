import json


class Section:
    
    def __init__(self,nom):
        self.nom=nom

class CV:

    def __init__(self,sections):
        self.liste_sections=sections