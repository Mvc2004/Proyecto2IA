

import tkinter as tk
from tkinter import messagebox
from logic import Pokemon, Attack, GameState
from utils import calculate_damage, minimax
from PIL import Image, ImageTk  # Asegúrate de tener instalado Pillow

# Crear el muñequito Pokémon y ataques
player_attacks = [
    Attack("Thunderbolt", "Electric", 40),
    Attack("Quick Attack", "Normal", 30),
    Attack("Iron Tail", "Steel", 35),
    Attack("Electro Ball", "Electric", 50)
]
ai_attacks = [
    Attack("Flamethrower", "Fire", 40),
    Attack("Scratch", "Normal", 20),
    Attack("Ember", "Fire", 30),
    Attack("Bite", "Dark", 25)
]

player_pokemon = Pokemon("Pikachu", "Electric", 100, player_attacks)
ai_pokemon = Pokemon("Charmander", "Fire", 100, ai_attacks)

game_state = GameState(player_pokemon, ai_pokemon)

# GUI
root = tk.Tk()
root.title("Pokeminmax: Combate Pokémon")

status_text = tk.StringVar()

def update_labels():
    player_label.config(text=f"{player_pokemon.name}: {player_pokemon.hp} PS")
    ai_label.config(text=f"{ai_pokemon.name}: {ai_pokemon.hp} PS")

def player_turn(attack):
    if player_pokemon.is_fainted() or ai_pokemon.is_fainted():
        return

    dmg = calculate_damage(attack, player_pokemon, ai_pokemon)
    ai_pokemon.apply_damage(dmg)
    status_text.set(f"{player_pokemon.name} usó {attack.name} e hizo {dmg} de daño.")

    update_labels()

    if ai_pokemon.is_fainted():
        messagebox.showinfo("Fin del juego", "¡Ganaste!")
        return

    root.after(1000, ai_turn)

def ai_turn():
    _, ai_attack = minimax(game_state, depth=2, alpha=float('-inf'), beta=float('inf'), maximizing=True)
    dmg = calculate_damage(ai_attack, ai_pokemon, player_pokemon)
    player_pokemon.apply_damage(dmg)
    status_text.set(f"{ai_pokemon.name} usó {ai_attack.name} e hizo {dmg} de daño.")
    update_labels()

    if player_pokemon.is_fainted():
        messagebox.showinfo("Fin del juego", "¡Perdiste!")

# Cargar imágenes
def load_image(path, size=(120, 120)):
    img = Image.open(path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

pikachu_img = load_image("assets/pikachu.png")
charmander_img = load_image("assets/charmander.png")

# Layout
player_label = tk.Label(root, text="")
player_label.pack()

player_img_label = tk.Label(root, image=pikachu_img)
player_img_label.pack()

ai_label = tk.Label(root, text="")
ai_label.pack()

ai_img_label = tk.Label(root, image=charmander_img)
ai_img_label.pack()

tk.Label(root, text="Elige tu ataque:").pack()

for atk in player_pokemon.attacks:
    btn = tk.Button(root, text=atk.name, command=lambda a=atk: player_turn(a))
    btn.pack(pady=2)

status = tk.Label(root, textvariable=status_text, wraplength=300)
status.pack(pady=10)

update_labels()
root.mainloop()
