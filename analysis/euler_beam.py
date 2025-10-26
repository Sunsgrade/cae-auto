from sympy import Matrix,det,symbols,sin,cos,sinh,cosh,diff,Eq,solve,simplify,expand,pprint
from sympy import latex,lambdify,factor,symbols,sstr
import os

class EulerBeam:
    def __init__(self, bc_type='cantilever', bc_fixed_func=None, bc_free_func=None):
        # 定义符号  M 顶端点质量，m 分布质量
        self.a, self.x, self.L, self.E, self.I, self.w, self.M, self.J, self.m = symbols('a x L E I w M J m', nonzero=True)
        self.A, self.B, self.C, self.D = symbols('A B C D')
        self.bc_type = bc_type
        self.bc_fixed_func = bc_fixed_func
        self.bc_free_func = bc_free_func
        self._Qx()
        self._boundary_conditions()
        self._solve()
        self._c_matrix()
        self._replace()

    def _Qx(self):
        self.Q = self.A*sin(self.a*self.x) + self.B*cos(self.a*self.x) + self.C*sinh(self.a*self.x) + self.D*cosh(self.a*self.x)
        self.Q1 = diff(self.Q,self.x)
        self.Q2 = diff(self.Q,self.x,2)
        self.Q3 = diff(self.Q,self.x,3)

    def _default_fixed_bc(self):
        # 默认悬臂梁固定端边界条件，x=0处位移和斜率为零
        bc1 = Eq(self.Q.subs(self.x, 0), 0)
        bc2 = Eq(self.Q1.subs(self.x, 0), 0)
        return bc1, bc2

    def _default_free_bc(self):
        # 默认悬臂梁自由端边界条件，x=L处弯矩和剪力为零
        bc3 = Eq(self.E*self.I*self.Q3.subs(self.x,self.L), -self.w**2*self.Q.subs(self.x,self.L)*self.M)
        bc4 = Eq(self.E*self.I*self.Q2.subs(self.x,self.L), 0)
        return bc3, bc4

    def _boundary_conditions(self):
        # 根据 bc_type 选择边界条件
        if self.bc_type == 'cantilever':
            if self.bc_fixed_func:
                self.bc1, self.bc2 = self.bc_fixed_func(self)
            else:
                self.bc1, self.bc2 = self._default_fixed_bc()
            if self.bc_free_func:
                self.bc3, self.bc4 = self.bc_free_func(self)
            else:
                self.bc3, self.bc4 = self._default_free_bc()
        elif self.bc_type == 'simply':
            if self.bc_fixed_func:
                self.bc1, self.bc2 = self.bc_fixed_func(self)
            else:
                # 简支梁固定端边界条件，x=0处位移和弯矩为零
                bc1 = Eq(self.Q.subs(self.x, 0), 0)
                bc2 = Eq(self.Q2.subs(self.x, 0), 0)
                self.bc1, self.bc2 = bc1, bc2
            if self.bc_free_func:
                self.bc3, self.bc4 = self.bc_free_func(self)
            else:
                # 简支梁自由端边界条件，x=L处位移和弯矩为零
                bc3 = Eq(self.Q.subs(self.x, self.L), 0)
                bc4 = Eq(self.Q2.subs(self.x, self.L), 0)
                self.bc3, self.bc4 = bc3, bc4
        else:
            raise ValueError(f"Unknown bc_type: {self.bc_type}")

    def _solve(self):
        self.sol = solve([self.bc1,self.bc2],(self.A,self.B))

    def _c_matrix(self):
        bc3_sub = self.bc3.subs(self.sol)
        bc4_sub = self.bc4.subs(self.sol)
        f1 = expand(bc3_sub.lhs - bc3_sub.rhs)
        f2 = expand(bc4_sub.lhs - bc4_sub.rhs)
        f1_c = f1.coeff(self.C)
        f1_d = f1.coeff(self.D)
        f2_c = f2.coeff(self.C)
        f2_d = f2.coeff(self.D)
        self.M_c = Matrix([
            [f1_c,f1_d],
            [f2_c,f2_d],
        ])

    def _replace(self):
        det = self.M_c.det()
        # w替换掉
        det_w = det.subs(self.w*self.w,self.E*self.I*self.a**4/self.m)
        det_w = factor(det_w)
        self.det_w= simplify(det_w)

    def write_latex(self, filename:str, expressions:list, title=None):
        """将latex表达式写入文件
        Args:
            filename (str): 文件名
            expressions (list): latex表达式列表
            title (str, optional): 标题. Defaults to None.
        """
        # 确保目录存在
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            
        lines = []
        if title:
            lines.append(f"\\section*{{{title}}}\n")
        for desc,expr,numbered in expressions:
            if desc:
                lines.append(f"%{desc}\n")
            if numbered:
                lines.append(f"\\begin{{equation}} + {latex(expr)} + \n\\end{{equation}}\n")
            else:
                lines.append("\\[\n" + latex(expr) + "\n\\]\n")
        with open(filename, "w+", encoding="utf-8") as f:
            f.writelines(lines)

if __name__ == "__main__":
    # 悬臂梁实例
    beam_cantilever = EulerBeam(bc_type='cantilever')
    expressions_cantilever = [
        ("边界条件 bc1", beam_cantilever.bc1, True),
        ("边界条件 bc2", beam_cantilever.bc2, True),
        ("边界条件 bc3", beam_cantilever.bc3, True),
        ("边界条件 bc4", beam_cantilever.bc4, True),
        ("系数矩阵 M_c", beam_cantilever.M_c, False),
        ("特征方程 det_w", beam_cantilever.det_w, True)
    ]
    beam_cantilever.write_latex("latex/cantilever.tex", expressions_cantilever, title="悬臂梁推导")
    print("LaTeX 文件生成完成：latex/cantilever.tex 和 latex/simply.tex")