from math import sqrt
from itertools import product

class Parameter: #classe dos parâmetros
    name_prompt = "Informe o nome do parâmetro que será estudado (e.g. Temperatura, Massa, Molaridade do Soluto, etc)."
    unit_prompt = "Informe as unidades o parâmetro que será estudado (e.g. °C, Kg, mol/L, etc)."
    is_integer_prompt = "Informe se o parâmetro a ser estudado deve ser um número inteiro ou não (e.g. se o parâmetro for o número de impregnações de um catalisador ele deve ser um número inteiro)."
    center_prompt = "Informe o valor central do seu experimento. A variação do parametro será em torno deste valor."
    lower_limit_prompt = "Informe qual o limite inferior possivel para o parâmetro (e.g. a temperatura mínima que o refrigerador utilizado chega é de -20 °C)."
    upper_limit_prompt = "Informe qual o limite superior possivel para o parâmetro (e.g. a temperatura máxima que o forno utilizado chega é de 900 °C)."
    delta_prompt = "Informe a variação tipica do parâmetro desejada em seu experimento. Os valores analisados do parâmetro estarão a uma distância de aproximadamente 1 delta do valor central."

    def __init__(self, name, unit, is_integer, center, lower_limit, upper_limit, delta): #recebe nome, unidade, se é inteiro, limite inferior, superior e delta
        self.name = name
        self.unit = unit
        self.is_integer = is_integer
        self.center = center
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.delta = delta

        if self.is_integer: #caso o parâmetro seja inteiro, testa se os casos recebido são consistentes
            Parameter.center_integer_check()
            
            Parameter.lower_limit_integer_check()
            
            Parameter.upper_limit_integer_check()
            
            Parameter.delta_integer_check()
    
    def center_integer_check(self): #imprime que o centro não é inteiro
        if not(isinstance(self.center, int)):
            return "O valor central inserido não foi um número inteiro. Como o parâmetro é um número inteiro, o mesmo deve ser válido para o valor central."
                
    def lower_limit_integer_check(self): #imprime que o limite inferior não é inteiro
        if not(isinstance(self.lower_limit, int)):
            return "O valor do limite inferior inserido não foi um número inteiro. Como o parâmetro é um número inteiro, o mesmo deve ser válido para o valor do limite inferior."

    def upper_limit_integer_check(self): #imprime que o limite superior não é inteiro
        if not(isinstance(self.upper_limit, int)):
            return "O valor do limite superior inserido não foi um número inteiro. Como o parâmetro é um número inteiro, o mesmo deve ser válido para o valor do limite superior."
                
    def delta_integer_check(self): #imprime que o delta não é inteiro
        if not(isinstance(self.delta, int)):
            return "O valor de delta inserido não foi um número inteiro. Caso delta não seja inteiro, o planejamento experimental vai pedir que coordenadas não inteiras sejam analisadas. Como o parâmetro é um número inteiro, o mesmo deve ser válido para suas coordenadas, e portanto, para o valor de delta."
    
    def encode(self, value): #codifica os valores reais
        return (value - self.center) / self.delta
    
    def decode(self, value): #decodifica os valores
        return (value * self.delta) + self.center

class Point: #To achando esse Point meio desnecessário. Se pá, melhor tirar.
    def __init__(self, number_of_parameters):
        self.dimensions = number_of_parameters
        self.coordinates = []

class FatorialPlan: #classe do planejamento fatorial
    alpha_prompt = "Informe o valor de alpha, usado para a escolha dos pontos axiais do planejamento fatorial."

    def __init__(self, parameters_list, alpha, has_integer): #recebe uma lista com os parâmetros, o valor de alpha e se possui pelo menos um parâmetro inteiro
        self.dimensions = len(parameters_list)
        self.parameters_list = parameters_list
        self.alpha = alpha
        self.has_integer = has_integer

        if self.has_integer and not(isinstance(self.alpha, int)): #checa se alpha é inteiro
            alpha_integer_check()

        if self.alpha < 1: #checa se alpha não é muito pequeno
            alpha_small_check()
                
        elif self.alpha > sqrt(self.dimensions): #checa se alpha não é muito grande
            alpha_big_check()

        def alpha_integer_check():
            return "O valor de alpha inserido não foi um número inteiro. Caso alpha não seja inteiro, o planejamento fatorial vai pedir que coordenadas não inteiras sejam analisadas. Como o parâmetro é um número inteiro, o mesmo deve ser válido para suas coordenadas, e portanto, para o valor de alpha."

        def alpha_small_check():
            return "O valor de alpha inserido foi menor que 1. Dessa forma, os pontos axiais do planejamento fatorial vão ficar mais próximos do que a distancia típica, o delta, escolhida para cada parâmetro."

        def alpha_big_check():
            return "O valor de alpha inserido foi maior que a raiz quadrada do número de parâmetros a serem estudados. Dessa forma, os pontos axiais do planejamento fatorial vão ficar muito longe do ponto central, e portanto a analise dos resultados referentes a esses pontos podem perder relevância."

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
        
    return_center_info = "Este é o ponto central do planejamento fatorial. Ele assim é chamado pois o planejamento é construido em volta dele. Devem ser feitas de 3 a 5 repetições do experimento no ponto central, pois ele será importante para estimar a variância dos dados."

    def return_center(self):
        real_plan = []

        for i in range(self.dimensions):
            real_plan.append(self.parameters_list[i].decode(self.center[i]))

        return real_plan
    
    return_cubic_info = "Esses são os pontos cúbicos do planejamento fatorial. Eles assim são chamados pois no espaço de planejamento eles formam um quadrado (para 2 parâmetros), um cubo (para 3 parâmetros), ou um hypercubo (para mais de 3 parâmetros)."
    
    def return_cubic(self):
        real_plan = []

        for i in range(len(self.cubic)):
            real_plan.append([])
            for j in range(len(self.dimensions)):
                real_plan[i].append(self.parameters_list[j].decode(self.cubic[i][j]))
    
        return real_plan

    return_axial_info = "Esses são os pontos axiais do planejamento fatorial. Eles assim são chamados pois ficam sobre os eixos do espaço de planejamento."
    
    def return_axial(self):
        real_plan = []

        for i in range(len(self.axial)):
            real_plan.append([])
            for j in range(len(self.dimensions)):
                real_plan[i].append(self.parameters_list[j].decode(self.axial[i][j]))
    
        return real_plan