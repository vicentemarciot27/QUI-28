import itertools
import math

class Parameter:
    def __init__(self, name, unit, is_integer, center, lower_limit, upper_limit, delta):
        self.name = name
        self.unit = unit
        self.is_integer = is_integer
        self.center = center
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.delta = delta
        
    def code(self, value):
        return (value - self.center) / self.delta
    
    def decode(self, value):
        return (value * self.delta) + self.center

class Point:
    def __init__(self, number_of_parameters):
        self.dimensions = number_of_parameters
        self.coordinates = []

class FatorialPlan:
    def __init__(self, number_of_parameters, alpha):
        self.dimensions = number_of_parameters
        self.alpha = alpha

        self.fatorial = list(itertools.product([-1, 1], repeat=number_of_parameters))
        self.axial = []
        for i in range(number_of_parameters):
            axial_point = [0] * number_of_parameters
            axial_point[i] = -alpha
            self.axial.append(axial_point)
            axial_point = [0] * number_of_parameters
            axial_point[i] = alpha
            self.axial.append(axial_point)

def return_plan(parameters_list, fatorial_plan_list):
    real_plan = []

    for i in range(len(fatorial_plan_list)):
        real_plan.append([])

        for j in range(len(parameters_list)):
            real_plan[i].append(parameters_list[j].decode(fatorial_plan_list[i][j]))

    return real_plan

param1 = Parameter("Temperature", "°C", False, 0, 0, 100, 1)
param2 = Parameter("Pressure", "kPa", False, 0, 50, 150, 2)
param3 = Parameter("Bortolazzos", "Tenentes", True, 0, 0, 100, 3)

parameters_list = [param1, param2, param3]
fatorial = FatorialPlan(len(parameters_list), math.sqrt(2))

fatorial_plan_list = fatorial.fatorial

real_plan = return_plan(parameters_list, fatorial_plan_list)

for point in real_plan:
    print(point)
