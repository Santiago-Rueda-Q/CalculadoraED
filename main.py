import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import sympy as sp
from sympy import symbols, Function, Eq, dsolve, cos, sin, tan, exp, E, pi, I, sqrt
from sympy import diff, integrate, simplify, latex
from sympy.abc import x, y, t
import re

class CalculadoraEcuacionesDiferenciales:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Calculadora de Ecuaciones Diferenciales")
        self.root.geometry("1200x800")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables simbólicas
        self.x = sp.Symbol('x')
        self.y = sp.Function('y')
        self.t = sp.Symbol('t')
        self.C1 = sp.Symbol('C1')
        self.C2 = sp.Symbol('C2')
        self.C3 = sp.Symbol('C3')
        self.C4 = sp.Symbol('C4')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(
            main_frame, 
            text="Calculadora de Ecuaciones Diferenciales",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=10)
        
        # Frame para entrada
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Tipo de ecuación
        ctk.CTkLabel(input_frame, text="Tipo de Ecuación:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.tipo_ecuacion = ctk.CTkComboBox(
            input_frame,
            values=[
                "Variables Separables",
                "Homogénea",
                "Exacta",
                "Lineal de Primer Orden",
                "Bernoulli",
                "Coeficientes Constantes",
                "Coeficientes Indeterminados",
                "Automático (SymPy)"
            ],
            width=250
        )
        self.tipo_ecuacion.grid(row=0, column=1, padx=5, pady=5)
        self.tipo_ecuacion.set("Automático (SymPy)")
        
        # Variable independiente
        ctk.CTkLabel(input_frame, text="Variable independiente:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.var_indep = ctk.CTkEntry(input_frame, width=100)
        self.var_indep.insert(0, "x")
        self.var_indep.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Variable dependiente
        ctk.CTkLabel(input_frame, text="Variable dependiente:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.var_dep = ctk.CTkEntry(input_frame, width=100)
        self.var_dep.insert(0, "y")
        self.var_dep.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Ecuación diferencial
        ctk.CTkLabel(input_frame, text="Ecuación Diferencial:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ecuacion_entry = ctk.CTkTextbox(input_frame, height=80, width=500)
        self.ecuacion_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        # Ayuda de sintaxis
        ayuda_text = """Sintaxis: Use y' o dy/dx para derivadas, y'' para segunda derivada
Ejemplos: 
- Variables separables: y' = x*y
- Lineal: y' + 2*y = x
- Orden superior: y'' + 4*y' + 4*y = 0
Funciones: sin(), cos(), tan(), exp(), sqrt(), E (euler), pi, I (imaginario)"""
        
        ayuda_label = ctk.CTkLabel(input_frame, text=ayuda_text, font=ctk.CTkFont(size=10), justify="left")
        ayuda_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        btn_resolver = ctk.CTkButton(
            button_frame,
            text="Resolver",
            command=self.resolver_ecuacion,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        btn_resolver.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(
            button_frame,
            text="Limpiar",
            command=self.limpiar,
            font=ctk.CTkFont(size=16),
            height=40,
            fg_color="gray"
        )
        btn_limpiar.pack(side="left", padx=5)
        
        btn_ejemplos = ctk.CTkButton(
            button_frame,
            text="Ver Ejemplos",
            command=self.mostrar_ejemplos,
            font=ctk.CTkFont(size=16),
            height=40,
            fg_color="green"
        )
        btn_ejemplos.pack(side="left", padx=5)
        
        # Frame de resultados
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(result_frame, text="Solución:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.resultado_text = ctk.CTkTextbox(result_frame, font=ctk.CTkFont(size=12))
        self.resultado_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def parsear_ecuacion(self, ec_str, var_indep_str, var_dep_str):
        """Parsea la ecuación diferencial ingresada"""
        x = sp.Symbol(var_indep_str)
        y = sp.Function(var_dep_str)
        
        # Reemplazar notaciones comunes
        ec_str = ec_str.replace('^', '**')
        ec_str = ec_str.replace('e', 'E')
        
        # Manejar y', y'', y'''
        ec_str = ec_str.replace(f"{var_dep_str}'''", f"diff({var_dep_str}({var_indep_str}), {var_indep_str}, 3)")
        ec_str = ec_str.replace(f"{var_dep_str}''", f"diff({var_dep_str}({var_indep_str}), {var_indep_str}, 2)")
        ec_str = ec_str.replace(f"{var_dep_str}'", f"diff({var_dep_str}({var_indep_str}), {var_indep_str})")
        
        # Manejar dy/dx
        ec_str = re.sub(rf'd{var_dep_str}/d{var_indep_str}', f"diff({var_dep_str}({var_indep_str}), {var_indep_str})", ec_str)
        
        # Reemplazar y por y(x)
        ec_str = re.sub(rf'\b{var_dep_str}\b(?!\()', f"{var_dep_str}({var_indep_str})", ec_str)
        
        # Preparar namespace para eval
        namespace = {
            var_indep_str: x,
            var_dep_str: y,
            'diff': sp.diff,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'exp': sp.exp,
            'sqrt': sp.sqrt,
            'E': sp.E,
            'pi': sp.pi,
            'I': sp.I,
            'log': sp.log,
            'ln': sp.log,
        }
        
        try:
            # Dividir por '='
            if '=' in ec_str:
                izq, der = ec_str.split('=')
                ec_izq = eval(izq.strip(), namespace)
                ec_der = eval(der.strip(), namespace)
                ecuacion = sp.Eq(ec_izq, ec_der)
            else:
                ec_parsed = eval(ec_str, namespace)
                ecuacion = sp.Eq(ec_parsed, 0)
            
            return ecuacion, x, y
        except Exception as e:
            raise ValueError(f"Error al parsear la ecuación: {str(e)}")
    
    def resolver_variables_separables(self, ecuacion, x, y):
        """Resuelve ecuaciones de variables separables"""
        resultado = "=== Método: Variables Separables ===\n\n"
        try:
            sol = sp.dsolve(ecuacion, y(x), hint='separable')
            resultado += f"Solución general:\n{sol}\n\n"
            return resultado
        except:
            return None
    
    def resolver_homogenea(self, ecuacion, x, y):
        """Resuelve ecuaciones homogéneas"""
        resultado = "=== Método: Ecuación Homogénea ===\n\n"
        try:
            sol = sp.dsolve(ecuacion, y(x), hint='1st_homogeneous_coeff_best')
            resultado += f"Solución general:\n{sol}\n\n"
            return resultado
        except:
            return None
    
    def resolver_exacta(self, ecuacion, x, y):
        """Resuelve ecuaciones exactas"""
        resultado = "=== Método: Ecuación Exacta ===\n\n"
        try:
            sol = sp.dsolve(ecuacion, y(x), hint='1st_exact')
            resultado += f"Solución general:\n{sol}\n\n"
            return resultado
        except:
            return None
    
    def resolver_lineal(self, ecuacion, x, y):
        """Resuelve ecuaciones lineales de primer orden"""
        resultado = "=== Método: Ecuación Lineal de Primer Orden ===\n\n"
        try:
            sol = sp.dsolve(ecuacion, y(x), hint='1st_linear')
            resultado += f"Solución general:\n{sol}\n\n"
            return resultado
        except:
            return None
    
    def resolver_bernoulli(self, ecuacion, x, y):
        """Resuelve ecuaciones de Bernoulli"""
        resultado = "=== Método: Ecuación de Bernoulli ===\n\n"
        try:
            sol = sp.dsolve(ecuacion, y(x), hint='Bernoulli')
            resultado += f"Solución general:\n{sol}\n\n"
            return resultado
        except:
            return None
    
    def resolver_coef_constantes(self, ecuacion, x, y):
        """Resuelve ecuaciones con coeficientes constantes"""
        resultado = "=== Método: Coeficientes Constantes ===\n\n"
        try:
            sol = sp.dsolve(ecuacion, y(x))
            resultado += f"Solución general:\n{sol}\n\n"
            return resultado
        except:
            return None
    
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
            
            # Parsear ecuación
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", "Procesando...\n")
            self.root.update()
            
            ecuacion, x, y = self.parsear_ecuacion(ec_str, var_indep_str, var_dep_str)
            
            resultado = f"Ecuación ingresada:\n{ecuacion}\n\n"
            
            # Resolver según el tipo
            solucion = None
            
            if tipo == "Variables Separables":
                solucion = self.resolver_variables_separables(ecuacion, x, y)
            elif tipo == "Homogénea":
                solucion = self.resolver_homogenea(ecuacion, x, y)
            elif tipo == "Exacta":
                solucion = self.resolver_exacta(ecuacion, x, y)
            elif tipo == "Lineal de Primer Orden":
                solucion = self.resolver_lineal(ecuacion, x, y)
            elif tipo == "Bernoulli":
                solucion = self.resolver_bernoulli(ecuacion, x, y)
            elif tipo == "Coeficientes Constantes":
                solucion = self.resolver_coef_constantes(ecuacion, x, y)
            else:  # Automático
                resultado += "=== Resolución Automática (SymPy) ===\n\n"
                sol = sp.dsolve(ecuacion, y(x))
                
                # Clasificar la ecuación
                clasificacion = sp.classify_ode(ecuacion, y(x))
                resultado += f"Clasificación de la ecuación:\n{clasificacion}\n\n"
                
                resultado += f"Solución general:\n{sol}\n\n"
                solucion = ""
            
            if solucion:
                resultado += solucion
            
            # Mostrar resultado
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", resultado)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver la ecuación:\n{str(e)}")
            self.resultado_text.delete("1.0", "end")
            self.resultado_text.insert("1.0", f"Error: {str(e)}")
    
    def limpiar(self):
        """Limpia todos los campos"""
        self.ecuacion_entry.delete("1.0", "end")
        self.resultado_text.delete("1.0", "end")
        self.var_indep.delete(0, "end")
        self.var_indep.insert(0, "x")
        self.var_dep.delete(0, "end")
        self.var_dep.insert(0, "y")
        self.tipo_ecuacion.set("Automático (SymPy)")
    
    def mostrar_ejemplos(self):
        """Muestra ejemplos de ecuaciones"""
        ejemplos = """
EJEMPLOS DE ECUACIONES DIFERENCIALES:

1. Variables Separables:
   y' = x*y
   y' = y/x

2. Ecuaciones Lineales:
   y' + 2*y = x
   y' - 3*y = exp(x)

3. Ecuaciones Homogéneas:
   y' = (x + y)/(x - y)

4. Ecuaciones Exactas:
   (2*x*y + 1) + (x**2 + 2*y) * y' = 0

5. Ecuación de Bernoulli:
   y' + y = y**2

6. Coeficientes Constantes (orden superior):
   y'' + 4*y' + 4*y = 0
   y'' - 5*y' + 6*y = 0

7. Coeficientes Indeterminados:
   y'' + y = sin(x)
   y'' + 4*y = exp(x)

8. Con funciones trigonométricas:
   y' = sin(x)*cos(y)
   y'' + y = cos(2*x)

9. Con exponenciales:
   y' = exp(x - y)
   y'' - 2*y' + y = exp(2*x)

NOTACIÓN:
- Use y' para dy/dx
- Use y'' para la segunda derivada
- Use ** para potencias (x**2 para x²)
- Use exp() para exponenciales
- Funciones: sin(), cos(), tan(), sqrt()
- Constantes: E (número de Euler), pi, I (imaginario)
        """
        
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Ejemplos de Ecuaciones")
        ventana.geometry("700x600")
        
        text = ctk.CTkTextbox(ventana, font=ctk.CTkFont(size=12))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", ejemplos)
        text.configure(state="disabled")
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CalculadoraEcuacionesDiferenciales()
    app.run()