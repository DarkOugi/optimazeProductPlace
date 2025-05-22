import random
import numpy as np

start_point = (0, 0)

class Gen:
    def __init__(self, data: list = None, place: set = None, generations: int = 100, population_size: int = 50,
                 mutation_rate: float = 0.1):
        self.data = data
        self.mutation_rate = mutation_rate

        self.generations = generations
        self.population_size = population_size
        self.products = self.get_products()
        self.place = place

    def genetic_algorithm(self):
        population = self.create_population()

        for _ in range(self.generations):
            population = sorted(population, key=self.fitness)
            next_gen = population[:10]  # элита

            while len(next_gen) < self.population_size:
                p1, p2 = random.sample(population[:20], 2)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                next_gen.append(child)

            population = next_gen

        best = min(population, key=self.fitness)
        return self.new_place(best), self.fitness(best)

    def new_place(self,best_placement):
        final_mapping = {product: loc for product, loc in zip(best_placement, self.place)}
        return final_mapping
    def create_population(self):
        return [random.sample(self.products, len(self.products)) for _ in range(self.population_size)]

    #
    def route_distance(self, purchase, placement):
        # получаем координаты товаров из покупки
        coords = [placement[item] for item in purchase]
        dist = self.distance(start_point, coords[0])
        for i in range(len(coords) - 1):
            dist += self.distance(coords[i], coords[i + 1])
        dist += self.distance(coords[-1], start_point)
        return dist

    # Фитнес-функция: средняя длина маршрута по всем покупкам
    def fitness(self, gene):  # gene = размещение товаров по точкам
        placement = {product: loc for product, loc in zip(gene, self.place)}
        total = 0
        for purchase in self.data:
            total += self.route_distance(purchase, placement)
        return total / len(self.data)

    def mutate(self, gene):
        for i in range(len(gene)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(gene) - 1)
                gene[i], gene[j] = gene[j], gene[i]
        return gene

    #
    def get_products(self):
        product = set()
        for tr in self.data:
            for pr in tr:
                product.add(pr)

        return list(product)
    @staticmethod
    def distance(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    @staticmethod
    def crossover(p1, p2):
        cut = random.randint(1, len(p1) - 2)
        child = p1[:cut] + [item for item in p2 if item not in p1[:cut]]
        return child


locations = [(1,1), (2,5), (4,4), (6,1), (3,2), (5,5)]

# История покупок — наборы покупок пользователей
purchase_history = [
    ["milk", "bread", "eggs"],
    ["cheese", "apples"],
    ["bread", "milk"],
    ["eggs", "fish"],
    ["fish", "cheese", "milk"]
]
# Запуск
algo = Gen(data = purchase_history, place=locations)
best_route, total_distance = algo.genetic_algorithm()
print("Список покупок:", best_route)
print("Оптимальный маршрут длиной:", round(total_distance, 2))
