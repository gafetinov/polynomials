import argparse
from polynomial import Polynomial
import postfix_notation


def main():
    parser = argparse.ArgumentParser(
        description='This program compares two polynomials')
    parser.add_argument('string', nargs=2,
                        help='Enter polynomials to compare them')
    arguments = parser.parse_args()
    polynomials = []
    for string in arguments.string:
        expr = postfix_notation.remove_brackets(string)
        polynomials.append(Polynomial(expr))
        polynomials[-1].simplify()
    print(polynomials[0].string == polynomials[1].string)


if __name__ == '__main__':
    main()
