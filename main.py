import re


class Product:
    # Класс Блюда из Меню
    def __init__(self, name_raw, price_raw):
        self.name = name_raw
        self.price = float(price_raw)
        self.status = True

    def change_status(self):
        self.status = not self.status
        return self.status

    def update_price(self, new_price):
        self.price = float(new_price)

    def update_name(self, new_name):
        self.name = new_name

    def __str__(self):
        return f"{self.name} - {self.price}₽ ({'доступен' if self.status else 'не доступен'})"


class Restaurant:
    # класс Ресторана
    phone_pattern = r'^(8\d{10}|\+7\d{10}|\d{10})$'

    def __init__(self, name_raw, phone_raw, address_raw):
        self.name = name_raw
        self.phone = self.phone_check(phone_raw)
        self.address = address_raw
        self.menu = []

    def phone_check(self, phone_raw):
        if re.fullmatch(self.phone_pattern, phone_raw):
            return phone_raw
        else:
            raise ValueError("Некорректный номер телефона")

    def add_product(self, product: Product):
        if isinstance(product, Product):
            self.menu.append(product)
        else:
            raise ValueError("Попытка добавить в меню что-то стороннее")

    def show_menu(self):
        if not self.menu:
            print("Меню пустое")
            return False
        else:
            print(f"Меню ресторана '{self.name}':")
            for i, product in enumerate(self.menu, 1):
                print(f"{i}. {product}")
            return True

    def update_info(self, new_name=None, new_phone=None, new_address=None):
        if new_name:
            self.name = new_name
        if new_phone:
            self.phone = self.phone_check(new_phone)
        if new_address:
            self.address = new_address

    def __str__(self):
        return f"Ресторан: {self.name}\nАдрес: {self.address}\nТелефон: {self.phone}"

# Добавление нового ресторана
def create_restaurant():
    name_raw = input("Название ресторана: ")
    address_raw = input("Адрес: ")
    while True:
        phone_raw = input("Номер телефона (форматы: 8ХХХХХХХХХХ, +7ХХХХХХХХХХ): ")
        try:
            restaurant = Restaurant(name_raw, phone_raw, address_raw)
            return restaurant
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте еще раз.")

#Добавление блюда в меню ресторана
def create_product():
    name = input("Введите название блюда: ")
    while True:
        price = input("Введите цену блюда: ")
        try:
            return Product(name, float(price))
        except ValueError:
            print("Цена должна быть числом. Попробуйте еще раз.")

#выбор ресторана из списка
def select_restaurant(restaurants, prompt="Выберите ресторан: "):
    if not restaurants:
        print("Нет доступных ресторанов")
        return None

    print("\nСписок ресторанов:")
    for i, r in enumerate(restaurants, 1):
        print(f"{i}. {r.name} - {r.address}")

    try:
        choice = int(input(prompt)) - 1
        if 0 <= choice < len(restaurants):
            return restaurants[choice]
        else:
            print("Неверный номер ресторана")
            return None
    except ValueError:
        print("Введите число!")
        return None

#вывод всех ресторанов
def show_all_restaurants(restaurants):
    if not restaurants:
        print("Нет доступных ресторанов")
    else:
        print("\nСписок ресторанов:")
        for i, restaurant in enumerate(restaurants, 1):
            print(f"{i}. {restaurant.name} - {restaurant.address}")

#вывод информации о ресторане
def show_restaurant_details(restaurants):
    if not restaurants:
        print("Нет доступных ресторанов")
        return

    show_all_restaurants(restaurants)
    try:
        choice = int(input("Введите номер ресторана для просмотра: ")) - 1
        if 0 <= choice < len(restaurants):
            print("\n" + str(restaurants[choice]))
            restaurants[choice].show_menu()
        else:
            print("Неверный номер ресторана")
    except ValueError:
        print("Введите число!")

#поиск ресторана по названию или адресу
def search_restaurant(restaurants):
    query = input("Введите часть названия или адреса для поиска: ").lower()
    found = [r for r in restaurants if query in r.name.lower() or query in r.address.lower()]

    if not found:
        print("Ничего не найдено")
    else:
        print("\nРезультаты поиска:")
        for i, restaurant in enumerate(found, 1):
            print(f"{i}. {restaurant.name} - {restaurant.address}")

#выбор блюда из списка
def select_product(restaurant, prompt="Выберите блюдо: "):
    if not restaurant.show_menu():
        return None

    try:
        choice = int(input(prompt)) - 1
        if 0 <= choice < len(restaurant.menu):
            return restaurant.menu[choice]
        else:
            print("Неверный номер блюда")
            return None
    except ValueError:
        print("Введите число!")
        return None

#редактирование информации о ресторане
def edit_restaurant(restaurants):
    restaurant = select_restaurant(restaurants, "Выберите ресторан для редактирования: ")
    if not restaurant:
        return

    print("\nТекущая информация:")
    print(restaurant)

    print("\nЧто вы хотите изменить?")
    print("1. Название")
    print("2. Телефон")
    print("3. Адрес")
    print("4. Вернуться назад")

    choice = input("Выберите действие: ")

    if choice == "1":
        new_name = input("Введите новое название: ")
        restaurant.update_info(new_name=new_name)
        print("Название успешно изменено!")
    elif choice == "2":
        while True:
            new_phone = input("Введите новый телефон: ")
            try:
                restaurant.update_info(new_phone=new_phone)
                print("Телефон успешно изменён!")
                break
            except ValueError as e:
                print(f"Ошибка: {e}")
    elif choice == "3":
        new_address = input("Введите новый адрес: ")
        restaurant.update_info(new_address=new_address)
        print("Адрес успешно изменён!")
    elif choice == "4":
        return
    else:
        print("Неверный ввод")

#изменение меню ресторана
def edit_menu(restaurants):
    restaurant = select_restaurant(restaurants, "Выберите ресторан для редактирования меню: ")
    if not restaurant:
        return

    while True:
        print("\nРедактирование меню:")
        if not restaurant.show_menu():
            print("1. Добавить блюдо")
            print("2. Вернуться назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                product = create_product()
                restaurant.add_product(product)
                print("блюдо успешно добавлено!")
            elif choice == "2":
                return
            else:
                print("Неверный ввод")
        else:
            print("1. Добавить блюдо")
            print("2. Изменить блюдо")
            print("3. Удалить блюдо")
            print("4. Изменить статус блюда")
            print("5. Вернуться назад")

            choice = input("Выберите действие: ")

            if choice == "1":
                product = create_product()
                restaurant.add_product(product)
                print("блюдо успешно добавлен!")
            elif choice == "2":
                product = select_product(restaurant, "Выберите блюдо для изменения: ")
                if product:
                    new_name = input(f"Введите новое название (текущее: {product.name}): ") or product.name
                    new_price = input(f"Введите новую цену (текущая: {product.price}): ") or product.price

                    product.update_name(new_name)
                    try:
                        product.update_price(new_price)
                        print("блюдо успешно изменён!")
                    except ValueError:
                        print("Цена должна быть числом. Изменения не сохранены.")
            elif choice == "3":
                product = select_product(restaurant, "Выберите блюдо для удаления: ")
                if product:
                    restaurant.menu.remove(product)
                    print("блюдо успешно удалён!")
            elif choice == "4":
                product = select_product(restaurant, "Выберите блюдо для изменения статуса: ")
                if product:
                    new_status = product.change_status()
                    print(f"Статус изменён на {'доступен' if new_status else 'не доступен'}")
            elif choice == "5":
                return
            else:
                print("Неверный ввод")

# главное меню
def main_menu():
    restaurants = []

    while True:
        print("\nГлавное меню:")
        print("1. Добавить ресторан")
        print("2. Редактировать ресторан")
        print("3. Редактировать меню")
        print("4. Просмотреть все рестораны")
        print("5. Просмотреть детали ресторана")
        print("6. Поиск ресторана")
        print("7. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            restaurants.append(create_restaurant())
        elif choice == "2":
            edit_restaurant(restaurants)
        elif choice == "3":
            edit_menu(restaurants)
        elif choice == "4":
            show_all_restaurants(restaurants)
        elif choice == "5":
            show_restaurant_details(restaurants)
        elif choice == "6":
            search_restaurant(restaurants)
        elif choice == "7":
            print("Выход из программы")
            break
        else:
            print("Неверный ввод, попробуйте еще раз")

# запуск программы
if __name__ == '__main__':
    main_menu()