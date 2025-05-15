import random
import numpy as np

# Допустим, 6 товаров и 6 точек
products = ["milk", "bread", "eggs", "cheese", "apples", "fish"]

# Фиксированные координаты ячеек в магазине
locations = [(1,1), (2,5), (4,4), (6,1), (3,2), (5,5)]

# История покупок — наборы покупок пользователей
purchase_history = [
    ["milk", "bread", "eggs"],
    ["cheese", "apples"],
    ["bread", "milk"],
    ["eggs", "fish"],
    ["fish", "cheese", "milk"]
]

start_point = (0, 0)

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Вычисление маршрута по одной покупке
def route_distance(purchase, placement):
    # получаем координаты товаров из покупки
    coords = [placement[item] for item in purchase]
    dist = distance(start_point, coords[0])
    for i in range(len(coords) - 1):
        dist += distance(coords[i], coords[i+1])
    dist += distance(coords[-1], start_point)
    return dist

# Фитнес-функция: средняя длина маршрута по всем покупкам
def fitness(gene):  # gene = размещение товаров по точкам
    placement = {product: loc for product, loc in zip(gene, locations)}
    total = 0
    for purchase in purchase_history:
        total += route_distance(purchase, placement)
    return total / len(purchase_history)

# Генерация начальной популяции
def create_population(size):
    return [random.sample(products, len(products)) for _ in range(size)]

def crossover(p1, p2):
    cut = random.randint(1, len(p1)-2)
    child = p1[:cut] + [x for x in p2 if x not in p1[:cut]]
    return child

def mutate(gene, rate=0.1):
    for i in range(len(gene)):
        if random.random() < rate:
            j = random.randint(0, len(gene)-1)
            gene[i], gene[j] = gene[j], gene[i]
    return gene

# Генетический алгоритм
def genetic_algorithm(generations=100, pop_size=50):
    population = create_population(pop_size)

    for _ in range(generations):
        population = sorted(population, key=fitness)
        next_gen = population[:10]  # элита

        while len(next_gen) < pop_size:
            p1, p2 = random.sample(population[:20], 2)
            child = crossover(p1, p2)
            child = mutate(child)
            next_gen.append(child)

        population = next_gen

    best = min(population, key=fitness)
    return best, fitness(best)

# Запуск
best_placement, best_score = genetic_algorithm()
final_mapping = {product: loc for product, loc in zip(best_placement, locations)}

print("Лучшее размещение товаров:")
for k, v in final_mapping.items():
    print(f"{k:>8} → {v}")
print("Средняя длина маршрута:", round(best_score, 2))