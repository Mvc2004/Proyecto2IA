from utils import calcular_daño, copiar_estado
 
TAB = "   "

def aplicar_daño(atacante, defensor, movimiento):
    daño = calcular_daño(movimiento.tipo, defensor.tipo, movimiento.poder)
    defensor.ps -= daño
   
    if not defensor.esta_vivo():
        print(f"{defensor.nombre} ha sido debilitado!")


def funcion_evaluacion(estado):
    
    ia = estado['ia']
    jugador = estado['jugador']

    vida_ia = ia.ps
    vida_jugador = jugador.ps

    daño_potencial_ia = sum(calcular_daño(m.tipo, jugador.tipo, m.poder) for m in ia.movimientos) / len(ia.movimientos)
    daño_potencial_jugador = sum(calcular_daño(m.tipo, ia.tipo, m.poder) for m in jugador.movimientos) / len(jugador.movimientos)

    return (vida_ia - vida_jugador) + (daño_potencial_ia - daño_potencial_jugador)


def minimax_con_poda(estado, profundidad, alpha, beta, es_max_turno):
    if profundidad == 0 or not estado['jugador'].esta_vivo() or not estado['ia'].esta_vivo():
        return funcion_evaluacion(estado), None

    mejor_movimiento = None

    if es_max_turno:
        max_eval = float('-inf')
        for movimiento in estado['ia'].movimientos:
            estado_copia = copiar_estado(estado)
            aplicar_daño_simulado(estado_copia['ia'], estado_copia['jugador'], movimiento)
            evaluacion, _ = minimax_con_poda(estado_copia, profundidad - 1, alpha, beta, False)
            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = movimiento
            alpha = max(alpha, evaluacion)
            if beta <= alpha:
                break
        return max_eval, mejor_movimiento
    else:
        min_eval = float('inf')
        for movimiento in estado['jugador'].movimientos:
            estado_copia = copiar_estado(estado)
            aplicar_daño_simulado(estado_copia['jugador'], estado_copia['ia'], movimiento)
            evaluacion, _ = minimax_con_poda(estado_copia, profundidad - 1, alpha, beta, True)
            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = movimiento
            beta = min(beta, evaluacion)
            if beta <= alpha:
                break
        return min_eval, mejor_movimiento


def aplicar_daño_simulado(atacante, defensor, movimiento):
    daño = calcular_daño(movimiento.tipo, defensor.tipo, movimiento.poder)
    defensor.ps -= daño

