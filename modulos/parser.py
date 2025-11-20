"""
Parser de Ecuaciones Diferenciales
Convierte strings a expresiones SymPy
"""

import sympy as sp
import re

class EcuacionParser:
    """Clase para parsear ecuaciones diferenciales desde texto"""
    
    def __init__(self):
        self.funciones_matematicas = {
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'cot': sp.cot,
            'sec': sp.sec,
            'csc': sp.csc,
            'arcsin': sp.asin,
            'arccos': sp.acos,
            'arctan': sp.atan,
            'sinh': sp.sinh,
            'cosh': sp.cosh,
            'tanh': sp.tanh,
            'exp': sp.exp,
            'log': sp.log,
            'ln': sp.log,
            'sqrt': sp.sqrt,
            'abs': sp.Abs,
        }
        
        self.constantes = {
            'E': sp.E,
            'e': sp.E,
            'pi': sp.pi,
            'PI': sp.pi,
            'I': sp.I,
            'i': sp.I,
        }
    
    def limpiar_ecuacion(self, ec_str):
        """Limpia y prepara la cadena de ecuación"""
        # Remover espacios extras
        ec_str = ' '.join(ec_str.split())
        
        # Reemplazar notaciones comunes
        ec_str = ec_str.replace('^', '**')
        
        # Convertir e^x a exp(x) pero cuidado con variable e
        ec_str = re.sub(r'\be\s*\*\*\s*\(', 'exp(', ec_str)
        ec_str = re.sub(r'\be\s*\*\*\s*([a-zA-Z0-9_]+)', r'exp(\1)', ec_str)
        
        return ec_str
    
    def convertir_derivadas(self, ec_str, var_dep, var_indep):
        """Convierte notación de derivadas a formato SymPy"""
        # y''', y'', y'
        ec_str = ec_str.replace(f"{var_dep}'''", f"Derivative({var_dep}({var_indep}), {var_indep}, 3)")
        ec_str = ec_str.replace(f"{var_dep}''", f"Derivative({var_dep}({var_indep}), {var_indep}, 2)")
        ec_str = ec_str.replace(f"{var_dep}'", f"Derivative({var_dep}({var_indep}), {var_indep})")
        
        # dy/dx, d²y/dx², d³y/dx³
        ec_str = re.sub(rf'd{var_dep}/d{var_indep}', 
                       f"Derivative({var_dep}({var_indep}), {var_indep})", ec_str)
        ec_str = re.sub(rf'd2{var_dep}/d{var_indep}2', 
                       f"Derivative({var_dep}({var_indep}), {var_indep}, 2)", ec_str)
        ec_str = re.sub(rf'd3{var_dep}/d{var_indep}3', 
                       f"Derivative({var_dep}({var_indep}), {var_indep}, 3)", ec_str)
        
        # d²y/dx², d³y/dx³ con superíndices Unicode
        ec_str = ec_str.replace(f"d²{var_dep}/d{var_indep}²", 
                               f"Derivative({var_dep}({var_indep}), {var_indep}, 2)")
        ec_str = ec_str.replace(f"d³{var_dep}/d{var_indep}³", 
                               f"Derivative({var_dep}({var_indep}), {var_indep}, 3)")
        
        return ec_str
    
    def reemplazar_variable_dependiente(self, ec_str, var_dep, var_indep):
        """Reemplaza la variable dependiente por función"""
        # Evitar reemplazar dentro de nombres de funciones
        # Buscar 'y' que no esté seguido de '(' y no esté precedido por letra
        ec_str = re.sub(rf'(?<![a-zA-Z]){var_dep}(?!\()', 
                       f"{var_dep}({var_indep})", ec_str)
        return ec_str
    
    def crear_namespace(self, var_indep, var_dep):
        """Crea el namespace para evaluar la ecuación"""
        x = sp.Symbol(var_indep)
        y = sp.Function(var_dep)
        
        namespace = {
            var_indep: x,
            var_dep: y,
            'Derivative': sp.Derivative,
            'diff': sp.diff,
        }
        
        # Agregar funciones matemáticas
        namespace.update(self.funciones_matematicas)
        
        # Agregar constantes
        namespace.update(self.constantes)
        
        return namespace, x, y
    
    def parsear(self, ec_str, var_indep='x', var_dep='y'):
        """
        Parsea una ecuación diferencial desde string a SymPy
        
        Args:
            ec_str: String con la ecuación
            var_indep: Variable independiente (default 'x')
            var_dep: Variable dependiente (default 'y')
            
        Returns:
            tuple: (ecuacion_sympy, variable_x, funcion_y)
            
        Raises:
            ValueError: Si la ecuación no puede parsearse
        """
        try:
            # Limpiar ecuación
            ec_str = self.limpiar_ecuacion(ec_str)
            
            # Convertir derivadas
            ec_str = self.convertir_derivadas(ec_str, var_dep, var_indep)
            
            # Reemplazar variable dependiente
            ec_str = self.reemplazar_variable_dependiente(ec_str, var_dep, var_indep)
            
            # Crear namespace
            namespace, x, y = self.crear_namespace(var_indep, var_dep)
            
            # Evaluar ecuación
            if '=' in ec_str:
                # Ecuación con =
                izq, der = ec_str.split('=', 1)
                ec_izq = eval(izq.strip(), namespace)
                ec_der = eval(der.strip(), namespace)
                ecuacion = sp.Eq(ec_izq, ec_der)
            else:
                # Ecuación sin =, asumir = 0
                ec_parsed = eval(ec_str, namespace)
                ecuacion = sp.Eq(ec_parsed, 0)
            
            return ecuacion, x, y
            
        except SyntaxError as e:
            raise ValueError(f"Error de sintaxis: {str(e)}\n"
                           f"Verifique operadores (* para multiplicar, ** para potencias)")
        except NameError as e:
            raise ValueError(f"Variable o función no reconocida: {str(e)}\n"
                           f"Use 'exp()' para exponenciales, verifique nombres de funciones")
        except Exception as e:
            raise ValueError(f"Error al parsear la ecuación: {str(e)}")
    
    def validar_ecuacion(self, ecuacion, var_dep):
        """Valida que la ecuación sea una ecuación diferencial válida"""
        # Verificar que contiene derivadas
        if not any(isinstance(arg, sp.Derivative) for arg in ecuacion.atoms()):
            return False, "La ecuación no contiene derivadas"
        
        return True, "Ecuación válida"


def parsear_ecuacion(ec_str, var_indep='x', var_dep='y'):
    """Función de conveniencia para parsear ecuaciones"""
    parser = EcuacionParser()
    return parser.parsear(ec_str, var_indep, var_dep)