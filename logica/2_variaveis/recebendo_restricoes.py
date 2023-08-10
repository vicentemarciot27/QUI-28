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


nome_variavel1 = "jose"

quantidade_variavel1 = input("Qual a sua quantidade no teste central? ")

if quantidade_variavel1.isdigit():
    resposta_inteiro = obter_resposta_sim_nao("Ela precisa ser um número inteiro? (Sim/Não) ")
    if resposta_inteiro:
        quantidade_variavel1 = int(quantidade_variavel1)

# Pergunta o nome da variável 2
nome_variavel2 = input("Qual o nome da variável 2? ")

# Pergunta a quantidade no teste central da variável 2
quantidade_variavel2 = input("Qual a sua quantidade no teste central? ")

# Verifica se a resposta anterior é um número inteiro
if quantidade_variavel2.isdigit():
    # Pergunta se ela precisa ser um número inteiro
    resposta_inteiro = obter_resposta_sim_nao("Ela precisa ser um número inteiro? (Sim/Não) ")
    if resposta_inteiro:
        quantidade_variavel2 = int(quantidade_variavel2)

# Impressão dos valores obtidos
print("Valores obtidos:")
print("Variável 1: ", nome_variavel1, ", Quantidade no teste central: ", quantidade_variavel1)
print("Variável 2: ", nome_variavel2, ", Quantidade no teste central: ", quantidade_variavel2)