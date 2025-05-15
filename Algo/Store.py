store = {
    (1, 1),
    (2, 5),
    (4, 4),
    (6, 1),
    (3, 2),
    (5, 5),
}

class Store:  # set tuples
    def __init__(self):
        self.store = {}
        # self.store = store

    def create_base_store(self):
        self.store = store

    def get_store(self):

        return self.store

    def set_store(self, new_store):

        self.store = new_store

    def add_place(self, new_place):

        self.store.add(new_place)

    def add_places(self, new_places):

        for place in new_places:
            self.add_place(place)

    def del_place(self, d_place):

        if d_place in self.store:
            self.store.remove(d_place)
        else:
            print(f"{d_place} not in store")

    def del_places(self, d_places):

        for place in d_places:
            self.del_place(place)

s = Store()
s.create_base_store()
print(s.get_store())
