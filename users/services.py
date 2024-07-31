import stripe

from config.settings import API_KEY_STRIPE

stripe.api_key = API_KEY_STRIPE


def create_price_for_payment(amount):
    """cоздает цену в stripe"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product_data={"name": "Payment"},
    )


def create_session_for_payment(price):
    """cоздает сессию в stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')



