from itertools import product

class Parameter:
    name_prompt = "Informe o nome do parâmetro que será estudado (e.g. Temperatura, Massa, Molaridade do Soluto, etc)."
    unit_prompt = "Informe as unidades o parâmetro que será estudado (e.g. °C, Kg, mol/L, etc)."
    is_integer_prompt = "Informe se o parâmetro a ser estudado deve ser um número inteiro ou não (e.g. se o parâmetro for o número de impregnações de um catalisador ele deve ser um número inteiro)."
    center_prompt = "Informe o valor central do seu experimento. A variação do parametro será em torno deste valor."
    lower_limit_prompt = "Informe qual o limite inferior possivel para o parâmetro (e.g. a temperatura mínima que o refrigerador utilizado chega é de -20 °C)."
    upper_limit_prompt = "Informe qual o limite superior possivel para o parâmetro (e.g. a temperatura máxima que o forno utilizado chega é de 900 °C)."
    delta_prompt = "Informe a variação tipica do parâmetro desejada em seu experimento. Os valores analisados do parâmetro estarão a uma distância de aproximadamente 1 delta do valor central."

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
    def __init__(self, parameters_list, alpha):
        self.dimensions = len(parameters_list)
        self.parameters_list = parameters_list
        self.alpha = alpha

        self.center = [0] * self.dimensions

        self.cubic = list(product([-1, 1], repeat=self.dimensions))

        self.axial = []
        for i in range(self.dimensions):
            axial_point = [0] * self.dimensions
            axial_point[i] = -alpha
            self.axial.append(axial_point)
            axial_point = [0] * self.dimensions
            axial_point[i] = alpha
            self.axial.append(axial_point)
        
    def return_center(self):
        real_plan = []

        for i in range(self.dimensions):
            real_plan.append(self.parameters_list[i].decode(self.center[i]))

        return real_plan
    
    def return_cubic(self):
        real_plan = []

        for i in range(len(self.cubic)):
            real_plan.append([])
            for j in range(len(self.dimensions)):
                real_plan[i].append(self.parameters_list[j].decode(self.cubic[i][j]))
    
        return real_plan

    def return_axial(self):
        real_plan = []

        for i in range(len(self.axial)):
            real_plan.append([])
            for j in range(len(self.dimensions)):
                real_plan[i].append(self.parameters_list[j].decode(self.axial[i][j]))
    
        return real_plan


def return_plan(parameters_list, fatorial_plan_list): #Função desatualizada. Tirá-la posteriormente.
    real_plan = []

    for i in range(len(fatorial_plan_list)):
        real_plan.append([])

        for j in range(len(parameters_list)):
            real_plan[i].append(parameters_list[j].decode(fatorial_plan_list[i][j]))

    return real_plan