from pokemon import Pokemon, Movimiento
from utils import calcular_daño, copiar_estado
import random
import json
from pathlib import Path
from utils import seleccionar_mejor_ataque

@dataclass
class Ataque:
    nombre: str
    poder: int
    tipo: str

@dataclass
class Pokemon:
    nombre: str
    tipo: str
    ps_max: int
    ps_actual: int
    ataques: List[Ataque]
    
    def esta_debil(self) -> bool:
        return self.ps_actual <= 0
    
    def ataques_disponibles(self) -> List[Ataque]:
        if self.esta_debil():
            return []
        return self.ataques if self.ataques else [Ataque("Tackle", 40, "Normal")]  # Ataque por defecto
    
            

@dataclass
class Entrenador:
    nombre: str
    pokemons: List[Pokemon]
    pokemon_actual_idx: int = 0
    
    def pokemon_actual(self) -> Pokemon:
        return self.pokemons[self.pokemon_actual_idx]
    
    def tiene_pokemons_disponibles(self) -> bool:
        return any(not pokemon.esta_debil() for pokemon in self.pokemons)
    
    def cambiar_pokemon(self, idx: int) -> bool:
        if 0 <= idx < len(self.pokemons) and not self.pokemons[idx].esta_debil():
            self.pokemon_actual_idx = idx
            return True
        return False
    
    def cantidad_pokemons_restantes(self) -> int:
        return sum(1 for pokemon in self.pokemons if not pokemon.esta_debil())

class BatallaPokemon:
    def __init__(self, jugador: Entrenador, oponente: Entrenador):
        self.jugador = jugador
        self.oponente = oponente
        self.turno_actual = 'jugador'
        self.historial = []
    
    def calcular_daño(self, atacante: Pokemon, defensor: Pokemon, ataque: Ataque) -> int:
        from utils import calcular_efectividad
        
        efectividad = calcular_efectividad(ataque.tipo, defensor.tipo)
        
        # STAB (Same Type Attack Bonus)
        if ataque.tipo == atacante.tipo:
            efectividad *= 1.5
            
        daño = int((ataque.poder * efectividad) * random.uniform(0.85, 1.0))
        return daño
    
    def aplicar_ataque(self, ataque: Ataque, es_oponente_atacando: bool) -> str:
        if es_oponente_atacando:
            atacante = self.oponente.pokemon_actual()
            defensor = self.jugador.pokemon_actual()
        else:
            atacante = self.jugador.pokemon_actual()
            defensor = self.oponente.pokemon_actual()
        
        daño = self.calcular_daño(atacante, defensor, ataque)
        defensor.ps_actual = max(0, defensor.ps_actual - daño)
        
        mensaje = f"{atacante.nombre} usó {ataque.nombre} e hizo {daño} de daño!"
        
        if defensor.esta_debil():
            mensaje += f"\n¡{defensor.nombre} se debilitó!"
        
        self.turno_actual = 'oponente' if self.turno_actual == 'jugador' else 'jugador'
        self.historial.append(mensaje)
        
        return mensaje
    
    def copiar(self) -> 'BatallaPokemon':
        # Crear copias manuales para evitar recursión
        jugador_copia = Entrenador(
            nombre=self.jugador.nombre,
            pokemons=[Pokemon(
                nombre=p.nombre,
                tipo=p.tipo,
                ps_max=p.ps_max,
                ps_actual=p.ps_actual,
                ataques=[Ataque(a.nombre, a.poder, a.tipo) for a in p.ataques]
            ) for p in self.jugador.pokemons],
            pokemon_actual_idx=self.jugador.pokemon_actual_idx
        )
        
        oponente_copia = Entrenador(
            nombre=self.oponente.nombre,
            pokemons=[Pokemon(
                nombre=p.nombre,
                tipo=p.tipo,
                ps_max=p.ps_max,
                ps_actual=p.ps_actual,
                ataques=[Ataque(a.nombre, a.poder, a.tipo) for a in p.ataques]
            ) for p in self.oponente.pokemons],
            pokemon_actual_idx=self.oponente.pokemon_actual_idx
        )
        
        nueva_batalla = BatallaPokemon(jugador_copia, oponente_copia)
        nueva_batalla.turno_actual = self.turno_actual
        nueva_batalla.historial = self.historial.copy()
        
        return nueva_batalla
    
    def seleccionar_ataque_ia(self) -> Ataque:
        pokemon = self.oponente.pokemon_actual()
        ataques_disponibles = pokemon.ataques_disponibles()

        if not ataques_disponibles:
            print(f"Advertencia: {pokemon.nombre} no tiene ataques disponibles")
            return Ataque("Tackle", 40, "Normal")

        return seleccionar_mejor_ataque(self, profundidad=2)
    
    def estado_actual(self) -> dict:
        return {
            'jugador': {
                'nombre': self.jugador.nombre,
                'pokemon_actual': self.jugador.pokemon_actual().nombre,
                'ps_actual': self.jugador.pokemon_actual().ps_actual,
                'ps_max': self.jugador.pokemon_actual().ps_max,
                'tipo': self.jugador.pokemon_actual().tipo,
                'ataques': [{'nombre': a.nombre, 'poder': a.poder, 'tipo': a.tipo} 
                           for a in self.jugador.pokemon_actual().ataques_disponibles()]
            },
            'oponente': {
                'nombre': self.oponente.nombre,
                'pokemon_actual': self.oponente.pokemon_actual().nombre,
                'ps_actual': self.oponente.pokemon_actual().ps_actual,
                'ps_max': self.oponente.pokemon_actual().ps_max,
                'tipo': self.oponente.pokemon_actual().tipo
            },
            'turno': self.turno_actual,
            'historial': self.historial[-3:] if len(self.historial) > 3 else self.historial
        }
    
    def es_combate_terminado(self) -> bool:
        return (not self.jugador.tiene_pokemons_disponibles() or 
                not self.oponente.tiene_pokemons_disponibles())
    
    def ganador(self) -> Optional[str]:
        if not self.jugador.tiene_pokemons_disponibles():
            return self.oponente.nombre
        if not self.oponente.tiene_pokemons_disponibles():
            return self.jugador.nombre
        return None

def cargar_pokemons_desde_json(ruta: str = 'data/pokemons.json') -> List[Pokemon]:
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo {ruta}")
    except json.JSONDecodeError:
        raise ValueError(f"Error al decodificar el archivo {ruta}")

    pokemons = []
    for poke_data in datos:
        nombre = poke_data.get('nombre', 'Desconocido')
        tipo = poke_data.get('tipo', 'Normal')
        ps_max = poke_data.get('ps_max', 50)

        # Validar que tenga ataques definidos
        if not poke_data.get('ataques'):
            print(f"Advertencia: {nombre} no tiene ataques definidos")
            continue  # O usa Tackle si prefieres

        # Crear lista de ataques con validación
        ataques_validos = []
        for ataque_data in poke_data['ataques']:
            try:
                # Verifica que todos los campos necesarios estén presentes
                if all(key in ataque_data for key in ['nombre', 'poder', 'tipo']):
                    ataques_validos.append(Ataque(**ataque_data))
                else:
                    print(f"Advertencia: Ataque inválido en {nombre}: {ataque_data}")
            except Exception as e:
                print(f"Error al procesar ataque de {nombre}: {ataque_data} - {e}")

        if not ataques_validos:
            print(f"Advertencia: {nombre} no tiene ataques válidos")
            continue  # O asigna Tackle si prefieres

        # Añadir Pokémon con sus ataques validados
        pokemons.append(Pokemon(
            nombre=nombre,
            tipo=tipo,
            ps_max=ps_max,
            ps_actual=ps_max,
            ataques=ataques_validos
        ))

    return pokemons
def crear_entrenador_aleatorio(pokemons_disponibles: List[Pokemon], nombre: str = "Entrenador IA", tamaño_equipo: int = 3) -> Entrenador:
    equipo = random.sample(pokemons_disponibles, min(tamaño_equipo, len(pokemons_disponibles)))
    return Entrenador(nombre, [copy.deepcopy(p) for p in equipo])

if __name__ == "__main__":
    from logic import cargar_pokemons_desde_json
    pokemons = cargar_pokemons_desde_json()
    
    exeggutor = next((p for p in pokemons if p.nombre == "Exeggutor"), None)
    if exeggutor:
        print("Nombre:", exeggutor.nombre)
        print("Tipo:", exeggutor.tipo)
        print("PS máximos:", exeggutor.ps_max)
        print("Ataques:")
        for ataque in exeggutor.ataques:
            print(f"- {ataque.nombre} ({ataque.tipo}, Poder: {ataque.poder})")
    else:
        print("\n💀 La IA te ha derrotado.")