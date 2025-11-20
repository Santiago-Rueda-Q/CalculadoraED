"""
Módulo de Calculadora de Ecuaciones Diferenciales
Contiene parser, solvers y utilidades
"""

from .parser import EcuacionParser, parsear_ecuacion
from .solvers import SolucionadorED, resolver_ecuacion_diferencial
from .utils import FormateadorMatematico, GeneradorPasos, ValidadorEcuaciones

__all__ = [
    'EcuacionParser',
    'parsear_ecuacion',
    'SolucionadorED',
    'resolver_ecuacion_diferencial',
    'FormateadorMatematico',
    'GeneradorPasos',
    'ValidadorEcuaciones',
]

__version__ = '1.0.0'
__author__ = 'Calculadora ED'
__description__ = 'Sistema completo para resolver ecuaciones diferenciales'