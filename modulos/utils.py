"""
Utils - Utilidades para formateo y visualización
"""

import sympy as sp
from sympy import latex, pretty, simplify

class FormateadorMatematico:
    """Clase para formatear expresiones matemáticas"""
    
    def __init__(self):
        # Símbolos Unicode para matemáticas
        self.simbolos_unicode = {
            # Operadores
            '*': '·',
            'sqrt': '√',
            'integral': '∫',
            'partial': '∂',
            'sum': '∑',
            'product': '∏',
            'infinity': '∞',
            
            # Letras griegas
            'alpha': 'α',
            'beta': 'β',
            'gamma': 'γ',
            'delta': 'δ',
            'epsilon': 'ε',
            'theta': 'θ',
            'lambda': 'λ',
            'mu': 'μ',
            'pi': 'π',
            'sigma': 'σ',
            'phi': 'φ',
            'omega': 'ω',
            
            # Comparadores
            '<=': '≤',
            '>=': '≥',
            '!=': '≠',
            '~': '≈',
            
            # Otros
            '+-': '±',
        }
    
    def expresion_a_unicode(self, expr):
        """Convierte expresión SymPy a texto con símbolos Unicode"""
        try:
            # Usar pretty print de SymPy (mejor opción)
            return sp.pretty(expr, use_unicode=True)
        except:
            return str(expr)
    
    def expresion_a_latex(self, expr):
        """Convierte expresión SymPy a LaTeX"""
        try:
            return latex(expr)
        except:
            return str(expr)
    
    def formatear_ecuacion(self, ecuacion):
        """Formatea una ecuación completa"""
        if isinstance(ecuacion, sp.Eq):
            izq = self.expresion_a_unicode(ecuacion.lhs)
            der = self.expresion_a_unicode(ecuacion.rhs)
            return f"{izq}\n\n  =\n\n{der}"
        else:
            return self.expresion_a_unicode(ecuacion)
    
    def crear_caja_titulo(self, titulo, ancho=80):
        """Crea una caja decorativa para títulos"""
        return f"╔{'═' * (ancho-2)}╗\n║{titulo.center(ancho-2)}║\n╚{'═' * (ancho-2)}╝"
    
    def crear_separador(self, texto="", ancho=80, simbolo="━"):
        """Crea un separador decorativo"""
        if texto:
            return f"\n{simbolo * ancho}\n{texto}\n{simbolo * ancho}"
        return simbolo * ancho
    
    def formatear_lista_bonita(self, items, simbolo="•"):
        """Formatea una lista con viñetas"""
        return "\n".join([f"  {simbolo} {item}" for item in items])


class GeneradorPasos:
    """Genera explicaciones paso a paso"""
    
    def __init__(self):
        self.formateador = FormateadorMatematico()
    
    def generar_pasos_separables(self, ecuacion):
        """Genera pasos para variables separables"""
        pasos = []
        pasos.append("🔹 PASO 1: Identificar la forma separable")
        pasos.append("   La ecuación puede escribirse como: dy/dx = g(x)·h(y)")
        pasos.append("")
        pasos.append("🔹 PASO 2: Separar las variables")
        pasos.append("   Reorganizar: dy/h(y) = g(x)dx")
        pasos.append("")
        pasos.append("🔹 PASO 3: Integrar ambos lados")
        pasos.append("   ∫ dy/h(y) = ∫ g(x)dx")
        pasos.append("")
        pasos.append("🔹 PASO 4: Resolver las integrales")
        pasos.append("   Aplicar técnicas de integración apropiadas")
        pasos.append("")
        pasos.append("🔹 PASO 5: Despejar y (si es posible)")
        pasos.append("   Expresar y como función de x")
        return "\n".join(pasos)
    
    def generar_pasos_lineal(self, ecuacion):
        """Genera pasos para ecuación lineal"""
        pasos = []
        pasos.append("🔹 PASO 1: Forma estándar")
        pasos.append("   dy/dx + P(x)y = Q(x)")
        pasos.append("")
        pasos.append("🔹 PASO 2: Calcular factor integrante")
        pasos.append("   μ(x) = exp(∫P(x)dx)")
        pasos.append("")
        pasos.append("🔹 PASO 3: Multiplicar por μ(x)")
        pasos.append("   μ(x)·dy/dx + μ(x)·P(x)·y = μ(x)·Q(x)")
        pasos.append("")
        pasos.append("🔹 PASO 4: Observar que el lado izquierdo es d/dx[μ(x)·y]")
        pasos.append("   d/dx[μ(x)·y] = μ(x)·Q(x)")
        pasos.append("")
        pasos.append("🔹 PASO 5: Integrar")
        pasos.append("   μ(x)·y = ∫μ(x)·Q(x)dx + C")
        pasos.append("")
        pasos.append("🔹 PASO 6: Despejar y")
        pasos.append("   y = [∫μ(x)·Q(x)dx + C] / μ(x)")
        return "\n".join(pasos)
    
    def generar_pasos_exacta(self, ecuacion):
        """Genera pasos para ecuación exacta"""
        pasos = []
        pasos.append("🔹 PASO 1: Verificar si es exacta")
        pasos.append("   Para M(x,y)dx + N(x,y)dy = 0")
        pasos.append("   Verificar: ∂M/∂y = ∂N/∂x")
        pasos.append("")
        pasos.append("🔹 PASO 2: Encontrar F(x,y)")
        pasos.append("   ∂F/∂x = M(x,y) → F = ∫M(x,y)dx + g(y)")
        pasos.append("")
        pasos.append("🔹 PASO 3: Determinar g(y)")
        pasos.append("   ∂F/∂y = N(x,y) → g'(y) = N - ∂/∂y[∫M dx]")
        pasos.append("")
        pasos.append("🔹 PASO 4: Solución implícita")
        pasos.append("   F(x,y) = C")
        return "\n".join(pasos)
    
    def generar_pasos_bernoulli(self, ecuacion):
        """Genera pasos para ecuación de Bernoulli"""
        pasos = []
        pasos.append("🔹 PASO 1: Identificar la forma de Bernoulli")
        pasos.append("   dy/dx + P(x)y = Q(x)y^n  (n ≠ 0, 1)")
        pasos.append("")
        pasos.append("🔹 PASO 2: Hacer sustitución")
        pasos.append("   v = y^(1-n)")
        pasos.append("   dv/dx = (1-n)y^(-n)·dy/dx")
        pasos.append("")
        pasos.append("🔹 PASO 3: Transformar a ecuación lineal")
        pasos.append("   dv/dx + (1-n)P(x)v = (1-n)Q(x)")
        pasos.append("")
        pasos.append("🔹 PASO 4: Resolver ecuación lineal en v")
        pasos.append("   Usar método de factor integrante")
        pasos.append("")
        pasos.append("🔹 PASO 5: Sustituir de vuelta")
        pasos.append("   y = v^(1/(1-n))")
        return "\n".join(pasos)
    
    def generar_pasos_coef_constantes(self, ecuacion):
        """Genera pasos para coeficientes constantes"""
        pasos = []
        pasos.append("🔹 PASO 1: Ecuación característica")
        pasos.append("   Para a_n·y^(n) + ... + a_1·y' + a_0·y = 0")
        pasos.append("   Ecuación característica: a_n·r^n + ... + a_1·r + a_0 = 0")
        pasos.append("")
        pasos.append("🔹 PASO 2: Resolver ecuación característica")
        pasos.append("   Encontrar las raíces r₁, r₂, ..., r_n")
        pasos.append("")
        pasos.append("🔹 PASO 3: Construir solución según tipo de raíces")
        pasos.append("   • Raíces reales distintas: y = C₁e^(r₁x) + C₂e^(r₂x) + ...")
        pasos.append("   • Raíces repetidas: y = (C₁ + C₂x + ...)e^(rx)")
        pasos.append("   • Raíces complejas α±βi: y = e^(αx)[C₁cos(βx) + C₂sin(βx)]")
        return "\n".join(pasos)
    
    def generar_pasos_automatico(self, clasificacion):
        """Genera pasos genéricos según clasificación"""
        if 'separable' in str(clasificacion):
            return self.generar_pasos_separables(None)
        elif '1st_linear' in str(clasificacion):
            return self.generar_pasos_lineal(None)
        elif 'exact' in str(clasificacion):
            return self.generar_pasos_exacta(None)
        elif 'Bernoulli' in str(clasificacion):
            return self.generar_pasos_bernoulli(None)
        elif 'constant_coeff' in str(clasificacion):
            return self.generar_pasos_coef_constantes(None)
        else:
            return "Método automático aplicado por SymPy"


class ValidadorEcuaciones:
    """Valida y verifica ecuaciones"""
    
    @staticmethod
    def tiene_derivadas(ecuacion):
        """Verifica si la ecuación contiene derivadas"""
        return any(isinstance(arg, sp.Derivative) for arg in ecuacion.atoms())
    
    @staticmethod
    def orden_ecuacion(ecuacion, y_func):
        """Determina el orden de la ecuación diferencial"""
        max_orden = 0
        for atom in ecuacion.atoms(sp.Derivative):
            if atom.expr == y_func:
                orden = len(atom.variables)
                max_orden = max(max_orden, orden)
        return max_orden
    
    @staticmethod
    def es_lineal(ecuacion, y_func):
        """Verifica si la ecuación es lineal"""
        # Una ecuación es lineal si y y sus derivadas aparecen solo a la primera potencia
        # y no hay productos entre ellas
        try:
            # Expandir y verificar
            ec_expandida = sp.expand(ecuacion.lhs - ecuacion.rhs)
            
            # Obtener todos los términos con y o derivadas de y
            terminos_y = [term for term in sp.Add.make_args(ec_expandida) 
                         if y_func in term.free_symbols or 
                         any(isinstance(a, sp.Derivative) for a in term.atoms())]
            
            # Verificar que cada término sea lineal
            for term in terminos_y:
                if term.as_coefficient(y_func) is None:
                    # No es simplemente un múltiplo de y
                    derivs = [a for a in term.atoms(sp.Derivative)]
                    if not derivs:
                        return False
            
            return True
        except:
            return None
    
    @staticmethod
    def constantes_en_solucion(solucion):
        """Extrae las constantes de una solución"""
        if isinstance(solucion, sp.Eq):
            expr = solucion.rhs
        else:
            expr = solucion
        
        constantes = [sym for sym in expr.free_symbols if 'C' in str(sym)]
        return sorted(constantes, key=str)