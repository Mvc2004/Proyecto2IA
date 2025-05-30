import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from logic import BatallaPokemon, Entrenador, cargar_pokemons_desde_json, crear_entrenador_aleatorio
import random
import json
from pathlib import Path

class PokemonBattleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Combate Pokémon con IA")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Cargar datos
        try:
            self.todos_pokemons = cargar_pokemons_desde_json()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los Pokémon:\n{str(e)}")
            self.root.destroy()
            return
        
        # Variables de estado
        self.batalla_actual = None
        self.equipo_jugador = []
        self.equipo_oponente = []
        
        # Crear interfaz inicial
        self.crear_interfaz_inicio()
    
    def crear_interfaz_inicio(self):
        self.limpiar_pantalla()
        
        # Marco principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(main_frame, text="¡Simulador de Combate Pokémon!", style='Title.TLabel').pack(pady=20)
        
        # Frame de entrada de nombre
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(pady=10)
        
        ttk.Label(name_frame, text="Nombre del Entrenador:").pack(side="left")
        self.nombre_entrenador = tk.StringVar(value="Ash")
        ttk.Entry(name_frame, textvariable=self.nombre_entrenador, width=20).pack(side="left", padx=5)
        
        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Nueva Batalla", command=self.preparar_batalla).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="Salir", command=self.root.quit).pack(pady=5, fill="x")
    
    def preparar_batalla(self):
        self.limpiar_pantalla()
        
        # Verificar nombre
        nombre = self.nombre_entrenador.get().strip()
        if not nombre:
            messagebox.showwarning("Nombre vacío", "Por favor ingresa un nombre para el entrenador")
            self.crear_interfaz_inicio()
            return
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(main_frame, text=f"Preparar Batalla: {nombre}", style='Title.TLabel').pack(pady=10)
        
        # Frame de selección
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill="both", expand=True)
        
        # Lista de Pokémon disponibles
        ttk.Label(selection_frame, text="Pokémon Disponibles:").grid(row=0, column=0, sticky="w")
        
        self.lista_pokemons = ttk.Treeview(selection_frame, columns=('nombre', 'tipo', 'ps'), selectmode='extended')
        self.lista_pokemons.heading('nombre', text='Nombre')
        self.lista_pokemons.heading('tipo', text='Tipo')
        self.lista_pokemons.heading('ps', text='PS')
        self.lista_pokemons.column('nombre', width=150)
        self.lista_pokemons.column('tipo', width=100)
        self.lista_pokemons.column('ps', width=50)
        self.lista_pokemons.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(selection_frame, orient="vertical", command=self.lista_pokemons.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.lista_pokemons.configure(yscrollcommand=scrollbar.set)
        
        # Llenar lista
        for pokemon in self.todos_pokemons:
            self.lista_pokemons.insert('', 'end', values=(pokemon.nombre, pokemon.tipo, pokemon.ps_max))
        
        # Frame de equipo seleccionado
        team_frame = ttk.Frame(selection_frame)
        team_frame.grid(row=1, column=2, padx=10, sticky="nsew")
        
        ttk.Label(team_frame, text="Tu Equipo (3 Pokémon):").pack()
        self.lista_equipo = tk.Listbox(team_frame, width=30, height=10)
        self.lista_equipo.pack(fill="both", expand=True)
        
        # Botones de control
        button_frame = ttk.Frame(selection_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Añadir al Equipo", command=self.añadir_al_equipo).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Quitar del Equipo", command=self.quitar_del_equipo).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Iniciar Batalla", command=self.iniciar_batalla).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.crear_interfaz_inicio).pack(side="right", padx=5)
        
        # Configurar grid
        selection_frame.rowconfigure(1, weight=1)
        selection_frame.columnconfigure(0, weight=1)
        selection_frame.columnconfigure(2, weight=1)
    
    def añadir_al_equipo(self):
        seleccionados = self.lista_pokemons.selection()
        if not seleccionados:
            return
        
        for item in seleccionados:
            if self.lista_equipo.size() >= 3:
                messagebox.showwarning("Equipo completo", "Solo puedes seleccionar 3 Pokémon")
                break
            
            valores = self.lista_pokemons.item(item, 'values')
            nombre_pokemon = valores[0]
            
            # Verificar si ya está en el equipo
            if nombre_pokemon not in self.lista_equipo.get(0, tk.END):
                self.lista_equipo.insert(tk.END, nombre_pokemon)
    
    def quitar_del_equipo(self):
        seleccionados = self.lista_equipo.curselection()
        if seleccionados:
            self.lista_equipo.delete(seleccionados[0])
    
    def iniciar_batalla(self):
        if self.lista_equipo.size() != 3:
            messagebox.showwarning("Equipo incompleto", "Debes seleccionar exactamente 3 Pokémon")
            return

        equipo_jugador = []
        for nombre in self.lista_equipo.get(0, tk.END):
            for pokemon in self.todos_pokemons:
                if pokemon.nombre == nombre:
                    equipo_jugador.append(pokemon)
                    break

        # Verificar que todos los Pokémon tengan ataques
        for pokemon in equipo_jugador:
            if not pokemon.ataques:
                messagebox.showerror("Error", f"{pokemon.nombre} no tiene ataques definidos")
                return

        # Crear equipo del oponente
        pokemons_disponibles = [p for p in self.todos_pokemons if p not in equipo_jugador]
        equipo_oponente = crear_entrenador_aleatorio(pokemons_disponibles).pokemons

        # Verificar ataques del oponente
        for pokemon in equipo_oponente:
            if not pokemon.ataques:
                messagebox.showerror("Error", f"{pokemon.nombre} (IA) no tiene ataques definidos")
                return

        # Iniciar combate
        self.batalla_actual = BatallaPokemon(
            jugador=Entrenador(self.nombre_entrenador.get(), equipo_jugador),
            oponente=Entrenador("Entrenador IA", equipo_oponente)
        )
        self.mostrar_interfaz_batalla()
    
    def mostrar_interfaz_batalla(self):
        self.limpiar_pantalla()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame del oponente
        oponent_frame = ttk.LabelFrame(main_frame, text="Oponente")
        oponent_frame.pack(fill="x", pady=10)
        
        estado = self.batalla_actual.estado_actual()
        
        ttk.Label(oponent_frame, text=f"{estado['oponente']['nombre']}", font=('Arial', 12, 'bold')).pack(anchor="w")
        
        # Barra de PS del oponente
        self.oponente_hp = ttk.Progressbar(oponent_frame, length=300, 
                                         maximum=estado['oponente']['ps_max'],
                                         value=estado['oponente']['ps_actual'])
        self.oponente_hp.pack(fill="x", pady=5)
        
        ttk.Label(oponent_frame, 
                 text=f"{estado['oponente']['pokemon_actual']} ({estado['oponente']['tipo']}) | PS: {estado['oponente']['ps_actual']}/{estado['oponente']['ps_max']}").pack(anchor="w")
        
        # Frame de historial
        hist_frame = ttk.LabelFrame(main_frame, text="Historial del Combate")
        hist_frame.pack(fill="both", expand=True, pady=10)
        
        self.historial_text = tk.Text(hist_frame, height=10, state='disabled', wrap="word")
        self.historial_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(hist_frame, command=self.historial_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.historial_text['yscrollcommand'] = scrollbar.set
        
        # Frame del jugador
        player_frame = ttk.LabelFrame(main_frame, text="Tu Pokémon")
        player_frame.pack(fill="x", pady=10)
        
        ttk.Label(player_frame, text=f"{estado['jugador']['nombre']}", font=('Arial', 12, 'bold')).pack(anchor="w")
        
        # Barra de PS del jugador
        self.jugador_hp = ttk.Progressbar(player_frame, length=300, 
                                        maximum=estado['jugador']['ps_max'],
                                        value=estado['jugador']['ps_actual'])
        self.jugador_hp.pack(fill="x", pady=5)
        
        ttk.Label(player_frame, 
                 text=f"{estado['jugador']['pokemon_actual']} ({estado['jugador']['tipo']}) | PS: {estado['jugador']['ps_actual']}/{estado['jugador']['ps_max']}").pack(anchor="w")
        
        # Frame de ataques
        attack_frame = ttk.LabelFrame(main_frame, text="Ataques Disponibles")
        attack_frame.pack(fill="x", pady=10)
        
        self.botones_ataques = []
        for i, ataque in enumerate(estado['jugador']['ataques']):
            btn = ttk.Button(
                attack_frame, 
                text=f"{ataque['nombre']} ({ataque['tipo']}, Poder: {ataque['poder']})",
                command=lambda a=ataque: self.realizar_turno(a)
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            self.botones_ataques.append(btn)
        
        # Configurar grid de ataques
        for i in range(2):
            attack_frame.columnconfigure(i, weight=1)
        
        # Botón de rendirse
        ttk.Button(main_frame, text="Rendirse", command=self.rendirse).pack(pady=10)
        
        # Actualizar interfaz
        self.actualizar_interfaz()
    
    def realizar_turno(self, ataque_dict):
        # Buscar el ataque real en el Pokémon del jugador
        ataque = None
        for a in self.batalla_actual.jugador.pokemon_actual().ataques:
            if a.nombre == ataque_dict['nombre']:
                ataque = a
                break
        
        if not ataque:
            messagebox.showerror("Error", "Ataque no encontrado")
            return
        
        # Turno del jugador
        mensaje = self.batalla_actual.aplicar_ataque(ataque, es_oponente_atacando=False)
        self.actualizar_interfaz()
        
        if self.batalla_actual.es_combate_terminado():
            self.mostrar_resultado()
            return
        
        # Turno de la IA
        ataque_ia = self.batalla_actual.seleccionar_ataque_ia()
        mensaje_ia = self.batalla_actual.aplicar_ataque(ataque_ia, es_oponente_atacando=True)
        self.actualizar_interfaz()
        
        if self.batalla_actual.es_combate_terminado():
            self.mostrar_resultado()
    
    def actualizar_interfaz(self):
        estado = self.batalla_actual.estado_actual()
        
        # Actualizar barras de salud
        self.jugador_hp['value'] = estado['jugador']['ps_actual']
        self.oponente_hp['value'] = estado['oponente']['ps_actual']
        
        # Actualizar historial
        self.historial_text.config(state='normal')
        self.historial_text.delete(1.0, tk.END)
        
        if len(estado['historial']) == 0:
            self.historial_text.insert(tk.END, "¡Que comience el combate!\n")
        else:
            for mensaje in estado['historial']:
                self.historial_text.insert(tk.END, mensaje + "\n\n")
        
        self.historial_text.config(state='disabled')
        self.historial_text.yview(tk.END)
        
        # Actualizar botones de ataques si es el turno del jugador
        if estado['turno'] == 'jugador':
            for i, ataque in enumerate(estado['jugador']['ataques']):
                self.botones_ataques[i].config(
                    text=f"{ataque['nombre']} ({ataque['tipo']}, Poder: {ataque['poder']})",
                    state='normal'
                )
        else:
            for btn in self.botones_ataques:
                btn.config(state='disabled')
    
    def mostrar_resultado(self):
        ganador = self.batalla_actual.ganador()
        mensaje = f"¡{ganador} gana el combate!"
        messagebox.showinfo("Combate terminado", mensaje)
        self.crear_interfaz_inicio()
    
    def rendirse(self):
        if messagebox.askyesno("Rendirse", "¿Estás seguro de que quieres rendirte?"):
            self.batalla_actual.jugador.pokemons = []  # Debilitar todos los Pokémon
            self.mostrar_resultado()
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonBattleApp(root)
    root.mainloop()