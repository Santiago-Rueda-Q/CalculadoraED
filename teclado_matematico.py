"""
Teclado Matemático para Calculadora de Ecuaciones Diferenciales
Módulo independiente que proporciona un teclado virtual con símbolos matemáticos
"""

import customtkinter as ctk


class TecladoMatematico:
    """Clase que crea una ventana de teclado matemático flotante"""
    
    def __init__(self, parent, entry_widget):
        """
        Inicializa el teclado matemático
        
        Args:
            parent: Ventana principal (root)
            entry_widget: Widget de texto donde se insertarán los símbolos
        """
        self.parent = parent
        self.entry_widget = entry_widget
        self.ventana = None
        
        # Definir grupos de botones
        self.botones_derivadas = [
            ("y'", "y'", "Primera derivada"),
            ("y''", "y''", "Segunda derivada"),
            ("y'''", "y'''", "Tercera derivada"),
            ("dy/dx", "dy/dx", "Notación Leibniz"),
            ("d²y/dx²", "d2y/dx2", "Segunda derivada Leibniz"),
        ]
        
        self.botones_funciones = [
            ("sin", "sin()", "Seno"),
            ("cos", "cos()", "Coseno"),
            ("tan", "tan()", "Tangente"),
            ("cot", "cot()", "Cotangente"),
            ("sec", "sec()", "Secante"),
            ("csc", "csc()", "Cosecante"),
            ("exp", "exp()", "Exponencial e^x"),
            ("ln", "log()", "Logaritmo natural"),
            ("log", "log()", "Logaritmo"),
            ("√", "sqrt()", "Raíz cuadrada"),
            ("|x|", "abs()", "Valor absoluto"),
        ]
        
        self.botones_funciones_hip = [
            ("sinh", "sinh()", "Seno hiperbólico"),
            ("cosh", "cosh()", "Coseno hiperbólico"),
            ("tanh", "tanh()", "Tangente hiperbólica"),
        ]
        
        self.botones_constantes = [
            ("π", "pi", "Pi (3.14159...)"),
            ("e", "E", "Número de Euler"),
            ("i", "I", "Unidad imaginaria"),
            ("∞", "oo", "Infinito"),
        ]
        
        self.botones_operadores = [
            ("+", "+", "Suma"),
            ("−", "-", "Resta"),
            ("×", "*", "Multiplicación"),
            ("÷", "/", "División"),
            ("^", "**", "Potencia"),
            ("(", "(", "Paréntesis izquierdo"),
            (")", ")", "Paréntesis derecho"),
            ("=", "=", "Igual"),
        ]
        
        self.botones_numeros = [
            ("7", "7", ""), ("8", "8", ""), ("9", "9", ""),
            ("4", "4", ""), ("5", "5", ""), ("6", "6", ""),
            ("1", "1", ""), ("2", "2", ""), ("3", "3", ""),
            ("0", "0", ""), (".", ".", ""), ("±", "-", "Negativo"),
        ]
        
        self.botones_variables = [
            ("x", "x", "Variable independiente"),
            ("y", "y", "Variable dependiente"),
            ("t", "t", "Variable tiempo"),
            ("n", "n", "Índice/Exponente"),
            ("C₁", "C1", "Constante 1"),
            ("C₂", "C2", "Constante 2"),
        ]
        
        self.botones_plantillas = [
            ("y' = ", "y' = ", "Ecuación primer orden"),
            ("y'' + y = ", "y'' + y = ", "Ecuación segundo orden"),
            ("y' + P(x)y = ", "y' + *y = ", "Forma lineal"),
            ("M + N·y' = 0", " + *y' = 0", "Forma exacta"),
        ]
    
    def mostrar(self):
        """Muestra la ventana del teclado matemático"""
        if self.ventana is not None and self.ventana.winfo_exists():
            self.ventana.focus()
            return
        
        self.ventana = ctk.CTkToplevel(self.parent)
        self.ventana.title("⌨️ Teclado Matemático")
        self.ventana.geometry("650x580")
        self.ventana.resizable(False, False)
        
        # Mantener siempre visible
        self.ventana.attributes('-topmost', True)
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.ventana)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="⌨️ Teclado Matemático",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.pack(pady=5)
        
        instruccion = ctk.CTkLabel(
            main_frame,
            text="Haz clic en los botones para insertar símbolos en la ecuación",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        instruccion.pack(pady=2)
        
        # Crear secciones
        self._crear_seccion(main_frame, "📐 Derivadas", self.botones_derivadas, 5, "#1f6aa5")
        self._crear_seccion(main_frame, "📊 Funciones Trigonométricas", self.botones_funciones[:6], 6, "#2b7a0b")
        self._crear_seccion(main_frame, "📈 Funciones Matemáticas", self.botones_funciones[6:], 5, "#8b4513")
        self._crear_seccion(main_frame, "〰️ Funciones Hiperbólicas", self.botones_funciones_hip, 3, "#6b3fa0")
        self._crear_seccion(main_frame, "🔢 Constantes", self.botones_constantes, 4, "#b8860b")
        self._crear_seccion(main_frame, "➕ Operadores", self.botones_operadores, 8, "#4a4a4a")
        self._crear_seccion(main_frame, "🔤 Variables", self.botones_variables, 6, "#2d5a87")
        self._crear_seccion(main_frame, "🔢 Números", self.botones_numeros, 3, "#3a3a3a")
        self._crear_seccion(main_frame, "📝 Plantillas Rápidas", self.botones_plantillas, 2, "#6b2d5a")
        
        # Botones de acción
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", pady=10, padx=5)
        
        btn_borrar = ctk.CTkButton(
            action_frame,
            text="⌫ Borrar último",
            command=self._borrar_ultimo,
            fg_color="#c0392b",
            hover_color="#922b21",
            width=120
        )
        btn_borrar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(
            action_frame,
            text="🗑️ Limpiar todo",
            command=self._limpiar_todo,
            fg_color="#7f8c8d",
            hover_color="#5d6d7e",
            width=120
        )
        btn_limpiar.pack(side="left", padx=5)
        
        btn_cerrar = ctk.CTkButton(
            action_frame,
            text="✖ Cerrar",
            command=self.ventana.destroy,
            fg_color="#34495e",
            hover_color="#2c3e50",
            width=100
        )
        btn_cerrar.pack(side="right", padx=5)
    
    def _crear_seccion(self, parent, titulo, botones, columnas, color):
        """Crea una sección de botones"""
        # Frame de sección
        seccion_frame = ctk.CTkFrame(parent)
        seccion_frame.pack(fill="x", pady=5, padx=5)
        
        # Título de sección
        label = ctk.CTkLabel(
            seccion_frame,
            text=titulo,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color
        )
        label.pack(anchor="w", padx=5, pady=2)
        
        # Frame para botones
        botones_frame = ctk.CTkFrame(seccion_frame, fg_color="transparent")
        botones_frame.pack(fill="x", padx=5, pady=2)
        
        # Crear botones en grid
        for i, (texto, valor, tooltip) in enumerate(botones):
            fila = i // columnas
            col = i % columnas
            
            btn = ctk.CTkButton(
                botones_frame,
                text=texto,
                command=lambda v=valor: self._insertar(v),
                width=70,
                height=35,
                font=ctk.CTkFont(size=13),
                fg_color=color,
                hover_color=self._oscurecer_color(color)
            )
            btn.grid(row=fila, column=col, padx=2, pady=2)
            
            # Tooltip (simulado con binding)
            if tooltip:
                btn.bind("<Enter>", lambda e, t=tooltip: self._mostrar_tooltip(e, t))
                btn.bind("<Leave>", self._ocultar_tooltip)
    
    def _oscurecer_color(self, color):
        """Oscurece un color hex para el hover"""
        try:
            # Convertir hex a RGB
            color = color.lstrip('#')
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            # Oscurecer 20%
            r = max(0, int(r * 0.8))
            g = max(0, int(g * 0.8))
            b = max(0, int(b * 0.8))
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return "#333333"
    
    def _insertar(self, texto):
        """Inserta texto en el widget de entrada"""
        try:
            # Obtener posición actual del cursor
            self.entry_widget.insert("insert", texto)
            
            # Si es una función con paréntesis, mover cursor adentro
            if texto.endswith("()"):
                # Mover cursor una posición atrás (dentro del paréntesis)
                pos = self.entry_widget.index("insert")
                self.entry_widget.mark_set("insert", f"{pos}-1c")
            
            # Enfocar el widget de entrada
            self.entry_widget.focus()
        except Exception as e:
            print(f"Error al insertar: {e}")
    
    def _borrar_ultimo(self):
        """Borra el último carácter"""
        try:
            contenido = self.entry_widget.get("1.0", "end-1c")
            if contenido:
                self.entry_widget.delete("end-2c", "end-1c")
                self.entry_widget.focus()
        except:
            pass
    
    def _limpiar_todo(self):
        """Limpia todo el contenido"""
        try:
            self.entry_widget.delete("1.0", "end")
            self.entry_widget.focus()
        except:
            pass
    
    def _mostrar_tooltip(self, event, texto):
        """Muestra un tooltip (simplificado)"""
        # Para una implementación completa, se podría usar un Label flotante
        pass
    
    def _ocultar_tooltip(self, event):
        """Oculta el tooltip"""
        pass
    
    def cerrar(self):
        """Cierra la ventana del teclado"""
        if self.ventana is not None and self.ventana.winfo_exists():
            self.ventana.destroy()
            self.ventana = None


class BotonAyudaTeclado:
    """Clase helper para crear el botón de ayuda/teclado en la interfaz principal"""
    
    @staticmethod
    def crear_boton(parent_frame, root, entry_widget):
        """
        Crea y retorna un botón que abre el teclado matemático
        
        Args:
            parent_frame: Frame donde colocar el botón
            root: Ventana principal
            entry_widget: Widget de texto para insertar símbolos
            
        Returns:
            tuple: (botón, instancia del teclado)
        """
        teclado = TecladoMatematico(root, entry_widget)
        
        btn = ctk.CTkButton(
            parent_frame,
            text="⌨️ Teclado",
            command=teclado.mostrar,
            font=ctk.CTkFont(size=16),
            height=45,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        
        return btn, teclado


# Función de prueba independiente
if __name__ == "__main__":
    # Prueba del módulo
    root = ctk.CTk()
    root.title("Prueba Teclado Matemático")
    root.geometry("600x400")
    
    ctk.set_appearance_mode("dark")
    
    label = ctk.CTkLabel(root, text="Ecuación:", font=ctk.CTkFont(size=14))
    label.pack(pady=10)
    
    entrada = ctk.CTkTextbox(root, height=100, width=500)
    entrada.pack(pady=10)
    
    btn, teclado = BotonAyudaTeclado.crear_boton(root, root, entrada)
    btn.pack(pady=10)
    
    root.mainloop()