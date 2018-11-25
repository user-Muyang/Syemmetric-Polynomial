#trying to use sympy
# from sympy import *
import sympy as sym
# x = symbols('x')
# print(x*x)
# poly1 = x*(x**2)
# a = symbols('a')
# print(poly1.subs(x**3,a))



# x = symbols('x')
# a = symbols('a')
# poly2 = (x+a)**2
# expand_poly2 = expand(poly2)
# print(poly2)
# print(expand_poly2)


# x = symbols('x')
# a = symbols('a')
# y = symbols('y')
# poly3 = y*x**5 + x**3 + 5*x + x**6
# system_a = [(x**i, a*x**(i-3)) for i in range(7) if i >= 3]
# # poly3.subs(substitu)
# print(poly3)
# print(poly3.subs(system_a))


x = sym.symbols('x')
a = sym.symbols('a')
y = sym.symbols('y')
b = sym.symbols('b')
z = sym.symbols('z')
poly4 = ((2*x+y)**3)*(x*y**2)*z**4
print('poly4 is ',poly4)
poly4 = sym.expand(poly4)
print('expand is ',poly4)

substitute_x = [(x**i, y*a*x**(i-2)) for i in range(10) if i >= 2]
substitute_y = [(y**i, (x**2)*b*y**(i-3)) for i in range(10) if i >= 3]
substitute_z = [(z**i, y*x*z**(i-1)) for i in range(10) if i >= 1]
while any(str(term[0]) in str(poly4) for term in substitute_x) or \
any(str(term[0]) in str(poly4) for term in substitute_y) or \
any(str(term[0]) in str(poly4) for term in substitute_z):
    # print(term)
    # while str(term[0]) in str(poly4):
    print("YEAH")
    poly4=poly4.subs(substitute_y)
    print("after Y",poly4)
    poly4=poly4.subs(substitute_x)
    print("after X",poly4)
    poly4 = poly4.subs(substitute_z)
    print("after Z", poly4)
print(poly4)

# substitute_x = [(x**i, a*x**(i-2)) for i in range(10) if i >= 2]
# a_x_poly4 = poly4.subs(substitute_x)
# print(a_x_poly4)
# poly4 = a_x_poly4




# x = sym.symbols('x')
# a = sym.symbols('a')
# relation = [(x**i, a*x**(i-2)) for i in range(10) if i >= 2]
# print(relation)

# y = sym.symbols('y')
# b = sym.symbols('b')
# ys = [(y**i, (x**2)*b*y**(i-3)) for i in range(10) if i >= 3]
# print(ys)



# def substitute(polynomial, var_list, sub_list):
#     polynomial = sym.expand(polynomial)
#     while (str(var_list[0]) in str(polynomial) or str(var_list[1]) in str(polynomial)):
#         for i in range(len(var_list)):
#             polynomial = polynomial.subs(var_list[i], sub_list[i])
#     return polynomial

# x = sym.symbols('x')
# y = sym.symbols('y')
# a = sym.symbols('a')
# b = sym.symbols('b')
# polynomial = (x+y)*(x*y**2)*y
# polynomial = substitute(polynomial, [x**2, y**3], [a, b*x])
# print(polynomial)

# def aname(subs_what, with_what):
#     relation = [(subs_what,with_what) for i in range(7) if i >= 3]
#     return relation

