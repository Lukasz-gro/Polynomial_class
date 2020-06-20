class Polynomial(object):
    __epsilon = 10**(-8)

    def __init__(self, *coefficient, **kwargs):
        self.coefficient = list(coefficient[0])

        # self.__epsilon = 10**(-8)

    def __repr__(self):
        # printing polynomial without 0 and 1 when they are coefficient
        poly = ""
        for counter, value in enumerate(self.coefficient):
            if counter == 0 and value != 0:
                poly += "{} ".format(value)
            elif counter != 0 and value != 0:
                if value > 0 and counter != 1:
                    if value != 1:
                        poly += "+{}x^{} ".format(value, counter)
                    else:
                        poly += "+x^{} ".format(counter)
                elif value < 0 and counter != 1:
                    if value != -1:
                        poly += "{}x^{} ".format(value, counter)
                    else:
                        poly += "-x^{} ".format(counter)
                elif value > 0 and counter == 1:
                    if value != 1:
                        poly += "+{}x ".format(value)
                    else:
                        poly += "+x "
                elif value < 0 and counter == 1:
                    if value != -1:
                        poly += "{}x ".format(value)
                    else:
                        poly += "-x "
        if self.coefficient[0] == 0:
            if poly[0] == "+":
                poly = poly[1:]
        return poly

    # one way of initialisation of object
    def copy(self):
        return Polynomial(self.coefficient)

    # returning a value of polynomial in given point
    def __call__(self, x):
        if (type(x) in (int, float)) or ('numpy' in str(type(x))):
            y = 0
            for counter, value in enumerate(self.coefficient):
                y += value*(x**counter)
            return y
        raise TypeError

    # adding two polynomials or number and polynomial
    def __add__(self, other):
        if type(other) == Polynomial:
            n = Polynomial.degree(self)
            m = Polynomial.degree(other)
            limit = max(n, m)
            coef = []
            for i in range(limit+1):
                value = 0
                if i <= n:
                    value += self.coefficient[i]
                if i <= m:
                    value += other.coefficient[i]
                coef.append(value)
            return Polynomial(coef)
        elif type(other) in (int, float) or ('numpy' in str(type(other))):
            new_poly = Polynomial(self.coefficient)
            new_poly.coefficient[0] += other
            return new_poly

        raise TypeError

    # subtracting of two polynomials or polynomial and number
    def __sub__(self, other):
        if type(other) == Polynomial:
            n = Polynomial.degree(self)
            m = Polynomial.degree(other)
            limit = max(n, m)
            coef = []
            for i in range(limit+1):
                value = 0
                if i <= n:
                    value += self.coefficient[i]
                if i <= m:
                    value -= other.coefficient[i]
                coef.append(value)
            return Polynomial(coef)
        elif type(other) in (int, float) or ('numpy' in str(type(other))):
            new_poly = Polynomial(self.coefficient)
            new_poly.coefficient[0] -= other
            return new_poly
        raise TypeError

    # multiplication of polynomial and number
    def __mul__(self, other):
        if type(other) in (int, float) or ('numpy' in str(type(other))):
            new_coefficient = []
            for i in self.coefficient:
                if abs(i*other) > Polynomial.__epsilon:
                    new_coefficient.append(i*other)
                else:
                    new_coefficient.append(0)
            return Polynomial(new_coefficient)
        raise TypeError

    # checking if two polynomials are equal
    def __eq__(self, other):
        if type(other) == Polynomial:
            n = Polynomial.degree(self)
            m = Polynomial.degree(other)
            if n != m:
                return False
            else:
                for i in range(n+1):
                    if self.coefficient[i] != other.coefficient[i]:
                        return False
                return True
        elif type(other) in (int, float) and Polynomial.degree(self) == 0:
            if other == self.coefficient[0]:
                return True
            else:
                return False
        else:
            return False

    # constant used in multiplication to hide small coefficient
    def new_epsilon(self, x):
        Polynomial.__epsilon = x

    # returning degree of given polynomial
    def degree(self):
        new_degree = 0
        for counter, value in enumerate(self.coefficient):
            if value != 0:
                new_degree = counter
        return new_degree
