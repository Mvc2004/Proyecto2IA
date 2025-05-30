import random
from typing import List, Any, Optional

# Tabla de tipos simplificada (primera generación)
TABLA_TIPOS = {
    'Normal': {'debil': ['Roca'], 'resistente': [], 'inmune': ['Fantasma']},
    'Fuego': {'debil': ['Agua', 'Roca'], 'resistente': ['Fuego', 'Planta']},
    'Agua': {'debil': ['Eléctrico', 'Planta'], 'resistente': ['Fuego', 'Agua']},
    'Eléctrico': {'debil': ['Tierra'], 'resistente': ['Eléctrico']},
    'Planta': {'debil': ['Fuego', 'Hielo'], 'resistente': ['Agua', 'Eléctrico', 'Planta']},
    'Hielo': {'debil': ['Fuego'], 'resistente': ['Hielo']},
    'Lucha': {'debil': ['Psíquico'], 'resistente': ['Roca']},
    'Veneno': {'debil': ['Tierra', 'Psíquico'], 'resistente': ['Planta']},
    'Tierra': {'debil': ['Agua', 'Planta'], 'resistente': ['Veneno'], 'inmune': ['Eléctrico']},
    'Volador': {'debil': ['Eléctrico', 'Roca'], 'resistente': ['Planta'], 'inmune': ['Tierra']},
    'Psíquico': {'debil': [], 'resistente': ['Psíquico'], 'inmune': ['Fantasma']},
    'Bicho': {'debil': ['Fuego', 'Volador'], 'resistente': ['Planta']},
    'Roca': {'debil': ['Agua', 'Planta'], 'resistente': ['Normal', 'Fuego']},
    'Fantasma': {'debil': [], 'resistente': [], 'inmune': ['Normal', 'Psíquico']},
    'Dragón': {'debil': ['Dragón'], 'resistente': ['Fuego', 'Agua', 'Eléctrico', 'Planta']}
}

def calcular_efectividad(tipo_ataque: str, tipo_defensor: str) -> float:
    efectividad = 1.0

    if tipo_defensor in TABLA_TIPOS:
        defensa = TABLA_TIPOS[tipo_defensor]

        if tipo_ataque in defensa['debil']:
            efectividad *= 2
        if tipo_ataque in defensa['resistente']:
            efectividad *= 0.5
        if 'inmune' in defensa and tipo_ataque in defensa['inmune']:
            efectividad *= 0

    return efectividad


def minimax(estado: Any, profundidad: int, alfa: float = float('-inf'), beta: float = float('inf'), es_maximizando: bool = True) -> float:
    if profundidad == 0 or estado.es_combate_terminado():
        return evaluar_estado(estado)

    if es_maximizando:
        max_eval = float('-inf')
        for ataque in estado.oponente.pokemon_actual().ataques_disponibles():
            nuevo_estado = estado.copiar()
            nuevo_estado.aplicar_ataque(ataque, es_oponente_atacando=True)
            eval = minimax(nuevo_estado, profundidad - 1, alfa, beta, False)
            max_eval = max(max_eval, eval)
            alfa = max(alfa, eval)
            if beta <= alfa:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for ataque in estado.jugador.pokemon_actual().ataques_disponibles():
            nuevo_estado = estado.copiar()
            nuevo_estado.aplicar_ataque(ataque, es_oponente_atacando=False)
            eval = minimax(nuevo_estado, profundidad - 1, alfa, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alfa:
                break
        return min_eval


def evaluar_estado(estado: Any) -> float:
    if estado.es_combate_terminado():
        ganador = estado.ganador()
        if ganador == estado.oponente.nombre:
            return float('-inf')  # IA pierde
        else:
            return float('inf')   # IA gana

    pokemon_jugador = estado.jugador.pokemon_actual()
    pokemon_oponente = estado.oponente.pokemon_actual()

    salud_jugador = pokemon_jugador.ps_actual / pokemon_jugador.ps_max
    salud_oponente = pokemon_oponente.ps_actual / pokemon_oponente.ps_max
    factor_salud = 0.5 * (salud_oponente - salud_jugador)

    pokemons_jugador = estado.jugador.cantidad_pokemons_restantes()
    pokemons_oponente = estado.oponente.cantidad_pokemons_restantes()
    factor_numero = 0.3 * (pokemons_oponente - pokemons_jugador)

    ataques_oponente = pokemon_oponente.ataques_disponibles()
    ataques_jugador = pokemon_jugador.ataques_disponibles()

    max_daño_ia = max(
        (calcular_efectividad(ataque.tipo, pokemon_jugador.tipo) * ataque.poder 
         for ataque in ataques_oponente),
        default=0
    )

    max_daño_jugador = max(
        (calcular_efectividad(ataque.tipo, pokemon_oponente.tipo) * ataque.poder 
         for ataque in ataques_jugador),
        default=0
    )

    ventaja_tipo = 0
    if max_daño_ia + max_daño_jugador > 0:
        ventaja_tipo = 0.2 * (max_daño_ia - max_daño_jugador) / (max_daño_ia + max_daño_jugador)

    return factor_salud + factor_numero + ventaja_tipo


def seleccionar_mejor_ataque(estado: Any, profundidad: int) -> Any:
    mejor_ataque = None
    max_eval = float('-inf')
    alfa = float('-inf')
    beta = float('inf')

    for ataque in estado.oponente.pokemon_actual().ataques_disponibles():
        nuevo_estado = estado.copiar()
        nuevo_estado.aplicar_ataque(ataque, es_oponente_atacando=True)
        eval = minimax(nuevo_estado, profundidad - 1, alfa, beta, False)

        if eval > max_eval:
            max_eval = eval
            mejor_ataque = ataque

        alfa = max(alfa, eval)
        if beta <= alfa:
            break  # Poda beta

    return mejor_ataque