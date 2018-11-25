#trying to use sympy
# from sympy import *
import sympy as sym

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