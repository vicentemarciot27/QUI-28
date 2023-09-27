import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
from Entregando_perifericos import Parameter

class LinearModel: #modelo linear
    def __init__(self, data_frame, parameters_list):
        self.data_plan = data_frame
        self.paramter = parameters_list
        self.number_of_observations = self.data_plan.shape[1]
        self.number_of_parameters = len(self.parameter)
        self.number_of_coefficients = 1 + self.number_of_parameters

        self.response_matrix = self.data_plan["Resposta"].values

        matrix = []
        for index, row in self.data_plan.iterrows():
            matrix.append([1])
            for i in range(self.number_of_parameters):
                matrix[index].append(row[self.parameter[i].name])

        self.planning_matrix = np.array(matrix)

        self.coefficients_matrix = (np.linalg.inv(np.transpose(self.planning_matrix)@self.planning_matrix))@np.transpose(self.planning_matrix)@self.response_matrix

        self.expected_response_matrix = self.planning_matrix@self.coefficients_matrix

        self.mean_response = np.mean(self.response_matrix)

        self.SQR = np.sum(np.square(self.expected_response_matrix - self.mean_response))
        self.MQR = self.SQR/(self.number_of_coefficients - 1)

        self.SQr = np.sum(np.square(np.subtract(self.response_matrix, self.expected_response_matrix)))
        self.MQr = self.SQr/(self.number_of_observations - self.number_of_coefficients)

        self.SQT = np.sum(np.square(self.response_matrix - self.mean_response))
        
        self.explained_variation = self.SQR/self.SQT
    
class QuadraticModel: #modelo quadratico
    def __init__(self, data_frame, parameters_list):
        self.data_plan = data_frame
        self.paramter = parameters_list
        self.number_of_observations = self.data_plan.shape[1]
        self.number_of_parameters = len(self.parameter)
        self.number_of_coefficients = 1 + 2*self.number_of_parameters + (self.number_of_parameters*(self.number_of_parameters - 1))/2

        self.response_matrix = self.data_plan["Resposta"].values

        matrix = []
        cross_terms = (self.number_of_parameters*(self.number_of_parameters - 1))/2

        for index, row in self.data_plan.iterrows():
            matrix.append([1])
            for i in range(self.number_of_parameters):
                matrix[index].append(row[self.parameter[i].name])

            for i in range(self.number_of_parameters):
                matrix[index].append(row[self.parameter[i].name]**2)

            for i in range(cross_terms):
                for j in range(cross_terms):
                    if(j>i):
                        matrix[index].append(row[self.parameter[i].name] * row[self.parameter[j].name])

        self.planning_matrix = np.array(matrix)

        self.coefficients_matrix = (np.linalg.inv(np.transpose(self.planning_matrix)@self.planning_matrix))@np.transpose(self.planning_matrix)@self.response_matrix

        self.expected_response_matrix = self.planning_matrix@self.coefficients_matrix

        self.mean_response = np.mean(self.response_matrix)

        self.SQR = np.sum(np.square(self.expected_response_matrix - self.mean_response))
        self.MQR = self.SQR/(self.number_of_coefficients - 1)

        self.SQr = np.sum(np.square(np.subtract(self.response_matrix, self.expected_response_matrix)))
        self.MQr = self.SQr/(self.number_of_observations - self.number_of_coefficients)

        self.SQT = np.sum(np.square(self.response_matrix - self.mean_response))
        
        self.explained_variation = self.SQR/self.SQT
    
def F_test(model):
        MQ_ratio = model.MQR/model.MQr
        F_value = sp.stats.f.ppf(.95, model.number_of_coefficients - 1, model.number_of_observations - model.number_of_coefficients)
        return_string = []

        return_string.append(f"A razão entre a média quadratica devido a regrassão e a média quadrática residual é de {MQ_ratio}.")
        return_string.append(f"O valor crítico F para um nível de significância de 95%, {model.number_of_coefficients - 1} graus de liberdade da média quadrática devido a regressão e {model.number_of_observations - model.number_of_coefficients} graus de liberdade da média quadrática residual é de {F_value}.")

        if(MQ_ratio > F_value):
            return_string.append("A razão entre as média quadráticas é maior que o valor crítico F. Portanto, a regressão é estatisticamente relevante.")
        else:
            return_string.append("A razão entre as média quadráticas não é maior que o valor crítico F. Portanto, a regressão não é estatisticamente relevante.")
        
        return return_string