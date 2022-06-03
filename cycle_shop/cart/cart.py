from decimal import Decimal
from django.conf import settings
from shop.models import Cycle


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_slug = str(product.slug)
        if product_slug not in self.cart:
            self.cart[product_slug] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_slug]['quantity'] = quantity
        else:
            self.cart[product_slug]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def increase(self, product):
        """
        Увеличение кол-ва товара в корзине.
        """
        product_slug = str(product.slug)
        self.cart[product_slug]['quantity'] += 1
        self.save()

    def decrease(self, product):
        """
        Уменьшение кол-ва товара в корзине.
        """
        product_slug = str(product.slug)
        if self.cart[product_slug]['quantity'] == 1:
            del self.cart[product_slug]
            self.save()
        else:
            self.cart[product_slug]['quantity'] -= 1
            self.save()

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_slug = str(product.slug)
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_slugs = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Cycle.objects.filter(slug__in=product_slugs)
        print(1)
        for product in products:
            self.cart[str(product.slug)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
