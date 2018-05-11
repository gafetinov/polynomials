from polynomial import Polynomial
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
        assert d == ['12', '21', 'bbcdg', 'abcdg', '12A^1212b']
        assert f == ['4', '8k', '3k', '4h']

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
        assert pol1.get_str() == '4h+3k+8k+4'
        pol2 = Polynomial('12+21+abcdg+13A^1212b')
        assert pol2.get_str() == '13A^1212b+abcdg+33'

    def test_get_monomial(self):
        pol = Polynomial('3k+4h+8k+4')
        monomials = pol.get_monomials(pol.string)
        assert monomials == ['3k', '+4h', '+8k', '+4']