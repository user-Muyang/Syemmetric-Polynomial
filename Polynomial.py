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
    monomials = []
    for item in relation_dict:
        monomials.append(item)
    print(monomials)

    base = 1
    for monomial in monomials:
        base = base*monomial
    print(base)
    polynomial = base.copy()
    print(polynomial.free_symbols)

    grand_list = []
    for symbol in polynomial.free_symbols:
        variable_sub_list = []
        variable_sub_list.append(symbol**0)
        while sym.degree(variable_sub_list[len(variable_sub_list)-1], gen=symbol) < sym.degree(polynomial, gen=symbol)-1:
            variable_sub_list.append(variable_sub_list[len(variable_sub_list)-1]*symbol)
        grand_list.append(variable_sub_list)
    print(grand_list)

    final_list = []
    basis_list = list(itertools.product(*grand_list))
    print(basis_list)
    for sub_basis in basis_list:
        base = 1
        for symbol in sub_basis:
            base = base*symbol
        final_list.append(base)
    print(final_list)

    # basis_list=[]
    # for i in range(len(grand_list)):
    #     current_list = grand_list[i]
    #     for sub_basis in current_list:
    #         print("sub_basis", sub_basis)
    #     for j in range(i+1, len(grand_list)):
    #         print("hi")




    # basis_list = []
    # for i in range(len(grand_list)):
    #     this_list = grand_list[i]
    #     other_lists = 
    #     for monomial in this_list:


    #         basis_list.append(a_basis)
    # print(basis_list)
    # for variable_sub_list in grand_list:
    #     for monomial in variable_sub_list:
    #         basis_list.append(monomial)

    return final_list
    