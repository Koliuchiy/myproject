from decimal import Decimal
from django.conf import settings
from shop.models import Article


class Cart(object):

    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, article, quantity=1, update_quantity=False):
        """Add a article to the cart or update its quantity."""
        article_id = str(article.id)
        if article_id not in self.cart:
            self.cart[article_id] = {'quantity': 0, 'price': str(article.price)}
        if update_quantity:
            self.cart[article_id]['quantity'] = quantity
        elif self.cart[article_id]['quantity'] + quantity > 20:
            self.cart[article_id]['quantity'] = 20
        else:
            self.cart[article_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, article):
        """Remove a product from the cart."""
        article_id = str(article.id)
        if article_id in self.cart:
            del self.cart[article_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products
        from the database."""
        article_ids = self.cart.keys()
        # get the product objects and add them to the cart
        articles = Article.objects.filter(id__in=article_ids)
        for article in articles:
            self.cart[str(article.id)]['article'] = article
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
