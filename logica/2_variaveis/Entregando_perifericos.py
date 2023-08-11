import math

class variable:
    def __init__(self, name, center, delta, upper_limit, lower_limit, is_integer):
        self.name = name
        self.center = center
        self.delta = delta
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.is_integer = is_integer
    
    def code(self, value):
        return (value-self.center)/self.delta
    
    def decode(self, value):
        return (value*self.delta)+self.center

def experimental_points(variables, ):
    codes = [0, 1, math.sqrt(len(variables))]
    answer = []
    i=0
    j=0

    while(true)



def teste(nome_variavel_1, quantidade_variavel_1, unidade_variavel_1, restricao_inteiro_1,
                                  nome_variavel_2, quantidade_variavel_2, unidade_variavel_2, restricao_inteiro_2):
    quantidade_variavel_1 = quantidade_variavel_1 * 2
    quantidade_variavel_2 = quantidade_variavel_2 * 2

    print ("\n multi por 2")
    print("Variável 1:", nome_variavel_1, ", Quantidade:", quantidade_variavel_1, unidade_variavel_1)
    print("Variável 2:", nome_variavel_2, ", Quantidade:", quantidade_variavel_2, unidade_variavel_2)

if __name__ == "__main__":
    from recebendo_restricoes import nome_variavel_1, quantidade_variavel_1, unidade_variavel_1, restricao_inteiro_1
    from recebendo_restricoes import nome_variavel_2, quantidade_variavel_2, unidade_variavel_2, restricao_inteiro_2

    teste(nome_variavel_1, quantidade_variavel_1, unidade_variavel_1, restricao_inteiro_1,
                                  nome_variavel_2, quantidade_variavel_2, unidade_variavel_2, restricao_inteiro_2)
