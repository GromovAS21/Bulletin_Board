import stripe

from config.settings import STRIPE_API_KEY
from orders.models import Order

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product: Order) -> str:
    """
    Создание новый продукт в Stripe
    """
    stripe_product = stripe.Product.create(name=product.basket.goods)
    return stripe_product.get("id")


def create_price_stripe_product(product: Order, stripe_product) -> str:
    """
    Создание цены для продукта в Stripe
    """
    product_price = product.amount

    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=product_price * 100,
        product_data={"name": stripe_product},
    )
    return stripe_price.get("id")


def create__stripe_session(price):
    """
    Создание сессии в Stripe для оплаты
    """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/orders/success_pay/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def check_stripe_status_pay(session):
    """
    Проверка статуса оплаты в Stripe
    """
    response = stripe.checkout.Session.retrieve(session)
    return response.get("payment_status")
