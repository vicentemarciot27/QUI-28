import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import Entregando_perifericos

class PlanData: #salva os dados recebidos dos experimentos no plano fatorial
    def __init__(self, fatorial_plan, center_data_list, cubic_data_list, axial_data_list): #recebe o plano fatorial, uma lista com os dados coletados nos pontos centrais, uma com os coletados nos cubicos e uma com os coletado nos axiais
        self.center = center_data_list
        self.cubic = cubic_data_list
        self.axial = axial_data_list
        self.fatorial_plan = fatorial_plan

class LinearModel: #modelo linear
    def __init__(self, plan_data): #recebe o plano de dados
        self.dependent_variables = np.transpose(np.array(plan_data.center + plan_data.cubic + plan_data.axial))
        
        lista = []
        i=0
        
        for j in range(len(plan_data.center)):
            lista.append([1])
            for k in range(plan_data.fatorial_plan.dimensions):
                lista[i].append(plan_data.fatorial_plan.center[k])
            i += 1

        for j in range(len(plan_data.cubic)):
            lista.append([1])
            for k in range(plan_data.fatorial_plan.dimensions):
                lista[i].append(plan_data.fatorial_plan.cubic[j][k])
            i += 1
        
        for j in range(len(plan_data.axial)):
            lista.append([1])
            for k in range(plan_data.fatorial_plan.dimensions):
                lista[i].append(plan_data.fatorial_plan.axial[j][k])
            i += 1

        self.independent_variables = np.array(lista)

        self.coeficients = (np.linalg.inv(np.transpose(self.independent_variables)@self.independent_variables))@np.transpose(self.independent_variables)@self.dependent_variables