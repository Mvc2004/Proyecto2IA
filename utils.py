
TYPE_EFFECTIVENESS = {
    "Fire": {"Grass": 2, "Water": 0.5, "Fire": 0.5},
    "Water": {"Fire": 2, "Grass": 0.5, "Water": 0.5},
    "Grass": {"Water": 2, "Fire": 0.5, "Grass": 0.5},
    "Electric": {"Water": 2, "Grass": 0.5, "Electric": 0.5},
}

def type_multiplier(attack_type, target_type):
    return TYPE_EFFECTIVENESS.get(attack_type, {}).get(target_type, 1.0)

def calculate_damage(attack, attacker, defender):
    multiplier = type_multiplier(attack.type, defender.type)
    return int(attack.power * multiplier)

def evaluate(game_state):
    ai_hp = game_state.ai_pokemon.hp
    player_hp = game_state.player_pokemon.hp
    return ai_hp - player_hp  # mayor es mejor para la IA

def minimax(game_state, depth, alpha, beta, maximizing):
    if depth == 0 or game_state.player_pokemon.is_fainted() or game_state.ai_pokemon.is_fainted():
        return evaluate(game_state), None

    if maximizing:
        max_eval = float('-inf')
        best_attack = None
        for attack in game_state.ai_pokemon.attacks:
            new_state = game_state.clone()
            damage = calculate_damage(attack, new_state.ai_pokemon, new_state.player_pokemon)
            new_state.player_pokemon.apply_damage(damage)
            eval_, _ = minimax(new_state, depth - 1, alpha, beta, False)
            if eval_ > max_eval:
                max_eval = eval_
                best_attack = attack
            alpha = max(alpha, eval_)
            if beta <= alpha:
                break
        return max_eval, best_attack
    else:
        min_eval = float('inf')
        for attack in game_state.player_pokemon.attacks:
            new_state = game_state.clone()
            damage = calculate_damage(attack, new_state.player_pokemon, new_state.ai_pokemon)
            new_state.ai_pokemon.apply_damage(damage)
            eval_, _ = minimax(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_)
            beta = min(beta, eval_)
            if beta <= alpha:
                break
        return min_eval, None
