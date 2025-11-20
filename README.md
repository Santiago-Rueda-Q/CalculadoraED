Jefe, Ing. Santiago… aquí tienes **un README extremadamente estructurado, profesional, completo y limpio**, listo para GitHub.
No hay relleno absurdo, todo es útil. Lo puedes copiar/pegar tal cual.

---

# 📘 **Calculadora de Ecuaciones Diferenciales – Proyecto Completo**

Sistema modular desarrollado en **Python + SymPy + CustomTkinter**, diseñado para resolver ecuaciones diferenciales de manera automática, guiada y con explicación paso a paso.
Incluye parser avanzado, motor de resolución, herramientas de verificación y un teclado matemático interactivo.

---

# 📌 **Tabla de Contenidos**

1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)

   * 3.1. main.py
   * 3.2. parser.py
   * 3.3. solvers.py
   * 3.4. utils.py
   * 3.5. teclado_matematico.py
4. [Flujo Interno de Funcionamiento](#flujo-interno-de-funcionamiento)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Instalación](#instalación)
7. [Uso de la Aplicación](#uso-de-la-aplicación)
8. [Tipos de Ecuaciones Soportadas](#tipos-de-ecuaciones-soportadas)
9. [Capturas del Sistema (opcional)](#capturas-opcionales)
10. [Errores Comunes y Soluciones](#errores-comunes-y-soluciones)
11. [Créditos y Tecnología](#créditos-y-tecnología)

---

# 🧠 **Descripción General**

La *Calculadora de Ecuaciones Diferenciales* es una herramienta diseñada para:

* Resolver ecuaciones diferenciales de 1° y 2° orden
* Permitir resolución automática o guiada por método
* Mostrar la solución detallada y paso a paso
* Incluir validación y verificación simbólica
* Funcionar con un teclado matemático para ingresar expresiones complejas

El sistema está pensado para estudiantes, docentes y personas con dificultades cognitivas que necesitan explicaciones claras y visuales.

---

# 🚀 **Características Principales**

### ✔ Interfaz moderna con CustomTkinter

Tema oscuro, botones estilizados, scroll y diseño responsivo.

### ✔ Parser especializado

Convierte ecuaciones escritas por el usuario en expresiones SymPy:

* `y'`, `y''`, `y'''`
* `dy/dx`, `d²y/dx²`
* Funciones trigonométricas
* Notación e^x → exp(x)

### ✔ Motor de resolución inteligente

Detecta el tipo de ecuación y aplica:

* Variables separables
* Lineal de primer orden
* Exactas
* Homogéneas
* Bernoulli
* Coeficientes constantes
* Indeterminados
* Variación de parámetros
* Modo automático SymPy

### ✔ Explicación paso a paso

Incluye teoría, proceso matemático y solución final formateada.

### ✔ Verificación simbólica

Comprueba que la solución satisface la ecuación original.

### ✔ Teclado matemático interactivo

Inserta símbolos y funciones sin necesidad de escribirlos manualmente.

---

# 🏗️ **Arquitectura del Sistema**

El proyecto está dividido en módulos independientes y bien encapsulados.

---

## 🟦 **1. main.py – Interfaz y Control Principal**

Responsable de:

* Crear la ventana principal
* Mostrar campos de entrada
* Mostrar resultados
* Ejecutar el flujo completo
* Conectar con parser/solvers/utils
* Administrar botones:

  * Resolver
  * Limpiar
  * Copiar
  * Ver ejemplos
  * Teclado matemático

Además monta:

* Combobox de métodos
* Opciones de modo detallado
* Panel de resultados con scroll

---

## 🟪 **2. parser.py – Traductor Matemático**

Encargado de convertir un texto en una ecuación SymPy válida.

Funciones principales:

* `limpiar_ecuacion()`
* `convertir_derivadas()`
* `reemplazar_variable_dependiente()`
* `crear_namespace()`
* `parsear()`
* `validar_ecuacion()`

Funciones soportadas:

`sin, cos, tan, exp, sqrt, log, abs, sinh, cosh, tanh...`
Constantes: `pi, E, I`

Derivadas soportadas:

* y', y'', y'''
* dy/dx
* d²y/dx²
* d³y/dx³

---

## 🟩 **3. solvers.py – Motor de Resolución Matemática**

Implementa la lógica matemática que usa SymPy.

Funciones clave:

* Clasificación con `classify_ode()`
* Resolución automática con `dsolve()`
* Métodos específicos (lineal, separable, exacta, Bernoulli…)
* `resolver_con_metodo()` para ejecutar un método definido por el usuario
* Verificación simbólica
* Simplificación de expresiones
* Extracción de constantes de integración

Este módulo es el “cerebro matemático” del sistema.

---

## 🟧 **4. utils.py – Formateo y Explicación**

Divide su funcionalidad en:

### **FormateadorMatematico**

* Convierte expresiones a Unicode bonito
* Convierte a LaTeX
* Genera decoraciones ASCII
* Formatea ecuaciones completas

### **GeneradorPasos**

Produce explicación detallada para:

* Separables
* Lineales
* Exactas
* Bernoulli
* Coeficientes constantes
* Métodos automáticos

### **ValidadorEcuaciones**

* Verifica si hay derivadas
* Detecta orden de la ecuación
* Verifica linealidad
* Extrae constantes

---

## 🟨 **5. teclado_matematico.py – Teclado Interactivo**

Incluye:

* Derivadas
* Operadores
* Constantes
* Plantillas rápidas
* Funciones trigonométricas e hiperbólicas
* Números y variables clásicas

Funciones especiales:

* Insertar donde está el cursor
* Borrar último
* Limpiar todo
* Ventana flotante siempre visible

---

# 🔄 **Flujo Interno de Funcionamiento**

```
                            ┌───────────────┐
                            │ Usuario escribe│
                            │ la ecuación   │
                            └──────┬────────┘
                                    │
                            main.py│
                                    ▼
                        ┌──────────────────────┐
                        │ parser.py            │
                        │ → Traduce la ecuación│
                        └──────────┬───────────┘
                                    │
                            main.py│
                                    ▼
                        ┌──────────────────────┐
                        │ solvers.py           │
                        │ → Clasifica          │
                        │ → Resuelve           │
                        │ → Verifica           │
                        └──────────┬───────────┘
                                    │
                            main.py│
                                    ▼
                        ┌──────────────────────┐
                        │ utils.py             │
                        │ → Formatea           │
                        │ → Genera pasos       │
                        └──────────┬───────────┘
                                    │
                                    ▼
                        ┌──────────────────────┐
                        │ Interfaz (main.py)   │
                        │ → Muestra resultado  │
                        └──────────────────────┘
```

---

# 📂 **Estructura del Proyecto**

```
📁 calculadora-ed/
│
├── main.py
├── parser.py
├── solvers.py
├── utils.py
├── teclado_matematico.py
│
├── requirements.txt
└── README.md
```

---

# 🛠️ **Instalación**

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar

```bash
python main.py
```

---

# 🧩 **Uso de la Aplicación**

### 1. Escribe la ecuación en el cuadro de texto

Ejemplos:

```
y' = x*y
y'' + 4*y = 0
(2*x + y) + (x + 2*y)*y' = 0
```

### 2. Selecciona un método (o usa modo automático)

### 3. Presiona **Resolver Ecuación**

### 4. Observa:

* Clasificación
* Solución
* Pasos detallados
* Verificación

### 5. (Opcional) Usa:

* Teclado matemático
* Ver ejemplos
* Copiar resultado

---

# 📘 **Tipos de Ecuaciones Soportadas**

| Tipo             | Ejemplo             |
| ---------------- | ------------------- |
| Separables       | y' = x y            |
| Lineales         | y' + 2y = x         |
| Exactas          | (2x+y)+(x+2y)y'=0   |
| Homogéneas       | y' = (x+y)/x        |
| Bernoulli        | y' + P(x)y = Q(x)yⁿ |
| Coef. constantes | y'' + 4y = 0        |
| Indeterminados   | y'' + y = sin(x)    |

---

# ❗ **Errores Comunes y Soluciones**

### 🔸 “Sintaxis inválida”

– Falta multiplicación → usar `2*x`, no `2x`
– Potencias → `x**2`, no `x^2`

### 🔸 “Variable no reconocida”

Verificar que esté bien escrita:

* `exp(x)`
* `sin(x)`
* `sqrt(x)`

### 🔸 “No se pudo resolver”

Ecuaciones extremadamente complejas pueden exceder la capacidad de SymPy.

---

# 🧰 **Créditos y Tecnología**

### Tecnologías usadas:

* **Python 3**
* **SymPy** (motor matemático)
* **CustomTkinter** (interfaz gráfica moderna)
* **Regex** (procesamiento de texto)
* **Unicode Math Rendering**

Sistema diseñado para uso académico, aprendizaje asistido y apoyo inclusivo para personas con dificultades cognitivas.

