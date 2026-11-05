from abc import ABC, abstractmethod
from typing import List, Optional


class ZeroQuantityError(Exception):
    """Пользовательское исключение: попытка добавить товар
    с нулевым количеством."""
    pass


# --- Миксин (ОБЯЗАТЕЛЬНО первым в файле) ---
class CreationLoggerMixin:
    """Миксин: ставит флаг инициализации и выводит лог ДО
    основной инициализации."""

    def __init__(self, *args, **kwargs):
        # 1. Ставим флаг — это гарантия, что миксин отработал
        self._mixin_initialized = True
        print("[MIXIN] Logger activated!")

        # 2. Передаём управление дальше по цепочке MRO
        super().__init__(*args, **kwargs)


# --- Абстрактный базовый класс (если используется в других местах) ---
class BaseProduct(ABC):
    @abstractmethod
    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
        self.name = name
        self.description = description
        self.__price = price
        self._quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            raise ValueError("Цена должна быть положительной")
        self.__price = new_price

    @abstractmethod
    def total_cost(self) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Нельзя складывать объекты разных классов")
        return self.total_cost() + other.total_cost()


class Orderable(ABC):
    @abstractmethod
    def calculate_total(self) -> float:
        pass


# --- Основной класс Product ---
class Product(CreationLoggerMixin):
    """Товар: проверка количества строго в __init__,
    сеттер — как дополнительная защита."""

    def __init__(self, name: str, description: str, price: float,
                 quantity: int):

        super().__init__()

        # ПРОВЕРКА КОЛИЧЕСТВА: сразу при создании
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не "
                             "может быть добавлен")

        # Сохраняем данные
        self.name = name
        self.description = description
        self._quantity = quantity
        self.price = price  # используем сеттер для валидации цены

    @classmethod
    def new_product(cls, data: dict,
                    products_list: Optional[List['Product']] = None):
        """
        Фабрика для создания/обновления продукта.
        Если в products_list есть товар с таким же именем — обновляем его.
        Иначе создаём новый.
        """
        # Ищем существующий продукт по имени
        if products_list:
            for existing in products_list:
                if existing.name == data["name"]:
                    # Обновляем поля
                    existing.price = data.get("price", existing.price)
                    existing.quantity = data.get("quantity", existing.quantity)
                    return existing

        # Создаём новый
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            price=data["price"],
            quantity=data["quantity"],
        )

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value <= 0:
            raise ValueError("Товар с нулевым количеством не "
                             "может быть добавлен")
        self._quantity = value

    @property
    def price(self) -> float:
        # Безопасное получение, если вдруг сеттер не сработал
        return getattr(self, '_price', 0.0)

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        setattr(self, '_price', value)

    def total_cost(self) -> float:
        return self.price * self.quantity

    def __str__(self) -> str:
        return (f"{self.name}, {self.price} руб. "
                f"Остаток: {self.quantity} шт.")


# --- Наследники ---
class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} | Смартфон: {self.model}, "
            f"память {self.memory} ГБ, цвет {self.color}"
        )

    def __add__(self, other: 'Smartphone') -> float:
        if not isinstance(other, Smartphone):
            raise TypeError("Нельзя складывать объекты разных классов")
        return self.total_cost() + other.total_cost()


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} | Трава: страна {self.country}, "
            f"прорастание {self.germination_period} дней, цвет {self.color}"
        )

    def __add__(self, other: 'LawnGrass') -> float:
        if not isinstance(other, LawnGrass):
            raise TypeError("Нельзя складывать объекты разных классов")
        return self.total_cost() + other.total_cost()


# --- Класс Order ---
class Order(Orderable):
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Количество товара в заказе "
                             "должно быть положительным")
        self.product = product
        self.quantity = quantity

    def calculate_total(self) -> float:
        return self.product.total_cost() * self.quantity

    def __str__(self) -> str:
        total = self.calculate_total()
        return (
            f"Заказ: {self.quantity} шт. товара '{self.product.name}'. "
            f"Итого: {total:.2f} руб."
        )


# --- Категория ---
class Category(Orderable):
    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        self.name = name
        self.description = description

        for p in products:
            if not isinstance(p, Product):
                raise TypeError(
                    "В категорию можно добавлять только объекты"
                    " Product или его наследников"
                )

        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только объекты "
                "Product или его наследников"
            )

        if product.quantity <= 0:
            raise ZeroQuantityError(
                "Товар с нулевым или отрицательным количеством "
                "нельзя добавить в категорию"
            )

        self.__products.append(product)

    @property
    def products(self) -> List[Product]:
        return self.__products

    def total_quantity(self) -> int:
        return sum(p.quantity for p in self.__products)

    def calculate_total(self) -> float:
        return sum(p.total_cost() for p in self.__products)

    def average_price(self) -> float:
        products = self.__products
        if not products:
            return 0.0
        total = sum(p.price for p in products)
        return total / len(products)

    def __str__(self) -> str:
        qty = self.total_quantity()
        return f"{self.name}, количество продуктов: {qty} шт."

    def __add__(self, other: "Category") -> float:
        if not isinstance(other, Category):
            return NotImplemented
        return sum(p.total_cost() for p in self.__products) + sum(
            p.total_cost() for p in other.__products
        )
