import argparse
from polynomial import Polynomial


def main():
    parser = argparse.ArgumentParser(
        description='This program compares two polynomials')
    parser.add_argument('--simple', nargs='*',
                        help='Enter two polynomials to compare them')
    arguments = parser.parse_args()
    polynomials = []
    for string in arguments.simple:
        polynomials.append(Polynomial(string))
        polynomials[-1].simplify()
    if arguments.simple:
        for polynomial in polynomials:
            print(polynomial.string)


if __name__ == '__main__':
    main()
