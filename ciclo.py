from datetime import date
'''
  Verifica o trimestre atual e quais okrs são desse trimestre
'''

class Ciclo:
    def __init__(self):
        self.hoje = date.today()
        self.ciclo = 0
        

    def ciclo_def(self):
        """retorna o trimestre atual"""
        if 1 <= self.hoje.month <= 3:
            tri = 1
        elif 4 <= self.hoje.month <= 6:
            tri = 2
        elif 7 <= self.hoje.month <= 9:
            tri = 3
        else:
            tri = 4  
        self.ciclo = tri
      