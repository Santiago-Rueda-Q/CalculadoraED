import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import re

# =========================================
# Cargar variables de entorno
# =========================================
load_dotenv()

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# =========================================
# VALIDACIÓN FLEXIBLE (ACEPTA TODA NOTACIÓN)
# =========================================
# Acepta: letras, números, operadores, sqrt, raíces, comas, espacios, etc.
ALLOWED_CHARS = r"^[0-9a-zA-Z+\-*/^=().,\s\[\]√']+$"


# =========================================
# Página principal
# =========================================
@app.route('/')
def index():
    return render_template('index.html')


# =========================================
# NORMALIZACIÓN DE ECUACIONES
# =========================================
def normalizar_ecuacion(eq: str):
    """Normaliza notación matemática a un formato legible por DeepSeek/Sympy."""

    # Eliminar múltiples espacios
    eq = re.sub(r"\s+", " ", eq)

    # Reemplazar raíz unicode por sqrt()
    eq = eq.replace("√", "sqrt")

    # Notación con apóstrofes
    eq = eq.replace("y'''", "d^3/dx^3(y)")
    eq = eq.replace("y''", "d^2/dx^2(y)")
    eq = eq.replace("y'", "d/dx(y)")

    # d/dx y → d/dx(y)
    eq = re.sub(r"d/dx\s*([a-zA-Z][a-zA-Z0-9]*)", r"d/dx(\1)", eq)

    # sqrt(a+b) → (a+b)**(1/2)  si DeepSeek se confunde, Sympy SIEMPRE lo procesa
    eq = re.sub(r"sqrt\s*\(([^()]+)\)", r"(\1)**(1/2)", eq)

    return eq.strip()


# =========================================
# VALIDACIONES
# =========================================
def validar_ecuacion(eq: str):
    if not eq or eq.strip() == "":
        return "La ecuación no puede estar vacía."

    if len(eq) > 350:
        return "La ecuación es demasiado larga."

    if not re.match(ALLOWED_CHARS, eq):
        return "La ecuación contiene caracteres no permitidos."

    return None


def validar_condiciones(conds):
    if not conds:
        return []

    limpias = []

    for c in conds:
        c = c.strip()

        if "=" not in c:
            return f"La condición '{c}' no es válida. Formato: y(0)=2"

        if len(c) > 60:
            return f"La condición '{c}' es demasiado larga."

        limpias.append(c)

    return limpias


# =========================================
# Resolver ODE con DeepSeek
# =========================================
@app.route('/solve_ode', methods=['POST'])
def solve_ode():
    if not DEEPSEEK_API_KEY:
        return jsonify({"error": "DEEPSEEK_API_KEY no configurada."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos."}), 400

    equation_raw = data.get('equation', '').strip()
    initial_conditions = data.get('initial_conditions', [])

    # Validación básica ANTES de normalizar
    err = validar_ecuacion(equation_raw)
    if err:
        return jsonify({"error": err}), 400

    # Normalizar notación matemática
    equation_str = normalizar_ecuacion(equation_raw)

    # Validar condiciones
    conds = validar_condiciones(initial_conditions)
    if isinstance(conds, str):
        return jsonify({"error": conds}), 400

    # =========================================
    # Construcción del prompt
    # =========================================
    prompt = f"Resuelve la siguiente ecuación diferencial ordinaria:\n{equation_str}\n\n"

    if conds:
        prompt += (
            "Usa las siguientes condiciones iniciales para calcular la solución particular:\n"
            + ", ".join(conds) + ".\n\n"
        )
    else:
        prompt += (
            "Determina las constantes de integración de forma explícita si es necesario.\n\n"
        )

    prompt += (
        "Devuelve únicamente el procedimiento matemático paso a paso, "
        "de forma clara, ordenada y matemática. No escribas comentarios, "
        "presentaciones, saludos, despedidas ni explicaciones fuera de los pasos."
    )

    # =========================================
    # DeepSeek API
    # =========================================
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content":
                "Eres un experto matemático en cálculo y ecuaciones diferenciales. "
                "Siempre entregas soluciones exactas, limpias y correctas."
            },
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        deepseek_response = response.json()
        solution_text = deepseek_response["choices"][0]["message"]["content"]

        return jsonify({
            "success": True,
            "equation": equation_str,
            "conditions": conds,
            "solution": solution_text
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Error al comunicarse con DeepSeek.",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor.",
            "details": str(e)
        }), 500


# =========================================
# Ejecutar servidor
# =========================================
if __name__ == '__main__':
    app.run(debug=True)
