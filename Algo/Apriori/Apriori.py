from itertools import combinations
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

# здесь мы пытаемся минимизировать расстояние между товарами которые покупаются вместе
class Apriori:

    def __init__(self, min_support: int = 2, min_confidence: int = 0.5, place: set = None, data: list = None):
        self.data = data

        self.min_support = min_support
        self.min_confidence = min_confidence

        self.product_popularity = None
        self.stats = self.get_frequent_itemsets()
        self.rules = self.generate_association_rules()
        self.place = self._first_init_place(place)
        self.op_place = self.optimize_shop_place()

    def _first_init_place(self, place) -> dict:
        if len(place) < len(self.product_popularity):
            raise 'Error size place less product count'

        place = list(place)
        place.sort(key=lambda x: (x[0], x[1]))

        random_place = {}
        num = 0
        for product in self.product_popularity:
            random_place[product] = place[num]
            num += 1
        return random_place

    def get_frequent_itemsets(self) -> dict:
        stats = {}
        uniq_products = set()
        self.product_popularity = {}
        for tr in self.data:
            for pr in tr:
                uniq_products.add(frozenset([pr]))
                self.product_popularity[pr] = self.product_popularity.get(pr, 0) + 1

        products = uniq_products
        while products:
            # Подсчитываем поддержку
            counts = {}
            for tr in self.data:
                for pr in products:
                    if pr.issubset(tr):
                        counts[pr] = counts.get(pr, 0) + 1

            # Фильтруем по min_support
            products = set()
            for pr, count in counts.items():
                if count >= self.min_support:
                    stats[pr] = count
                    products.add(pr)

            # Генерируем новые комбинации
            products = set(
                [a.union(b) for a in products for b in products if len(a.union(b)) == len(a) + 1]
            )

        return stats

    def generate_association_rules(self) -> list:
        rules = []
        for pr, count in self.stats.items():
            if len(pr) > 1:
                for i in range(1, len(pr)):
                    for antecedent in combinations(pr, i):
                        antecedent = frozenset(antecedent)
                        consequent = pr - antecedent
                        if consequent:
                            confidence = count / self.stats[antecedent]
                            if confidence >= self.min_confidence:
                                rules.append((antecedent, consequent, confidence))
        return rules

    def optimize_shop_place(self) -> dict:
        item_positions = {}

        # Формируем матрицу связей между товарами
        item_graph = {item: set() for item in self.product_popularity}
        for antecedent, consequent, _ in self.rules:
            for item in antecedent:
                item_graph[item].update(consequent)
            for item in consequent:
                item_graph[item].update(antecedent)

        # Формируем список товаров по популярности
        sorted_items = sorted(self.product_popularity.keys(), key=lambda x: -self.product_popularity[x])
        shelf_positions = list(self.place.values())

        # Распределяем товары по позициям, минимизируя суммарное расстояние
        for item in sorted_items:
            if shelf_positions:
                best_position = min(shelf_positions, key=lambda pos: sum(
                    cdist([pos], [self.place[neighbor]])[0][0] for neighbor in item_graph[item] if
                    neighbor in self.place))
                item_positions[item] = best_position
                shelf_positions.remove(best_position)

        return item_positions


# def optimize_shelf_placement(rules, item_popularity, shelf_coordinates):
#     """
#     Оптимизирует расположение товаров на складе, уменьшая время сбора.
#     """
#     item_positions = {}
#
#     # Формируем матрицу связей между товарами
#     item_graph = {item: set() for item in item_popularity}
#     for antecedent, consequent, _ in rules:
#         for item in antecedent:
#             item_graph[item].update(consequent)
#         for item in consequent:
#             item_graph[item].update(antecedent)
#
#     # Формируем список товаров по популярности
#     sorted_items = sorted(item_popularity.keys(), key=lambda x: -item_popularity[x])
#     shelf_positions = list(shelf_coordinates.values())
#
#     # Распределяем товары по позициям, минимизируя суммарное расстояние
#     for item in sorted_items:
#         if shelf_positions:
#             best_position = min(shelf_positions, key=lambda pos: sum(
#                 cdist([pos], [self.place[neighbor]])[0][0] for neighbor in item_graph[item] if
#                 neighbor in shelf_coordinates))
#             item_positions[item] = best_position
#             shelf_positions.remove(best_position)
#
#     return item_positions


# Пример использования
transactions = [
    {'молоко', 'хлеб', 'масло'},
    {'хлеб', 'масло'},
    {'молоко', 'хлеб', 'масло', 'сыр'},
    {'хлеб', 'сыр'},
    {'молоко', 'хлеб', 'сыр'}
]
shelf_coordinates = {(1, 2), (2, 3), (3, 1), (4, 5)}
t = Apriori(data=transactions, place=shelf_coordinates)
print(t.optimize_shop_place())
# item_popularity = {'молоко': 10, 'хлеб': 15, 'масло': 8, 'сыр': 5}

#
# min_support = 2
# min_confidence = 0.5
#
# frequent_itemsets = get_frequent_itemsets(transactions, min_support)
# rules = generate_association_rules(frequent_itemsets, min_confidence)
# optimized_positions = optimize_shelf_placement(rules, item_popularity, shelf_coordinates)

# print("Частые наборы элементов:")
# print(frequent_itemsets)
# print("\nАссоциативные правила:")
# for rule in rules:
#     print(f"{set(rule[0])} -> {set(rule[1])} (достоверность: {rule[2]:.2f})")
# print("\nОптимизированное расположение товаров:")
# print(optimized_positions)
