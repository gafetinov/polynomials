class Polynomial():
    def __init__(self, string):
        self.string = string

    def simplify(self):
        unrepresented_pol = self.string
        for i in range(len(unrepresented_pol)):
            if unrepresented_pol[i] is '^':
                pass


    def get_strng(self):
        return self.string
