import reflex as rx
import os
from app.pages.home_page import home_page
from app.pages.products import products_page
from app.pages.sign_in import sign_in_page
from app.pages.sign_up import sign_up_page
from app.pages.checkout import checkout_page
from app.pages.contact import contact_page
from app.pages.forgot_password import forgot_password_page
from app.pages.profile_page import profile_page
from app.pages.admin_dashboard import admin_dashboard_page
from app.pages.admin_manage_products import (
    admin_manage_products_page,
)
from app.pages.admin_statistics import admin_statistics_page
from app.pages.confirmation_page import confirmation_page
from app.pages.admin_purchase_history import (
    admin_purchase_history_page,
)
from app.pages.admin_mailbox import admin_mailbox_page
from app.states.auth_state import AuthState
from app.states.product_state import ProductState
from app.states.cart_state import CartState
from app.states.checkout_state import CheckoutState
from app.states.contact_state import ContactState
from app.states.theme_state import ThemeState
from app.states.admin_product_state import AdminProductState
from app.states.admin_stats_state import AdminStatsState
from app.states.feedback_state import FeedbackState
from app.states.invoice_state import InvoiceState
from app.states.admin_purchase_history_state import (
    AdminPurchaseHistoryState,
)
from app.states.admin_mailbox_state import AdminMailboxState
from app.states.chat_ai_state import ChatAIState
from app.database import create_db_and_tables


def index() -> rx.Component:
    return home_page()


create_db_and_tables()
app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/animations.css"],
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            crossorigin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=DejaVu+Sans+Condensed&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(products_page, route="/products")
app.add_page(sign_in_page, route="/sign_in")
app.add_page(sign_up_page, route="/sign_up")
app.add_page(checkout_page, route="/checkout")
app.add_page(contact_page, route="/contact")
app.add_page(forgot_password_page, route="/forgot-password")
app.add_page(profile_page, route="/profile")
app.add_page(confirmation_page, route="/confirmation")
app.add_page(admin_dashboard_page, route="/admin")
app.add_page(
    admin_manage_products_page,
    route="/admin/manage-products",
)
app.add_page(
    admin_statistics_page, route="/admin/statistics"
)
app.add_page(
    admin_purchase_history_page,
    route="/admin/purchase-history",
)
app.add_page(admin_mailbox_page, route="/admin/mailbox")