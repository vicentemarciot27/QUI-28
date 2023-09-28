import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Entregando_perifericos import Parameter
from math import floor
from math import ceil

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

        self.residuals_matrix = np.subtract(self.response_matrix, self.expected_response_matrix)

        self.mean_response = np.mean(self.response_matrix)

        self.SQR = np.sum(np.square(self.expected_response_matrix - self.mean_response))
        self.MQR = self.SQR/(self.number_of_coefficients - 1)

        self.SQr = np.sum(np.square(self.residuals_matrix))
        self.MQr = self.SQr/(self.number_of_observations - self.number_of_coefficients)

        self.SQT = np.sum(np.square(self.response_matrix - self.mean_response))
        
        self.explained_variation = self.SQR/self.SQT

    def linear_plot(self):
        if(self.number_of_parameters == 1):
            x = np.linspace(floor(self.data_plan[self.paramter[0].name].min()), ceil(self.data_plan[self.paramter[0].name].max()), 100)
            y = self.coefficients_matrix[0] + x*self.coefficients_matrix[1]

            plt.scatter(self.data_plan[self.parameter[0].name], self.data_plan["Resposta"])
            plt.plot(x, y)
            plt.xlabel(f"{self.parameter[0].name} ({self.parameter[0].unit})")
            plt.ylabel("Resposta")
            plt.title(f"Resposta em função de {self.parameter[0].name}")

            return plt.gcf()
        elif(self.number_of_parameters == 2):
            x_lin = np.linspace(floor(self.data_plan[self.paramter[0].name].min()), ceil(self.data_plan[self.paramter[0].name].max()), 100)
            y_lin = np.linspace(floor(self.data_plan[self.paramter[1].name].min()), ceil(self.data_plan[self.paramter[1].name].max()), 100)

            x, y = np.meshgrid(x_lin, y_lin)
            z = self.coefficients_matrix[0] + x*self.coefficients_matrix[1] + y*self.coefficients_matrix[2]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.data_plan[self.parameter[0].name], self.data_plan[self.parameter[1].name], self.data_plan["Resposta"])
            ax.plot_surface(x, y, z, cmap='viridis')
            ax.set_xlabel(f"{self.parameter[0].name} ({self.parameter[0].unit})")
            ax.set_ylabel(f"{self.parameter[1].name} ({self.parameter[1].unit})")
            ax.set_zlabel("Resposta")
            ax.set_title(f"Resposta em função de {self.parameter[0].name} e {self.parameter[0].name}")

            return plt.gcf()
        else:
            return 0

    
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

        self.residuals_matrix = np.subtract(self.response_matrix, self.expected_response_matrix)

        self.mean_response = np.mean(self.response_matrix)

        self.SQR = np.sum(np.square(self.expected_response_matrix - self.mean_response))
        self.MQR = self.SQR/(self.number_of_coefficients - 1)

        self.SQr = np.sum(np.square(self.residuals_matrix))
        self.MQr = self.SQr/(self.number_of_observations - self.number_of_coefficients)

        self.SQT = np.sum(np.square(self.response_matrix - self.mean_response))
        
        self.explained_variation = self.SQR/self.SQT

    def quadratic_plot(self):
        if(self.number_of_parameters == 1):
            x = np.linspace(floor(self.data_plan[self.paramter[0].name].min()), ceil(self.data_plan[self.paramter[0].name].max()), 100)
            y = self.coefficients_matrix[0] + x*self.coefficients_matrix[1] + (x**2)*self.coefficients_matrix[2]

            plt.scatter(self.data_plan[self.parameter[0].name], self.data_plan["Resposta"])
            plt.plot(x, y)
            plt.xlabel(f"{self.parameter[0].name} ({self.parameter[0].unit})")
            plt.ylabel("Resposta")
            plt.title(f"Resposta em função de {self.parameter[0].name}")

            return plt.gcf()
        elif(self.number_of_parameters == 2):
            x_lin = np.linspace(floor(self.data_plan[self.paramter[0].name].min()), ceil(self.data_plan[self.paramter[0].name].max()), 100)
            y_lin = np.linspace(floor(self.data_plan[self.paramter[1].name].min()), ceil(self.data_plan[self.paramter[1].name].max()), 100)

            x, y = np.meshgrid(x_lin, y_lin)
            z = self.coefficients_matrix[0] + x*self.coefficients_matrix[1] + y*self.coefficients_matrix[2] + (x**2)*self.coefficients_matrix[3] + (y**2)*self.coefficients_matrix[4] + (x*y)*self.coefficients_matrix[5]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.data_plan[self.parameter[0].name], self.data_plan[self.parameter[1].name], self.data_plan["Resposta"])
            ax.plot_surface(x, y, z, cmap='viridis')
            ax.set_xlabel(f"{self.parameter[0].name} ({self.parameter[0].unit})")
            ax.set_ylabel(f"{self.parameter[1].name} ({self.parameter[1].unit})")
            ax.set_zlabel("Resposta")
            ax.set_title(f"Resposta em função de {self.parameter[0].name} e {self.parameter[0].name}")

            return plt.gcf()
        else:
            return 0
    
def F_test(model): #realiza o teste F
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

def data_plan_plot(data_frame, parameter): #plota os dados coletados
    dimensions = len(parameter)

    if(dimensions == 1):
        plt.scatter(data_frame[parameter[0].name], data_frame["Resposta"])
        plt.xlabel(f"{parameter[0].name} ({parameter[0].unit})")
        plt.ylabel("Resposta")
        plt.title(f"Resposta em função de {parameter[0].name}")

        return plt.gcf()
    elif(dimensions == 2):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(data_frame[parameter[0].name], data_frame[parameter[1].name], data_frame["Resposta"])
        ax.set_xlabel(f"{parameter[0].name} ({parameter[0].unit})")
        ax.set_ylabel(f"{parameter[1].name} ({parameter[1].unit})")
        ax.set_zlabel("Resposta")
        ax.set_title(f"Resposta em função de {parameter[0].name} e {parameter[0].name}")

        return plt.gcf()
    else:
        return 0

def residuals_expectations_plot(model): #plota os resíduos pela resposta prevista
    plt.scatter(model.expected_response_matrix, model.residuals_matrix)
    plt.xlabel("Resposta prevista")
    plt.ylabel("Resíduos")
    plt.title("Resíduos em fução das respostas previstas")

    return plt.gcf()

def residuals_parameters_plot(model): #plota os resíduos por cada parâmetro
    fig, axs = plt.subplots(floor(model.number_of_parameters), ceil(model.number_of_parameters), figsize=(10, 4))

    for i in range(model.number_of_parameters):
        axs[i].scatter(model.data_plan[model.parameter[i].name], model.residuals_matrix)
        axs[i].set_xlabel(f"{model.parameter[i].name} ({model.parameter[i].unit})")
        axs[i].set_ylabel("Resíduos")
        axs[i].set_title(f"Resíduos em função de {model.parameter[i].name} e {model.parameter[i].name}")

    plt.tight_layout()

    return fig