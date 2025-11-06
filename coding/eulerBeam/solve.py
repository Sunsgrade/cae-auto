import numpy as np
from math import sqrt, pi
from sympy import lambdify
from formula import EulerBeam


class BeamModel:
    def __init__(self, params: dict):
        """初始化并计算派生参数"""
        self.params = params.copy()
        self._compute_derived_params()
        self._build_det_function()
        self.beam = EulerBeam()
        

    def _compute_derived_params(self):
        """根据输入参数计算派生参数"""
        p = self.params
        p["I"] = pi / 64 * (p["D"]**4 - p["d"]**4)
        p["m"] = p["rho"] * pi / 4 * (p["D"]**2 - p["d"]**2)

    def _build_det_function(self):
        """构建特征方程 f(a)"""
        p = self.params
        det_expr = self.beam.det_simple.subs({
            self.beam.m: p["m"],
            self.beam.M: p["M"],
            self.beam.L: p["L"],
        })
        self.f = lambdify(self.beam.a, det_expr, "numpy")

    # ------------------ 数值方法 ------------------
    @staticmethod
    def bisection(f, a, b, tol=1e-12, max_iter=200):
        """二分法求根"""
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            raise ValueError(f"区间 [{a},{b}] 无符号变化 (fa={fa:.3e}, fb={fb:.3e})")
        for _ in range(max_iter):
            m = (a + b) / 2
            fm = f(m)
            if abs(fm) < tol or (b - a) / 2 < tol:
                return m
            if fa * fm <= 0:
                b, fb = m, fm
            else:
                a, fa = m, fm
        return m

    def find_roots(self, n=3, x_max=50, step=1e-3):
        """扫描区间并自动用二分法求前n个正根"""
        xs = np.arange(1e-6, x_max, step)
        vals = self.f(xs)
        roots = []
        for i in range(len(xs) - 1):
            if vals[i] * vals[i + 1] < 0:
                root = self.bisection(self.f, xs[i], xs[i + 1])
                roots.append(root)
                if len(roots) >= n:
                    break
        return roots

    def natural_frequency(self, r):
        """根据特征根计算固有频率"""
        p = self.params
        return r**2 * sqrt(p["E"] * p["I"] / (p["m"] * p["L"]**4)) / (2 * pi)

    def summary(self, roots):
        """打印结果"""
        print("\n特征根 r (前3个):")
        for i, r in enumerate(roots, 1):
            print(f"  r{i} = {r:.6f}")
        print("\n固有频率 f (Hz):")
        for i, r in enumerate(roots, 1):
            fn = self.natural_frequency(r)
            print(f"  f{i} = {fn:.6f}")


# ------------------ 主程序 ------------------
if __name__ == "__main__":
    params = {
        "E": 2.06e11,
        "D": 0.114,
        "d": 0.109,
        "L": 3.3,
        "M": 15.4,
        "rho": 7850,
    }

    model = BeamModel(params)
    roots = model.find_roots(n=3)
    model.summary(roots)