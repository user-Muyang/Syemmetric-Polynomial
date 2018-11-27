# Use sympy to perform symbolic operation
# from sympy import *
import sympy as sym

x = sym.symbols('x')
a = sym.symbols('a', integer=True)
y = sym.symbols('y')
b = sym.symbols('b', integer=True)
z = sym.symbols('z')
poly4 = ((2*x+y)**3)*(x*y**2)*z**4
print('poly4 is', poly4)
poly4 = sym.expand(poly4)
print('expand is', poly4)

# substitute_x = [(x**i, y*a*x**(i-2)) for i in range(10) if i >= 2]

# substitute_y = [(y**i, (x**2)*b*y**(i-3)) for i in range(10) if i >= 3]
# substitute_z = [(z**i, y*x*z**(i-1)) for i in range(10) if i >= 1]
# print(sym.degree(poly4,gen=x))
# while any(str(term[0]) in str(poly4) for term in substitute_x) or \
# any(str(term[0]) in str(poly4) for term in substitute_y) or \
# any(str(term[0]) in str(poly4) for term in substitute_z):
#     poly4 = poly4.subs([(x**i, y*a*x**(i-2)) for i in range(sym.degree(poly4, gen=x)+1) if i >= 2])
#     poly4 = poly4.subs([(y**i, (x**2)*b*y**(i-3)) for i in range(sym.degree(poly4, gen=y)+1) if i >= 3])
#     poly4 = poly4.subs([(z**i, y*x*z**(i-1)) for i in range(sym.degree(poly4, gen=y)+1) if i >= 1])
# print(poly4)


while sym.degree(poly4, gen=x) >= 2 or \
        sym.degree(poly4, gen=y) >= 3 or \
        sym.degree(poly4, gen=z) >=1:
    poly4 = poly4.subs([(x**i, y*a*x**(i-2)) for i in range(sym.degree(poly4, gen=x)+1) if i >= 2])
    poly4 = poly4.subs([(y**i, (x**2)*b*y**(i-3)) for i in range(sym.degree(poly4, gen=y)+1) if i >= 3])
    poly4 = poly4.subs([(z**i, y*x*z**(i-1)) for i in range(sym.degree(poly4, gen=y)+1) if i >= 1])
print(poly4)




def find_basis(polynomial=0,relation_list=[]):
    # degree_list = []
    # degree_x = sym.degree(x**2-a, gen=x)
    # degree_y = sym.degree(y**3-b*x, gen=y)
    # # degree_z = sym.degree(polynomial, gen=z)
    # degree_list.append(degree_x)
    # degree_list.append(degree_y)
    # # degree_list.append(degree_z)
    # for i in range(len(degree_list)):
    #     if degree_list[i] != 0:
    #         degree_list[i] = degree_list[i] - 1
    # print(degree_list)


    # basis_list = []
    # basis_list.append(1)
    # # basis_large = x**degree_list[0]*y**degree_list[1]
    # # basis_list.append(basis_large)
    # copied_list = degree_list.copy()
    # while copied_list[1] > 0:
    #     basis_list.append(x**copied_list[0]*y**copied_list[1])
    #     copied_list[1] = copied_list[1] - 1
    # basis_list.append(x**copied_list[0]*y**copied_list[1])

    # copied_list = degree_list.copy()
    # print(copied_list)
    # while copied_list[0] > 0:
    #     basis_list.append(x**copied_list[0]*y**copied_list[1])
    #     copied_list[0] = copied_list[0] - 1
    # basis_list.append(x**copied_list[0]*y**copied_list[1])
    relation = x**2*y**3
    list_x = [1]
    list_y = [1]
    while sym.degree(list_x[len(list_x)-1], gen=x) < sym.degree(relation, gen=x)-1:
        list_x.append(list_x[len(list_x)-1]*x)
    print('list_x',list_x)
    while sym.degree(list_y[len(list_y)-1], gen=y) < sym.degree(relation, gen=y)-1:
        list_y.append(list_y[len(list_y)-1]*y)
    print('list_y', list_y)

    list_final = []
    for x_basis in list_x:
        for y_basis in list_y:
            list_final.append(x_basis*y_basis)
    print('list_final', list_final)
    return list_final