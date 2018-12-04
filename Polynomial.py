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
print('After expansion, the polynomial is', polynomial)


def build_matrix(polynomial,variable,relation_dict):
    matrix = sym.Matrix()
    basis_list=[1]
    if len(relation_dict) != 0:
        basis_list = find_basis(relation_dict)
    # print(matrix,matrix.shape)
    for basis in basis_list:
        this_column_polynomial = polynomial*basis
        this_column=[]
        for basis in basis_list:
            this_column_polynomial = substitution(sym.expand(this_column_polynomial),relation_dict)
            # print(this_column_polynomial)
            # print(polynomial,basis==1,isinstance(polynomial, sym.symbol.Symbol))
            if basis == 1:
                # coefficient = this_column_polynomial.coeff(variable,0) #Need to figure out a way to check constant term
                #coefficient = constant_term(this_column_polynomial,variable)
                coefficient = this_column_polynomial.coeff(variable,0)
            # print(basis,coefficient)
            else:
                coefficient = this_column_polynomial.coeff(basis)
            this_column.append(coefficient)
            # print(this_column)
        matrix = matrix.col_insert(matrix.shape[1], sym.Matrix(this_column)) #columns are added one at a time
        # print(matrix,matrix.shape)
    return matrix
def constant_term(polynomial,variable):
    if len(variable.free_symbols) > 1:
        return polynomial.coeff(variable) #when there are multi variables, coeff(variable,0) acts weirdly
    else: #only one variable
        return polynomial.coeff(variable,0)

def substitution(polynomial=sym.expand(((2*x+y)**3)*(x*y**2)*z**4), relation_dict={x**2:y*a, y**3:(x**2)*b, z**4:y*x}):
    while need_substitute(polynomial, relation_dict):
        # polynomial = replace(polynomial, relation_dict)
        for monomial in relation_dict:
            number_of_var = len(monomial.free_symbols)
            if number_of_var == 1:
                polynomial = single_var_substitution(polynomial, monomial, relation_dict[monomial])
            else:
                polynomial = multi_var_substitution(polynomial, monomial, relation_dict[monomial])
    return polynomial
    
#helper method used in substitution
def need_substitute(polynomial, relation_dict):
    for monomial in relation_dict:
        if isinstance(polynomial, sym.add.Add): #if this polynomial has multiple terms added together
            for arg in polynomial.args: #will this always be a 'poly'nomial?
                if is_factor(monomial, arg):
                    return True
        else:
            #print('Polynomial has only one term',polynomial,monomial)

            if is_factor(monomial, polynomial):
                return True
    return False
#helper method used in substitution
    #single variable substitution acts weirdly in the poly.subs(a,b) function
    #so I implement our own
def single_var_substitution(polynomial,monomial,value):
    symbol = list(monomial.free_symbols)[0]

    degree_in_relation = sym.degree(monomial, gen=symbol) #the degree of this variable in the relation_dict
    degree_in_polynomial = sym.degree(polynomial, gen=symbol) #the degree of this variable in the polynomial
    list_to_replace = [(symbol**i, value*symbol**(i-degree_in_relation)) for i in range(degree_in_polynomial + 1) if i >= degree_in_relation]

    polynomial = polynomial.subs(list_to_replace)
    return polynomial
#The poly.subs(a,b) function works fine for multi-variable substitution
def multi_var_substitution(polynomial,monomial,value):
    polynomial = polynomial.subs(monomial, value)
    return polynomial



def find_basis(relation_dict={x**2:a, y**3:b*x, z**4:x*y}):
    single_var_basis_list = find_basis_single_var(relation_dict) #First find the basis of each symbol
    
    for basis in single_var_basis_list: #rule out multiples of the relations
        for relation in relation_dict:
            if is_factor(relation, basis):
                single_var_basis_list.remove(basis)

    final_list = single_var_basis_list
    return final_list

#helper method used in find basis
#construct basis from single variable relations
def find_basis_single_var(relation_dict):
    monomials = extract_single_variable(relation_dict) #extract single variables from relation_dict
    substitution = construct_poly(monomials) #Multiply variables together (to use free_symbols)
    grand_list = [] #Construct a grand_list consist of each symbol's legit basis
    for symbol in substitution.free_symbols:
        variable_sub_list = []
        variable_sub_list.append(symbol**0)
        while sym.degree(variable_sub_list[len(variable_sub_list)-1], gen=symbol) < sym.degree(substitution, gen=symbol)-1:
            variable_sub_list.append(variable_sub_list[len(variable_sub_list)-1]*symbol)
        grand_list.append(variable_sub_list)

    #Find all combination within grand_list, and construct final basis_list
    single_var_final_list = []
    combinations = list(itertools.product(*grand_list))
    for combination in combinations:
        base = 1
        for symbol in combination:
            base = base*symbol
        single_var_final_list.append(base)
    return single_var_final_list

#helper method used in find_basis
def construct_poly(variable_list):
    #Multiply variables together (to use free_symbols)
    base = 1
    for monomial in variable_list:
        base = base*monomial
    polynomial = base.copy()
    return polynomial
#extract single variables from relation_dict, used in find_basis
def extract_single_variable(relation_dict):
    #extract variables from relation_dict
    monomials = []
    for key in relation_dict:
        if len(key.free_symbols) == 1:
            monomials.append(key)
    return monomials
def is_factor(monomial_1, monomial_2):
    for symbol in monomial_1.free_symbols:
        if not sym.degree(monomial_1, gen=symbol) <= sym.degree(monomial_2, gen=symbol): #if any symbol has a degree larger than its degree in the monomial_2
            return False
    return True
    
#helper method that was used in find_basis
# def extract_variables(relation_dict):
#     #extract variables from relation_dict
#     monomials = []
#     for key in relation_dict:
#         monomials.append(key)
#     # print(monomials)
#     return monomials


#helper method that was used in substitution
# def replace(polynomial, relation_dict):
#     for monomial in relation_dict:
#         symbol_set = monomial.free_symbols
#         symbol = list(symbol_set)[0]

#         replace_degree = sym.degree(monomial, gen=symbol) #the degree of this variable in the relation_dict
#         symbol_polynomial_degree = sym.degree(polynomial, gen=symbol) #the degree of this variable in the polynomial
#         replace = [(symbol**i,relation_dict[monomial]*symbol**(i-replace_degree)) for i in range(symbol_polynomial_degree+1) if i >= replace_degree]

#         polynomial = polynomial.subs(replace)
#     return polynomial
# [(x**i*y**j,z*x**(i-1)*y**(j-1)) for i in range(10) if i >=1 for j in range(10) if j >=1]
# Turn this to be more general
# Or try to separate the polynomial into terms, for each term, substitute


# while sym.degree(polynomial, gen=x) >= 2 or \
#         sym.degree(polynomial, gen=y) >= 3 or \
#         sym.degree(polynomial, gen=z) >=4:
#     polynomial = polynomial.subs([(x**i, y*a*x**(i-2)) for i in range(sym.degree(polynomial, gen=x)+1) if i >= 2])
#     polynomial = polynomial.subs([(y**i, (x**2)*b*y**(i-3)) for i in range(sym.degree(polynomial, gen=y)+1) if i >= 3])
#     polynomial = polynomial.subs([(z**i, y*x*z**(i-4)) for i in range(sym.degree(polynomial, gen=z)+1) if i >= 4])
# print('check answer', polynomial)