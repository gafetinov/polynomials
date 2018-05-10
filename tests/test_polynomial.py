from polynomial import Polynomial


class TestPolynomial():
    def test_sort_by_monomial(self):
        a = ['y', 'x^3']
        b = Polynomial('as')
        c = ['x^4', 'x^3y^3']
        a.sort(key=b.sort_by_monomial)
        c.sort(key=b.sort_by_monomial.itemgetter(1, 2, 3))
        #assert a == ['x^3', 'y']
        assert c == ['x^3y^3', 'x^3']
