import tkinter as tk
from tkinter import messagebox, ttk
import random
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
from utils import cargar_pokemons_desde_json
from pokemon import Pokemon
from logic import aplicar_daño, copiar_estado, minimax_con_poda

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
POKEMON_IMG_SIZE = (100, 100)
MOVE_IMG_SIZE = (32, 32)
BACKGROUND_COLOR = "#2c3e50"
CARD_COLOR = "#34495e"
ACCENT_COLOR = "#3498db"
SUCCESS_COLOR = "#27ae60"
DANGER_COLOR = "#e74c3c"
WARNING_COLOR = "#f39c12"
TEXT_COLOR = "#ecf0f1"
HEALTH_BAR_WIDTH = 250
HEALTH_BAR_HEIGHT = 25

class PantallaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Pokémon Battle - Bienvenido")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Main container
        self.main_container = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create welcome screen
        self.create_welcome_screen()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def create_welcome_screen(self):
        """Create the welcome screen with title, image, rules, and next button"""
        
        # Title section
        title_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        title_frame.pack(pady=(0, 20))
        
        welcome_label = tk.Label(
            title_frame,
            text="🎮 BIENVENIDO A POKÉMON BATTLE 🎮",
            font=("Arial Black", 24, "bold"),
            bg=BACKGROUND_COLOR,
            fg="#f1c40f"
        )
        welcome_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="¡Prepárate para la batalla definitiva!",
            font=("Arial", 14),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        subtitle_label.pack(pady=5)
        
        # Main content frame
        content_frame = tk.Frame(self.main_container, bg=CARD_COLOR, relief=tk.RAISED, bd=3)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Rules section
        rules_frame = tk.Frame(content_frame, bg=CARD_COLOR)
        rules_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        rules_title = tk.Label(
            rules_frame,
            text="📋 REGLAS DEL JUEGO",
            font=("Arial Black", 16, "bold"),
            bg=CARD_COLOR,
            fg="#f39c12"
        )
        rules_title.pack(pady=(0, 15))
        
        # Rules text
        rules_text = [
            "🎯 Objetivo: Derrota al Pokémon de la IA reduciendo sus PS a 0",
            "⚔️ Combate: Selecciona uno de los 4 movimientos disponibles",
            "💥 Daño: Cada movimiento tiene diferente poder de ataque",
            "🎨 Tipos: Los tipos afectan la efectividad de los movimientos",
            "🤖 IA Inteligente: La IA usa algoritmo minimax para elegir movimientos",
            "❤️ Vida: Las barras de vida cambian de color según el daño recibido",
            "🏆 Victoria: ¡Gana siendo el último Pokémon en pie!"
        ]
        
        for rule in rules_text:
            rule_label = tk.Label(
                rules_frame,
                text=rule,
                font=("Arial", 11),
                bg=CARD_COLOR,
                fg=TEXT_COLOR,
                anchor="w",
                justify="left"
            )
            rule_label.pack(fill="x", pady=3)
        
        # Buttons section
        buttons_frame = tk.Frame(content_frame, bg=CARD_COLOR)
        buttons_frame.pack(pady=60)
        
        # Next button
        next_button = tk.Button(
            buttons_frame,
            text="🚀 COMENZAR AVENTURA",
            font=("Arial", 14, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.ir_a_seleccion
        )
        next_button.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        exit_button = tk.Button(
            buttons_frame,
            text="SALIR",
            font=("Arial", 14, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.salir_aplicacion
        )
        exit_button.pack(side=tk.LEFT, padx=10)
        
        # Hover effects
        def on_enter_next(e):
            next_button.config(bg="#2ecc71")
        
        def on_leave_next(e):
            next_button.config(bg=SUCCESS_COLOR)
            
        def on_enter_exit(e):
            exit_button.config(bg="#c0392b")
        
        def on_leave_exit(e):
            exit_button.config(bg=DANGER_COLOR)
        
        next_button.bind("<Enter>", on_enter_next)
        next_button.bind("<Leave>", on_leave_next)
        exit_button.bind("<Enter>", on_enter_exit)
        exit_button.bind("<Leave>", on_leave_exit)

    def ir_a_seleccion(self):
        """Go to Pokemon selection screen"""
        self.root.destroy()
        root = tk.Tk()
        app = PantallaSeleccion(root)
        root.mainloop()

    def salir_aplicacion(self):
        """Exit the application"""
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.quit()


class PantallaCombate:
    def __init__(self, root, pkm_jugador, pkm_ia):
        self.root = root
        self.root.title("⚔️ Combate Pokémon con IA")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.estado = {
            'jugador': pkm_jugador,
            'ia': pkm_ia
        }
        
        # Track AI's chosen move
        self.ai_chosen_move = None
        
        # Main container
        self.canvas = tk.Canvas(self.root, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.main_container = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)

        # Empaquetar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Configurar el canvas para que tenga el main_container dentro
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")

        # Actualizar scrollregion cuando cambie el tamaño del contenido
        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.main_container.bind("<Configure>", on_frame_configure)
        
        # Title
        self.create_title()
        
        # Battle area
        self.create_battle_area()
        
        # AI move display
        self.create_ai_move_display()
        
        # Battle log
        self.create_battle_log()
        
        # Move buttons
        self.create_move_buttons()
        
        # Exit button
        self.create_exit_button()
        
        # Configure styles
        self.configure_styles()
        
        # Initialize display
        self.actualizar_estado()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def get_type_effectiveness(self, attack_type, defend_type):
        """Calculate type effectiveness multiplier and return description"""
        # Type effectiveness chart
        effectiveness = {
            "fuego": {
                "planta": "Súper Eficaz",
                "hielo": "Súper Eficaz",
                "bicho": "Súper Eficaz",
                "acero": "Súper Eficaz",
                "agua": "No muy eficaz",
                "fuego": "No muy eficaz",
                "roca": "No muy eficaz",
                "dragón": "No muy eficaz"
            },
            "agua": {
                "fuego": "Súper Eficaz",
                "tierra": "Súper Eficaz",
                "roca": "Súper Eficaz",
                "agua": "No muy eficaz",
                "planta": "No muy eficaz",
                "dragón": "No muy eficaz"
            },
            "planta": {
                "agua": "Súper Eficaz",
                "tierra": "Súper Eficaz",
                "roca": "Súper Eficaz",
                "fuego": "No muy eficaz",
                "planta": "No muy eficaz",
                "veneno": "No muy eficaz",
                "volador": "No muy eficaz",
                "bicho": "No muy eficaz",
                "dragón": "No muy eficaz",
                "acero": "No muy eficaz"
            },
            "eléctrico": {
                "agua": "Súper Eficaz",
                "volador": "Súper Eficaz",
                "planta": "No muy eficaz",
                "eléctrico": "No muy eficaz",
                "dragón": "No muy eficaz",
                "tierra": "No afecta"
            },
            "hielo": {
                "planta": "Súper Eficaz",
                "tierra": "Súper Eficaz",
                "volador": "Súper Eficaz",
                "dragón": "Súper Eficaz",
                "agua": "No muy eficaz",
                "hielo": "No muy eficaz",
                "acero": "No muy eficaz"
            },
            "lucha": {
                "normal": "Súper Eficaz",
                "hielo": "Súper Eficaz",
                "roca": "Súper Eficaz",
                "acero": "Súper Eficaz",
                "veneno": "No muy eficaz",
                "volador": "No muy eficaz",
                "psíquico": "No muy eficaz",
                "bicho": "No muy eficaz",
                "hada": "No muy eficaz",
                "fantasma": "No afecta"
            },
            "veneno": {
                "planta": "Súper Eficaz",
                "hada": "Súper Eficaz",
                "veneno": "No muy eficaz",
                "tierra": "No muy eficaz",
                "roca": "No muy eficaz",
                "fantasma": "No muy eficaz",
                "acero": "No afecta"
            },
            "tierra": {
                "fuego": "Súper Eficaz",
                "eléctrico": "Súper Eficaz",
                "veneno": "Súper Eficaz",
                "roca": "Súper Eficaz",
                "acero": "Súper Eficaz",
                "planta": "No muy eficaz",
                "bicho": "No muy eficaz",
                "volador": "No afecta"
            },
            "volador": {
                "eléctrico": "Súper Eficaz",
                "hielo": "Súper Eficaz",
                "roca": "Súper Eficaz",
                "planta": "Súper Eficaz",
                "lucha": "Súper Eficaz",
                "bicho": "Súper Eficaz",
                "eléctrico": "No muy eficaz",
                "roca": "No muy eficaz",
                "acero": "No muy eficaz"
            },
            "psíquico": {
                "lucha": "Súper Eficaz",
                "veneno": "Súper Eficaz",
                "psíquico": "No muy eficaz",
                "acero": "No muy eficaz"
            },
            "bicho": {
                "planta": "Súper Eficaz",
                "psíquico": "Súper Eficaz",
                "fuego": "No muy eficaz",
                "lucha": "No muy eficaz",
                "veneno": "No muy eficaz",
                "volador": "No muy eficaz",
                "fantasma": "No muy eficaz",
                "acero": "No muy eficaz",
                "hada": "No muy eficaz"
            },
            "roca": {
                "fuego": "Súper Eficaz",
                "hielo": "Súper Eficaz",
                "volador": "Súper Eficaz",
                "bicho": "Súper Eficaz",
                "lucha": "No muy eficaz",
                "tierra": "No muy eficaz",
                "acero": "No muy eficaz"
            },
            "fantasma": {
                "psíquico": "Súper Eficaz",
                "fantasma": "Súper Eficaz",
                "normal": "No afecta"
            },
            "dragón": {
                "dragón": "Súper Eficaz",
                "acero": "No muy eficaz",
                "hada": "No afecta"
            },
            "acero": {
                "hielo": "Súper Eficaz",
                "roca": "Súper Eficaz",
                "hada": "Súper Eficaz",
                "fuego": "No muy eficaz",
                "agua": "No muy eficaz",
                "eléctrico": "No muy eficaz",
                "acero": "No muy eficaz"
            },
            "hada": {
                "lucha": "Súper Eficaz",
                "dragón": "Súper Eficaz",
                "fuego": "No muy eficaz",
                "veneno": "No muy eficaz",
                "acero": "No muy eficaz"
            }
        }
        
        attack_type = attack_type.lower()
        defend_type = defend_type.lower()
        
        if attack_type in effectiveness and defend_type in effectiveness[attack_type]:
            return effectiveness[attack_type][defend_type]
        else:
            return "Eficaz"

    def create_title(self):
        """Create the battle title"""
        title_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        title_frame.pack(pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="⚔️ COMBATE POKÉMON ⚔️",
            font=("Arial Black", 20, "bold"),
            bg=BACKGROUND_COLOR,
            fg="#f1c40f",
            relief=tk.FLAT
        )
        title_label.pack()

    def create_battle_area(self):
        """Área de combate con los dos Pokémon enfrentados horizontalmente"""
        battle_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        battle_frame.pack(fill="x", pady=10, padx=80)

        # Configura columnas para IA - VS - Jugador
        for i in range(3):
            battle_frame.grid_columnconfigure(i, weight=1)

        # Pokémon de la IA (izquierda)
        self.create_pokemon_display(battle_frame, self.estado['ia'], 'ia', 0, 0)

        # VS en el centro (columna 1)
        vs_label = tk.Label(
            battle_frame,
            text="VS",
            font=("Arial Black", 22, "bold"),
            bg=BACKGROUND_COLOR,
            fg="#e74c3c"
        )
        vs_label.grid(row=0, column=1, padx=10)

        # Pokémon del jugador (derecha)
        self.create_pokemon_display(battle_frame, self.estado['jugador'], 'jugador', 0, 2)

    def create_pokemon_display(self, parent, pokemon, side, row, column):
        """Muestra Pokémon con imagen, tipo y vida"""
        pokemon_frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
        pokemon_frame.grid_propagate(False)
        pokemon_frame.grid(row=row, column=column, padx=20, pady=5, sticky="nsew")

        img = self.load_pokemon_image(pokemon.nombre.lower())
        setattr(self, f"{side}_img", img)

        img_label = tk.Label(pokemon_frame, image=img, bg=CARD_COLOR)
        img_label.pack(pady=10)
        setattr(self, f"{side}_img_label", img_label)

        info_frame = tk.Frame(pokemon_frame, bg=CARD_COLOR)
        info_frame.pack(padx=10, pady=10)

        tk.Label(info_frame, text=pokemon.nombre.upper(), font=("Arial", 16, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack()

        type_label = tk.Label(
            info_frame,
            text=pokemon.tipo.upper(),
            font=("Arial", 10, "bold"),
            bg=self.get_type_color(pokemon.tipo),
            fg="white",
            padx=10,
            pady=2,
            relief=tk.RAISED,
            bd=1
        )
        type_label.pack(pady=5)

        health_frame = tk.Frame(info_frame, bg="#2c3e50", relief=tk.SUNKEN, bd=2)
        health_frame.pack(fill="x", pady=5)

        tk.Label(health_frame, text="HP", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack(anchor="w", padx=5)

        health_bar = ttk.Progressbar(
            health_frame,
            orient="horizontal",
            length=HEALTH_BAR_WIDTH,
            mode="determinate",
            style=f"{side}.Horizontal.TProgressbar"
        )
        health_bar.pack(padx=5, pady=3)
        health_bar["value"] = 100
        setattr(self, f"{side}_health_bar", health_bar)

        health_text = tk.Label(
            health_frame,
            text=f"{pokemon.ps:.0f} / {pokemon.ps:.0f}",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="white"
        )
        health_text.pack(anchor="e", padx=5)
        setattr(self, f"{side}_health_text", health_text)

    def create_ai_move_display(self):
        """Create frame to display AI's chosen move"""
        ai_move_frame = tk.Frame(self.main_container, bg="#e74c3c", relief=tk.RAISED, bd=3)
        ai_move_frame.pack(fill="x", pady=10, padx=80)
        
        ai_move_title = tk.Label(
            ai_move_frame,
            text="🤖 MOVIMIENTO DE LA IA",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white"
        )
        ai_move_title.pack(pady=5)
        
        # AI move info container
        self.ai_move_info_frame = tk.Frame(ai_move_frame, bg="#e74c3c")
        self.ai_move_info_frame.pack(pady=10)
        
        # Initially show "Thinking..."
        self.ai_move_label = tk.Label(
            self.ai_move_info_frame,
            text="🤔 La IA está pensando...",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white"
        )
        self.ai_move_label.pack()

    def update_ai_move_display(self, move):
        """Update the AI move display with the chosen move"""
        self.ai_chosen_move = move
        
        # Clear previous content
        for widget in self.ai_move_info_frame.winfo_children():
            widget.destroy()
        
        # Create new display
        move_container = tk.Frame(self.ai_move_info_frame, bg="#e74c3c")
        move_container.pack()
        
        # Move type icon
        move_img = self.load_move_image(move.tipo.lower())
        move_img_label = tk.Label(move_container, image=move_img, bg="#e74c3c")
        move_img_label.image = move_img  # Keep reference
        move_img_label.pack(side=tk.LEFT, padx=10)
        
        # Move info
        move_info_frame = tk.Frame(move_container, bg="#e74c3c")
        move_info_frame.pack(side=tk.LEFT, padx=10)
        
        move_name_label = tk.Label(
            move_info_frame,
            text=f"⚡ {move.nombre}",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white"
        )
        move_name_label.pack()
        
        move_details_label = tk.Label(
            move_info_frame,
            text=f"Tipo: {move.tipo.upper()} | Poder: {move.poder}",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white"
        )
        move_details_label.pack()
        
        # Update player move buttons with effectiveness
        self.update_move_buttons_effectiveness()

    def update_move_buttons_effectiveness(self):
        """Update player move buttons to show effectiveness against AI's chosen move"""
        if not self.ai_chosen_move:
            return
            
        for idx, (btn, movimiento) in enumerate(zip(self.botones_ataque, self.estado['jugador'].movimientos)):
            # Calculate effectiveness of player move against AI move type
            effectiveness = self.get_type_effectiveness(movimiento.tipo, self.ai_chosen_move.tipo)
            
            # Update button text
            btn.config(
                text=f"{movimiento.nombre}\n💥 {movimiento.poder} poder\n{effectiveness} vs {self.ai_chosen_move.tipo}"
            )

    def create_battle_log(self):
        """Create the battle log area"""
        log_frame = tk.Frame(self.main_container, bg=CARD_COLOR, relief=tk.RAISED, bd=3)
        log_frame.pack(fill="x", pady=20,padx=80)
        
        log_title = tk.Label(
            log_frame,
            text="📜 REGISTRO DE BATALLA",
            font=("Arial", 12, "bold"),
            bg=CARD_COLOR,
            fg="#f39c12"
        )
        log_title.pack(pady=5)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(log_frame, bg=CARD_COLOR)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.mensaje = tk.Text(
            text_frame,
            height=6,
            width=80,
            wrap='word',
            font=("Consolas", 10),
            bg="#ecf0f1",
            fg="#2c3e50",
            relief=tk.SUNKEN,
            bd=2
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.mensaje.yview)
        self.mensaje.configure(yscrollcommand=scrollbar.set)
        
        self.mensaje.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial message
        self.mensaje.insert(tk.END, "🎮 ¡Comienza el combate Pokémon!\n")
        self.mensaje.insert(tk.END, f"🔥 {self.estado['jugador'].nombre} vs {self.estado['ia'].nombre} ⚡\n")
        self.mensaje.insert(tk.END, "=" * 50 + "\n\n")

    def create_move_buttons(self):
        print("Creating move selection buttons...")
        """Create the move selection buttons"""
        moves_frame = tk.Frame(self.main_container, bg=CARD_COLOR, relief=tk.RAISED, bd=3)
        moves_frame.pack(fill="x", pady=20,padx=80)
        
        moves_title = tk.Label(
            moves_frame,
            text="⚡ SELECCIONA TU ATAQUE",
            font=("Arial", 12, "bold"),
            bg=CARD_COLOR,
            fg="#3498db"
        )
        moves_title.pack(pady=10)
        
        # Buttons container
        buttons_container = tk.Frame(moves_frame, bg=CARD_COLOR)
        buttons_container.pack(pady=10)
        
        # Configure grid for centering
        print("Movimientos del jugador:", self.estado['jugador'].movimientos)

        for i in range(2):
            buttons_container.grid_columnconfigure(i, weight=1)
        
        self.botones_ataque = []
        for idx, movimiento in enumerate(self.estado['jugador'].movimientos):
            # Move button frame
            move_frame = tk.Frame(buttons_container, bg=CARD_COLOR)
            move_frame.grid(row=idx // 2, column=idx % 2, padx=15, pady=10)
            
            # Move type icon
            print(movimiento.tipo.lower())
            move_img = self.load_move_image(movimiento.tipo.lower())
            move_img_label = tk.Label(move_frame, image=move_img, bg=CARD_COLOR)
            move_img_label.image = move_img  # Keep reference
            move_img_label.pack(side=tk.LEFT, padx=5)
            
            # Move button - initially without effectiveness
            btn = tk.Button(
                move_frame,
                text=f"{movimiento.nombre}\n💥 {movimiento.poder} poder\nEsperando IA...",
                width=22,
                height=4,
                font=("Arial", 9, "bold"),
                bg=self.get_type_color(movimiento.tipo),
                fg="white",
                relief=tk.RAISED,
                bd=3,
                cursor="hand2",
                command=lambda m=movimiento: self.jugar_turno_usuario(m)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.botones_ataque.append(btn)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.RIDGE))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.RAISED))

    def create_exit_button(self):
        """Create exit button"""
        self.exit_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        # Don't pack initially - will be shown when battle ends
        
        self.exit_button = tk.Button(
            self.exit_frame,
            text="SALIR DEL JUEGO",
            font=("Arial", 12, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            padx=30,
            pady=10,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.salir_juego
        )
        self.exit_button.pack(pady=20)

    def configure_styles(self):
        """Configure ttk styles for health bars"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Player health bar (green)
        style.configure(
            "jugador.Horizontal.TProgressbar",
            troughcolor='#7f8c8d',
            background=SUCCESS_COLOR,
            thickness=HEALTH_BAR_HEIGHT
        )
        
        # AI health bar (blue)
        style.configure(
            "ia.Horizontal.TProgressbar",
            troughcolor='#7f8c8d',
            background=ACCENT_COLOR,
            thickness=HEALTH_BAR_HEIGHT
        )

    def load_pokemon_image(self, pokemon_name):
        """Load and resize a Pokémon image"""
        try:
            img_path = f"assets/pokemon/{pokemon_name}.png"
            if not os.path.exists(img_path):
                img_path = "assets/pokemon/default.png"
            
            img = Image.open(img_path)
            img = img.resize(POKEMON_IMG_SIZE, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading Pokémon image: {e}")
            return self.create_placeholder_pokemon_image(pokemon_name)

    def create_placeholder_pokemon_image(self, name):
        """Create a placeholder Pokémon image"""
        img = Image.new('RGBA', POKEMON_IMG_SIZE, color=(52, 73, 94, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw circle
        circle_x, circle_y = POKEMON_IMG_SIZE[0] // 2, POKEMON_IMG_SIZE[1] // 2
        circle_radius = min(POKEMON_IMG_SIZE) // 2 - 10
        draw.ellipse(
            (circle_x - circle_radius, circle_y - circle_radius,
             circle_x + circle_radius, circle_y + circle_radius),
            fill=(241, 196, 15, 255),
            outline=(255, 255, 255, 255),
            width=3
        )
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()
        
        letter = name[0].upper() if name else "?"
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            (circle_x - text_width // 2, circle_y - text_height // 2),
            letter,
            fill=(255, 255, 255, 255),
            font=font
        )
        
        return ImageTk.PhotoImage(img)

    def load_move_image(self, move_type):
        """Load and resize a move type image"""
        print(f"Loading move image for type: {move_type}")
        try:
            img_path = f"assets/types/{move_type}.png"
            print(f"Image path: {img_path}")
            if not os.path.exists(img_path):
                img_path = "assets/types/normal.png"
            
            img = Image.open(img_path)
            img = img.resize(MOVE_IMG_SIZE, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading move image: {e}")
            return self.create_placeholder_move_image(move_type)

    def create_placeholder_move_image(self, move_type):
        """Create a placeholder move type image"""
        color = self.get_type_color(move_type)
        img = Image.new('RGBA', MOVE_IMG_SIZE, color=color)
        draw = ImageDraw.Draw(img)
        
        # Add border
        draw.rectangle(
            (0, 0, MOVE_IMG_SIZE[0]-1, MOVE_IMG_SIZE[1]-1),
            outline=(255, 255, 255, 255),
            width=2
        )
        
        return ImageTk.PhotoImage(img)

    def get_type_color(self, tipo):
        """Return a color based on Pokémon type"""
        colors = {
            "normal": "#A8A878",
            "fuego": "#F08030",
            "agua": "#6890F0",
            "planta": "#78C850",
            "eléctrico": "#F8D030",
            "hielo": "#98D8D8",
            "lucha": "#C03028",
            "veneno": "#A040A0",
            "tierra": "#E0C068",
            "volador": "#A890F0",
            "psíquico": "#F85888",
            "bicho": "#A8B820",
            "roca": "#B8A038",
            "fantasma": "#705898",
            "dragón": "#7038F8",
            "acero": "#B8B8D0",
            "hada": "#EE99AC"
        }
        return colors.get(tipo.lower(), "#68A090")

    def jugar_turno_usuario(self, movimiento):
        if not self.estado['jugador'].esta_vivo() or not self.estado['ia'].esta_vivo():
            return

        self.mensaje.insert(tk.END, f"\n🔥 {self.estado['jugador'].nombre} usó {movimiento.nombre}!\n")
        
        # Flash effect
        self.ia_img_label.config(bg="#e74c3c")
        self.root.after(200, lambda: self.ia_img_label.config(bg=CARD_COLOR))
        
        # Apply damage
        ps_antes = self.estado['ia'].ps
        aplicar_daño(self.estado['jugador'], self.estado['ia'], movimiento)
        ps_despues = self.estado['ia'].ps
        
        damage = ps_antes - ps_despues
        
        # Show effectiveness if AI has chosen a move
        if self.ai_chosen_move:
            effectiveness = self.get_type_effectiveness(movimiento.tipo, self.ai_chosen_move.tipo)
            if effectiveness != "Eficaz":
                self.mensaje.insert(tk.END, f"   ⚡ {effectiveness} contra {self.ai_chosen_move.tipo}!\n")
        
        self.mensaje.insert(tk.END, f"   💥 Causó {damage:.0f} puntos de daño!\n")
        
        self.actualizar_estado()
        self.mensaje.see(tk.END)

        if not self.estado['ia'].esta_vivo():
            self.mensaje.insert(tk.END, "\n🎉 ¡VICTORIA! ¡Has ganado el combate!\n")
            self.mostrar_resultado("🎉 ¡VICTORIA!", "¡Has derrotado a la IA!", SUCCESS_COLOR)
            self.finalizar_combate()
            return

        self.root.after(1500, self.turno_ia)

    def turno_ia(self):
        # First, determine AI's move choice
        estado_copia = copiar_estado(self.estado)
        _, mejor_ataque = minimax_con_poda(
            estado_copia, profundidad=3, alpha=float('-inf'), beta=float('inf'), es_max_turno=True
        )

        # Update AI move display
        self.update_ai_move_display(mejor_ataque)

        # Find the actual move object
        ataque_real = None
        for m in self.estado['ia'].movimientos:
            if m.nombre == mejor_ataque.nombre:
                ataque_real = m
                break

        self.mensaje.insert(tk.END, f"\n⚡ {self.estado['ia'].nombre} usó {mejor_ataque.nombre}!\n")
        
        # Flash effect
        self.jugador_img_label.config(bg="#e74c3c")
        self.root.after(200, lambda: self.jugador_img_label.config(bg=CARD_COLOR))
        
        # Apply damage
        ps_antes = self.estado['jugador'].ps
        aplicar_daño(self.estado['ia'], self.estado['jugador'], ataque_real)
        ps_despues = self.estado['jugador'].ps
        
        damage = ps_antes - ps_despues
        self.mensaje.insert(tk.END, f"   💥 Causó {damage:.0f} puntos de daño!\n")
        
        self.actualizar_estado()
        self.mensaje.see(tk.END)

        if not self.estado['jugador'].esta_vivo():
            self.mensaje.insert(tk.END, "\n💀 DERROTA. La IA te ha vencido.\n")
            self.mostrar_resultado("💀 DERROTA", "Has sido derrotado por la IA.", DANGER_COLOR)
            self.finalizar_combate()

    def actualizar_estado(self):
        # Update player health
        health_percentage = max(0, (self.estado['jugador'].ps / self.estado['jugador'].ps_max) * 100)
        self.jugador_health_bar["value"] = health_percentage
        self.jugador_health_text.config(
            text=f"{max(0, self.estado['jugador'].ps):.0f} / {self.estado['jugador'].ps_max:.0f}"
        )
        
        # Update health bar color based on percentage
        style = ttk.Style()
        if health_percentage > 50:
            style.configure("jugador.Horizontal.TProgressbar", background=SUCCESS_COLOR)
        elif health_percentage > 20:
            style.configure("jugador.Horizontal.TProgressbar", background=WARNING_COLOR)
        else:
            style.configure("jugador.Horizontal.TProgressbar", background=DANGER_COLOR)
        
        # Update AI health
        health_percentage = max(0, (self.estado['ia'].ps / self.estado['ia'].ps_max) * 100)
        self.ia_health_bar["value"] = health_percentage
        self.ia_health_text.config(
            text=f"{max(0, self.estado['ia'].ps):.0f} / {self.estado['ia'].ps_max:.0f}"
        )

    def finalizar_combate(self):
        """Finalize the battle and show exit options"""
        self.deshabilitar_botones()
        self.exit_frame.pack(pady=20)

    def deshabilitar_botones(self):
        for btn in self.botones_ataque:
            btn.config(state=tk.DISABLED, bg="#7f8c8d")

    def mostrar_resultado(self, titulo, mensaje, color):
        """Show a styled result window"""
        result_window = tk.Toplevel(self.root)
        result_window.title(titulo)
        result_window.geometry("400x200")
        result_window.configure(bg=BACKGROUND_COLOR)
        result_window.resizable(False, False)
        
        # Center the result window
        result_window.transient(self.root)
        result_window.grab_set()
        
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
        result_window.geometry(f"400x200+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(result_window, bg=color, relief=tk.RAISED, bd=5)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(
            main_frame,
            text=titulo,
            font=("Arial Black", 18, "bold"),
            bg=color,
            fg="white"
        ).pack(pady=20)
        
        # Message
        tk.Label(
            main_frame,
            text=mensaje,
            font=("Arial", 12),
            bg=color,
            fg="white"
        ).pack(pady=10)
        

    def salir_juego(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir del juego?"):
            self.root.quit()


class PantallaSeleccion:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Selecciona tu Pokémon")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Main container
        self.main_container = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        self.create_title()
        
        # Load Pokémon data
        self.pokemons = cargar_pokemons_desde_json()
        
        if not self.pokemons:
            messagebox.showerror("Error", "No se encontraron Pokémon en el archivo JSON.")
            root.destroy()
            return
        
        # Create selection area
        self.create_selection_area()
        
        # Exit button
        self.create_exit_button()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def create_title(self):
        """Create the selection title"""
        title_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        title_frame.pack(pady=(0, 30))
        
        title_label = tk.Label(
            title_frame,
            text="🎮 SELECCIONA TU POKÉMON",
            font=("Arial Black", 24, "bold"),
            bg=BACKGROUND_COLOR,
            fg="#f1c40f"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Elige sabiamente para la batalla",
            font=("Arial", 12),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        subtitle_label.pack(pady=5)

    def create_selection_area(self):
        """Create the Pokémon selection area"""
        # Selection frame
        selection_frame = tk.Frame(self.main_container, bg=CARD_COLOR, relief=tk.RAISED, bd=3)
        selection_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas with scrollbar
        canvas_frame = tk.Frame(selection_frame, bg=CARD_COLOR)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg=CARD_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=CARD_COLOR)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid for centering
        for i in range(3):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Create Pokémon cards
        self.pokemon_images = []
        
        for i, pkm in enumerate(self.pokemons):
            self.create_pokemon_card(pkm, i)

    def create_pokemon_card(self, pkm, index):
        """Create a card for a Pokémon"""
        row = index // 3
        col = index % 3
        
        # Card frame
        card_frame = tk.Frame(
            self.scrollable_frame,
            bg="#ecf0f1",
            relief=tk.RAISED,
            bd=3,
            cursor="hand2"
        )
        card_frame.grid(row=row, column=col, padx=35, pady=15, sticky="nsew")
        
        # Pokémon image
        img = self.load_pokemon_image(pkm.nombre.lower())
        self.pokemon_images.append(img)
        
        img_label = tk.Label(card_frame, image=img, bg="#ecf0f1")
        img_label.pack(pady=15)
        
        # Info frame
        info_frame = tk.Frame(card_frame, bg="#ecf0f1")
        info_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Name
        name_label = tk.Label(
            info_frame,
            text=pkm.nombre.upper(),
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        name_label.pack()
        
        # Type badge
        type_frame = tk.Frame(info_frame, bg="#ecf0f1")
        type_frame.pack(pady=5)
        
        type_label = tk.Label(
            type_frame,
            text=pkm.tipo.upper(),
            font=("Arial", 10, "bold"),
            bg=self.get_type_color(pkm.tipo),
            fg="white",
            padx=15,
            pady=3,
            relief=tk.RAISED,
            bd=1
        )
        type_label.pack()
        
        # HP
        hp_label = tk.Label(
            info_frame,
            text=f"HP: {pkm.ps}",
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        hp_label.pack(pady=2)
        
        # Select button
        select_btn = tk.Button(
            info_frame,
            text="SELECCIONAR",
            font=("Arial", 10, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            padx=20,
            pady=5,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            command=lambda p=pkm: self.seleccionar_pokemon(p)
        )
        select_btn.pack(pady=10)
        
        # Hover effects
        def on_enter(e):
            card_frame.config(bg="#d5dbdb")
            img_label.config(bg="#d5dbdb")
            info_frame.config(bg="#d5dbdb")
            for child in info_frame.winfo_children():
                if isinstance(child, tk.Label) and child != type_label:
                    child.config(bg="#d5dbdb")
                elif isinstance(child, tk.Frame) and child != type_frame:
                    child.config(bg="#d5dbdb")
        
        def on_leave(e):
            card_frame.config(bg="#ecf0f1")
            img_label.config(bg="#ecf0f1")
            info_frame.config(bg="#ecf0f1")
            for child in info_frame.winfo_children():
                if isinstance(child, tk.Label) and child != type_label:
                    child.config(bg="#ecf0f1")
                elif isinstance(child, tk.Frame) and child != type_frame:
                    child.config(bg="#ecf0f1")
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        for widget in [img_label, info_frame]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_exit_button(self):
        """Create exit button"""
        exit_frame = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)
        exit_frame.pack(fill="x", expand=True, pady=20)
        
        exit_button = tk.Button(
            exit_frame,
            text="SALIR",
            font=("Arial", 12, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            padx=30,
            pady=10,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.salir_aplicacion
        )
        exit_button.pack()

    def load_pokemon_image(self, pokemon_name):
        """Load and resize a Pokémon image"""
        try:
            img_path = f"assets/pokemon/{pokemon_name}.png"
            if not os.path.exists(img_path):
                img_path = "assets/pokemon/default.png"
            
            img = Image.open(img_path)
            img = img.resize(POKEMON_IMG_SIZE, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading Pokémon image: {e}")
            return self.create_placeholder_pokemon_image(pokemon_name)

    def create_placeholder_pokemon_image(self, name):
        """Create a placeholder Pokémon image"""
        img = Image.new('RGBA', POKEMON_IMG_SIZE, color=(52, 73, 94, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw circle
        circle_x, circle_y = POKEMON_IMG_SIZE[0] // 2, POKEMON_IMG_SIZE[1] // 2
        circle_radius = min(POKEMON_IMG_SIZE) // 2 - 10
        draw.ellipse(
            (circle_x - circle_radius, circle_y - circle_radius,
             circle_x + circle_radius, circle_y + circle_radius),
            fill=(241, 196, 15, 255),
            outline=(255, 255, 255, 255),
            width=3
        )
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except IOError:
            font = ImageFont.load_default()
        
        letter = name[0].upper() if name else "?"
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            (circle_x - text_width // 2, circle_y - text_height // 2),
            letter,
            fill=(255, 255, 255, 255),
            font=font
        )
        
        return ImageTk.PhotoImage(img)

    def get_type_color(self, tipo):
        """Return a color based on Pokémon type"""
        colors = {
            "normal": "#A8A878",
            "fuego": "#F08030",
            "agua": "#6890F0",
            "planta": "#78C850",
            "eléctrico": "#F8D030",
            "hielo": "#98D8D8",
            "lucha": "#C03028",
            "veneno": "#A040A0",
            "tierra": "#E0C068",
            "volador": "#A890F0",
            "psíquico": "#F85888",
            "bicho": "#A8B820",
            "roca": "#B8A038",
            "fantasma": "#705898",
            "dragón": "#7038F8",
            "acero": "#B8B8D0",
            "hada": "#EE99AC"
        }
        return colors.get(tipo.lower(), "#68A090")

    def seleccionar_pokemon(self, pkm):
        self.root.destroy()
        self.abrir_combate(pkm)

    def abrir_combate(self, pkm_jugador):
        root = tk.Tk()
        
        # Make copies to avoid modifying originals
        pkm_jugador_copia = Pokemon(
            pkm_jugador.nombre,
            pkm_jugador.tipo,
            pkm_jugador.ps,
            pkm_jugador.movimientos
        )
        pkm_jugador_copia.ps_max = pkm_jugador_copia.ps
        
        todos_los_pokemons = cargar_pokemons_desde_json()
        pkm_ia = random.choice(todos_los_pokemons)
        
        pkm_ia_copia = Pokemon(
            pkm_ia.nombre,
            pkm_ia.tipo,
            pkm_ia.ps,
            pkm_ia.movimientos
        )
        pkm_ia_copia.ps_max = pkm_ia_copia.ps

        PantallaCombate(root, pkm_jugador_copia, pkm_ia_copia)
        root.mainloop()

    def salir_aplicacion(self):
        """Exit the application"""
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            self.root.quit()


def create_directories():
    """Create necessary directories for assets if they don't exist"""
    directories = [
        "assets",
        "assets/pokemon",
        "assets/types",
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


if __name__ == "__main__":
    try:
        # Create necessary directories
        create_directories()
        
        # Create main window and start with welcome screen
        root = tk.Tk()
        app = PantallaInicio(root)
        root.mainloop()
    except Exception as e:
        print("Error:", str(e))
