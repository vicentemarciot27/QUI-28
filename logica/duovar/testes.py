from math import sqrt
import Entregando_perifericos #Importando para não ter que rescrever toda a Entregando _perifericos

#Entregando_perifericos foi consideravelmente alterada, então testes precisa ser corrigida para ficar consistente.

param1 = Entregando_perifericos.Parameter("Temperature", "°C", False, 0, 0, 100, 1)
param2 = Entregando_perifericos.Parameter("Pressure", "kPa", False, 0, 50, 150, 2)
param3 = Entregando_perifericos.Parameter("Bortolazzos", "Tenentes", True, 0, 0, 100, 3)

parameters_list = [param1, param2, param3]
fatorial = Entregando_perifericos.FatorialPlan(len(parameters_list), sqrt(2))

fatorial_plan_list = fatorial.cubic

real_plan = Entregando_perifericos.return_plan(parameters_list, fatorial_plan_list)

for point in real_plan:
    print(point)
