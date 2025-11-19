# Calculadora de Ecuaciones Diferenciales - Estructura del Proyecto

## 📁 Estructura de Carpetas

```
calculadora-ecuaciones-diferenciales/
│
├── main.py                          # Archivo principal (código del artifact)
├── requirements.txt                 # Dependencias
├── README.md                        # Documentación
│
├── modulos/                         # Módulos adicionales (opcional)
│   ├── __init__.py
│   ├── parser.py                    # Parser de ecuaciones
│   ├── solvers.py                   # Métodos de solución
│   └── utils.py                     # Utilidades
│
└── tests/                           # Pruebas (opcional)
    ├── __init__.py
    └── test_ecuaciones.py
```

## 📦 requirements.txt

```
customtkinter==5.2.1
sympy==1.12
numpy==1.24.3
matplotlib==3.7.2
```

## 🚀 Instalación y Uso

### 1. Instalar Python
Asegúrate de tener Python 3.8 o superior instalado.

### 2. Crear entorno virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
python main.py
```

## 📖 Guía de Uso

### Sintaxis de Ecuaciones

**Derivadas:**
- Primera derivada: `y'` o `dy/dx`
- Segunda derivada: `y''` o `d2y/dx2`
- Tercera derivada: `y'''`

**Operadores:**
- Suma: `+`
- Resta: `-`
- Multiplicación: `*`
- División: `/`
- Potencia: `**` (ejemplo: `x**2` para x²)

**Funciones Matemáticas:**
- Trigonométricas: `sin(x)`, `cos(x)`, `tan(x)`
- Exponencial: `exp(x)` o `E**x`
- Logaritmo: `log(x)` o `ln(x)`
- Raíz cuadrada: `sqrt(x)`

**Constantes:**
- Número de Euler: `E`
- Pi: `pi`
- Número imaginario: `I`
- Número de oro: `(1 + sqrt(5))/2`

### Ejemplos por Tipo

#### 1. Variables Separables
```
Ecuación: y' = x*y
Tipo: Variables Separables
```

#### 2. Ecuación Homogénea
```
Ecuación: y' = (x + y)/(x - y)
Tipo: Homogénea
```

#### 3. Ecuación Exacta
```
Ecuación: (2*x*y + 1) + (x**2 + 2*y)*y' = 0
Tipo: Exacta
```

#### 4. Ecuación Lineal de Primer Orden
```
Ecuación: y' + 2*y = x
Tipo: Lineal de Primer Orden
```

#### 5. Ecuación de Bernoulli
```
Ecuación: y' + y = y**2
Tipo: Bernoulli
```

#### 6. Coeficientes Constantes (Orden Superior)
```
Ecuación: y'' + 4*y' + 4*y = 0
Tipo: Coeficientes Constantes
```

#### 7. Coeficientes Indeterminados
```
Ecuación: y'' + y = sin(x)
Tipo: Coeficientes Indeterminados
```

#### 8. Con Números Complejos
```
Ecuación: y' = I*y
Tipo: Automático
```

## 🔧 Características Implementadas

### ✅ Tipos de Ecuaciones Soportadas:
- ✅ Variables Separables
- ✅ Ecuaciones Homogéneas
- ✅ Ecuaciones Exactas
- ✅ Ecuaciones Lineales de Primer Orden
- ✅ Ecuaciones de Bernoulli
- ✅ Ecuaciones Reducibles a Primer Orden
- ✅ Coeficientes Constantes
- ✅ Método de Coeficientes Indeterminados
- ✅ Factores Integrantes

### ✅ Funciones Matemáticas:
- ✅ Trigonométricas (sin, cos, tan)
- ✅ Exponenciales (exp, E)
- ✅ Logaritmos (log, ln)
- ✅ Raíces (sqrt)
- ✅ Números complejos (I)
- ✅ Constantes (pi, E, número de oro)

### ✅ Interfaz:
- ✅ Interfaz moderna con CustomTkinter
- ✅ Tema oscuro
- ✅ Selección de tipo de ecuación
- ✅ Variables personalizables
- ✅ Área de resultados amplia
- ✅ Botón de ejemplos
- ✅ Manejo de errores

## 🎨 Personalización de la Interfaz

Para cambiar el tema:
```python
# En la clase __init__
ctk.set_appearance_mode("dark")  # Opciones: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"
```

Para cambiar colores de botones:
```python
btn_resolver = ctk.CTkButton(
    ...,
    fg_color="blue",  # Color de fondo
    hover_color="darkblue"  # Color al pasar el mouse
)
```

## 🐛 Solución de Problemas

### Error: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error: "No module named 'sympy'"
```bash
pip install sympy
```

### La ecuación no se resuelve
- Verifica la sintaxis (usa `**` para potencias, no `^`)
- Asegúrate de usar `y'` o `dy/dx` para derivadas
- Prueba con el modo "Automático (SymPy)"

### Interfaz no se ve bien en Linux
Instala dependencias adicionales:
```bash
sudo apt-get install python3-tk
```

## 📚 Recursos Adicionales

- [Documentación SymPy](https://docs.sympy.org/)
- [Documentación CustomTkinter](https://customtkinter.tomschimansky.com/)
- [Ecuaciones Diferenciales - Khan Academy](https://www.khanacademy.org/math/differential-equations)

## 🤝 Mejoras Futuras

- [ ] Visualización gráfica de soluciones
- [ ] Exportar soluciones a PDF/LaTeX
- [ ] Resolución paso a paso
- [ ] Condiciones iniciales/de frontera
- [ ] Historial de ecuaciones resueltas
- [ ] Modo de sistema de ecuaciones diferenciales
- [ ] Métodos numéricos (Euler, Runge-Kutta)

## 📝 Licencia

Proyecto educativo - Libre uso para fines académicos.

---

**Desarrollado para presentación académica**  
**Powered by SymPy & CustomTkinter**