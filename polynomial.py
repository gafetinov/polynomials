class Polynomial():
    def __init__(self, string):
        self.string = string

    def sort_by_monomial(self, input):
        exponents = []
        variables = []
        i = 0
        if input.isdigit():
            exponents.append(0)
        input = input.lstrip('123456789+-')
        while i < len(input):
            if input[i].isdigit():
                exponent = ''
                while i < len(input) and input[i].isdigit():
                    exponent += input[i]
                    i += 1
                exponents.append(int(exponent))
            elif input[i].isalpha():
                variables.append(str(input[i]))
                if i == len(input)-1 or input[i+1] != '^':
                    exponents.append(1)
                i += 1
            else:
                i += 1
        return exponents, variables

    def sort_by_variables(self, string):
        if len(string) == 1:
            return string[0]
        else:
            return string[2:] and string[0]

    def get_monomials(self, polinom):
        monomials = []
        monomial_begin = 0
        for i in range(len(polinom)):
            if polinom[i] == '+' or polinom[i] == '-':
                monomials.append(polinom[monomial_begin:i])
                monomial_begin = i
        monomials.append(polinom[monomial_begin:])
        return monomials

    def multiply(self, numbers):
        multiple = 1
        for number in numbers:
            multiple *= number
        return multiple

    def simplify(self):
        monomials = self.get_monomials(self.string)
        simple_monomials = []
        monomial_index = 0
        for monomial in monomials:
            variables = []
            multipliers = [1]
            i = 0
            while i < len(monomial):
                if monomial[i].isdigit():
                    multiplier = ''
                    j = i
                    while j < len(monomial) and monomial[j].isdigit():
                        multiplier += monomial[j]
                        j += 1
                    multipliers.append(multiplier)
                    i = j - 1
                elif monomial[i] == '-':
                    multipliers.append(-1)
                elif monomial[i].isalpha():
                    variable = monomial[i]
                    if i < len(monomial)-1 and monomial[i+1] == '^':
                        variable += monomial[i:i+2]
                        j = i + 2
                        while monomial[j].isdigit():
                            variable += monomial[j]
                            j += 1
                        i = j
                    variables.append(variable)
                i += 1
            variables.sort(key=self.sort_by_variables)
            variables = self.simplify_monomial(variables)
            variables.sort(key=self.sort_by_variables)
            common_multiplier = self.multiply(multipliers)
            simple_monomials.append(str(common_multiplier)+''.join(variables))
            monomial_index += 1
        simple_monomials.sort(key=self.sort_by_monomial, reverse=True)
        self.string = '+'.join(simple_monomials)

    def simplify_monomial(self, variables):
        simple_variables = []
        i = 0
        while i < len(variables):
            if i < len(variables)-1 and variables[i][0] == variables[i+1][0]:
                exponent = 0
                for j in range(2):
                    if len(variables[i+j]) == 1:
                        exponent += 1
                    else:
                        exponent += int(variables[i+j]
                                        [variables[i+j].find('^')+1:])
                simple_variable = '{}^{}'.format(variables[i][0], exponent)
                variables.pop(i)
            else:
                simple_variable = variables[i]
            simple_variables.append(simple_variable)
            i += 1
        return simple_variables

    def get_str(self):
        return self.string
