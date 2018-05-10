import argparse
from polynomial import Polynomial


def main():
    parser = argparse.ArgumentParser(
        description='This program compares two polynomials')
    parser.add_argument('string', nargs='*',
                        help='Enter two polynomials to compare them')
    arguments = parser.parse_args()
    polynomials = []
    for string in arguments.string:
        polynomials.append(Polynomial(string))
        polynomials[-1].simplify()
    print(polynomials[0].get_str() == polynomials[1].get_str())


if __name__ == '__main__':
    main()
