def obter_resposta_sim_nao(pergunta):
    while True: 
        resposta = input(pergunta)
        resposta = resposta.lower()
        if resposta == "sim" or resposta == "s":
            return True
        elif resposta == "não" or resposta == "nao" or resposta == "n":
            return False
        else:
            print("Resposta inválida. Por favor, responda com 'Sim' ou 'Não'.")

restricao_inteiro_1 = 0
restricao_inteiro_2 = 0


# Pergunta o nome da variável 1
nome_variavel_1 = input("Qual o nome da variável 1? ")

# Pergunta a quantidade no teste central da variável 1
quantidade_variavel_1 = input("Qual a sua quantidade/valor no teste central? (apenas o valor numerico) ")

# Pergunta sobre o tipo da variável
unidade_variavel_1 = input("Qual a unidade da variável? ")


# conversão de string para numero
if quantidade_variavel_1.isdigit():
    # Pergunta se ela precisa ser um número inteiro, se for vai ter a restricao_inteiro_1 =1
    quantidade_variavel_1 = float(quantidade_variavel_1)
    resposta_inteiro = obter_resposta_sim_nao("Ela precisa ser um número inteiro? (Sim/Não) ")
    if resposta_inteiro:
        restricao_inteiro_1 = 1
else:
    quantidade_variavel_1 = float(quantidade_variavel_1.replace(',','.'))

limite_superior_1 = input("Qual o máximo valor para essa variavel?")
limite_inferior_1 = input("Qual o minimo valor para essa variavel?")
        

# Pergunta o nome da variável 2
nome_variavel_2 = input("Qual o nome da variável 2? ")

# Pergunta a quantidade no teste central da variável 2
quantidade_variavel_2 = input("Qual a sua quantidade no teste central? (apenas o valor numerico) ")

# Pergunta sobre o tipo da variável
unidade_variavel_2 = input("Qual a unidade da variável? ")

# conversão de string para numero
if quantidade_variavel_2.isdigit():
    # Pergunta se ela precisa ser um número inteiro, se for vai ter a restricao_inteiro_2 =1
    quantidade_variavel_2 = float(quantidade_variavel_2)
    resposta_inteiro = obter_resposta_sim_nao("Ela precisa ser um número inteiro? (Sim/Não) ")
    if resposta_inteiro:
        restricao_inteiro_2 = 1
else:
    quantidade_variavel_2 = float(quantidade_variavel_1.replace(',','.'))

limite_superior_2 = input("Qual o máximo valor para essa variavel?")
limite_inferior_2 = input("Qual o minimo valor para essa variavel?")

delta = input("Qual o delta desejado para o experimento?")

# Impressão dos valores obtidos
print("Valores obtidos:")
print("Variável 1: ", nome_variavel_1, ", Quantidade no teste central: ", quantidade_variavel_1, unidade_variavel_1)
print("Variável 2: ", nome_variavel_2, ", Quantidade no teste central: ", quantidade_variavel_2, unidade_variavel_2)