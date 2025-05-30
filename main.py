import tkinter as tk
from tkinter import messagebox
import random
from utils import cargar_pokemons_desde_json
from pokemon import Pokemon, Movimiento
from logic import iniciar_combate, aplicar_daño, copiar_estado, minimax_con_poda

TAB = "   "

class PantallaCombate:
    def __init__(self, root, pkm_jugador, pkm_ia):
        self.root = root
        self.root.title("⚔️ Combate Pokémon con IA")

        self.estado = {
            'jugador': pkm_jugador,
            'ia': pkm_ia
        }

        self.frame_info = tk.Frame(root)
        self.frame_info.pack(pady=10)

        self.label_jugador = tk.Label(self.frame_info, text=f"{self.estado['jugador'].nombre}: {self.estado['jugador'].ps} PS")
        self.label_jugador.grid(row=0, column=0, padx=20)

        self.label_ia = tk.Label(self.frame_info, text=f"{self.estado['ia'].nombre}: {self.estado['ia'].ps} PS")
        self.label_ia.grid(row=0, column=1, padx=20)

        self.mensaje = tk.Text(root, height=6, width=50, wrap='word')
        self.mensaje.pack(pady=10)

        self.boton_frame = tk.Frame(root)
        self.boton_frame.pack()

        self.botones_ataque = []
        for idx, movimiento in enumerate(self.estado['jugador'].movimientos):
            btn = tk.Button(
                self.boton_frame,
                text=f"{movimiento.nombre}\n({movimiento.tipo}, {movimiento.poder} daño)",
                width=25,
                command=lambda m=movimiento: self.jugar_turno_usuario(m)
            )
            btn.grid(row=idx // 2, column=idx % 2, padx=5, pady=5)
            self.botones_ataque.append(btn)

    def jugar_turno_usuario(self, movimiento):
        if not self.estado['jugador'].esta_vivo() or not self.estado['ia'].esta_vivo():
            return

        self.mensaje.insert(tk.END, f"\n{TAB}{self.estado['jugador'].nombre} usó {movimiento.nombre}\n")
        aplicar_daño(self.estado['jugador'], self.estado['ia'], movimiento)
        self.actualizar_estado()

        if not self.estado['ia'].esta_vivo():
            self.mensaje.insert(tk.END, "\n🎉 ¡Has ganado el combate!\n")
            self.deshabilitar_botones()
            return

        self.root.after(1000, self.turno_ia)

    def turno_ia(self):
        estado_copia = copiar_estado(self.estado)
        _, mejor_ataque = minimax_con_poda(
            estado_copia, profundidad=3, alpha=float('-inf'), beta=float('inf'), es_max_turno=True
        )

        ataque_real = None
        for m in self.estado['ia'].movimientos:
            if m.nombre == mejor_ataque.nombre:
                ataque_real = m
                break

        self.mensaje.insert(tk.END, f"\n{TAB}{self.estado['ia'].nombre} usó {mejor_ataque.nombre}\n")
        aplicar_daño(self.estado['ia'], self.estado['jugador'], ataque_real)
        self.actualizar_estado()

        if not self.estado['jugador'].esta_vivo():
            self.mensaje.insert(tk.END, "\n💀 La IA te ha derrotado.\n")
            self.deshabilitar_botones()

    def actualizar_estado(self):
        self.label_jugador.config(text=f"{self.estado['jugador'].nombre}: {self.estado['jugador'].ps:.0f} PS")
        self.label_ia.config(text=f"{self.estado['ia'].nombre}: {self.estado['ia'].ps:.0f} PS")
        self.mensaje.see(tk.END)

    def deshabilitar_botones(self):
        for btn in self.botones_ataque:
            btn.config(state=tk.DISABLED)


class PantallaSeleccion:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Selecciona tu Pokémon")

        self.label = tk.Label(root, text="Selecciona tu Pokémon:", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.pokemons = cargar_pokemons_desde_json()

        if not self.pokemons:
            messagebox.showerror("Error", "No se encontraron Pokémon en el archivo JSON.")
            root.destroy()
            return

        for i, pkm in enumerate(self.pokemons):
            btn = tk.Button(
                self.frame,
                text=f"{pkm.nombre}\n({pkm.tipo}, {pkm.ps} PS)",
                width=20,
                height=3,
                command=lambda p=pkm: self.seleccionar_pokemon(p)
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    def seleccionar_pokemon(self, pkm):
        self.root.destroy()
        self.abrir_combate(pkm)

    def abrir_combate(self, pkm_jugador):
        root = tk.Tk()

        todos_los_pokemons = cargar_pokemons_desde_json()
        pkm_ia = random.choice(todos_los_pokemons)

        PantallaCombate(root, pkm_jugador, pkm_ia)
        root.mainloop()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        PantallaSeleccion(root)
        root.mainloop()
    except Exception as e:
        print("Error:", str(e))