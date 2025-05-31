from utils import calcular_daño, copiar_estado
 
TAB = "   "

def aplicar_daño(atacante, defensor, movimiento):
    daño = calcular_daño(movimiento.tipo, defensor.tipo, movimiento.poder)
    print(movimiento.tipo," ", defensor.tipo," ", movimiento.poder)
    defensor.ps -= daño
    print(f"\n{TAB}{atacante.nombre} usó {movimiento.nombre}")
    print(f"Daño infligido: {daño:.1f}")
    print(defensor.ps)
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


"""def iniciar_combate(pkm_jugador, pkm_ia):
    print("ENTRAAAAAA")
    print("⚔️ ¡Comienza el combate!")
    print(f"{pkm_jugador.nombre} (Jugador) vs {pkm_ia.nombre} (IA)\n")

    while pkm_jugador.esta_vivo() and pkm_ia.esta_vivo():
        print("\n--- Tu turno ---")
        print(f"{pkm_jugador.nombre}: {pkm_jugador.ps:.1f} PS")
        print(f"{pkm_ia.nombre}: {pkm_ia.ps:.1f} PS")

        print("\nTus movimientos:")
        for idx, movimiento in enumerate(pkm_jugador.movimientos):
            print(f"{idx + 1}. {movimiento.nombre} ({movimiento.tipo}, {movimiento.poder} daño)")

        try:
            eleccion = int(input("Selecciona un ataque (1-4): ")) - 1
            ataque_jugador = pkm_jugador.movimientos[eleccion]
            aplicar_daño(pkm_jugador, pkm_ia, ataque_jugador)

            if not pkm_ia.esta_vivo():
                break

            print("\n--- Turno de la IA ---")
            _, mejor_ataque = minimax_con_poda(
                {'jugador': pkm_jugador, 'ia': pkm_ia}, 
                profundidad=3, alpha=float('-inf'), beta=float('inf'),
                es_max_turno=True
            )
            aplicar_daño(pkm_ia, pkm_jugador, mejor_ataque)

        except (ValueError, IndexError):
            print("Selección inválida.")

    if pkm_jugador.esta_vivo():
        print("\n🎉 ¡Has ganado el combate!")
    else:
        print("\n💀 La IA te ha derrotado.")"""