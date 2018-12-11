# Use sympy to perform symbolic operation
# from sympy import *
import sympy as sym
import itertools

x = sym.symbols('x')
a = sym.symbols('a', integer=True)
y = sym.symbols('y')
b = sym.symbols('b', integer=True)
z = sym.symbols('z')
# polynomial = ((2*x+y)**3)*(x*y**2)*z**4
# print('polynomial is', polynomial)
# polynomial = sym.expand(polynomial)
# print('After expansion, the polynomial is', polynomial)

#can use sym.factor(poly)

def build_matrix(polynomial,variable,relation_dict): #variables that are not in the base ring
    matrix = sym.Matrix()
    basis_list=[1]
    dict_for_basis = dict()
    for var in variable:
        # print('var',var)
        for relation in relation_dict:
            # print('relation',relation)
            if relation.free_symbols == var.free_symbols:
                dict_for_basis.update({relation:relation_dict[relation]})
    # print(dict_for_basis)
    if len(dict_for_basis) != 0:
        basis_list = find_basis(dict_for_basis)
    print('list of basis is: ',basis_list)
    for basis in basis_list:
        this_column_polynomial = polynomial*basis
        this_column=[]
        for basis in list(reversed(basis_list)):
            this_column_polynomial = substitution(sym.expand(this_column_polynomial),relation_dict)
            if basis == 1:
                coefficient = constant_term(this_column_polynomial,variable)
            else:
                coefficient = this_column_polynomial.coeff(basis)
                this_column_polynomial = this_column_polynomial-coefficient*basis
            # print(basis,coefficient)
            this_column.append(coefficient)
            # print(this_column)
        this_column = list(reversed(this_column))
        matrix = matrix.col_insert(matrix.shape[1], sym.Matrix(this_column)) #columns are added one at a time
        # print(matrix,matrix.shape)
    return matrix
def constant_term(polynomial,variable):
    for symbol in polynomial.free_symbols:
        if symbol in variable:
            polynomial = polynomial.subs(symbol,0)
    return polynomial


def find_char_poly(matrix):
    λ = sym.symbols('λ')
    size = matrix.shape[0]
    M = λ*sym.eye(size) - matrix
    char_poly = sym.expand(M.det())
    return char_poly

def find_all_coeff_lambda(char_poly):
    λ = sym.symbols('λ')
    char_poly = sym.Poly(char_poly, sym.symbols('λ'))
    list_of_coeffs = char_poly.all_coeffs()
    coeff_dict = dict()
    for i in range(len(list_of_coeffs)-1,-1,-1): #len(list_of_coeffs)-1 = λ's highest_degree, second -1 loop i to 0
        coeff_dict[λ**i] = list_of_coeffs[len(list_of_coeffs)-1-i]
    return coeff_dict
def find_coeff_lambda_n_k(char_poly, k):
    λ = sym.symbols('λ')
    char_poly = sym.Poly(char_poly, sym.symbols('λ'))
    list_of_coeffs = char_poly.all_coeffs()
    coeff_dict = find_all_coeff_lambda(char_poly)
    n = len(list_of_coeffs) - 1 #highest_degree of λ
    coeff = coeff_dict[λ**(n-k)]
    return coeff #value returned is the coefficient of λ**(n-k)
def find_s(char_poly,k):
    # find coeff of λ**(n-k)*(-1)**k
    #return s_k, i.e. s_0 will always be 1
    λ_coeff = find_coeff_lambda_n_k(char_poly, k)
    return λ_coeff*(-1)**k

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