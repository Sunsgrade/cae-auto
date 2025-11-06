from sympy import Matrix,det,symbols,sin,cos,sinh,cosh,diff,Eq,solve,simplify,expand,pprint
from sympy import latex,lambdify,factor,symbols,sstr
import os

class EulerBeam:
    def __init__(self, bc_fixed_func=None, bc_free_func=None):
        # 定义符号  M 顶端点质量，m 分布质量
        self.a, self.x, self.L, self.E, self.I, self.w, self.M, self.J, self.m = symbols('a x L E I w M J m', nonzero=True)
        self.A, self.B, self.C, self.D = symbols('A B C D')
        # 边界类型
        self.bc_fixed_func = bc_fixed_func
        self.bc_free_func = bc_free_func
        # 调用初始化函数
        self._initialize()

    def _initialize(self):
        self._Qx()
        self._default_fixed_bc()
        self._default_free_bc()
        self._boundary_conditions()
        self._solve()
        self._c_matrix()
        self._replace()
    # _ 表示这是一个内部方法（internal method），不建议外部直接调用。
    def _Qx(self):
        """
        定义Q(x) 及其导数
        """
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
        # 默认悬臂梁自由端边界条件，带质量的。
        bc3 = Eq(self.E*self.I*self.Q3.subs(self.x,self.L), -self.w**2*self.Q.subs(self.x,self.L)*self.M)
        bc4 = Eq(self.E*self.I*self.Q2.subs(self.x,self.L), 0)
        return bc3, bc4

    def _boundary_conditions(self):
        # 边界条件选择
        if self.bc_fixed_func:
            self.bc1, self.bc2 = self.bc_fixed_func(self)
        else:
            self.bc1, self.bc2 = self._default_fixed_bc()
        if self.bc_free_func:
            self.bc3, self.bc4 = self.bc_free_func(self)
        else:
            self.bc3, self.bc4 = self._default_free_bc()

    def _solve(self):
        self.sol = solve([self.bc1,self.bc2],(self.A,self.B))
        if not self.sol:
            raise ValueError("无法求解 A, B —— 检查边界条件定义。")

    def _c_matrix(self):
        bc3_sub = self.bc3.subs(self.sol)
        bc4_sub = self.bc4.subs(self.sol)
        f1 = expand(bc3_sub.lhs - bc3_sub.rhs)
        f2 = expand(bc4_sub.lhs - bc4_sub.rhs)
        self.M_c = Matrix([
            [f1.coeff(self.C),f1.coeff(self.D)],
            [f2.coeff(self.C),f2.coeff(self.D)],
        ])

    def _replace(self):
        det = self.M_c.det()
        # w替换掉
        det_w = det.subs(self.w**2,self.E*self.I*self.a**4/self.m)
        det_w = factor(det_w)
        self.det = simplify(det_w)
        self.det_simple = simplify(self.det/(2*self.E**2 * self.I**2 * self.a**5))
        self.det_simple = self.det_simple.subs(self.a,self.a/self.L)

    def write_latex(self, filename: str, expressions: list, title=None):
        """
        将符号表达式写成完整的可编译 LaTeX 文档（自动限制公式宽度）。
        Args:
            filename (str): 输出文件路径，例如 "latex/cantilever.tex"
            expressions (list): [(描述, 表达式, 是否编号), ...]
            title (str, optional): 文档标题
        """
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        lines = [
            r"\documentclass[12pt,a4paper]{article}",
            r"\usepackage[UTF8]{ctex}",
            r"\usepackage{amsmath,amssymb,amsfonts}",
            r"\usepackage{geometry}",
            r"\geometry{a4paper, left=1.5cm, right=1.5cm, top=2cm, bottom=2cm}",
            r"\usepackage{graphicx}",
            r"\usepackage{adjustbox}",  # ⭐ 自动缩放关键包
            r"\usepackage{hyperref}",
            "",
            rf"\title{{{title or '自动生成的LaTeX文档'}}}",
            r"\author{EulerBeam 自动生成}",
            r"\date{\today}",
            "",
            r"\begin{document}",
            r"\maketitle",
            "",
        ]
        if title:
            lines.append(f"\\section*{{{title}}}\n")
        for desc, expr, numbered in expressions:
            if desc:
                lines.append(f"% {desc}\n")
                lines.append(f"\\subsection*{{{desc}}}\n")
            expr_tex = latex(expr)
            # ✅ 自动缩放以适配页面宽度
            expr_tex = f"\\begin{{adjustbox}}{{max width=\\textwidth}}${expr_tex}$\\end{{adjustbox}}"
            if numbered:
                lines.append(f"\\begin{{equation}}\n{expr_tex}\n\\end{{equation}}\n")
            else:
                lines.append("\\[\n" + expr_tex + "\n\\]\n")
        lines.append(r"\end{document}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"LaTeX 文件已生成：{filename}")
if __name__ == "__main__":
    # 悬臂梁实例
    beam_cantilever = EulerBeam()
    expressions_cantilever = [
        ("边界条件 bc1", beam_cantilever.bc1, True),
        ("边界条件 bc2", beam_cantilever.bc2, True),
        ("边界条件 bc3", beam_cantilever.bc3, True),
        ("边界条件 bc4", beam_cantilever.bc4, True),
        ("系数矩阵 M\\_c", beam_cantilever.M_c, False),
        ("最终结果 det", beam_cantilever.det, True),
        ("简化结果 det\\_simple", beam_cantilever.det_simple, True),
      
    ]
    beam_cantilever.write_latex("latex/cantilever.tex", expressions_cantilever, title="悬臂梁推导")
