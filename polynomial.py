class Polynomial():
    def __init__(self, string):
        self.string = string

    def sort_by_monomial(self, input):
        exponents = [0]
        variables = []
        for symbol in input:
            if symbol.isdigit():
                exponents.append(str(symbol))
            elif symbol.isalpha():
                variables.append(str(symbol))
        return exponents, variables, -len(variables)

    def simplify(self):

        def sort_by_variables(string):
            if len(string) == 1:
                return string[0]
            else:
                return string[2:] and string[0]

        def multiply(numbers):
            multiple = 1
            for number in numbers:
                multiple *= multiple
            return multiple

        monomials = []
        operators = []
        monomial_begin = 0
        for i in range(len(self.string)):
            if self.string[i] == '+' or '-':
                monomials.append(self.string[monomial_begin:i])
                operators.append(self.string[i])
                monomial_begin = i+1
        operators.append('')  # Для того, чтобы добавить к последнему
        # одночлену пустую строку
        monomials.append(self.string[monomial_begin:])
        simple_monomials = []
        monomial_index = 0
        for monomial in monomials:
            variables = []
            multipliers = []
            i = 0
            while i < len(monomial):
                if monomial[i].isdigit():
                    multiplier = monomial[i]
                    j = i+1
                    while monomial[j].isdigit():
                        multiplier += monomial[j]
                        j += 1
                    multipliers.append(multiplier)
                    i = j
                if monomial[i].isalpha():
                    if monomial[i+1] != '^':
                        variables.append(monomial[i])
                    else:
                        variable = monomial[i:i+2]
                        j = i + 2
                        exponent = ''
                        while monomial[j].isdigit():
                            variable += monomial[j]
                            j += 1
                        variables.append(variable)
                        i = j
                i += 1
            variables.sort(key=sort_by_variables)
            common_multiplier = multiply(multipliers)
            simple_monomials.append(str(common_multiplier)+''.join(variables))
            monomial_index += 1
        simple_monomials.sort(key=self.sort_by_monomial)

    def get_str(self):
        return self.string
