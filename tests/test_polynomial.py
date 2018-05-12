from polynomial import Polynomial
import random
D = ['x', 'x', 's', 's', 'f']
A = Polynomial('example')


class TestPolynomial():
    def test_sort_by_monomial(self):
        a = ['y', 'x^3']
        b = Polynomial('example')
        c = ['x^23', '12', 'x^3y^3abc']
        d = ['12', '12A^1212b', 'abcdg', '21', 'bbcdg']
        f = ['8k', '4h', '3k', '4']
        d.sort(key=b.sort_by_monomial)
        a.sort(key=b.sort_by_monomial)
        c.sort(key=b.sort_by_monomial)
        f.sort(key=b.sort_by_monomial)
        assert a == ['y', 'x^3']
        assert c == ['12', 'x^3y^3abc', 'x^23']
        assert d == ['12', '21', 'abcdg', 'bbcdg', '12A^1212b']
        assert f == ['4', '4h', '8k', '3k']

    def test_sort_by_variables(self):
        b = ['12']
        c = ['s', 'A^2', 'd']
        b.sort(key=A.sort_by_variables)
        c.sort(key=A.sort_by_variables)
        D.sort(key=A.sort_by_variables)
        assert b == ['12']
        assert c == ['A^2', 'd', 's']
        assert D == ['f', 's', 's', 'x', 'x']

    def test_simplify_monomial(self):
        c = A.simplify_monomial(D)
        k = ['x^23', 'x^2', 'g', 's']
        k = A.simplify_monomial(k)
        assert c == ['f', 's^2', 'x^2']
        assert k == ['x^25', 'g', 's']

    def test_simplify(self):
        pol1 = Polynomial('3k+4h+8k+4')
        pol1.simplify()
        assert pol1.get_str() == '11k+4h+4'
        pol2 = Polynomial('12+21+abcdg+13A^1212b')
        pol2.simplify()
        assert pol2.get_str() == '13A^1212b+abcdg+33'
        pol3 = Polynomial('a-a')
        pol3.simplify()
        assert pol3.string == '0'
        pol4 = Polynomial('0')
        pol4.simplify()
        assert pol4.string == '0'
        pol5 = Polynomial('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        pol5.simplify()
        assert pol5.string == 'a^49'
        pol5 = Polynomial('bbbbb'
                          'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        pol5.simplify()
        assert pol5.string == 'a^49b^5'
        pol6 = Polynomial('2a-a+b-a-b')
        pol6.simplify()
        assert pol6.string == '0'
        pol7 = Polynomial('2a-a+2-a')
        pol7.simplify()
        assert pol7.string == '2'
        pol8 = Polynomial('3a-2a+2b-b-a')
        pol8.simplify()
        assert pol8.string == 'b'
        pol9 = Polynomial('3a-2b-4a+2b')
        pol9.simplify()
        assert pol9.string == '2a'

    def test_get_monomial(self):
        pol = Polynomial('3k+4h+8k+4')
        monomials = pol.get_monomials(pol.string)
        assert monomials == ['3k', '+4h', '+8k', '+4']

    def test_same_polynomial(self):
        monomials = ['abcdg', '13A^1212b', '23', '4a',
                     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                     'bbbbb'
                     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                     'vnsdkvndskl']
        for i in range(100):
            random.shuffle(monomials)
            string = '+'.join(monomials)
            polinom = Polynomial(string)
            polinom.simplify()
            assert polinom.string == '13A^1212b+a^49b^5+a^49+d^2k^2ln^2s^2v^2+abcdg+4a+23'
