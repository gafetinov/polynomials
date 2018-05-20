import re


class Polynomial():
    def __init__(self, string):
        self.string = string
        self.errors = self.check_for_errors()

    def simplify(self):
        monomials = self.get_monomials(self.string)
        simple_monomials = []
        for monomial in monomials:
            variables = []
            multipliers = [1]
            i = 0
            while i < len(monomial):
                if monomial[i].isdigit() or monomial[i] == '.':
                    multiplier = ''
                    j = i
                    while j < len(monomial) and \
                            (monomial[j].isdigit() or monomial[j] == '.'):
                        multiplier += monomial[j]
                        j += 1
                    multipliers.append(float(multiplier))
                    i = j - 1
                elif monomial[i] == '-':
                    multipliers.append(-1)
                elif monomial[i].isalpha():
                    variable = monomial[i]
                    if i < len(monomial)-1 and monomial[i+1] == '^':
                        variable += monomial[i+1:i+2]
                        j = i + 2
                        while j < len(monomial) and\
                                (monomial[j].isdigit() or monomial[j] == '.'):
                            variable += monomial[j]
                            j += 1
                        i = j-1
                    variables.append(variable)
                i += 1
            variables.sort(key=self.sort_by_variables)
            variables = self.simplify_monomial(variables)
            variables.sort(key=self.sort_by_variables)
            common_multiplier = self.multiply(multipliers)
            if common_multiplier == 1:
                common_multiplier = ''
            elif common_multiplier == -1:
                common_multiplier = '-'
            simple_monomials.append(str(common_multiplier)+''.join(variables))
        simple_monomials.sort(key=self.sort_by_monomial, reverse=True)
        simple_monomials = self.add_up_such_terms(simple_monomials)
        simple_monomials = self.add_up_such_terms(simple_monomials)
        simple_monomials.sort(key=self.sort_by_monomial, reverse=True)
        self.string = '+'.join(simple_monomials)

    def sort_by_monomial(self, input):
        exponents = []
        variables = []
        i = 0
        if input.isdigit():
            exponents.append(0)
        input = input.lstrip('123456789+-.')
        while i < len(input):
            if input[i].isdigit():
                exponent = ''
                while i < len(input) and\
                        (input[i].isdigit() or input[i] == '.'):
                    exponent += input[i]
                    i += 1
                exponents.append(float(exponent))
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

    def check_for_errors(self):
        index = 0
        errors = []
        operators = ['+', '-', '*', '/']
        brackets = 0
        previous_symbol = ''
        for symbol in self.string:
            if symbol == '(':
                brackets += 1
            elif symbol == ')':
                brackets -= 1
            if brackets < 0:
                errors.append((index, 'E01'))
            if previous_symbol in operators and symbol in operators:
                errors.append((index, 'E02'))
            index += 1
            previous_symbol = symbol
        if self.string[-1] in operators:
            errors.append((index, 'E03'))

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

    def add_up_such_terms(self, pol):
        i = 0
        simple_pols = []
        while i < len(pol):
            if i < len(pol)-1 and \
                    pol[i].lstrip('1234567890+-.') ==\
                    pol[i+1].lstrip('1234567890+-.'):
                multiplier = re.match(r'-?\d*.\d*', pol[i]).group(0)
                if multiplier is None or multiplier == '':
                    multiplier = 1
                elif multiplier == '-':
                    multiplier = -1
                else:
                    multiplier = float(multiplier)
                while i < len(pol)-1 and \
                        pol[i].lstrip('1234567890+-.') ==\
                        pol[i+1].lstrip('1234567890+-.'):
                    k2 = re.match(r'-?\d*.\d*', pol[i+1]).group(0)
                    if k2 is None or k2 == '':
                        k2 = 1
                    elif k2 == '-':
                        k2 = -1
                    else:
                        k2 = float(k2)
                    multiplier += k2
                    i += 1
                if multiplier == 0:
                    simple_pol = '0'
                elif multiplier == 1:
                    simple_pol = pol[i].lstrip('1234567890+-.')
                elif multiplier == -1:
                    simple_pol = '-'+pol[i].lstrip('1234567890+-.')
                else:
                    simple_pol = str(multiplier) + pol[i].lstrip(
                        '1234567890+-.')
            else:
                simple_pol = pol[i]
            simple_pols.append(simple_pol)
            i += 1
        return simple_pols

    def simplify_monomial(self, variables):
        simple_variables = []
        i = 0
        while i < len(variables):
            if i < len(variables)-1 and variables[i][0] == variables[i+1][0]:
                exponent = 0
                if len(variables[i]) == 1:
                    exponent += 1
                else:
                    exponent += float(variables[i]
                                      [variables[i].find('^') + 1:])
                while i < len(variables)-1 and \
                        variables[i][0] == variables[i+1][0]:
                    if len(variables[i+1]) == 1:
                        exponent += 1
                    else:
                        exponent += float(variables[i+1]
                                          [variables[i+1].find('^')+1:])
                    i += 1
                simple_variable = '{}^{}'.format(variables[i][0], exponent)
            else:
                simple_variable = variables[i]
            simple_variables.append(simple_variable)
            i += 1
        return simple_variables

    def get_str(self):
        return self.string
