from math import sqrt
from itertools import product
import numpy as np
import pandas as pd

class Parameter:  #classe dos parâmetros
    def __init__(
        self, name, unit, is_integer, center, lower_limit, upper_limit, delta
    ):  #recebe nome, unidade, se é inteiro, limite inferior, superior e delta
        self.name = name
        self.unit = unit
        self.is_integer = is_integer
        self.center = center
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.delta = delta

class ParameterPrompts: #classe de prompts para as caixas dos parametros
    name_prompt = "Informe o nome do parâmetro que será estudado (e.g. Temperatura, Massa, Molaridade do Soluto, etc)."
    unit_prompt = "Informe as unidades o parâmetro que será estudado (e.g. °C, Kg, mol/L, etc)."
    is_integer_prompt = "Informe se o parâmetro a ser estudado deve ser um número inteiro ou não (e.g. se o parâmetro for o número de impregnações de um catalisador ele deve ser um número inteiro)."
    center_prompt = "Informe o valor central do seu experimento. A variação do parametro será em torno deste valor."
    lower_limit_prompt = "Informe qual o limite inferior possivel para o parâmetro (e.g. a temperatura mínima que o refrigerador utilizado chega é de -20 °C)."
    upper_limit_prompt = "Informe qual o limite superior possivel para o parâmetro (e.g. a temperatura máxima que o forno utilizado chega é de 900 °C)."
    delta_prompt = "Informe a variação tipica do parâmetro desejada em seu experimento. Os valores analisados do parâmetro estarão a uma distância de aproximadamente 1 delta do valor central."

def encode(parameter, value): #codifica os valores reais
    return (value - parameter.center) / parameter.delta

def decode(parameter, value):  #decodifica os valores
    return (value * parameter.delta) + parameter.center

def parameters_test(parameter): #testa todos os parametros
    return_error = []

    for i in range(len(parameter)):
        if parameter[i].center >= parameter[i].upper_limit or parameter[i].center <= parameter[i].lower_limit:
            return_error.append(f"O valor central de {parameter[i].name} inserido não está situado entre os limites inferior e superior. Mude seu valor do centro, ou dos limites.")
    
        if parameter[i].delta > (parameter[i].upper_limit-parameter[i].center):
            return_error.append(f"O valor de delta de {parameter[i].name} inserido foi grande demais. Diminua seu valor de delta, ou aumente o do limite superior, para que o limite superior esteja a pelo menos um delta de distância do centro.")
        
        if parameter[i].delta > (parameter[i].center-parameter[i].lower_limit):
            return_error.append(f"O valor de delta de {parameter[i].name} inserido foi grande demais. Diminua seu valor de delta, ou diminua o do limite inferior, para que o limite inferior esteja a pelo menos um delta de distância do centro.")

        if parameter[i].is_integer and not(isinstance(parameter[i].center, int)):
            return_error.append(f"O valor central de {parameter[i].name} inserido não foi um número inteiro. Como {parameter[i].name} é um número inteiro, o mesmo deve ser válido para seu valor central.")
                    
        if parameter[i].is_integer and not(isinstance(parameter[i].lower_limit, int)):
            return_error.append(f"O valor do limite inferior de {parameter[i].name} inserido não foi um número inteiro. Como {parameter[i].name} é um número inteiro, o mesmo deve ser válido para seu valor do limite inferior.")

        if parameter[i].is_integer and not(isinstance(parameter[i].upper_limit, int)):
            return_error.append(f"O valor do limite superior de {parameter[i].name} inserido não foi um número inteiro. Como {parameter[i].name} é um número inteiro, o mesmo deve ser válido para seu valor do limite superior.")
                    
        if parameter[i].is_integer and not(isinstance(parameter[i].delta, int)):
            return_error.append(f"O valor de delta de {parameter[i].name} inserido não foi um número inteiro. Caso delta não seja inteiro, o planejamento fatorial vai pedir que coordenadas não inteiras sejam analisadas. Como {parameter[i].name} é um número inteiro, o mesmo deve ser válido para suas coordenadas, e portanto, para seu valor de delta.")

    return return_error

class FatorialPlan: #classe do planejamento fatorial
    def __init__(self, parameters_list, alpha, has_integer): #recebe uma lista com os parâmetros, o valor de alfa e se possui pelo menos um parâmetro inteiro
        self.dimensions = len(parameters_list)
        self.parameter = parameters_list
        self.alpha = alpha
        self.has_integer = has_integer

        self.center = [[0] * self.dimensions]

        self.real_center = []
        for i in range(len(self.center)):
            self.real_center.append([])
            for j in range(self.dimensions):
                self.real_center[i].append(decode(self.parameter[j], self.center[i][j]))

        self.cubic = list(product([-1, 1], repeat=self.dimensions))

        self.real_cubic = []
        for i in range(len(self.cubic)):
            self.real_cubic.append([])
            for j in range(self.dimensions):
                self.real_cubic[i].append(decode(self.parameter[j], self.cubic[i][j]))

        self.axial = []
        for i in range(self.dimensions):
            axial_point = [0] * self.dimensions
            axial_point[i] = -self.alpha
            self.axial.append(axial_point)
            axial_point = [0] * self.dimensions
            axial_point[i] = self.alpha
            self.axial.append(axial_point)

        self.real_axial = []
        for i in range(len(self.axial)):
            self.real_axial.append([])
            for j in range(self.dimensions):
                self.real_axial[i].append(decode(self.parameter[j], self.axial[i][j]))

        self.number_of_observations = len(self.center) + len(self.cubic) + len(self.axial)

    def return_plan(self):
        plan = pd.DataFrame()

        plan["Componente"] = []
        for i in range(self.dimensions):
            plan[f"{self.parameter[i].name} Codificada"] = []

        for i in range(self.dimensions):
            plan[f"{self.parameter[i].name} Real"] = []

        # Adding Center points
        for j in range(len(self.center)):
            plan.loc[len(plan)] = ["Central"] + np.round(self.center[j], 3).tolist() + np.round(self.real_center[j], 3).tolist()

        # Adding Cubic points
        for j in range(len(self.cubic)):
            plan.loc[len(plan)] = ["Cúbica"] + np.round(self.cubic[j], 3).tolist() + np.round(self.real_cubic[j], 3).tolist()

        # Adding Axial points
        for j in range(len(self.axial)):
            plan.loc[len(plan)] = ["Axial"] + np.round(self.axial[j], 3).tolist() + np.round(self.real_axial[j], 3).tolist()

        return plan

class FatorialPlanPrompts:
    alpha_prompt = "Informe o valor de alfa, usado para a escolha dos pontos axiais do planejamento fatorial."
    center_info = "Este é o ponto central do planejamento fatorial. Ele assim é chamado pois o planejamento é construido em volta dele. Devem ser feitas de 3 a 5 repetições do experimento no ponto central, pois ele será importante para estimar a variância dos dados."
    cubic_info = "Esses são os pontos cúbicos do planejamento fatorial. Eles assim são chamados pois no espaço de planejamento eles formam um quadrado (para 2 parâmetros), um cubo (para 3 parâmetros), ou um hypercubo (para mais de 3 parâmetros)."
    axial_info = "Esses são os pontos axiais do planejamento fatorial. Eles assim são chamados pois ficam sobre os eixos do espaço de planejamento."

def return_real_plan(fatorial_plan, plan): #possivelmente substituido pelo DataFrame
    real_plan = []

    for i in range(len(plan)):
        real_plan.append([])
        for j in range(fatorial_plan.dimensions):
            real_plan[i].append(decode(fatorial_plan.parameter[j], plan[i][j]))

    return np.round(real_plan, 3)

def fatorial_plan_test(fatorial_plan): #testa o alfa
    return_error = []

    if fatorial_plan.has_integer and not(isinstance(fatorial_plan.alpha, int)):
        return_error.append("O valor de alpha inserido não foi um número inteiro. Caso alpha não seja inteiro, o planejamento fatorial vai pedir que coordenadas não inteiras sejam analisadas. Como o parâmetro é um número inteiro, o mesmo deve ser válido para suas coordenadas, e portanto, para o valor de alpha.")
        
    if fatorial_plan.alpha < 1:
        return_error.append("O valor de alpha inserido foi menor que 1. Dessa forma, os pontos axiais do planejamento fatorial vão ficar mais próximos do que a distancia típica, o delta, escolhida para cada parâmetro.")
        
    if fatorial_plan.alpha > sqrt(fatorial_plan.dimensions):
        return_error.append("O valor de alpha inserido foi maior que a raiz quadrada do número de parâmetros a serem estudados. Dessa forma, os pontos axiais do planejamento fatorial vão ficar muito longe do ponto central, e portanto a analise dos resultados referentes a esses pontos podem perder relevância.") 
        
    for i in range(len(fatorial_plan.parameter)):
        if fatorial_plan.alpha > encode(fatorial_plan.parameter[i], fatorial_plan.parameter[i].upper_limit):
            return_error.append(f"O valor de alfa inserido foi grande demais. Diminua o valor de alfa, ou aumente o do limite superior de {fatorial_plan.parameter[i].name}, para que o valor codificado do limite superior de {fatorial_plan.parameter[i].name} esteja a pelo menos um alfa de distância do centro.")

        if fatorial_plan.alpha > - encode(fatorial_plan.parameter[i], fatorial_plan.parameter[i].lower_limit):
                return_error.append(f"O valor de alfa inserido foi grande demais. Diminua o valor de alfa, ou diminua o do limite inferior de {fatorial_plan.parameter[i].name}, para que o valor codificado do limite inferior de {fatorial_plan.parameter[i].name} esteja a pelo menos um alfa de distância do centro.")
        
    return return_error