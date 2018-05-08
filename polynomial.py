class Polynomial():
    def __init__(self, string):
        self.string = string

    def simplify(self):
        monomials = []
        operators = []
        monomial_begin = 0
        for i in range(len(self.string)):
            if self.string[i] == '+' or '-':
                monomials.append(self.string[monomial_begin:i])
                operators.append(self.string[i])
                monomial_begin = i+1
        monomials.append(self.string[monomial_begin:])
        for monomial in monomials:
            for i in range(monomial):
                if monomial[i].isdigit():
                    
                if monomial[i].isalpha():


    def get_str(self):
        return self.string
