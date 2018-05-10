class Polynomial():
    def __init__(self, string):
        self.string = string

    def sort_by_monomial(self, input):
        exponents = []
        variables = []
        i = 0
        if input.isdigit():
            exponents.append(0)
        while i < len(input):
            if input[i].isdigit():
                exponent = ''
                while i < len(input) and input[i].isdigit():
                    exponent += input[i]
                    i += 1
                exponents.append(int(exponent))
            elif input[i].isalpha():
                variables.append(str(input[i]))
                i += 1
                if i+1 < len(input) and input[i+1] != '^':
                    exponents.append(1)
            else:
                i += 1
        return exponents, variables

    def sort_by_variables(self, string):
        if len(string) == 1:
            return string[0]
        else:
            return string[2:] and string[0]

    def simplify(self):

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
            variables.sort(key=self.sort_by_variables)
            common_multiplier = multiply(multipliers)
            simple_monomials.append(str(common_multiplier)+''.join(variables))
            monomial_index += 1
        simple_monomials.sort(key=self.sort_by_monomial, reverse=True)

    def simplify_monomial(self, monomial):
        pass

    def get_str(self):
        return self.string
