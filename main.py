import argparse
from polynomial import Polynomial


def main():
    parser = argparse.ArgumentParser(
        description='This program compares two polynomials')
    parser.add_argument('string', nargs=2,
                        help='Enter polynomials to compare them')
    arguments = parser.parse_args()
    polynomials = []
    count = 1
    errors = []
    for string in arguments.string:
        errors += check_for_errors(string, count)
        count += 1
    if errors:
        print('ERRORS:\n')
        for error in errors:
            print(error)
        exit(1)
    for string in arguments.string:
        polynomials.append(Polynomial(string))
        polynomials[-1].simplify()
        count += 1
    print(polynomials[0].string == polynomials[1].string)


def check_for_errors(string, number):
    index = 0
    errors = []
    operators = ['+', '-', '*', '/', '^']
    brackets = 0
    dot_number = 0
    last_open_bracket = None
    last_close_bracket = None
    previous_symbol = ''
    for symbol in string:
        index += 1
        if symbol == '.':
            dot_number += 1
        elif not symbol.isdigit():
            dot_number = 0
        if symbol == '(':
            brackets += 1
            last_open_bracket = index
        elif symbol == ')':
            brackets -= 1
            last_close_bracket = index
        if previous_symbol == '^' and not symbol.isdigit() and symbol != '(':
            errors.append(((number, index), 'should be built to a '
                                            'numerical power'))
        if previous_symbol == '/' and not symbol.isdigit() and symbol != '(':
            errors.append(((number, index), 'You can divide only by number'))
        if dot_number > 1:
            errors.append(((number, index), 'In number can be only one dot'))
            dot_number = 0
        if brackets < 0:
            errors.append(((number, index), 'Problem with brackets'))
        if previous_symbol in operators and symbol in operators:
            errors.append(((number, index), 'Problem with operator'))
        if ((previous_symbol.isalpha()
                or (previous_symbol.isdigit() and symbol != '.'))
                and not symbol.isalpha() and not symbol.isdigit()
                and symbol not in operators
                and symbol != ')' and symbol != '('):
            errors.append(((number, index), 'Unknown symbol "{}"'.
                           format(symbol)))
        if not symbol.isdigit() and not symbol.isalpha \
                and symbol not in operators and symbol != '.' \
                and symbol != '(' and symbol != ')':
            errors.append(((number, index), 'Unknown symbol "{}"'.
                           format(symbol)))
        if symbol in operators and previous_symbol in operators:
            errors.append(((number, index), 'Repeating operator "{}"'.
                           format(symbol)))
        previous_symbol = symbol
    if brackets < 0:
        errors.append(((number, last_close_bracket), 'Problem with brackets'))
    elif brackets > 0:
        errors.append(((number, last_open_bracket), 'Problem with brackets'))
    return errors


if __name__ == '__main__':
    main()
