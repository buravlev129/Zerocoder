

class Store:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price

    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]

    def get_price(self, item_name):
        return self.items.get(item_name)

    def update_price(self, item_name, new_price):
        if item_name in self.items:
            self.items[item_name] = new_price

    def __str__(self):
        items_list = ", ".join(f"{item}: {price}" for item, price in self.items.items())
        return f"Магазин: {self.name}, Адрес: {self.address}, Товары: {items_list}"



if __name__ == "__main__":

    store1 = Store("Магазин №1", "Улица Кукушкина, 1")
    store1.add_item("Яблоки", 0.5)
    store1.add_item("Бананы", 0.75)

    store2 = Store("Магазин №2", "Улица Пушкина, 2")
    store2.add_item("Молоко", 1.2)
    store2.add_item("Хлеб", 0.8)

    store3 = Store("Магазин №3", "Улица Пушкина, 3")
    store3.add_item("Кофе", 3.0)
    store3.add_item("Чай", 2.5)

    stores = [store1, store2, store3]

    print("\nМагазины:")
    for store in stores:
        print(store)


    print("")
    print("Яблоки Цена: ", store1.get_price("Яблоки"))
    print("Огурцы Цена: ", store1.get_price("Огурцы"))

    assert store1.get_price("Яблоки") == 0.5
    assert store1.get_price("Огурцы") is None

    store1.update_price("Яблоки", 1.2)
    print("Яблоки Цена: ", store1.get_price("Яблоки"))
    assert store1.get_price("Яблоки") == 1.2

    store1.remove_item("Яблоки")
    print("Яблоки Цена: ", store1.get_price("Яблоки"))
    assert store1.get_price("Яблоки") is None

