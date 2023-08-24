from math import sqrt
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

        if self.is_integer:
            if not(isinstance(self.center, int)):
                print("O valor central inserido não foi um número inteiro. Como o parâmetro é um número inteiro, o mesmo deve ser válido para o valor central.")

            if not(isinstance(self.lower_limit, int)):
                print("O valor do limite inferior inserido não foi um número inteiro. Como o parâmetro é um número inteiro, o mesmo deve ser válido para o valor do limite inferior.")

            if not(isinstance(self.upper_limit, int)):
                print("O valor do limite superior inserido não foi um número inteiro. Como o parâmetro é um número inteiro, o mesmo deve ser válido para o valor do limite superior.")

            if not(isinstance(self.delta, int)):
                print("O valor de delta inserido não foi um número inteiro. Caso delta não seja inteiro, o planejamento experimental vai pedir que coordenadas não inteiras sejam analisadas. Como o parâmetro é um número inteiro, o mesmo deve ser válido para suas coordenadas, e portanto, para o valor de delta.")
    
    def encode(self, value):
        return (value - self.center) / self.delta
    
    def decode(self, value):
        return (value * self.delta) + self.center

class Point: #To achando esse Point meio desnecessário. Se pá, melhor tirar.
    def __init__(self, number_of_parameters):
        self.dimensions = number_of_parameters
        self.coordinates = []

class FatorialPlan:
    alpha_prompt = "Informe o valor de alpha, usado para a escolha dos pontos axiais do planejamento fatorial."

    def __init__(self, parameters_list, alpha, has_integer):
        self.dimensions = len(parameters_list)
        self.parameters_list = parameters_list
        self.alpha = alpha
        self.has_integer = has_integer

        if self.has_integer and not(isinstance(self.alpha, int)):
            print("O valor de alpha inserido não foi um número inteiro. Caso alpha não seja inteiro, o planejamento fatorial vai pedir que coordenadas não inteiras sejam analisadas. Como o parâmetro é um número inteiro, o mesmo deve ser válido para suas coordenadas, e portanto, para o valor de alpha.")

        if self.alpha < 1:
            print("O valor de alpha inserido foi menor que 1. Dessa forma, os pontos axiais do planejamento fatorial vão ficar mais próximos do que a distancia típica, o delta, escolhida para cada parâmetro.")
        elif self.alpha > sqrt(self.dimensions):
            print("O valor de alpha inserido foi maior que a raiz quadrada do número de parâmetros a serem estudados. Dessa forma, os pontos axiais do planejamento fatorial vão ficar muito longe do ponto central, e portanto a analise dos resultados referentes a esses pontos podem perder relevância.")

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