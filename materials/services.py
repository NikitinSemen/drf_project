import stripe


def create_product_for_payment(product):
    """cоздает сессию в stripe"""
    return stripe.Product.create(name=product.name, description=product.description)


