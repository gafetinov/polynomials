import re
from decimal import Decimal


OPERATORSPRIORITY = {"*": 2, "/": 2, "+": 1, "-": 1, "^": 3}


class Polynomial():
    def __init__(self, string):
        self.string = string
        self.errors = self.check_for_errors()

    def __mul__(self, other):
        monomials1 = self.get_monomials(self.string)
        monomials2 = other.get_monomials(other.string)
        string = ''
        for mon1 in monomials1:
            for mon2 in monomials2:
                string += '{}*{}'.format(mon1, mon2)
        new_pol = Polynomial(string)
        new_pol.simplify()

    def is_number(self, input):
        if re.match(r'-?\d*\.?\d*', input) is not None:
            return re.match(r'-?\d*\.?\d*', input).group(0) == input

    def simplify(self):
        if "(" in self.string or ")" in self.string:
            self.string = self.remove_brackets(self.string)
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
                    if monomial[i-1] != '/':
                        multipliers.append(float(multiplier))
                    else:
                        multipliers.append(1/float(multiplier))
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
            common_multiplier = self.multiply_numbers(multipliers)
            if common_multiplier == 1:
                if variables:
                    common_multiplier = ''
                else:
                    common_multiplier = 1.0
            elif common_multiplier == -1 and variables:
                common_multiplier = '-'
            elif common_multiplier == 0:
                variables.clear()
            simple_monomials.append(str(common_multiplier)+''.join(variables))
        simple_monomials.sort(key=self.sort_by_monomial, reverse=True)
        simple_monomials = self.add_up_such_terms(simple_monomials)
        simple_monomials = self.add_up_such_terms(simple_monomials)
        simple_monomials.sort(key=self.sort_by_monomial, reverse=True)
        self.string = self.glue_monomials(simple_monomials)

    def glue_monomials(self, monomials):
        result = monomials[0]
        for i in range(1, len(monomials)):
            if monomials[i][0] != "-":
                result += "+"
            result += monomials[i]
        return result

    def sort_by_monomial(self, input):
        exponents = []
        variables = []
        i = 0
        if re.match(r'-?\d*\.?\d*', input) is not None:
            if re.match(r'-?\d*\.?\d*', input).group(0) == input:
                exponents.append(0)
        input = input.lstrip('1234567890+-.')
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
        return max(exponents), variables

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
        i = 0
        while i < len(polinom):
            if (polinom[i] == '+' or polinom[i] == '-') and i > 0:
                monomials.append(polinom[monomial_begin:i])
                monomial_begin = i
            if polinom[i] == '(':
                expression = []
                sign = polinom[i-1]
                if sign == '*':
                    j = i
                    while j >= 0 and (polinom[j] != '+' or polinom[j] != '-'):
                        j -= 1
                    expression.append(polinom[j:i])
                indicator = 1
                for j in range(i+1, len(polinom)):
                    if polinom[j] == '(':
                        indicator += 1
                    elif polinom[j] == ')':
                        indicator -= -1
                    if indicator == 0:
                        expression.append(polinom[i-1:j+1])
            i += 1
        monomials.append(polinom[monomial_begin:])
        return monomials

    def multiply_numbers(self, numbers):
        multiple = Decimal('1')
        for number in numbers:
            multiple *= Decimal(str(number))
        return float(multiple)

    def add_up_such_terms(self, pol):
        i = 0
        simple_pols = []
        while i < len(pol):
            if i < len(pol)-1 and \
                    pol[i].lstrip('1234567890+-.') ==\
                    pol[i+1].lstrip('1234567890+-.'):
                source = re.match(r'-?\d*\.?\d*', pol[i])
                if source is None:
                    multiplier = 1
                else:
                    multiplier = source.group(0)
                if multiplier is None or multiplier == '':
                    multiplier = 1
                elif multiplier == '-':
                    multiplier = -1
                else:
                    multiplier = float(multiplier)
                while i < len(pol)-1 and \
                        pol[i].lstrip('1234567890+-.') ==\
                        pol[i+1].lstrip('1234567890+-.'):
                    source2 = re.match(r'-?\d*\.?\d*', pol[i+1])
                    if source2 is None:
                        k2 = 1
                    else:
                        k2 = source2.group(0)
                    if k2 is None or k2 == '':
                        k2 = 1
                    elif k2 == '-':
                        k2 = -1
                    else:
                        k2 = float(k2)
                    multiplier += k2
                    i += 1
                if multiplier == 0:
                    simple_pol = '0.0'
                elif multiplier == 1:
                    simple_pol = pol[i].lstrip('1234567890+-.')
                    if not simple_pol:
                        simple_pol = '1.0'
                elif multiplier == -1:
                    simple_pol = '-'+pol[i].lstrip('1234567890+-.')
                    if simple_pol == '-':
                        simple_pol = '-1.0'
                else:
                    simple_pol = str(float(multiplier)) + pol[i].lstrip(
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
                simple_variable = '{}^{}'.format(variables[i][0], float(exponent))
            else:
                search = variables[i].find('^')
                if search == -1:
                    simple_variable = variables[i]
                else:
                    exponent = ''
                    for j in range(search+1, len(variables[i])):
                        exponent += variables[i][j]
                    exponent = float(exponent)
                    if exponent == 1.0:
                        simple_variable = variables[i][:search]
                    elif exponent == 0.0:
                        if len(variables) == 1:
                            simple_variable = '1.0'
                        else:
                            simple_variable = ''
                    else:
                        simple_variable = '{}^{}'.format(variables[i][0], float(exponent))
            simple_variables.append(simple_variable)
            i += 1
        return simple_variables

    def get_postfix(self, expression):
        stack = []
        out_string = []
        prev_symb = ""
        sign = "+"
        for i in range(len(expression)):
            symb = expression[i]
            if symb.isdigit():
                if prev_symb.isdigit() or prev_symb == ".":
                    out_string[-1] += symb
                    prev_symb = symb
                    continue
                if sign == "-":
                    out_string.append("-" + symb)
                else:
                    out_string.append(symb)
                sign = "+"
            elif symb == ".":
                if prev_symb.isdigit():
                    out_string[-1] += symb
                else:
                    print("Непонятная точка")
                    exit(1)
            elif symb.isalpha():
                if prev_symb.isalpha() or prev_symb.isdigit():
                    while len(stack) != 0 and \
                            stack[-1] in OPERATORSPRIORITY and \
                            OPERATORSPRIORITY["*"] <= OPERATORSPRIORITY[
                            stack[-1]]:
                        out_string.append(stack.pop())
                    stack.append("*")
                if sign == "-":
                    out_string.append("-" + symb)
                else:
                    out_string.append(symb)
                sign = "+"
            elif symb == "(":
                if prev_symb == ")":
                    stack.append("*")
                stack.append(symb)
            elif symb == ")":
                while stack[-1] != "(":
                    out_string.append(stack.pop())
                stack.pop()
            elif symb in OPERATORSPRIORITY:
                if symb == "-":
                    if i == 0 or prev_symb == '(':
                        sign = "-"
                        continue
                while len(stack) != 0 and \
                        stack[-1] in OPERATORSPRIORITY and \
                        OPERATORSPRIORITY[symb] <= OPERATORSPRIORITY[
                    stack[-1]]:
                    out_string.append(stack.pop())
                stack.append(symb)
            prev_symb = symb
        for i in range(len(stack)):
            out_string.append(stack.pop())
        return out_string

    def read_postfix(self, expression):
        stack = []
        for el in expression:
            if el not in OPERATORSPRIORITY:
                stack.append(el)
            else:
                arg1 = stack[-2]
                arg2 = stack[-1]
                res = 0
                if self.isdigit(arg1) and self.isdigit(arg2):
                    arg1 = float(arg1)
                    arg2 = float(arg2)
                    if el == "+":
                        res = arg1 + arg2
                    elif el == "-":
                        res = arg1 - arg2
                    elif el == "*":
                        res = float(Decimal(str(arg1)) * Decimal(str(arg2)))
                    elif el == "/":
                        res = float(Decimal(str(arg1)) / Decimal(str(arg2)))
                    elif el == "^":
                        res = arg1 ** arg2
                else:
                    if el == "+":
                        res = arg1
                        if arg2[0] == "-":
                            res += "-"
                            res += arg2[1:]
                        else:
                            res += "+"
                            res += arg2
                    elif el == "-":
                        res = arg1
                        if arg2[0] != "-":
                            res += "-"
                        for symb in arg2:
                            if symb == "-":
                                res += "+"
                            elif symb == "+":
                                res += "-"
                            else:
                                res += symb
                    elif el == "*":
                        res = self.multiply(arg1, arg2)
                    elif el == "/":
                        if self.isdigit(arg2):
                            arg2 = float(Decimal('1')/Decimal(str(arg2)))
                            res = self.multiply(arg1, arg2)
                        else:
                            print("You can divide only by number")
                            exit(1)
                    elif el == "^":
                        if arg2.isdigit():
                            arg2 = int(arg2)
                            if arg2 == 0:
                                res = "1"
                            else:
                                res = arg1
                                while arg2 > 1:
                                    res = self.multiply(res, arg1)
                                    arg2 -= 1
                        else:
                            print(
                                "The expression with variables can be built "
                                "only in the natural degree.")
                            exit(1)
                stack.pop()
                stack[-1] = str(res)
        return stack[0]

    def multiply(self, expr1, expr2):
        if self.isdigit(expr1):
            return self.multiply_bracket_by_number(expr2, expr1)
        elif self.isdigit(expr2):
            return self.multiply_bracket_by_number(expr1, expr2)
        else:
            return self.multiply_brackets(expr1, expr2)

    def multiply_brackets(self, expr1, expr2):
        args1 = []
        args2 = []
        arg = ""
        start = 0
        if expr1[0] == "-":
            arg += "-"
            start = 1
        else:
            arg += "+"
        for i in range(start, len(expr1)):
            if expr1[i] != "-" and expr1[i] != "+":
                arg += expr1[i]
            else:
                args1.append(arg)
                arg = expr1[i]
        args1.append(arg)
        if expr2[0] == "-":
            arg = "-"
            start = 1
        else:
            arg = "+"
            start = 0
        for i in range(start, len(expr2)):
            if expr2[i] != "-" and expr2[i] != "+":
                arg += expr2[i]
            else:
                args2.append(arg)
                arg = expr2[i]
        args2.append(arg)
        res = ""
        for arg1 in args1:
            for arg2 in args2:
                if arg1[0] == arg2[0]:
                    if len(res) > 0:
                        res += "+" + arg1[1:] + "*" + arg2[1:]
                    else:
                        res = arg1[1:] + "*" + arg2[1:]
                else:
                    if len(res) > 0:
                        res += "-" + arg1[1:] + "*" + arg2[1:]
                    else:
                        res = "-" + arg1[1:] + "*" + arg2[1:]
        return res

    def multiply_bracket_by_number(self, bracket, number):
        if bracket[0] != "-":
            bracket = str(number) + "*" + bracket
        if float(number) >= 0:
            res = ""
            i = 0
            while i < len(bracket):
                if bracket[i] == "+":
                    res += "+" + str(number) + "*"
                elif bracket[i] == "-":
                    res += "-" + str(number) + "*"
                else:
                    res += bracket[i]
                i += 1
        else:
            res = "-"
            i = 1
            while i < len(bracket):
                if bracket[i] == "+":
                    res += "-" + str(number)[1:] + "*"
                elif bracket[i] == "-":
                    res += "+" + str(number)[1:] + "*"
                else:
                    res += bracket[i]
                i += 1
        return res

    def isdigit(self, string):
        start = 1
        if type(string) is int or type(string) is float:
            return True
        if string[0] == "-":
            if len(string) == 1:
                return False
            start = 2
        if string[start - 1].isdigit():
            is_integer = True
        else:
            return False
        for i in range(start, len(string)):
            if string[i] == '.':
                if is_integer is False:
                    return False
                else:
                    is_integer = False
            elif not string[i].isdigit():
                return False
        return True

    def remove_brackets(self, expr):
        postfix = self.get_postfix(expr)
        return self.read_postfix(postfix)

    def get_str(self):
        return self.string
