import reflex as rx


class ThemeState(rx.State):
    current_theme: str = "dark"
    is_lite_mode: bool = False

    @rx.event
    def toggle_theme(self):
        self.current_theme = (
            "light"
            if self.current_theme == "dark"
            else "dark"
        )

    @rx.event
    def toggle_lite_mode(self):
        self.is_lite_mode = not self.is_lite_mode
        yield rx.toast(
            f"Modo Lite {('Activado' if self.is_lite_mode else 'Desactivado')}",
            duration=2000,
        )

    @rx.var
    def light_mode_colors(self) -> dict[str, str]:
        return {
            "bg_primary": "bg-white",
            "bg_secondary": "bg-sky-50",
            "text_primary": "text-sky-800",
            "text_secondary": "text-sky-600",
            "accent": "text-sky-500",
            "border_primary": "border-sky-200",
            "button_bg": "bg-sky-500",
            "button_hover_bg": "hover:bg-sky-600",
            "card_bg": "bg-white",
            "card_shadow": "shadow-sky-200/50",
            "input_bg": "bg-sky-50",
            "input_border": "border-sky-300",
            "input_focus_ring": "focus:ring-sky-400",
        }

    @rx.var
    def dark_mode_colors(self) -> dict[str, str]:
        return {
            "bg_primary": "bg-slate-900",
            "bg_secondary": "bg-slate-800",
            "text_primary": "text-white",
            "text_secondary": "text-sky-300",
            "accent": "text-sky-400",
            "border_primary": "border-gray-700",
            "button_bg": "bg-sky-600",
            "button_hover_bg": "hover:bg-sky-700",
            "card_bg": "bg-gray-800",
            "card_shadow": "shadow-sky-500/40",
            "input_bg": "bg-gray-700",
            "input_border": "border-gray-600",
            "input_focus_ring": "focus:ring-sky-500",
        }

    @rx.var
    def active_colors(self) -> dict[str, str]:
        return (
            self.light_mode_colors
            if self.current_theme == "light"
            else self.dark_mode_colors
        )