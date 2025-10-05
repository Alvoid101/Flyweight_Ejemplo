import random
import matplotlib.pyplot as plt
import psutil
import os
from tqdm import tqdm  # barra de progreso

# ---- Clase Particle (sin Flyweight) ----
class Particle:
    def __init__(self, x, y, dx, dy, speed, color, sprite):
        self.coords = (x, y)
        self.vector = (dx, dy)
        self.speed = speed
        self.color = color
        self.sprite = sprite

    def move(self):
        x, y = self.coords
        dx, dy = self.vector
        self.coords = (x + dx * self.speed, y + dy * self.speed)

# ---- Clase Game ----
class Game:
    def __init__(self):
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def draw(self, n_show=10000):
        xs = [p.coords[0] for p in self.particles[:n_show]]
        ys = [p.coords[1] for p in self.particles[:n_show]]
        colors = [p.color for p in self.particles[:n_show]]
        plt.figure(figsize=(7, 7))
        plt.scatter(xs, ys, c=colors, s=2)
        plt.title(f"Partículas sin Flyweight (mostrando {n_show})")
        plt.show()

# ---- Crear Partículas ----
def main():
    N = 3_000_000  # número reducido para no colapsar la RAM
    game = Game()

    print(f"Creando {N:,} partículas sin Flyweight...")
    for _ in tqdm(range(N)):
        x, y = random.uniform(0, 100), random.uniform(0, 100)
        dx, dy = 0, 0
        speed = random.uniform(0.1, 1.0)
        color = random.choice(["red", "blue", "green", "yellow"])
        sprite = bytes(2000)  # simulamos 2 KB de sprite
        p = Particle(x, y, dx, dy, speed, color, sprite)
        game.add_particle(p)

    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    print(f"\nMemoria usada (sin Flyweight): {mem_mb:.2f} MB")

    game.draw()

if __name__ == "__main__":
    main()
