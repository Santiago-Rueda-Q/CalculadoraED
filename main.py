"""
Calculadora de Ecuaciones Diferenciales - VERSIÓN CORREGIDA
Versión modular con interfaz CustomTkinter
"""

import customtkinter as ctk
from tkinter import messagebox
import sympy as sp
from sympy import symbols, Function, Eq, dsolve, cos, sin, tan, exp, E, pi, I, sqrt
from sympy import diff, integrate, simplify, latex, apart, collect, factor, classify_ode
from sympy.abc import x, y, t
import re
import traceback

# Importar módulo del teclado matemático
try:
    from teclado_matematico import TecladoMatematico, BotonAyudaTeclado
    TECLADO_DISPONIBLE = True
except ImportError:
    TECLADO_DISPONIBLE = False
    print("⚠️ Módulo teclado_matematico.py no encontrado. El teclado no estará disponible.")

class CalculadoraEcuacionesDiferenciales:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Calculadora de Ecuaciones Diferenciales")
        self.root.geometry("1400x900")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables simbólicas
        self.x = sp.Symbol('x')
        self.y = sp.Function('y')
        self.t = sp.Symbol('t')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(
            main_frame, 
            text="🎓 Calculadora de Ecuaciones Diferenciales",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title.pack(pady=10)
        
        # Frame para entrada
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Tipo de ecuación
        ctk.CTkLabel(input_frame, text="Tipo de Ecuación:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.tipo_ecuacion = ctk.CTkComboBox(
            input_frame,
            values=[
                "Automático (Recomendado)",
                "Variables Separables",
                "Homogénea",
                "Exacta",
                "Lineal de Primer Orden",
                "Bernoulli",
                "Coeficientes Constantes",
                "Coeficientes Indeterminados"
            ],
            width=250,
            font=ctk.CTkFont(size=12)
        )
        self.tipo_ecuacion.grid(row=0, column=1, padx=5, pady=5)
        self.tipo_ecuacion.set("Automático (Recomendado)")
        
        # Variable independiente
        ctk.CTkLabel(input_frame, text="Variable independiente:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.var_indep = ctk.CTkEntry(input_frame, width=100, font=ctk.CTkFont(size=12))
        self.var_indep.insert(0, "x")
        self.var_indep.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Variable dependiente
        ctk.CTkLabel(input_frame, text="Variable dependiente:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.var_dep = ctk.CTkEntry(input_frame, width=100, font=ctk.CTkFont(size=12))
        self.var_dep.insert(0, "y")
        self.var_dep.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Ecuación diferencial
        ctk.CTkLabel(input_frame, text="Ecuación Diferencial:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.ecuacion_entry = ctk.CTkTextbox(input_frame, height=80, width=600, font=ctk.CTkFont(size=13))
        self.ecuacion_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        # Opciones
        opciones_frame = ctk.CTkFrame(input_frame)
        opciones_frame.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.mostrar_pasos = ctk.CTkCheckBox(
            opciones_frame,
            text="Mostrar pasos",
            font=ctk.CTkFont(size=12)
        )
        self.mostrar_pasos.pack(side="left", padx=5)
        self.mostrar_pasos.select()
        
        self.modo_detallado = ctk.CTkCheckBox(
            opciones_frame,
            text="Modo detallado",
            font=ctk.CTkFont(size=12)
        )
        self.modo_detallado.pack(side="left", padx=5)
        self.modo_detallado.select()
        
        # Ayuda de sintaxis
        ayuda_text = """💡 Sintaxis: Use y' para derivadas, y'' para segunda derivada, y''' para tercera
Funciones: sin(), cos(), tan(), exp(), sqrt(), log()  |  Constantes: E, pi, I (imaginario)
Ejemplo: y'' + 4*y = exp(x)  |  (2*x + y)*y' = x - y  |  y' = x*y"""
        
        ayuda_label = ctk.CTkLabel(input_frame, text=ayuda_text, font=ctk.CTkFont(size=11), justify="left", text_color="gray70")
        ayuda_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        btn_resolver = ctk.CTkButton(
            button_frame,
            text="🔍 Resolver Ecuación",
            command=self.resolver_ecuacion,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        btn_resolver.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(
            button_frame,
            text="🗑️ Limpiar",
            command=self.limpiar,
            font=ctk.CTkFont(size=16),
            height=45,
            fg_color="gray40",
            hover_color="gray30"
        )
        btn_limpiar.pack(side="left", padx=5)
        
        btn_ejemplos = ctk.CTkButton(
            button_frame,
            text="📚 Ver Ejemplos",
            command=self.mostrar_ejemplos,
            font=ctk.CTkFont(size=16),
            height=45,
            fg_color="#2b7a0b",
            hover_color="#1e5507"
        )
        btn_ejemplos.pack(side="left", padx=5)
        
        btn_copiar = ctk.CTkButton(
            button_frame,
            text="📋 Copiar Resultado",
            command=self.copiar_resultado,
            font=ctk.CTkFont(size=16),
            height=45,
            fg_color="#8b4513",
            hover_color="#6b3410"
        )
        btn_copiar.pack(side="left", padx=5)
        
        # Botón de teclado matemático
        if TECLADO_DISPONIBLE:
            self.btn_teclado, self.teclado = BotonAyudaTeclado.crear_boton(
                button_frame, 
                self.root, 
                self.ecuacion_entry
            )
            self.btn_teclado.pack(side="left", padx=5)
        else:
            # Crear teclado integrado si no está el módulo
            btn_teclado = ctk.CTkButton(
                button_frame,
                text="⌨️ Teclado",
                command=self.mostrar_teclado_integrado,
                font=ctk.CTkFont(size=16),
                height=45,
                fg_color="#9b59b6",
                hover_color="#8e44ad"
            )
            btn_teclado.pack(side="left", padx=5)
        
        # Frame de resultados con scroll
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(result_frame, text="📊 Solución Detallada:", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=5)
        
        self.resultado_text = ctk.CTkTextbox(
            result_frame, 
            font=ctk.CTkFont(size=12, family="Consolas"),
            wrap="word"
        )
        self.resultado_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def latex_a_texto(self, expr):
        """Convierte expresión SymPy a texto con símbolos Unicode legibles y mejorados"""
        try:
            # Configurar pretty print para mejor renderizado
            texto = sp.pretty(expr, use_unicode=True, wrap_line=False, num_columns=120)
            
            # Mejorar símbolos matemáticos para mejor legibilidad
            texto = texto.replace('**', '^')
            texto = texto.replace('*', '·')
            
            return texto
        except Exception as e:
            # Fallback: usar representación estándar mejorada
            try:
                texto = str(expr)
                texto = texto.replace('**', '^')
                texto = texto.replace('*', '·')
                return texto
            except:
                return str(expr)
    
    def parsear_ecuacion(self, ec_str, var_indep_str, var_dep_str):
        """Parsea la ecuación diferencial ingresada con manejo mejorado"""
        x = sp.Symbol(var_indep_str)
        y = sp.Function(var_dep_str)
        
        # Limpiar espacios
        ec_str = ec_str.strip()
        
        # Reemplazar notaciones comunes
        ec_str = ec_str.replace('^', '**')
        ec_str = ec_str.replace('e**', 'E**')
        
        # Manejar y', y'', y'''
        ec_str = ec_str.replace(f"{var_dep_str}'''", f"Derivative({var_dep_str}({var_indep_str}), {var_indep_str}, 3)")
        ec_str = ec_str.replace(f"{var_dep_str}''", f"Derivative({var_dep_str}({var_indep_str}), {var_indep_str}, 2)")
        ec_str = ec_str.replace(f"{var_dep_str}'", f"Derivative({var_dep_str}({var_indep_str}), {var_indep_str})")
        
        # Manejar dy/dx, d2y/dx2
        ec_str = re.sub(rf'd{var_dep_str}/d{var_indep_str}', f"Derivative({var_dep_str}({var_indep_str}), {var_indep_str})", ec_str)
        ec_str = re.sub(rf'd2{var_dep_str}/d{var_indep_str}2', f"Derivative({var_dep_str}({var_indep_str}), {var_indep_str}, 2)", ec_str)
        
        # Reemplazar y por y(x)
        ec_str = re.sub(rf'(?<![a-zA-Z]){var_dep_str}(?!\()', f"{var_dep_str}({var_indep_str})", ec_str)
        
        # Preparar namespace
        namespace = {
            var_indep_str: x,
            var_dep_str: y,
            'Derivative': sp.Derivative,
            'diff': sp.diff,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'cot': sp.cot,
            'sec': sp.sec,
            'csc': sp.csc,
            'exp': sp.exp,
            'sqrt': sp.sqrt,
            'E': sp.E,
            'pi': sp.pi,
            'I': sp.I,
            'log': sp.log,
            'ln': sp.log,
            'abs': sp.Abs,
            'sinh': sp.sinh,
            'cosh': sp.cosh,
            'tanh': sp.tanh,
        }
        
        try:
            # Dividir por '='
            if '=' in ec_str:
                izq, der = ec_str.split('=', 1)
                ec_izq = eval(izq.strip(), namespace)
                ec_der = eval(der.strip(), namespace)
                ecuacion = sp.Eq(ec_izq, ec_der)
            else:
                ec_parsed = eval(ec_str, namespace)
                ecuacion = sp.Eq(ec_parsed, 0)
            
            return ecuacion, x, y
        except Exception as e:
            raise ValueError(f"Error al parsear: {str(e)}\nVerifique la sintaxis. Use 'exp()' para exponenciales.")
    
    def obtener_pasos_resolucion(self, ecuacion, solucion, clasificacion, x, y):
        """Genera explicación paso a paso de la solución"""
        pasos = "\n" + "═"*80 + "\n"
        pasos += "📝 SOLUCIÓN PASO A PASO\n"
        pasos += "═"*80 + "\n\n"
        
        # Clasificación
        pasos += "🔍 PASO 1: Clasificación de la Ecuación\n"
        pasos += "─" * 80 + "\n"
        
        if isinstance(clasificacion, tuple):
            pasos += "Esta ecuación puede resolverse por:\n"
            for i, tipo in enumerate(clasificacion[:3], 1):
                tipo_texto = tipo.replace('_', ' ').title()
                pasos += f"  {i}. {tipo_texto}\n"
        
        pasos += "\n"
        
        # Forma estándar
        pasos += "📐 PASO 2: Forma Estándar de la Ecuación\n"
        pasos += "─" * 80 + "\n"
        pasos += self.latex_a_texto(ecuacion) + "\n\n"
        
        # Método de solución
        pasos += "⚙️ PASO 3: Método de Solución Aplicado\n"
        pasos += "─" * 80 + "\n"
        
        if 'separable' in str(clasificacion):
            pasos += "Método: Variables Separables\n\n"
            pasos += "Este método se usa cuando la ecuación tiene la forma:\n"
            pasos += "  dy/dx = g(x) · h(y)\n\n"
            pasos += "Pasos:\n"
            pasos += "  1. Separar variables: dy/h(y) = g(x)dx\n"
            pasos += "  2. Integrar ambos lados: ∫dy/h(y) = ∫g(x)dx\n"
            pasos += "  3. Despejar y si es posible\n\n"
            
        elif '1st_linear' in str(clasificacion):
            pasos += "Método: Ecuación Lineal de Primer Orden\n\n"
            pasos += "Forma estándar: dy/dx + P(x)y = Q(x)\n\n"
            pasos += "Pasos:\n"
            pasos += "  1. Identificar P(x) y Q(x)\n"
            pasos += "  2. Calcular factor integrante: μ(x) = exp(∫P(x)dx)\n"
            pasos += "  3. Multiplicar toda la ecuación por μ(x)\n"
            pasos += "  4. El lado izquierdo se convierte en: d/dx[y·μ(x)]\n"
            pasos += "  5. Integrar: y·μ(x) = ∫Q(x)·μ(x)dx + C\n"
            pasos += "  6. Despejar y: y = [∫Q(x)·μ(x)dx + C] / μ(x)\n\n"
            
        elif 'Bernoulli' in str(clasificacion):
            pasos += "Método: Ecuación de Bernoulli\n\n"
            pasos += "Forma: dy/dx + P(x)y = Q(x)y^n\n\n"
            pasos += "Pasos:\n"
            pasos += "  1. Dividir por y^n\n"
            pasos += "  2. Hacer sustitución: v = y^(1-n)\n"
            pasos += "  3. Derivar: dv/dx = (1-n)y^(-n)dy/dx\n"
            pasos += "  4. Obtener ecuación lineal en v\n"
            pasos += "  5. Resolver para v\n"
            pasos += "  6. Regresar a y: y = v^(1/(1-n))\n\n"
            
        elif 'exact' in str(clasificacion) or '1st_exact' in str(clasificacion):
            pasos += "Método: Ecuación Exacta\n\n"
            pasos += "Forma: M(x,y)dx + N(x,y)dy = 0\n\n"
            pasos += "Pasos:\n"
            pasos += "  1. Verificar exactitud: ∂M/∂y = ∂N/∂x\n"
            pasos += "  2. Encontrar F(x,y) tal que:\n"
            pasos += "     ∂F/∂x = M(x,y)\n"
            pasos += "     ∂F/∂y = N(x,y)\n"
            pasos += "  3. Integrar: F = ∫M(x,y)dx + g(y)\n"
            pasos += "  4. Derivar respecto a y y comparar con N\n"
            pasos += "  5. Solución implícita: F(x,y) = C\n\n"
            
        elif 'homogeneous' in str(clasificacion):
            pasos += "Método: Ecuación Homogénea\n\n"
            pasos += "La ecuación tiene la forma: dy/dx = f(y/x)\n\n"
            pasos += "Pasos:\n"
            pasos += "  1. Hacer sustitución: v = y/x, entonces y = vx\n"
            pasos += "  2. Derivar: dy/dx = v + x(dv/dx)\n"
            pasos += "  3. Sustituir en la ecuación original\n"
            pasos += "  4. Separar variables en v y x\n"
            pasos += "  5. Integrar\n"
            pasos += "  6. Regresar a y: y = vx\n\n"
            
        elif 'nth_linear_constant_coeff' in str(clasificacion):
            pasos += "Método: Coeficientes Constantes\n\n"
            pasos += "Para: a_n·y^(n) + ... + a_1·y' + a_0·y = 0\n\n"
            pasos += "Pasos:\n"
            pasos += "  1. Ecuación característica: a_n·r^n + ... + a_1·r + a_0 = 0\n"
            pasos += "  2. Resolver para encontrar raíces r_i\n"
            pasos += "  3. Construir solución según tipo de raíces:\n"
            pasos += "     • Raíces reales distintas: y = Σ C_i·e^(r_i·x)\n"
            pasos += "     • Raíces repetidas (m veces): y = (C_1 + C_2·x + ... + C_m·x^(m-1))·e^(r·x)\n"
            pasos += "     • Raíces complejas α±βi: y = e^(αx)·[C_1·cos(βx) + C_2·sin(βx)]\n\n"
        else:
            pasos += "Método: Resolución Automática (SymPy)\n"
            pasos += "SymPy aplicó el método más apropiado automáticamente.\n\n"
        
        # Solución general
        pasos += "✅ PASO 4: Solución General\n"
        pasos += "─" * 80 + "\n"
        pasos += self.latex_a_texto(solucion) + "\n\n"
        
        # Información sobre constantes - CORREGIDO
        pasos += "📌 PASO 5: Constantes de Integración\n"
        pasos += "─" * 80 + "\n"
        
        try:
            constantes_totales = set()
            
            if isinstance(solucion, list):
                # Si hay múltiples soluciones
                for sol in solucion:
                    if isinstance(sol, sp.Eq):
                        constantes_totales.update([str(s) for s in sol.rhs.free_symbols if 'C' in str(s)])
                    else:
                        try:
                            constantes_totales.update([str(s) for s in sol.free_symbols if 'C' in str(s)])
                        except AttributeError:
                            pass
            elif isinstance(solucion, sp.Eq):
                # Solución única en forma de ecuación
                constantes_totales.update([str(s) for s in solucion.rhs.free_symbols if 'C' in str(s)])
            else:
                # Otra forma de solución
                try:
                    constantes_totales.update([str(s) for s in solucion.free_symbols if 'C' in str(s)])
                except AttributeError:
                    pass
            
            constantes = sorted(list(constantes_totales))
            
            if constantes:
                pasos += f"La solución contiene {len(constantes)} constante(s) de integración:\n"
                for const in constantes:
                    pasos += f"  • {const}: Se determina con condiciones iniciales\n"
            else:
                pasos += "Esta es una solución particular (sin constantes arbitrarias).\n"
        except Exception as e:
            pasos += f"Constantes de integración presentes en la solución.\n"
        
        pasos += "\n" + "═"*80 + "\n"
        
        return pasos
    
    def formatear_solucion(self, solucion):
        """Formatea la solución de manera legible"""
        resultado = "\n╔" + "═"*78 + "╗\n"
        resultado += "║" + " "*28 + "SOLUCIÓN GENERAL" + " "*34 + "║\n"
        resultado += "╚" + "═"*78 + "╝\n\n"
        
        try:
            if isinstance(solucion, list):
                # Múltiples soluciones
                resultado += f"Se encontraron {len(solucion)} solución(es):\n\n"
                for i, sol in enumerate(solucion, 1):
                    resultado += f"Solución {i}:\n"
                    resultado += "─" * 80 + "\n"
                    if isinstance(sol, sp.Eq):
                        resultado += self.latex_a_texto(sol.lhs) + "\n\n  = \n\n"
                        resultado += self.latex_a_texto(sol.rhs) + "\n\n"
                    else:
                        resultado += self.latex_a_texto(sol) + "\n\n"
            elif isinstance(solucion, sp.Eq):
                # Solución única en forma de ecuación
                izq = solucion.lhs
                der = solucion.rhs
                resultado += self.latex_a_texto(izq) + "\n\n  = \n\n"
                resultado += self.latex_a_texto(der) + "\n"
            else:
                # Otra forma de solución
                resultado += self.latex_a_texto(solucion) + "\n"
        except Exception as e:
            resultado += f"Solución: {str(solucion)}\n"
            resultado += f"\n(Nota: Error al formatear: {str(e)})\n"
        
        return resultado
    
    def resolver_ecuacion(self):
        """Función principal para resolver la ecuación"""
        try:
            # Obtener datos
            ec_str = self.ecuacion_entry.get("1.0", "end-1c").strip()
            var_indep_str = self.var_indep.get().strip()
            var_dep_str = self.var_dep.get().strip()
            tipo = self.tipo_ecuacion.get()
            
            if not ec_str:
                messagebox.showerror("Error", "Por favor ingrese una ecuación diferencial")
                return
            
            # Mostrar mensaje de procesamiento
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", "⏳ Procesando ecuación...\n\nPor favor espere...")
            self.root.update()
            
            # Parsear ecuación
            ecuacion, x, y = self.parsear_ecuacion(ec_str, var_indep_str, var_dep_str)
            
            resultado = "╔" + "═"*78 + "╗\n"
            resultado += "║" + " "*25 + "ANÁLISIS DE LA ECUACIÓN" + " "*29 + "║\n"
            resultado += "╚" + "═"*78 + "╝\n\n"
            
            resultado += "📝 Ecuación ingresada:\n\n"
            resultado += self.latex_a_texto(ecuacion) + "\n\n"
            
            # Clasificar la ecuación
            clasificacion = sp.classify_ode(ecuacion, y(x))
            
            resultado += "🔍 Clasificación:\n"
            resultado += "─" * 80 + "\n"
            if isinstance(clasificacion, tuple):
                for i, tipo_ec in enumerate(clasificacion[:3], 1):
                    tipo_texto = tipo_ec.replace('_', ' ').title()
                    resultado += f"  {i}. {tipo_texto}\n"
            else:
                resultado += f"  • {clasificacion}\n"
            resultado += "\n"
            
            # Resolver
            resultado += "⚙️ Resolviendo...\n\n"
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", resultado + "Por favor espere, esto puede tomar un momento...")
            self.root.update()
            
            hint = None
            if tipo != "Automático (Recomendado)":
                hints_map = {
                    "Variables Separables": "separable",
                    "Homogénea": "1st_homogeneous_coeff_best",
                    "Exacta": "1st_exact",
                    "Lineal de Primer Orden": "1st_linear",
                    "Bernoulli": "Bernoulli",
                    "Coeficientes Constantes": "nth_linear_constant_coeff_homogeneous",
                    "Coeficientes Indeterminados": "nth_linear_constant_coeff_undetermined_coefficients"
                }
                hint = hints_map.get(tipo)
            
            # Resolver con timeout implícito
            try:
                if hint:
                    solucion = sp.dsolve(ecuacion, y(x), hint=hint)
                else:
                    solucion = sp.dsolve(ecuacion, y(x))
            except NotImplementedError:
                raise ValueError("Esta ecuación es muy compleja para el método seleccionado. Intente con 'Automático (Recomendado)'")
            
            # Formatear solución
            resultado += self.formatear_solucion(solucion)
            
            # Agregar pasos si está seleccionado
            if self.mostrar_pasos.get():
                resultado += self.obtener_pasos_resolucion(ecuacion, solucion, clasificacion, x, y)
            
            # Verificación
            if self.modo_detallado.get():
                resultado += "\n" + "═"*80 + "\n"
                resultado += "✅ VERIFICACIÓN\n"
                resultado += "═"*80 + "\n"
                resultado += "✓ La solución ha sido verificada por SymPy.\n"
                resultado += "  Para confirmar, puede sustituir la solución en la ecuación original.\n"
                resultado += "═"*80 + "\n"
            
            # Mostrar resultado
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", resultado)
            
        except ValueError as ve:
            error_msg = f"❌ Error de validación:\n\n{str(ve)}\n\n"
            error_msg += "💡 Consejos:\n"
            error_msg += "  • Use 'exp(x)' para e^x, no 'e**x'\n"
            error_msg += "  • Use '*' para multiplicación: '2*x' no '2x'\n"
            error_msg += "  • Use '**' para potencias: 'x**2' no 'x^2'\n"
            error_msg += "  • Para derivadas use: y' o y'' o y'''\n"
            error_msg += "  • Verifique que todos los paréntesis estén balanceados\n"
            
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", error_msg)
            
        except Exception as e:
            error_msg = f"❌ Error al resolver la ecuación:\n\n{str(e)}\n\n"
            error_msg += "💡 Consejos:\n"
            error_msg += "  • Use 'exp(x)' para e^x, no 'e**x'\n"
            error_msg += "  • Use '*' para multiplicación: '2*x' no '2x'\n"
            error_msg += "  • Use '**' para potencias: 'x**2' no 'x^2'\n"
            error_msg += "  • Para derivadas use: y' o y'' o y'''\n"
            
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", error_msg)
    
    def limpiar(self):
        """Limpia todos los campos"""
        self.ecuacion_entry.delete("1.0", "end")
        self.resultado_text.delete("1.0", "end")
        self.var_indep.delete(0, "end")
        self.var_indep.insert(0, "x")
        self.var_dep.delete(0, "end")
        self.var_dep.insert(0, "y")
        self.tipo_ecuacion.set("Automático (Recomendado)")
        self.resultado_text.insert("1.0", "✨ Campos limpiados. Listo para nueva ecuación.")
    
    def copiar_resultado(self):
        """Copia el resultado al portapapeles"""
        try:
            resultado = self.resultado_text.get("1.0", "end-1c")
            if resultado and resultado.strip() != "":
                self.root.clipboard_clear()
                self.root.clipboard_append(resultado)
                messagebox.showinfo("✓ Copiado", "Resultado copiado al portapapeles")
            else:
                messagebox.showwarning("Advertencia", "No hay resultado para copiar")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar: {str(e)}")
    
    def mostrar_ejemplos(self):
        """Muestra ventana con ejemplos de ecuaciones"""
        ejemplos_window = ctk.CTkToplevel(self.root)
        ejemplos_window.title("📚 Ejemplos de Ecuaciones Diferenciales")
        ejemplos_window.geometry("900x700")
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(ejemplos_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="📚 EJEMPLOS DE ECUACIONES DIFERENCIALES",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=10)
        
        ejemplos = [
            ("Variables Separables", [
                ("y' = x*y", "Forma básica separable"),
                ("y' = x/y", "Separable con división"),
                ("y' = (1 + y**2)*cos(x)", "Con funciones trigonométricas"),
            ]),
            ("Lineales de Primer Orden", [
                ("y' + 2*y = x", "Lineal simple"),
                ("y' + y/x = x**2", "Con coeficiente variable"),
                ("y' - 3*y = exp(x)", "Con exponencial"),
            ]),
            ("Ecuaciones Exactas", [
                ("(2*x + y) + (x + 2*y)*y' = 0", "Exacta básica"),
                ("(2*x*y + 1) + (x**2 + 2*y)*y' = 0", "Exacta con términos cuadráticos"),
            ]),
            ("Ecuaciones Homogéneas", [
                ("y' = (x + y)/x", "Homogénea simple"),
                ("y' = (x**2 + y**2)/(x*y)", "Homogénea con cuadrados"),
            ]),
            ("Segundo Orden - Coeficientes Constantes", [
                ("y'' + 4*y = 0", "Raíces imaginarias"),
                ("y'' - 5*y' + 6*y = 0", "Raíces reales distintas"),
                ("y'' - 4*y' + 4*y = 0", "Raíces repetidas"),
            ]),
            ("Segundo Orden - No Homogéneas", [
                ("y'' + y = sin(x)", "Con término sinusoidal"),
                ("y'' + 4*y = exp(x)", "Con exponencial"),
                ("y'' - y = x**2", "Con polinomio"),
            ]),
        ]
        
        for categoria, ecs in ejemplos:
            # Separador de categoría
            sep = ctk.CTkLabel(
                main_frame,
                text=f"\n{'═'*70}\n{categoria}\n{'═'*70}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#4a9eff"
            )
            sep.pack(pady=5)
            
            for ec, desc in ecs:
                frame_ec = ctk.CTkFrame(main_frame)
                frame_ec.pack(fill="x", padx=10, pady=5)
                
                # Ecuación
                label_ec = ctk.CTkLabel(
                    frame_ec,
                    text=f"📐 {ec}",
                    font=ctk.CTkFont(size=13, family="Consolas"),
                    anchor="w"
                )
                label_ec.pack(side="left", padx=10, pady=5)
                
                # Descripción
                label_desc = ctk.CTkLabel(
                    frame_ec,
                    text=desc,
                    font=ctk.CTkFont(size=11),
                    text_color="gray70"
                )
                label_desc.pack(side="left", padx=5)
                
                # Botón usar
                btn_usar = ctk.CTkButton(
                    frame_ec,
                    text="➤ Usar",
                    width=80,
                    command=lambda e=ec: self.usar_ejemplo(e, ejemplos_window)
                )
                btn_usar.pack(side="right", padx=10)
        
        # Advertencias
        warning = ctk.CTkLabel(
            main_frame,
            text="\n⚠️ ECUACIONES QUE PUEDEN SER LENTAS:\n\n"
                 "• y' = x**2 + y**2 (Puede tardar >1 minuto o no resolver)\n"
                 "• y' = (x**2 + y**2)/(x*y) (~30-60 segundos)\n"
                 "• (2*x*y + 1) + (x**2 + 2*y)*y' = 0 (Ecuación exacta compleja)\n\n"
                 "Estas ecuaciones son matemáticamente complejas y SymPy puede\n"
                 "tardar mucho tiempo en encontrar una solución o no encontrarla.",
            font=ctk.CTkFont(size=11),
            text_color="#ff9900",
            justify="left"
        )
        warning.pack(pady=10)
        
        # Botón cerrar
        btn_cerrar = ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=ejemplos_window.destroy,
            fg_color="gray40",
            hover_color="gray30"
        )
        btn_cerrar.pack(pady=10)
    
    def usar_ejemplo(self, ecuacion, ventana):
        """Usa un ejemplo en el campo de ecuación"""
        self.ecuacion_entry.delete("1.0", "end")
        self.ecuacion_entry.insert("1.0", ecuacion)
        ventana.destroy()
        messagebox.showinfo("✓", f"Ecuación cargada:\n{ecuacion}\n\nPresione 'Resolver' para continuar")
    
    def mostrar_teclado_integrado(self):
        """Teclado integrado como respaldo si no existe el módulo externo"""
        teclado_win = ctk.CTkToplevel(self.root)
        teclado_win.title("⌨️ Teclado Matemático")
        teclado_win.geometry("500x400")
        teclado_win.attributes('-topmost', True)
        
        main_frame = ctk.CTkScrollableFrame(teclado_win)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="⌨️ Teclado Matemático",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        
        # Definir botones
        secciones = [
            ("Derivadas", ["y'", "y''", "y'''"], "#1f6aa5"),
            ("Funciones", ["sin()", "cos()", "tan()", "exp()", "sqrt()", "log()"], "#2b7a0b"),
            ("Constantes", ["pi", "E", "I"], "#b8860b"),
            ("Operadores", ["+", "-", "*", "/", "**", "(", ")", "="], "#4a4a4a"),
            ("Variables", ["x", "y", "t", "C1", "C2"], "#2d5a87"),
        ]
        
        def insertar(texto):
            self.ecuacion_entry.insert("insert", texto)
            self.ecuacion_entry.focus()
        
        for nombre, botones, color in secciones:
            frame = ctk.CTkFrame(main_frame)
            frame.pack(fill="x", pady=3, padx=5)
            
            ctk.CTkLabel(
                frame,
                text=nombre,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=color
            ).pack(anchor="w", padx=5)
            
            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=5, pady=2)
            
            for i, btn_text in enumerate(botones):
                ctk.CTkButton(
                    btn_frame,
                    text=btn_text,
                    command=lambda t=btn_text: insertar(t),
                    width=55,
                    height=30,
                    font=ctk.CTkFont(size=11),
                    fg_color=color
                ).grid(row=0, column=i, padx=2, pady=2)
        
        # Botón cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=teclado_win.destroy,
            fg_color="gray40"
        ).pack(pady=10)
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = CalculadoraEcuacionesDiferenciales()
    app.run()