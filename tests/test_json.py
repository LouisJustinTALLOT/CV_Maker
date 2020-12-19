import json

class Test:
    def __init__(self, name, age, composition):
        self.nom = name
        self.duree=age
        self.composition = composition

test1 = Test("Jean Pierre", 24, [1,2,3,4])

jsonstr = json.dumps(test1.__dict__)
print(jsonstr)