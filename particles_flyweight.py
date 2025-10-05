import random
import matplotlib.pyplot as plt
import psutil
import os
from tqdm import tqdm

# Este es mi Flyweight Representa el estado compartido o intrinseco de color y sprite.
class ParticleType:
    def __init__(self, color, sprite):
        self.color = color
        self.sprite = sprite

# Flyweight Factory
class ParticleFactory:
    _types = {}

    @classmethod
    def get_type(cls, color):
        if color not in cls._types:
            # Crear solo un sprite por color
            sprite = bytes(2000)  # 2 KB, compartido
            cls._types[color] = ParticleType(color, sprite)
        return cls._types[color]

# Clase extrinseca
class Particle:
    def __init__(self, x, y, dx, dy, speed, particle_type):
        self.coords = (x, y)
        self.vector = (dx, dy)
        self.speed = speed
        self.type = particle_type  # Flyweight compartido

    def move(self):
        x, y = self.coords
        dx, dy = self.vector
        self.coords = (x + dx * self.speed, y + dy * self.speed)

# Clase Game
class Game:
    def __init__(self):
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def draw(self, n_show=10000):
        xs = [p.coords[0] for p in self.particles[:n_show]]
        ys = [p.coords[1] for p in self.particles[:n_show]]
        colors = [p.type.color for p in self.particles[:n_show]]
        plt.figure(figsize=(7, 7))
        plt.scatter(xs, ys, c=colors, s=2)
        plt.title(f"Partículas con Flyweight (mostrando {n_show})")
        plt.show()

# Crear Partículas
def main():
    N = 3_000_000 
    game = Game()

    print(f"Creando {N:,} partículas con Flyweight...")
    for _ in tqdm(range(N)):
        x, y = random.uniform(0, 100), random.uniform(0, 100)
        dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
        speed = random.uniform(0.1, 1.0)
        color = random.choice(["red", "blue", "green", "yellow"])
        particle_type = ParticleFactory.get_type(color)
        p = Particle(x, y, dx, dy, speed, particle_type)
        game.add_particle(p)

    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    print(f"\nMemoria usada (con Flyweight): {mem_mb:.2f} MB")

    game.draw()

if __name__ == "__main__":
    main()
