import datetime

class Mesure:
    def __init__(self, p_donneeMesure):
        self.dateHeureMesure = datetime.datetime.now()
        self.donneeMesure = p_donneeMesure
        
    def __repr__(self):
        return f"{self.dateHeureMesure} , {self.donneeMesure}"
    
    