import itertools

class paramter: #parametros são as variaveis a serem analisadas
    def __init__(self, name, unit, is_integer, center, lower_limit, upper_limit, delta): #name e unit é str, is_integer é bool, e o resto é float
        self.name = name
        self.unit = unit
        self.is_integer = is_integer 
        self.center = center
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.delta = delta
        
    def code(self, value): #recebe o valor real e retorna o valor codificado
        return (value-self.center)/self.delta
    
    def decode(self, value): #recebe o valor codificado e retorna o valor real
        return (value*self.delta)+self.center

class point: #um ponto experimental
    def __init__ (self, number_of_paramters):
        self.dimensions = number_of_paramters
        self.coordinates = []

class fatorial_plan: #planejamento fatorial
    def __init__(self, number_of_paramters, alpha):
        self.dimensions = number_of_paramters
        self.alpha = alpha

        self.central = list(itertools.combinations_with_replacement([0], number_of_paramters))
        self.fatorial = list(itertools.combinations_with_replacement([-1, 1], number_of_paramters))
        self.axial = []

        for i in range(number_of_paramters):
            self.axial.append([])
            for j in range(number_of_paramters):
                if j==i:
                    self.axial[i].append(self.alpha)
                else:
                    self.axial[i].append(0)