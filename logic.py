

import random

class Attack:
    def __init__(self, name, type_, power):
        self.name = name
        self.type = type_
        self.power = power

class Pokemon:
    def __init__(self, name, type_, hp, attacks):
        self.name = name
        self.type = type_
        self.max_hp = hp
        self.hp = hp
        self.attacks = attacks

    def is_fainted(self):
        return self.hp <= 0

    def apply_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def reset(self):
        self.hp = self.max_hp

class GameState:
    def __init__(self, player_pokemon, ai_pokemon):
        self.player_pokemon = player_pokemon
        self.ai_pokemon = ai_pokemon

    def clone(self):
        # Crea una copia del estado actual
        cloned_player = Pokemon(
            self.player_pokemon.name,
            self.player_pokemon.type,
            self.player_pokemon.max_hp,
            self.player_pokemon.attacks
        )
        cloned_player.hp = self.player_pokemon.hp

        cloned_ai = Pokemon(
            self.ai_pokemon.name,
            self.ai_pokemon.type,
            self.ai_pokemon.max_hp,
            self.ai_pokemon.attacks
        )
        cloned_ai.hp = self.ai_pokemon.hp

        return GameState(cloned_player, cloned_ai)
