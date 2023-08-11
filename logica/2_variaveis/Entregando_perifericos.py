def teste(nome_variavel_1, quantidade_variavel_1, unidade_variavel_1,
                                  nome_variavel_2, quantidade_variavel_2, unidade_variavel_2):
    quantidade_variavel_1 = quantidade_variavel_1 * 2
    quantidade_variavel_2 = quantidade_variavel_2 * 2

    print ("\n multi por 2")
    print("Variável 1:", nome_variavel_1, ", Quantidade:", quantidade_variavel_1, unidade_variavel_1)
    print("Variável 2:", nome_variavel_2, ", Quantidade:", quantidade_variavel_2, unidade_variavel_2)


if __name__ == "__main__":
    from recebendo_restricoes import nome_variavel_1, quantidade_variavel_1, unidade_variavel_1
    from recebendo_restricoes import nome_variavel_2, quantidade_variavel_2, unidade_variavel_2

    teste(nome_variavel_1, quantidade_variavel_1, unidade_variavel_1,
                                  nome_variavel_2, quantidade_variavel_2, unidade_variavel_2)
