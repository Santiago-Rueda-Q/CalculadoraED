"""
Solvers - Métodos de solución para ecuaciones diferenciales
Implementa diferentes métodos de resolución
"""

import sympy as sp
from sympy import dsolve, classify_ode, simplify, expand, factor

class SolucionadorED:
    """Clase para resolver ecuaciones diferenciales con diferentes métodos"""
    
    def __init__(self):
        self.metodos_disponibles = {
            'separable': 'Variables Separables',
            '1st_linear': 'Lineal de Primer Orden',
            '1st_exact': 'Ecuación Exacta',
            'Bernoulli': 'Ecuación de Bernoulli',
            '1st_homogeneous_coeff_best': 'Ecuación Homogénea',
            'nth_linear_constant_coeff_homogeneous': 'Coeficientes Constantes (Homogénea)',
            'nth_linear_constant_coeff_undetermined_coefficients': 'Coeficientes Indeterminados',
            'nth_linear_constant_coeff_variation_of_parameters': 'Variación de Parámetros',
        }
    
    def clasificar(self, ecuacion, y_func):
        """Clasifica la ecuación diferencial"""
        try:
            clasificacion = classify_ode(ecuacion, y_func)
            return clasificacion
        except Exception as e:
            return None
    
    def resolver_automatico(self, ecuacion, y_func):
        """Resuelve usando el método automático de SymPy"""
        try:
            solucion = dsolve(ecuacion, y_func)
            return solucion, "Automático (SymPy)"
        except Exception as e:
            raise ValueError(f"No se pudo resolver: {str(e)}")
    
    def resolver_variables_separables(self, ecuacion, y_func):
        """Resuelve ecuaciones de variables separables"""
        try:
            solucion = dsolve(ecuacion, y_func, hint='separable')
            return solucion, "Variables Separables"
        except:
            return None, None
    
    def resolver_lineal_primer_orden(self, ecuacion, y_func):
        """Resuelve ecuaciones lineales de primer orden"""
        try:
            solucion = dsolve(ecuacion, y_func, hint='1st_linear')
            return solucion, "Lineal de Primer Orden"
        except:
            return None, None
    
    def resolver_exacta(self, ecuacion, y_func):
        """Resuelve ecuaciones exactas"""
        try:
            solucion = dsolve(ecuacion, y_func, hint='1st_exact')
            return solucion, "Ecuación Exacta"
        except:
            return None, None
    
    def resolver_bernoulli(self, ecuacion, y_func):
        """Resuelve ecuaciones de Bernoulli"""
        try:
            solucion = dsolve(ecuacion, y_func, hint='Bernoulli')
            return solucion, "Ecuación de Bernoulli"
        except:
            return None, None
    
    def resolver_homogenea(self, ecuacion, y_func):
        """Resuelve ecuaciones homogéneas"""
        try:
            solucion = dsolve(ecuacion, y_func, hint='1st_homogeneous_coeff_best')
            return solucion, "Ecuación Homogénea"
        except:
            return None, None
    
    def resolver_coeficientes_constantes(self, ecuacion, y_func):
        """Resuelve ecuaciones con coeficientes constantes"""
        try:
            # Intentar homogénea primero
            solucion = dsolve(ecuacion, y_func, hint='nth_linear_constant_coeff_homogeneous')
            return solucion, "Coeficientes Constantes (Homogénea)"
        except:
            # Si falla, intentar con coeficientes indeterminados
            try:
                solucion = dsolve(ecuacion, y_func, hint='nth_linear_constant_coeff_undetermined_coefficients')
                return solucion, "Coeficientes Indeterminados"
            except:
                return None, None
    
    def resolver_coeficientes_indeterminados(self, ecuacion, y_func):
        """Resuelve usando coeficientes indeterminados"""
        try:
            solucion = dsolve(ecuacion, y_func, hint='nth_linear_constant_coeff_undetermined_coefficients')
            return solucion, "Coeficientes Indeterminados"
        except:
            return None, None
    
    def resolver_variacion_parametros(self, ecuacion, y_func):
        """Resuelve usando variación de parámetros"""
        try:
            solucion = dsolve(ecuacion, y_func, hint='nth_linear_constant_coeff_variation_of_parameters')
            return solucion, "Variación de Parámetros"
        except:
            return None, None
    
    def resolver_con_metodo(self, ecuacion, y_func, metodo):
        """
        Resuelve la ecuación usando un método específico
        
        Args:
            ecuacion: Ecuación SymPy
            y_func: Función dependiente
            metodo: Nombre del método a usar
            
        Returns:
            tuple: (solucion, nombre_metodo) o (None, None) si falla
        """
        metodos = {
            'Automático (Recomendado)': self.resolver_automatico,
            'Variables Separables': self.resolver_variables_separables,
            'Lineal de Primer Orden': self.resolver_lineal_primer_orden,
            'Exacta': self.resolver_exacta,
            'Bernoulli': self.resolver_bernoulli,
            'Homogénea': self.resolver_homogenea,
            'Coeficientes Constantes': self.resolver_coeficientes_constantes,
            'Coeficientes Indeterminados': self.resolver_coeficientes_indeterminados,
        }
        
        resolver_func = metodos.get(metodo, self.resolver_automatico)
        return resolver_func(ecuacion, y_func)
    
    def simplificar_solucion(self, solucion):
        """Simplifica la solución obtenida"""
        try:
            if isinstance(solucion, sp.Eq):
                izq = simplify(solucion.lhs)
                der = simplify(solucion.rhs)
                return sp.Eq(izq, der)
            else:
                return simplify(solucion)
        except:
            return solucion
    
    def verificar_solucion(self, ecuacion, solucion, y_func, x_var):
        """Verifica que la solución satisface la ecuación diferencial"""
        try:
            # Extraer la expresión de y de la solución
            if isinstance(solucion, sp.Eq):
                y_sol = solucion.rhs
            else:
                y_sol = solucion
            
            # Sustituir en la ecuación original
            ec_verificada = ecuacion.subs(y_func, y_sol)
            ec_simplificada = simplify(ec_verificada)
            
            # Verificar si se cumple (debería ser 0 = 0 o True)
            if ec_simplificada == True or ec_simplificada == sp.S.Zero:
                return True, "✓ La solución satisface la ecuación"
            else:
                return False, "⚠ No se pudo verificar completamente la solución"
        except:
            return None, "⚠ No se pudo verificar la solución"
    
    def extraer_constantes(self, solucion):
        """Extrae las constantes de integración de la solución"""
        constantes = []
        if isinstance(solucion, sp.Eq):
            simbolos = solucion.rhs.free_symbols
        else:
            simbolos = solucion.free_symbols
        
        for sym in simbolos:
            if 'C' in str(sym):
                constantes.append(sym)
        
        return sorted(constantes, key=str)
    
    def obtener_tipo_solucion(self, clasificacion):
        """Obtiene descripción legible del tipo de solución"""
        if not clasificacion:
            return "No clasificada"
        
        if isinstance(clasificacion, tuple):
            tipos = []
            for cls in clasificacion[:3]:  # Primeros 3 tipos
                nombre = self.metodos_disponibles.get(cls, cls)
                tipos.append(nombre)
            return tipos
        else:
            return [self.metodos_disponibles.get(clasificacion, clasificacion)]


def resolver_ecuacion_diferencial(ecuacion, y_func, metodo='Automático (Recomendado)'):
    """Función de conveniencia para resolver ecuaciones"""
    solver = SolucionadorED()
    return solver.resolver_con_metodo(ecuacion, y_func, metodo)