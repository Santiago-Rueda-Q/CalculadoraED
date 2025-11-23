# KATSIO – Differential Equation Calculator

<div align="center">

![KATSIO Banner](https://img.shields.io/badge/KATSIO-Differential_Calculator-1C4E80?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Una calculadora interactiva de ecuaciones diferenciales ordinarias (EDO) con diseño inspirado en Casio FX-991ES Plus**

[Características](#-características-principales) • [Instalación](#-instalación) • [Uso](#-uso) • [Tecnologías](#-tecnologías-utilizadas) • [Créditos](#-créditos)

</div>

---
<div align="center">
  <h1>Miembros</h1>
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/Santiago-Rueda-Q">
          <img src="https://github.com/Santiago-Rueda-Q.png" width="100px;" alt="Santiago Rueda Quintero"/><br />
          <sub><b>Santiago Rueda Quintero</b></sub>
        </a><br />
      </td>
      <td align="center">
        <a href="https://github.com/TIC0o">
          <img src="https://github.com/TIC0o.png" width="100px;" alt="Eliecer Guevara Fuentes"/><br />
          <sub><b>Eliecer Guevara Fuentes</b></sub>
        </a><br />
      </td>
    </tr>
  </table>
</div>

## 📖 Descripción General

**KATSIO** es una calculadora web moderna diseñada para resolver ecuaciones diferenciales ordinarias (EDOs) con una interfaz que emula el estilo "Natural Display" de las calculadoras científicas **Casio FX-991ES Plus**. 

El proyecto está orientado a estudiantes, docentes y desarrolladores que necesitan una herramienta intuitiva, accesible y visualmente atractiva para resolver EDOs simbólicamente, obtener soluciones paso a paso y aplicar condiciones iniciales de manera flexible.

### 🎯 Objetivo del Proyecto

KATSIO combina la potencia del cálculo simbólico moderno con una experiencia de usuario realista, ofreciendo:

- ✅ **Resolución simbólica completa** de EDOs de primer, segundo y tercer orden
- ✅ **Interfaz estilo calculadora física** con botones interactivos
- ✅ **Notación matemática profesional** renderizada con MathJax
- ✅ **Procedimiento detallado paso a paso** generado por IA
- ✅ **Condiciones iniciales dinámicas** configurables en tiempo real

---

## 🧬 Origen del Proyecto

### 🔬 Versión Original en Python

KATSIO comenzó como un prototipo local desarrollado en Python utilizando:

| Tecnología | Propósito |
|------------|-----------|
| **SymPy** | Motor de cálculo simbólico para resolver EDOs |
| **Tkinter** | Interfaz gráfica de usuario básica |
| **Matplotlib** | Visualización gráfica de soluciones |

#### ❌ Limitaciones de la Versión Original

A pesar de su funcionalidad básica, el prototipo enfrentó varios desafíos técnicos:

1. **Problemas de SymPy con notación humana**:
   - Dificultad para interpretar `y'`, `y''`, `dy/dx`
   - Incompatibilidad con funciones como `sqrt()` sin normalización previa
   - Errores frecuentes con ecuaciones implícitas o complejas

2. **Limitaciones de Tkinter**:
   - Sin soporte para MathJax (notación matemática limitada)
   - Interfaz no responsiva ni moderna
   - Imposibilidad de implementar modales, tooltips o notificaciones
   - Difícil integración de copiar/pegar resultados

3. **Condiciones iniciales poco robustas**:
   - Fallos al procesar CI en ecuaciones implícitas
   - Validación insuficiente de formato

---

## ✨ Características Principales

### 🧮 Entrada Flexible y Normalización Inteligente

KATSIO acepta múltiples formatos de notación matemática, normalizándolos automáticamente:

| Notación del Usuario | Normalización Interna |
|---------------------|----------------------|
| `y'` | `d/dx(y)` |
| `y''` | `d^2/dx^2(y)` |
| `y'''` | `d^3/dx^3(y)` |
| `dy/dx` | `dy/dx` (sin cambios) |
| `√x` o `√(x)` | `sqrt(x)` |
| `sin(x)`, `cos(x)`, `tan(x)` | Sin cambios |
| `exp(x)` | Sin cambios |
| `log(x)` | Sin cambios |

**Ejemplo de entrada válida:**
```
y' = √(x^2 + y^2)
dy/dx + 2*y = sin(x)
y'' - 3*y' + 2*y = exp(x)
```

### 🎛️ Condiciones Iniciales Dinámicas

El sistema permite configurar hasta **3 condiciones iniciales** de forma interactiva:

- ➕ **Añadir** condiciones en tiempo real
- ➖ **Eliminar** condiciones no necesarias
- ✅ **Validación automática** de formato (`y(0)=1`, `y'(1)=2`, etc.)

**Casos de uso:**
- EDO de primer orden → 1 condición inicial
- EDO de segundo orden → 2 condiciones iniciales
- EDO de tercer orden → 3 condiciones iniciales

### 🤖 Motor Simbólico Inteligente (DeepSeek Chat)

KATSIO utiliza la **API de DeepSeek Chat** como motor matemático avanzado:

| Función | Descripción |
|---------|-------------|
| **Resolución simbólica** | Calcula la solución general y particular |
| **Procedimiento paso a paso** | Genera explicaciones detalladas del proceso |
| **Manejo de casos especiales** | Detecta ecuaciones lineales, separables, exactas, Bernoulli, etc. |
| **Aplicación de CI** | Determina constantes de integración automáticamente |

**Ventajas sobre SymPy:**
- Mayor flexibilidad interpretativa
- Generación de explicaciones educativas
- Mejor manejo de notación no estándar

### 🎨 Estilo Casio Auténtico

La interfaz replica fielmente el diseño de las calculadoras **Casio FX-991ES Plus**:

#### Teclado Interactivo

| Categoría | Botones Disponibles |
|-----------|-------------------|
| **Funciones trigonométricas** | `sin`, `cos`, `tan` |
| **Funciones especiales** | `log`, `exp`, `√` |
| **Operadores diferenciales** | `d/dx`, `d/dy` |
| **Constantes matemáticas** | `π`, `e` |
| **Operadores básicos** | `+`, `-`, `×`, `÷`, `^` |
| **Variables** | `x`, `y`, `t` |
| **Paréntesis** | `(`, `)` |
| **Control** | `AC` (limpiar pantalla) |

#### Pantalla LCD Simulada

- Fondo verde característico (`#C9D5B5`)
- Fuente monoespaciada (Roboto Mono)
- Área de texto expandible
- Cursor de inserción funcional

### 📚 Sistema de Ejemplos Precargados

KATSIO incluye **8 ecuaciones diferenciales** listas para usar:

```javascript
1. dy/dx = x*y                    // EDO separable básica
2. y' = (x^2)/y                   // EDO separable con potencias
3. dy/dx + y = e^x                // EDO lineal de primer orden
4. y' = x*exp(-y)                 // EDO con función exponencial
5. dy/dx = y/(x+1)                // EDO homogénea
6. y' + 2*y = sin(x)              // EDO lineal con función trigonométrica
7. dy/dx = (x^3 + 2)/(y+1)        // EDO separable compleja
8. y' = sqrt(x^2 + y^2)           // EDO con raíz cuadrada
```

Los ejemplos se cargan directamente en la pantalla con un solo clic.

### ❔ Modal de Ayuda Interactivo

Guía completa para el usuario:

- **¿Qué es KATSIO?** – Descripción del proyecto
- **¿Cómo escribir ecuaciones?** – Lista de operadores y funciones válidas
- **¿Cómo calcular?** – Instrucciones paso a paso
- **¿Qué muestra la calculadora?** – Interpretación de resultados
- **Consejos y trucos** – Mejores prácticas de uso

### 🎉 Notificaciones Toast

Sistema de feedback visual para el usuario:

| Tipo | Color | Uso |
|------|-------|-----|
| ✔ **Éxito** | Verde | Ecuación resuelta correctamente |
| ✖ **Error** | Rojo | Error de entrada o servidor |
| ℹ️ **Info** | Azul | Ejemplo cargado, acción completada |

---

## 🛠 Tecnologías Utilizadas

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **HTML5** | - | Estructura semántica del DOM |
| **TailwindCSS** | 3.x | Sistema de diseño utility-first |
| **JavaScript (ES6+)** | - | Lógica de interacción y validación |
| **MathJax** | 3.x | Renderizado de notación matemática (LaTeX) |

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.8+ | Lenguaje del servidor |
| **Flask** | 2.0+ | Framework web minimalista |
| **DeepSeek Chat API** | - | Motor de resolución simbólica por IA |

### Dependencias Principales

```plaintext
flask>=2.0.0
python-dotenv>=0.19.0
requests>=2.26.0
```

---

## 📁 Estructura del Proyecto

```
KATSIO/
│
├── app.py                      # Servidor Flask principal
├── .env                        # Variables de entorno (API keys)
├── .env.example                # Plantilla de configuración
├── requirements.txt            # Dependencias de Python
├── README.md                   # Este archivo
│
├── static/
│   └── js/
│       └── main.js             # Lógica del frontend (validación, normalización, eventos)
│
└── templates/
    └── index.html              # Interfaz principal de la calculadora
```

---

## ⚙️ Validación y Normalización Técnica

### 🔍 Pipeline de Procesamiento

```
Usuario ingresa ecuación → Validación de caracteres → Normalización de notación 
→ Construcción del prompt → Envío a DeepSeek API → Procesamiento de respuesta 
→ Formateo para MathJax → Renderizado en pantalla
```

### 📝 Normalización de Notación

**Función `normalizeEquation()`** en `main.js`:

```javascript
function normalizeEquation(raw) {
    let eq = raw;

    // Convertir √ a sqrt
    eq = eq.replace(/√\s*\(/g, 'sqrt(');
    eq = eq.replace(/√\s*([a-zA-Z0-9_]+)/g, 'sqrt($1)');
    eq = eq.replace(/√/g, 'sqrt');

    // Convertir notación de derivadas con apóstrofe
    eq = eq.replace(/y'''/g, 'd^3/dx^3(y)');
    eq = eq.replace(/y''/g, 'd^2/dx^2(y)');
    eq = eq.replace(/y'/g, 'd/dx(y)');

    // Normalizar d/dx y -> d/dx(y)
    eq = eq.replace(/d\/dx\s+([a-zA-Z][a-zA-Z0-9_]*)/g, 'd/dx($1)');

    return eq;
}
```

### 🚫 Filtrado de Caracteres Inválidos

**Validación en `keydown` event**:

```javascript
const allowedCharsRegex = /^[a-zA-Z0-9+\-*/().,=^' √_]$/;
if (!allowedCharsRegex.test(event.key)) {
    event.preventDefault();
}
```

### 🔄 Construcción del Prompt para DeepSeek

El backend construye un prompt estructurado:

```python
prompt = f"""
Resuelve la siguiente ecuación diferencial paso a paso:

Ecuación: {equation}
Condiciones iniciales: {initial_conditions}

Por favor:
1. Identifica el tipo de EDO
2. Resuelve simbólicamente
3. Aplica las condiciones iniciales si las hay
4. Muestra cada paso con notación LaTeX
"""
```

### 📐 Formateo de Respuestas para MathJax

**Función `formatSolution()`** en `main.js`:

```javascript
function formatSolution(text) {
    let cleaned = text;

    // Convertir **Paso X** a encabezados HTML
    cleaned = cleaned.replace(
        /\*\*(Paso.*?)\*\*/g,
        "<h3 class='text-gray-300 font-bold mt-4 mb-2'>$1</h3>"
    );

    // Preservar bloques LaTeX \[ ... \]
    cleaned = cleaned.replace(
        /\\\[([\s\S]*?)\\\]/g,
        "<div class='my-3 p-2 bg-[#1a1a1a] rounded border border-[#3a3a3a]'>\\[$1\\]</div>"
    );

    // Preservar inline LaTeX \( ... \)
    cleaned = cleaned.replace(/\\\((.*?)\\\)/g, '\\($1\\)');

    return cleaned;
}
```

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Clave de API de DeepSeek ([obtenerla aquí](https://platform.deepseek.com/))

### Pasos de Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/Santiago-Rueda-Q/KATSIO.git
cd KATSIO
```

2. **Crear un entorno virtual (recomendado):**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**

Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Edita `.env` y añade tu clave de API:

```plaintext
DEEPSEEK_API_KEY=tu_clave_api_aqui
```

5. **Ejecutar el servidor:**

```bash
python app.py
```

6. **Abrir en el navegador:**

```
http://localhost:5000
```

---

## 💻 Uso

### 1️⃣ Ingresar una Ecuación

Escribe la ecuación en la pantalla LCD verde usando:
- El **teclado físico** del ordenador
- Los **botones de la calculadora** en pantalla

**Ejemplo:**
```
dy/dx = x*y
```

### 2️⃣ Añadir Condiciones Iniciales (Opcional)

Haz clic en **"+ Añadir"** para agregar condiciones iniciales:

```
y(0) = 1
```

### 3️⃣ Calcular la Solución

Presiona el botón **"CALCULAR"** o pulsa **Enter**.

### 4️⃣ Ver el Resultado

La solución aparecerá formateada con:
- Procedimiento paso a paso
- Notación matemática profesional (MathJax)
- Solución general y particular

---

## 🖼️ Capturas de Pantalla

> **Nota:** Añadir capturas de pantalla en esta sección para mostrar:
> - Interfaz principal de la calculadora
> - Modal de ejemplos
> - Modal de ayuda
> - Ejemplo de solución renderizada

---

## 👥 Créditos

Este proyecto fue desarrollado por:
<div align="center">

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Santiago-Rueda-Q">
        <img src="https://github.com/Santiago-Rueda-Q.png" width="100px;" alt="Santiago Rueda Quintero"/><br />
        <sub><b>Santiago Rueda Quintero</b></sub>
      </a><br />
      <sub>Backend Developer</sub><br />
      🐍 Flask • 🤖 DeepSeek Integration • ⚙️ API Design
    </td>
    <td align="center">
      <a href="https://github.com/TIC0o">
        <img src="https://github.com/TIC0o.png" width="100px;" alt="Eliecer Guevara Fuentes"/><br />
        <sub><b>Eliecer Guevara Fuentes</b></sub>
      </a><br />
      <sub>QA & Testing</sub><br />
      🧪 Quality Assurance • 🐛 Bug Detection • ✅ Validation
    </td>
  </tr>
</table>
</div align="center">

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 Santiago Rueda Quintero & Eliecer Guevara Fuentes

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y archivos de documentación asociados (el "Software"), para
utilizar el Software sin restricciones, incluyendo sin limitación los derechos
de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o
vender copias del Software...
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📧 Contacto

Para preguntas, sugerencias o reportes de bugs:

- **Santiago Rueda Quintero**: [GitHub](https://github.com/Santiago-Rueda-Q)
- **Eliecer Guevara Fuentes**: [GitHub](https://github.com/TIC0o)

---

<div align="center">

**Hecho con ❤️ por estudiantes apasionados por las matemáticas y la programación**

[![GitHub](https://img.shields.io/badge/GitHub-KATSIO-181717?style=for-the-badge&logo=github)](https://github.com/Santiago-Rueda-Q/KATSIO)

</div>
