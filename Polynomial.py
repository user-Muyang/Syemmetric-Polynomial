# Use sympy to perform symbolic operation
# from sympy import *
import sympy as sym
import itertools

x = sym.symbols('x')
a = sym.symbols('a', integer=True)
y = sym.symbols('y')
b = sym.symbols('b', integer=True)
z = sym.symbols('z')
polynomial = ((2*x+y)**3)*(x*y**2)*z**4
print('polynomial is', polynomial)
polynomial = sym.expand(polynomial)
print('expand is', polynomial)



while sym.degree(polynomial, gen=x) >= 2 or \
        sym.degree(polynomial, gen=y) >= 3 or \
        sym.degree(polynomial, gen=z) >=1:
    polynomial = polynomial.subs([(x**i, y*a*x**(i-2)) for i in range(sym.degree(polynomial, gen=x)+1) if i >= 2])
    polynomial = polynomial.subs([(y**i, (x**2)*b*y**(i-3)) for i in range(sym.degree(polynomial, gen=y)+1) if i >= 3])
    polynomial = polynomial.subs([(z**i, y*x*z**(i-1)) for i in range(sym.degree(polynomial, gen=y)+1) if i >= 1])
print(polynomial)


def find_basis(relation_dict={x**2:a, y**3:b*x, z**4:x*y}):
    # #extract variables from relation_dict
    monomials = extract_variables(relation_dict)

    #Multiply variables together (to use free_symbols)
    polynomial = construct_poly(monomials)

    #Construct a grand_list consist of each symbol's legit basis
    grand_list = []
    for symbol in polynomial.free_symbols:
        variable_sub_list = []
        variable_sub_list.append(symbol**0)
        while sym.degree(variable_sub_list[len(variable_sub_list)-1], gen=symbol) < sym.degree(polynomial, gen=symbol)-1:
            variable_sub_list.append(variable_sub_list[len(variable_sub_list)-1]*symbol)
        grand_list.append(variable_sub_list)
    print(grand_list)

    #Find all combination within grand_list, and construct final basis_list
    final_list = []
    combinations = list(itertools.product(*grand_list))
    for combination in combinations:
        base = 1
        for symbol in combination:
            base = base*symbol
        final_list.append(base)

    return final_list

#helper method used in find_basis
def extract_variables(relation_dict):
    #extract variables from relation_dict
    monomials = []
    for item in relation_dict:
        monomials.append(item)
    # print(monomials)
    return monomials
#helper method used in find_basis
def construct_poly(variable_list):
    #Multiply variables together (to use free_symbols)
    base = 1
    for monomial in variable_list:
        base = base*monomial
    polynomial = base.copy()
    return polynomial