from sympy import Matrix,det,symbols,sin,cos,sinh,cosh,diff,Eq,solve,simplify,expand,pprint
from sympy import latex,lambdify
# 定义符号
a,x,L,E,I,w,M,J = symbols('a x L E I w M J',nonzero=True)
A,B,C,D = symbols('A B C D')
# 定义Q(x)和各阶导
Q = A*sin(a*x) + B*cos(a*x) + C*sinh(a*x) + D*cosh(a*x)
Q1 = diff(Q,x)
Q2 = diff(Q,x,2)
Q3 = diff(Q,x,3)
# 定义边界条件
# 在x = 0
bc1 = Eq(Q.subs(x,0),0)
bc2 = Eq(Q1.subs(x,0),0)

# 解A,B
sol = solve([bc1,bc2],(A,B))
# 在x=L
bc3 = Eq(E*I*Q3.subs(x,L),-w**2*Q.subs(x,L)*M)
bc3 = bc3.subs(sol)
# bc4 = Eq(E*I*Q2.subs(x,L),-w**2*Q1.subs(x,L)*J)
bc4 = Eq(E*I*Q2.subs(x,L),0)
bc4 = bc4.subs(sol)
f1 = expand(bc3.lhs-bc3.rhs)
f2 = expand(bc4.lhs-bc4.rhs)
f1_c = f1.coeff(C)
f1_d = f1.coeff(D)
f2_c = f2.coeff(C)
f2_d = f2.coeff(D)
M_c = Matrix([
    [f1_c,f1_d],
    [f2_c,f2_d],
])
