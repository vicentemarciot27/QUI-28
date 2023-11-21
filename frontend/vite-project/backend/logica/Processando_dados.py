import numpy as np
import scipy as sp
from scipy.optimize import minimize
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from logica.Entregando_perifericos import Parameter
from math import floor
from math import ceil
from math import sqrt

class LinearModel: #classe do modelo linear
    def __init__(self, data_frame):
        self.column = data_frame.columns
        self.data_plan = data_frame.sort_values(by=self.column)
        self.number_of_observations = len(self.data_plan)
        self.number_of_parameters = len(self.column) - 1
        self.number_of_levels = self.data_plan[self.column[0]].nunique()
        self.number_of_coefficients = 1 + self.number_of_parameters

        self.response_matrix = self.data_plan[self.column[-1]].values

        matrix = []
        for i in range(self.number_of_observations):
            matrix.append([1])
            for j in range(self.number_of_parameters):
                matrix[i].append(self.data_plan.at[i, self.column[j]])

        self.planning_matrix = np.array(matrix)
        self.coefficients_matrix = (np.linalg.inv(np.transpose(self.planning_matrix)@self.planning_matrix))@np.transpose(self.planning_matrix)@self.response_matrix
        self.expected_response_matrix = self.planning_matrix@self.coefficients_matrix
        self.residuals_matrix = np.subtract(self.response_matrix, self.expected_response_matrix)
        self.mean_response = np.mean(self.response_matrix)

        self.SQR = np.sum(np.square(self.expected_response_matrix - self.mean_response))
        self.MQR = self.SQR/(self.number_of_coefficients - 1)

        self.SQr = np.sum(np.square(self.residuals_matrix))
        self.MQr = self.SQr/(self.number_of_observations - self.number_of_coefficients)

        no_response = self.data_plan.drop(columns=[self.column[-1]])
        reference_line = no_response.loc[0]
        sum_i = [0]
        number_i = [0]
        average_i = [0]
        i = 0

        for j in range(self.number_of_observations):
            current_line = no_response.loc[j]
            if current_line != reference_line:
                reference_line = current_line
                average_i[i] = sum_i[i]/number_i[i]
                sum_i.append(0)
                number_i.append(0)
                average_i.append(0)
                i += 1
            
            sum_i[i] += self.data_plan.loc[j, self.column[-1]]
            number_i[i] += 1

        self.SQfaj = 0
        self.SQep = 0
        i = 0

        for j in range(self.number_of_observations):
            current_line = no_response.loc[j]
            if current_line != reference_line:
                reference_line = current_line
                i += 1
            
            self.SQfaj += (self.expected_response_matrix[j] - average_i[i])*(self.expected_response[j] - average_i[i])
            self.SQep += (self.response_matrix[j] - average_i[i])*(self.response_matrix[j] - average_i[i])

        self.MQfaj = self.SQfaj/(self.number_of_levels-self.number_of_parameters)
        self.MQep = self.SQep/(self.number_of_observations-self.number_of_levels)

        self.SQT = np.sum(np.square(self.response_matrix - self.mean_response))
        
        self.explained_variation = self.SQR/self.SQT
        self.maximum_explainable_variation = (self.SQT-self.SQep)/self.SQT

        self.covariance_matrix = np.linalg.inv(np.transpose(self.planning_matrix)@self.planning_matrix) * self.MQr

    def coefficients_table(self): #cria DataFrame com coeficientes e erros
        table = pd.DataFrame()

        table["Coeficiente"] = [1]

        for i in range(self.number_of_coefficients):
            table.loc[i+1, "Coeficientes"] = [f"X{i+1}"]
        
        table["Erros-Padrão"] = []
        i = 0
        
        for i in range(self.number_of_coefficients):
            table.loc[i, "Erros-Padrão"] = [sqrt(self.covariance_matrix[i][i])]

        return table
    
    def expected_response(self, point): #calcula resposta esperada pelo modelo para um ponto do dominio
        ans = self.coefficients_matrix[0]
        for i in range(self.number_of_parameters):
            ans += point[i]*self.coefficients_matrix[i+1]

        return ans
    
    def linear_plot(self): #plota gráfico do modelo linear
        fig = plt.figure()
        
        if(self.number_of_parameters == 1):
            x = np.linspace(floor(self.data_plan[self.column[0]].min()), ceil(self.data_plan[self.column[0]].max()), 100)
            y = self.coefficients_matrix[0] + x*self.coefficients_matrix[1]

            plt.scatter(self.data_plan[self.column[0]], self.data_plan[self.column[-1]])
            plt.plot(x, y)
            plt.xlabel(f"{self.column[0]}")
            plt.ylabel(self.column[-1])
            plt.title(f"{self.column[-1]} em função de {self.column[0]}")
            
        elif(self.number_of_parameters == 2):
            x_lin = np.linspace(floor(self.data_plan[self.column[0]].min()), ceil(self.data_plan[self.column[0]].max()), 100)
            y_lin = np.linspace(floor(self.data_plan[self.column[1]].min()), ceil(self.data_plan[self.column[1]].max()), 100)

            x, y = np.meshgrid(x_lin, y_lin)
            z = self.coefficients_matrix[0] + x*self.coefficients_matrix[1] + y*self.coefficients_matrix[2]

            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.data_plan[self.column[0]], self.data_plan[self.column[1]], self.data_plan[self.column[-1]])
            ax.plot_surface(x, y, z, cmap='viridis')
            ax.set_xlabel(f"{self.column[0]}")
            ax.set_ylabel(f"{self.column[1]}")
            ax.set_zlabel(self.column[-1])
            ax.set_title(f"{self.column[-1]} em função de {self.column[0]} e {self.column[1]}")

        elif(self.number_of_parameters == 3):
            x_lin = np.linspace(floor(self.data_plan[self.column[0]].min()), ceil(self.data_plan[self.column[0]].max()), 100)
            y_lin = np.linspace(floor(self.data_plan[self.column[1]].min()), ceil(self.data_plan[self.column[1]].max()), 100)
            z_lin = np.linspace(floor(self.data_plan[self.column[2]].min()), ceil(self.data_plan[self.column[2]].max()), 100)

            x, y, z = np.meshgrid(x_lin, y_lin, z_lin)
            colors = self.coefficients_matrix[0] + x*self.coefficients_matrix[1] + y*self.coefficients_matrix[2] + z*self.coefficients_matrix[3]

            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.data_plan[self.column[0]], self.data_plan[self.column[1]], self.data_plan[self.column[2]])
            plot_surface = ax.plot_surface(x, y, z, c=colors, cmap='viridis')
            cbar = plt.colorbar(plot_surface)
            ax.set_xlabel(f"{self.column[0]}")
            ax.set_ylabel(f"{self.column[1]}")
            ax.set_zlabel(f"{self.column[2]}")
            cbar.set_label(self.column[-1])
            ax.set_title(f"{self.column[-1]} em função de {self.column[0]}, {self.column[1]} e {self.column[2]}")
        
        buf = io.BytesIO()
        FigureCanvas(fig).print_png(buf)
        return base64.b64encode(buf.getvalue()).decode('utf-8')

class QuadraticModel:
    def __init__(self, data_frame):
        print(data_frame)
        print("We are in the quadratic constructor")
        self.column = data_frame.columns.tolist()
        self.data_plan = data_frame.sort_values(by=self.column).reset_index(drop=True)
        print("data_plan = " + str(self.data_plan))
        self.number_of_observations = len(self.data_plan)
        self.number_of_parameters = len(self.column) - 1
        self.number_of_levels = self.data_plan[self.column[0]].nunique()
        self.number_of_coefficients = int(1 + 2 * self.number_of_parameters + (self.number_of_parameters * (self.number_of_parameters - 1)) / 2)

        self.response_matrix = self.data_plan[self.column[-1]].values

        matrix = []

        for i in range(self.number_of_observations):
            matrix.append([1])
            for j in range(self.number_of_parameters):
                matrix[i].append(self.data_plan.at[i, self.column[j]])

            for j in range(self.number_of_parameters):
                matrix[i].append(self.data_plan.at[i, self.column[j]] ** 2)

            for j in range(self.number_of_parameters):
                for k in range(j+1, self.number_of_parameters):
                    matrix[i].append(self.data_plan.at[i, self.column[j]] * self.data_plan.at[i, self.column[k]])



        self.planning_matrix = np.array(matrix)
        self.coefficients_matrix = np.linalg.lstsq(self.planning_matrix, self.response_matrix, rcond=None)[0]
        self.expected_response_matrix = self.planning_matrix @ self.coefficients_matrix
        self.residuals_matrix = np.subtract(self.response_matrix, self.expected_response_matrix)
        self.mean_response = np.mean(self.response_matrix)
        
        print(self.coefficients_matrix)

        self.SQR = np.sum(np.square(self.expected_response_matrix - self.mean_response))
        self.MQR = self.SQR / (self.number_of_coefficients - 1)

        self.SQr = np.sum(np.square(self.residuals_matrix))
        self.MQr = self.SQr / (self.number_of_observations - self.number_of_coefficients)

        no_response = self.data_plan.drop(columns=[self.column[-1]])
        reference_line = no_response.loc[0]
        sum_i = [0]
        number_i = [0]
        average_i = [0]
        i = 0

        
        for j in range(self.number_of_observations):
            current_line = no_response.loc[j]
            if not (current_line == reference_line).all():
                reference_line = current_line
                average_i[i] = sum_i[i] / number_i[i]
                sum_i.append(0)
                number_i.append(0)
                average_i.append(0)
                i += 1

            sum_i[i] += self.data_plan.loc[j, self.column[-1]]
            number_i[i] += 1

        self.SQfaj = 0
        self.SQep = 0
        i = 0
        reference_line = no_response.loc[0]

        for j in range(self.number_of_observations):
            current_line = no_response.loc[j]
            if not (current_line == reference_line).all():
                reference_line = current_line
                i += 1

            self.SQfaj += (self.expected_response_matrix[j] - average_i[i]) * (self.expected_response_matrix[j] - average_i[i])
            self.SQep += (self.response_matrix[j] - average_i[i]) * (self.response_matrix[j] - average_i[i])

        self.MQfaj = self.SQfaj / (self.number_of_levels - self.number_of_parameters)
        self.MQep = self.SQep / (self.number_of_observations - self.number_of_levels)

        self.SQT = np.sum(np.square(self.response_matrix - self.mean_response))

        self.explained_variation = self.SQR / self.SQT
        self.maximum_explainable_variation = (self.SQT - self.SQep) / self.SQT

        self.covariance_matrix = np.linalg.inv(np.transpose(self.planning_matrix) @ self.planning_matrix) * self.MQr


    def coefficients_table(self): 
        table = pd.DataFrame()

        table["Coeficiente"] = [1]
        i = 1

        for j in range(self.number_of_coefficients):
            table.loc[i, "Coeficiente"] = [f"X{j + 1}"]
            i += 1

        for j in range(self.number_of_coefficients):
            table.loc[i, "Coeficiente"] = [f"X{j + 1}*X{j + 1}"]
            i += 1

        for j in range(self.number_of_parameters):
            for k in range(j+1, self.number_of_parameters):
                table.loc[i, "Coeficiente"] = [f"X{j + 1}*X{k + 1}"]
                i += 1

        # Placeholder for standard errors (you need to calculate them)
        table["Erros-Padrão"] = [0.0] * self.number_of_coefficients

        return table

    
    def expected_response(self, point): #calcula resposta esperada pelo modelo para um ponto do dominio
        ans = self.coefficients_matrix[0]
        i = 1

        for j in range(self.number_of_parameters):
            ans += point[j]*self.coefficients_matrix[i]
            i += 1

        for j in range(self.number_of_parameters):
            ans += (point[j]**2)*self.coefficients_matrix[i]
            i += 1

        for j in range(self.number_of_parameters):
            for k in range(j+1, self.number_of_parameters):
                ans += (point[j]*point[k])*self.coefficients_matrix[i]
                i += 1

        return ans
    
    def quadratic_plot(self): #plota gráfico do modelo quadratico
        fig = plt.figure()
        print("Quadratic plot now")
        
        if self.number_of_parameters == 1:
            # Assuming the first parameter is the x-axis
            x = np.linspace(np.floor(self.data_plan[self.column[0]].min()), 
                            np.ceil(self.data_plan[self.column[0]].max()), 100)
            # Calculate y using the model's coefficients
            y = (self.coefficients_matrix[0] + 
                x * self.coefficients_matrix[1] + 
                (x**2) * self.coefficients_matrix[2])

            plt.scatter(self.data_plan[self.column[0]], self.data_plan[self.column[-1]])
            plt.plot(x, y)
            plt.xlabel(self.column[0])
            plt.ylabel(self.column[-1])
            plt.title(f"{self.column[-1]} em função de {self.column[0]}")

        elif self.number_of_parameters == 2:
            # Define the ranges for plotting based on the actual data range
            x_range = np.linspace(self.data_plan[self.column[0]].min(), self.data_plan[self.column[0]].max(), 100)
            y_range = np.linspace(self.data_plan[self.column[1]].min(), self.data_plan[self.column[1]].max(), 100)
            x_mesh, y_mesh = np.meshgrid(x_range, y_range)

            # Apply the model's coefficients to get the Z values for the surface plot
            z_mesh = (self.coefficients_matrix[0] +
                      self.coefficients_matrix[1] * x_mesh +
                      self.coefficients_matrix[2] * y_mesh +
                      self.coefficients_matrix[3] * x_mesh**2 +
                      self.coefficients_matrix[4] * y_mesh**2 +
                      self.coefficients_matrix[5] * x_mesh * y_mesh)

            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.data_plan[self.column[0]], self.data_plan[self.column[1]], self.data_plan[self.column[-1]], color='r')
            ax.plot_surface(x_mesh, y_mesh, z_mesh, cmap='viridis', alpha=0.7)
            ax.set_xlabel(self.column[0])
            ax.set_ylabel(self.column[1])
            ax.set_zlabel(self.column[-1])
            ax.set_title(f"{self.column[-1]} em função de {self.column[0]} e {self.column[1]}")

        elif(self.number_of_parameters == 3):
            x_lin = np.linspace(floor(self.data_plan[self.column[0]].min()), ceil(self.data_plan[self.column[0]].max()), 100)
            y_lin = np.linspace(floor(self.data_plan[self.column[1]].min()), ceil(self.data_plan[self.column[1]].max()), 100)
            z_lin = np.linspace(floor(self.data_plan[self.column[2]].min()), ceil(self.data_plan[self.column[2]].max()), 100)

            x, y, z = np.meshgrid(x_lin, y_lin, z_lin)
            colors = self.coefficients_matrix[0] + x*self.coefficients_matrix[1] + y*self.coefficients_matrix[2] + z*self.coefficients_matrix[3] + (x**2)*self.coefficients_matrix[4] + (y**2)*self.coefficients_matrix[5] + (z**2)*self.coefficients_matrix[6] + (x*y)*self.coefficients_matrix[7] + (x*z)*self.coefficients_matrix[8] + (y*z)*self.coefficients_matrix[9] 

            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(self.data_plan[self.column[0]], self.data_plan[self.column[1]], self.data_plan[self.column[2]])
            plot_surface = ax.plot_surface(x, y, z, c=colors, cmap='viridis')
            cbar = plt.colorbar(plot_surface)
            ax.set_xlabel(f"{self.column[0]}")
            ax.set_ylabel(f"{self.column[1]}")
            ax.set_zlabel(f"{self.column[2]}")
            cbar.set_label(self.column[-1])
            ax.set_title(f"{self.column[-1]} em função de {self.column[0]}, {self.column[1]} e {self.column[2]}")
        
        plt.show()
        buf = io.BytesIO()
        FigureCanvas(fig).print_png(buf)
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    
def anova_table(model): #cria DataFrame com tabela ANOVA
    table = pd.DataFrame()

    table["Fonte de Variação"] = ["Regressão", "Resíduos", "Falta de Ajuste", "Erro Puro", "Total"]
    table["Soma Quadrática"] = [model.SQR, model.SQr, model.SQfaj, model.SQep, model.SQT]
    table["Número de Graus de Liberdade"] = [model.number_of_coefficients - 1, model.number_of_observations - model.number_of_coefficients, model.number_of_levels - model.number_of_coefficients, model.number_of_observations - model.number_of_levels, model.number_of_observations - 1]
    table["Média Quadrática"] = [model.MQR, model.MQr, model.MQfaj, model.MQep, ""]


    return table

def f_table(model): #cria DataFrame com parâmetros estatísticos
    table = pd.DataFrame()

    table["Parâmetro Estatístico"] = ["%% de Variação Explicada", "%% Máxima Variação Explicável", "F Calculado", "F Teórico"]
    table["Valor"] = [100*model.explained_variation, 100*model.maximum_explainable_variation, model.MQR/model.MQr, sp.stats.f.ppf(.95, model.number_of_coefficients - 1, model.number_of_observations - model.number_of_coefficients)]

    return table

def overall_f_test(model): #realiza o teste F (talvez seja melhor so devolver a f_table)
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

def optimal_point(model, optimization_type = False): #encontra o ponto ótimo do modelo
    initial_point = []
    
    for i in range(model.number_of_parameters):
        initial_point.append(model.data_plan.at[0, model.column[i]])
        
    # Exclude the last column by indexing to -1
    columns_to_include = model.data_plan.columns[:-1]
    # Generate bounds
    bounds = [(model.data_plan[column].min(), model.data_plan[column].max()) for column in columns_to_include]

    if(optimization_type):
        return minimize(lambda x: -model.expected_response(x), initial_point, bounds=bounds)
    else:
        return minimize(model.expected_response, initial_point, bounds=bounds)

def data_plan_plot(data_frame): #plota o gráfico dos dados coletados
    column = data_frame.columns
    dimensions = len(column) - 1
    fig = plt.figure()
    
    if(dimensions == 1):
        plt.scatter(data_frame[column[0]], data_frame[column[-1]])
        plt.xlabel(f"{column[0]}")
        plt.ylabel(column[-1])
        plt.title(f"{column[-1]} em função de {column[0]}")

    elif(dimensions == 2):
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(data_frame[column[0]], data_frame[column[1]], data_frame[column[-1]])
        ax.set_xlabel(f"{column[0]}")
        ax.set_ylabel(f"{column[1]}")
        ax.set_zlabel(column[-1])
        ax.set_title(f"{column[-1]} em função de {column[0]} e {column[1]}")

    elif(dimensions == 3):
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(data_frame[column[0]], data_frame[column[1]], data_frame[column[2]], c=data_frame[column[-1]], cmap="viridis", marker="o")
        cbar = plt.colorbar(scatter)
        ax.set_xlabel(f"{column[0]}")
        ax.set_ylabel(f"{column[1]}")
        ax.set_zlabel(f"{column[2]}")
        cbar.set_label(column[-1])
        ax.set_title(f"{column[-1]} em função de {column[0]}, {column[1]} e {column[2]}")
    
    
    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def residuals_expectations_plot(model): #plota o gráfico dos resíduos pela resposta prevista
    fig = plt.figure()
    plt.scatter(model.expected_response_matrix, model.residuals_matrix)
    plt.xlabel(f"{model.column[-1]} prevista")
    plt.ylabel("Resíduos")
    plt.title(f"Resíduos em fução da {model.column[-1]} prevista")

    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def residuals_parameters_plot(model): #cria grid de gráficos dos resíduos por cada parâmetro
    fig, axs = plt.subplots(ceil(sqrt(model.number_of_parameters)), ceil(sqrt(model.number_of_parameters)), figsize=(10, 4))

    for i in range(model.number_of_parameters):
        axs[i].scatter(model.data_plan[model.column[i]], model.residuals_matrix)
        axs[i].set_xlabel(f"{model.column[i]}")
        axs[i].set_ylabel("Resíduos")
        axs[i].set_title(f"Resíduos em função de {model.column[i]}")

    plt.tight_layout()

    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    return base64.b64encode(buf.getvalue()).decode('utf-8')