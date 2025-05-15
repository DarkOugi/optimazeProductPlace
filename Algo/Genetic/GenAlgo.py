import random
import numpy as np

# Все товары и их координаты
product_coords = {
    "milk": (2, 3),
    "bread": (5, 4),
    "eggs": (1, 1),
    "cheese": (6, 2),
    "apples": (3, 6),
    "fish": (7, 5),
    "coffee": (4, 1),
}

# Частота покупок по истории (на основе анализа данных)
purchase_prob = {
    "milk": 0.8,
    "bread": 0.7,
    "eggs": 0.6,
    "cheese": 0.5,
    "apples": 0.4,
    "fish": 0.2,
    "coffee": 0.3
}

start_point = (0, 0)

# Генерация случайного списка покупок с учетом вероятностей
def generate_shopping_list():
    return [item for item in product_coords if random.random() < purchase_prob[item]]

# Вычисление расстояния
def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Фитнес-функция
def fitness(route, coords):
    if not route:
        return float('inf')
    dist = distance(start_point, coords[route[0]])
    for i in range(len(route) - 1):
        dist += distance(coords[route[i]], coords[route[i + 1]])
    dist += distance(coords[route[-1]], start_point)
    return dist

# Создание популяции
def create_population(size, items):
    return [random.sample(items, len(items)) for _ in range(size)]

def crossover(p1, p2):
    cut = random.randint(1, len(p1) - 2)
    child = p1[:cut] + [item for item in p2 if item not in p1[:cut]]
    return child

def mutate(route, mutation_rate=0.1):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

# Генетический алгоритм
def genetic_algorithm(generations=100, population_size=50):
    shopping_list = generate_shopping_list()
    if not shopping_list:
        return [], 0.0  # ничего не покупает

    population = create_population(population_size, shopping_list)

    for gen in range(generations):
        population = sorted(population, key=lambda r: fitness(r, product_coords))
        next_gen = population[:10]

        while len(next_gen) < population_size:
            p1, p2 = random.sample(population[:20], 2)
            child = crossover(p1, p2)
            child = mutate(child)
            next_gen.append(child)

        population = next_gen

    best = min(population, key=lambda r: fitness(r, product_coords))
    return best, fitness(best, product_coords)

# Запуск
best_route, total_distance = genetic_algorithm()
print("Список покупок:", best_route)
print("Оптимальный маршрут длиной:", round(total_distance, 2))