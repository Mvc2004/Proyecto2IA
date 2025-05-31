import os
from PIL import Image, ImageDraw, ImageFont
import json

# Constants
POKEMON_IMG_SIZE = (120, 120)
MOVE_IMG_SIZE = (30, 30)
ASSETS_DIR = "assets"
POKEMON_DIR = os.path.join(ASSETS_DIR, "pokemon")
TYPES_DIR = os.path.join(ASSETS_DIR, "types")

# Create directories if they don't exist
for directory in [ASSETS_DIR, POKEMON_DIR, TYPES_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_pokemon_placeholder(name, type_color, output_path):
    """Create a placeholder image for a Pokémon"""
    img = Image.new('RGBA', POKEMON_IMG_SIZE, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a circle with the type color
    circle_x, circle_y = POKEMON_IMG_SIZE[0] // 2, POKEMON_IMG_SIZE[1] // 2
    circle_radius = min(POKEMON_IMG_SIZE) // 2 - 5
    draw.ellipse(
        (circle_x - circle_radius, circle_y - circle_radius, 
         circle_x + circle_radius, circle_y + circle_radius), 
        fill=type_color
    )
    
    # Try to add text (first letter of name)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    letter = name[0].upper() if name else "?"
    text_width, text_height = draw.textsize(letter, font=font)
    draw.text(
        (circle_x - text_width // 2, circle_y - text_height // 2),
        letter,
        fill="white",
        font=font
    )
    
    img.save(output_path)
    print(f"Created placeholder for {name} at {output_path}")

def create_type_icon(type_name, color, output_path):
    """Create an icon for a Pokémon type"""
    img = Image.new('RGBA', MOVE_IMG_SIZE, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle with the type color
    draw.rectangle(
        (0, 0, MOVE_IMG_SIZE[0], MOVE_IMG_SIZE[1]),
        fill=color,
        outline="white",
        width=1,
        radius=5
    )
    
    # Try to add text (first letter of type)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()
    
    letter = type_name[0].upper() if type_name else "?"
    text_width, text_height = draw.textsize(letter, font=font)
    draw.text(
        (MOVE_IMG_SIZE[0] // 2 - text_width // 2, MOVE_IMG_SIZE[1] // 2 - text_height // 2),
        letter,
        fill="white",
        font=font
    )
    
    img.save(output_path)
    print(f"Created type icon for {type_name} at {output_path}")

def create_background_images():
    """Create background images for selection and battle screens"""
    # Selection background
    selection_bg = Image.new('RGB', (800, 600), color="#a8d5ba")
    draw = ImageDraw.Draw(selection_bg)
    
    # Add some decorative elements
    for i in range(0, 800, 50):
        for j in range(0, 600, 50):
            if (i + j) % 100 == 0:
                draw.ellipse((i, j, i+10, j+10), fill="#8bc5a8")
    
    selection_bg.save(os.path.join(ASSETS_DIR, "selection_bg.png"))
    print("Created selection background")
    
    # Battle background
    battle_bg = Image.new('RGB', (800, 600), color="#c8e6c9")
    draw = ImageDraw.Draw(battle_bg)
    
    # Draw a simple battlefield
    draw.rectangle((100, 150, 700, 450), fill="#a5d6a7", outline="#2e7d32", width=2)
    
    # Add some decorative elements
    for i in range(150, 450, 50):
        draw.line((100, i, 700, i), fill="#81c784", width=1)
    
    for i in range(100, 700, 50):
        draw.line((i, 150, i, 450), fill="#81c784", width=1)
    
    battle_bg.save(os.path.join(ASSETS_DIR, "battle_bg.png"))
    print("Created battle background")

def create_default_pokemon():
    """Create a default Pokémon image"""
    create_pokemon_placeholder("Default", "#888888", os.path.join(POKEMON_DIR, "default.png"))

def create_type_icons():
    """Create icons for all Pokémon types"""
    type_colors = {
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
    
    for type_name, color in type_colors.items():
        create_type_icon(type_name, color, os.path.join(TYPES_DIR, f"{type_name}.png"))

def create_pokemon_images_from_json(json_path="pokemons.json"):
    """Create placeholder images for all Pokémon in the JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        type_colors = {
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
        
        for pokemon in data:
            name = pokemon.get("nombre", "").lower()
            tipo = pokemon.get("tipo", "normal").lower()
            color = type_colors.get(tipo, "#888888")
            
            if name:
                create_pokemon_placeholder(name, color, os.path.join(POKEMON_DIR, f"{name}.png"))
    
    except Exception as e:
        print(f"Error creating Pokémon images from JSON: {e}")

if __name__ == "__main__":
    print("Setting up assets for Pokémon Battle Game...")
    
    # Create background images
    create_background_images()
    
    # Create default Pokémon image
    create_default_pokemon()
    
    # Create type icons
    create_type_icons()
    
    # Create Pokémon images from JSON if available
    if os.path.exists("pokemons.json"):
        create_pokemon_images_from_json()
    else:
        print("pokemons.json not found. Run this script again after creating the JSON file to generate Pokémon images.")
    
    print("Asset setup complete!")
