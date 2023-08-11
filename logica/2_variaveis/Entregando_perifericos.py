import math

class variable:
    def __init__(self, name, center, delta, upper_limit, lower_limit, is_integer):
        self.name = name
        self.center = center
        self.delta = delta
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.is_integer = is_integer
    
    def code(self, value):
        return (value-self.center)/self.delta
    
    def decode(self, value):
        return (value*self.delta)+self.center

def experimental_points(variables, ):
    codes = [0, 1, math.sqrt(len(variables))]
    answer = []
    i=0
    j=0

    # while(true)


