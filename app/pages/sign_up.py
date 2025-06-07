import reflex as rx
from app.components.navbar import navbar
from app.components.auth_cards import sign_up_card
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def sign_up_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            sign_up_card(),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "flex flex-col items-center justify-center min-h-screen p-4 pt-20 bg-white",
                "flex flex-col items-center justify-center min-h-screen p-4 pt-20 bg-slate-900",
            ),
        ),
        class_name=ThemeState.current_theme,
        on_mount=AuthState.check_login_status,
    )