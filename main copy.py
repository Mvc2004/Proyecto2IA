import tkinter as tk
from tkinter import messagebox
from logic import Pokemon, Attack, GameState
from utils import calculate_damage, minimax
from PIL import Image, ImageTk  # Asegúrate de tener instalado Pillow

# Crear el muñequito Pokémon y ataques
player_attacks = [
    Attack("Thunderbolt", "Electric", 40, "assets/ataques-jugador/thunderbolt.png"),
    Attack("Quick Attack", "Normal", 30, "assets/ataques-jugador/quickattack.png"),
    Attack("Iron Tail", "Steel", 35, "assets/ataques-jugador/lick.png"),
    Attack("Electro Ball", "Electric", 50, "assets/ataques-jugador/electroball.png")
]
ai_attacks = [
    Attack("Flamethrower", "Fire", 40, "assets/ataques-ia/flamethrower.png"),
    Attack("Scratch", "Normal", 20, "assets/ataques-ia/scratch.png"),
    Attack("Bubble", "Fire", 30, "assets/ataques-ia/bubble.png"),
    Attack("Bite", "Dark", 25, "assets/ataques-ia/bite.png")
]


ai_pokemon = Pokemon("Charmander", "Fire", 100, ai_attacks)

game_state = GameState(player_pokemon, ai_pokemon)

# GUI
root = tk.Tk()
root.geometry("1010x670+250+50")
root.title("Pokeminmax: Combate Pokémon")



def update_labels():
    player_label.config(text=f"{player_pokemon.name}: {player_pokemon.hp} PS")
    #ai_label.config(text=f"{ai_pokemon.name}: {ai_pokemon.hp} PS")

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

frame_player = tk.Frame(root, width=500, height=670, bg="lightblue")
frame_player.pack(side="left", padx=0, pady=0)
frame_player.pack_propagate(False)  # Para mantener el tamaño fijo
h1 = tk.Label(frame_player, text="Human-Player", font=("Arial", 15), fg="black")
h1.pack(pady=10)

fr1 = tk.Frame(frame_player, bg="lightpink", width=500, height=670)
h1 = tk.Label(fr1, text="POKEMONES", font=("Arial", 13), fg="black")
h1.pack(pady=10)
h2 = tk.Label(fr1, text="Elige a tu Pokemón", font=("Arial", 10), fg="black")
h2.pack(pady=10)
fr1.pack(pady=20)

fr2 = tk.Frame(frame_player, bg="red", width=500, height=400)

pikachu = tk.Button(fr2, text="Pikachu", width=10)
pikachu.grid(row=0, column=0, padx=10, pady=10)

charmander = tk.Button(fr2, text="Charmander",width=10)
charmander.grid(row=0, column=1, padx=10, pady=10)

bulbasaur = tk.Button(fr2, text="Bulbasaur",width=10)
bulbasaur.grid(row=1, column=0, padx=10, pady=10)

otro = tk.Button(fr2, text="otro",width=10)
otro.grid(row=1, column=1, padx=10, pady=10)

if 
player_pokemon = Pokemon(, "Electric", 100, player_attacks)

fr2.pack(pady=10)

fr3 = tk.Frame(frame_player, bg="lightgreen", width=500, height=200)

img = Image.open("assets/pikachu.png")
img = img.resize((50, 50))
img_tk = ImageTk.PhotoImage(img)

h3 = tk.Label(fr3, text="Ataques", font=("Arial", 13), fg="black")
h3.grid(row=0, column=0, padx=10, pady=10)


for atk in player_pokemon.attacks:
    print(atk)
    print(atk.img)
    img = Image.open(atk.img)
    img = img.resize((50, 50))
    img_tk = ImageTk.PhotoImage(img)
    print(img_tk)
    btn = tk.Button(fr3, image=img_tk, command=lambda a=atk: player_turn(a))
    btn.grid(row=1, column=player_pokemon.attacks.index(atk), padx=10, pady=10)
   
    btn.image = img_tk  # Guarda la referencia de la imagen


fr3.pack(pady=10)

fr4 = tk.Frame(frame_player, width=500, height=100)

h4 = tk.Label(fr4, text="Puntos de Salud (PS)", font=("Arial", 13), fg="white", bg="black")
h4.grid(row=0, column=0, padx=10, pady=10)
puntos_player = tk.Label(fr4, text=f"{player_pokemon.hp}", font=("impact", 20), fg="black", bg="light sky blue",width=5, height=2)
puntos_player.grid(row=1, column=0, padx=10, pady=10)

player_label = tk.Label(fr4, text="")
player_label.grid(row=2, column=0, padx=10, pady=10)


fr4.pack(pady=10)




# Frame derecho
frame_ia = tk.Frame(root, width=500, height=670, bg="lightgreen")
frame_ia.pack(side="right", padx=0, pady=0)
frame_ia.pack_propagate(False)
h2 = tk.Label(frame_ia, text="IA-Player", font=("Arial", 24), fg="black")
h2.pack(pady=10)

status_text = tk.StringVar()

status = tk.Label(root, textvariable=status_text, wraplength=300)
status.pack(pady=10)

update_labels()

root.mainloop()
