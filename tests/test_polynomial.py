from polynomial import Polynomial


class TestPolynomial():
    def test_sort_by_monomial(self):
        a = ['y', 'x^3']
        b = Polynomial('example')
        c = ['x^23', '12', 'x^3y^3abc']
        d = ['12', 'a^1212b', 'abcdg', '21']
        d.sort(key=b.sort_by_monomial)
        a.sort(key=b.sort_by_monomial)
        c.sort(key=b.sort_by_monomial)
        assert a == ['y', 'x^3']
        assert c == ['12', 'x^3y^3abc', 'x^23']
        assert d == ['12', '21', 'abcdg', 'a^1212b']

    def test_sort_by_variables(self):
        a = Polynomial('example')
        b = ['12']
        c = ['s', 'a^2', 'd']
        d = ['x', 'y', 'x', 's', 's', 'f']
        b.sort(key=a.sort_by_variables)
        c.sort(key=a.sort_by_variables)
        d.sort(key=a.sort_by_variables)
        assert b == ['12']
        assert c == ['a^2', 'd', 's']
        print(d)
