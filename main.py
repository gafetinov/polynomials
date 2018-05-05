import argparse
from polynomial import Polynomial


def main():
    parser = argparse.ArgumentParser(
        description='This program compares two polynomials')
    parser.add_argument('string', nargs='*',
                        help='Enter two polynomials to compare them')
    arguments = parser.parse_args()
    polynomials = []
    for i in range(len(arguments)):
        polynomials[i] = Polynomial(arguments[i])
        polynomials[i].simplify()
    print(polynomials[0].get_str() == polynomials[1].get_str())