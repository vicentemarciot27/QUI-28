import itertools

class paramter: #parametros são as variaveis a serem analisadas
    def __init__(self, name, unit, is_integer, center, lower_limit, upper_limit, delta): #name e unit é str, is_integer é bool, e o resto é float
        """Defines the parameters (variables) to be analysed

        Args:
            name (string): Variable name
            unit (string): Unit of measure (SI)
            is_integer (bool): Defines wether the answers should be integer
            center (float): defines the central point
            lower_limit (float): defines the lower limit
            upper_limit (float): defines the upper limit
            delta (float): required variation
        """
        self.name = name
        self.unit = unit
        self.is_integer = is_integer 
        self.center = center
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.delta = delta
        
    def code(self, value): #recebe o valor real e retorna o valor codificado
        """Codifies a value, normalising it according to the bibliography

        Args:
            value (float): the value to be coded 

        Returns:
            (float): nomalized value
        """
        return (value-self.center)/self.delta
    
    def decode(self, value): #recebe o valor codificado e retorna o valor real
        """Decodifies a value, according to the bibliography

        Args:
            value (float): the normalized value to be decoded

        Returns:
            float: the decoded value
        """
        return (value*self.delta)+self.center

class point: #um ponto experimental
    def __init__ (self, number_of_paramters):
        """Defines the experimental point

        Args:
            number_of_paramters (int): The number of parameters (variables) to be analysed
        """
        self.dimensions = number_of_paramters
        self.coordinates = []

class fatorial_plan: #planejamento fatorial
    def __init__(self, number_of_paramters, alpha):
        """Defines the fatorial planning

        Args:
             number_of_paramters (int): The number of parameters (variables) to be analysed
            alpha (float): ?? explica melman
        """
        self.dimensions = number_of_paramters
        self.alpha = alpha

        self.central = list(itertools.combinations_with_replacement([0], number_of_paramters))
        self.fatorial = list(itertools.combinations_with_replacement([-1, 1], number_of_paramters))
        self.central = list(itertools.combinations_with_replacement([0], number_of_paramters))
        self.fatorial = list(itertools.combinations_with_replacement([-1, 1], number_of_paramters))
        self.axial = []

        for i in range(number_of_paramters):
            self.axial.append([])
            for j in range(number_of_paramters):
                if j==i:
                    self.axial[i].append(self.alpha)
                else:
                    self.axial[i].append(0)
    
def return_plan(paramters_list, fatorial_plan_list):
    """ Pratica nessa daqui :)
    Recomendo usar a extensão autodocstring para fazer essas documentações resenha
    Isso é bom pq todo projeto comercial precisa ser bem documentado

    Args:
        paramters_list (_type_): _description_
        fatorial_plan_list (_type_): _description_

    Returns:
        _type_: _description_
    """
    real_plan = []

    for i in range(fatorial_plan_list):
        real_plan.append([])

        for j in range(paramters_list):
            real_plan[i].append(paramters_list[j].decode(fatorial_plan_list[i][j]))

    return real_plan