import json
import os
from pokemon import Movimiento, Pokemon

EFECTIVIDAD = {
    'agua':     {'agua': 0.5, 'planta': 0.5, 'fuego': 2.0, 'dragon': 0.5, 'roca': 2.0, 'Tierra': 0.5},
    'fuego':    {'bicho': 2.0, 'planta': 2.0, 'agua': 0.5, 'fuego': 0.5, 'hielo':2.0, 'acero': 2.0, 'roca': 0.5, 'dragón': 0.5},
    'planta':   {'agua': 2.0, 'tierra': 2.0, 'roca': 2.0, 'fuego': 0.5, 'planta': 0.5, 'veneno': 0.5, 'volador': 0.5, 'bicho': 0.5, 'dragón': 0.5, 'acero': 0.5},
    'electrico':{'agua': 2.0, 'electrico': 0.5, 'tierra': 0.0, 'planta': 0.5, 'volador': 2.0, 'dragón': 0.5},
    'normal':   {'roca': 0.5, 'acero': 0.5, 'fantasma': 0.0},
    'bicho':    {'planta': 2.0, 'psíquico': 2.0, 'siniestro': 2.0, 'fuego': 0.5, 'volador': 0.5, 'lucha': 0.5, 'veneno': 0.5, 'hada': 0.5, 'fantasma': 0.5 , 'acero': 0.5},
    'lucha':    {'normal': 2.0, 'hielo': 2.0, 'roca': 2.0, 'siniestro': 2.0, 'acero': 2.0, 'veneno': 0.5, 'volador': 0.5, 'psíquico': 0.5, 'bicho': 0.5, 'hada': 0.5, 'fantasma': 0.0},
    'volador':  {'eléctrico': 0.5, 'roca': 0.5, 'planta': 2.0, 'lucha': 2.0, 'bicho': 2.0, 'acero': 0.5},
    'veneno':   {'planta': 2.0, 'hada': 2.0, 'veneno': 0.5, 'tierra': 0.5, 'roca': 0.5, 'fantasma': 0.5, 'acero': 0.0},
    'tierra':   {'fuego': 2.0, 'eléctrico': 2.0, 'veneno': 2.0, 'roca': 2.0, 'acero': 2.0, 'planta': 0.5, 'bicho': 0.5, 'volador': 0.0},
    'fantasma': {'normal': 0.0, 'psíquico': 2.0, 'fantasma': 2.0, 'siniestro': 0.5},
    'siniestro':{'psíquico': 2.0, 'siniestro': 0.5, 'lucha': 0.5, 'hada': 0.5, 'fantasma': 2.0},
    'psíquico': {'lucha': 2.0, 'veneno': 2.0, 'siniestro': 0.0, 'psíquico': 0.5, 'acero': 0.5},
    'dragón':   {'dragón': 2.0, 'acero': 0.5, 'hada': 0.0},
    'hielo':    {'dragón': 2.0, 'planta': 2.0, 'agua': 0.5, 'fuego': 0.5, 'volador': 2.0, 'tierra': 2.0, 'hielo': 0.5, 'acero': 0.5},
    'acero':    {'roca': 2.0, 'hielo': 2.0, 'volador': 2.0, 'agua': 0.5, 'planta': 0.5, 'fuego': 0.5, 'acero': 0.5, 'lucha': 0.5, 'psíquico': 0.5},
    'roca':     {'fuego': 2.0, 'hielo': 2.0, 'volador': 2.0, 'bicho': 2.0, 'lucha': 0.5, 'tierra': 0.5, 'acero': 0.5},
    'hada':     {'dragón': 2.0, 'lucha': 2.0, 'siniestro': 2.0, 'veneno': 0.5, 'acero': 0.5, 'fuego': 0.5}
}

def calcular_daño(tipo_ataque, tipo_defensa, poder):
    
    efectividad = EFECTIVIDAD.get(tipo_ataque.lower(), {}).get(tipo_defensa.lower(), 1)
    
    return poder * efectividad

 
def copiar_pokemon(pkm):
    return Pokemon(
        pkm.nombre,
        pkm.tipo,
        pkm.ps,
        [Movimiento(mov.nombre, mov.tipo, mov.poder) for mov in pkm.movimientos]
    )

 
def copiar_estado(estado):
    return {
        'jugador': copiar_pokemon(estado['jugador']),
        'ia': copiar_pokemon(estado['ia'])
    }

 
def cargar_pokemons_desde_json(ruta_archivo='data/pokemons.json'):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        pokemons = []
        for item in datos:
            ataques = [
                Movimiento(ataque['nombre'], ataque['tipo'], ataque['poder'])
                for ataque in item['ataques']
            ]
            pokemons.append(Pokemon(item['nombre'], item['tipo'], item['ps_max'], ataques))
        return pokemons
    except FileNotFoundError:
        print("Archivo JSON no encontrado.")
        return []