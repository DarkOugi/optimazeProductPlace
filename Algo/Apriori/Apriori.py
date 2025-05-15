'''
    Класс реализации алгоритма Apriori для поиска товаров часто покупаемых вместе
    Мы не будем рассматривать:
        1 - группироваку по пользователям
        2 - группироваку по времени
    Так как мы берем данные за определенный промежуток для анализа + нам важно расположить часто покупаемые товары рядом
    Даже если покупки идут от 1 пользователя
'''

class Apriori:
    def __init__(self, threshold : 2):
        self.threshold = threshold
        self.data = {}
    def Train(self, data):
        products = set()
        product_info = {}
        for transaction in data:
            for product in transaction:
                products.add(frozenset([product]))

        current_products = products
        while current_products:
            counts = {}

            # Подсчитываем поддержку
            for transaction in data:
                for product in current_products:
                    if product.issubset(transaction):
                        counts[product] = counts.get(product, 0) + 1

            # Фильтруем по min_support
            current_products = set()
            for product, count in counts.items():
                if count >= self.threshold:
                    product_info[product] = count
                    current_products.add(product)

            # Генерируем новые комбинации
            current_products = set(
                [a.union(b) for a in current_products for b in current_products if len(a.union(b)) == len(a) + 1]
            )

        self.data = product_info
        # products = {}
        # size = 0
        # for transaction in data:
        #     for product in transaction:
        #         if product in products:
        #             products[product] +=1
        #         else:
        #             products[product] = 1
        #         size+=1

    def get_info(self):
        return self.data
    @staticmethod
    def support(product, products):
        return product / products

