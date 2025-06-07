import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.admin_mailbox_state import AdminMailboxState
from app.states.theme_state import ThemeState
from app.models.models import Complaint


def reply_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.h2(
                "Responder a Queja",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-2xl font-bold text-sky-700 mb-4",
                    "text-2xl font-bold text-sky-300 mb-4",
                ),
            ),
            rx.cond(
                AdminMailboxState.selected_complaint,
                rx.el.div(
                    rx.el.p(
                        "De: ",
                        rx.el.strong(
                            AdminMailboxState.selected_complaint.name
                        ),
                        f" <{AdminMailboxState.selected_complaint.email}>",
                    ),
                    rx.el.p(
                        "Asunto: ",
                        rx.el.strong(
                            AdminMailboxState.selected_complaint.subject
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            AdminMailboxState.selected_complaint.message
                        ),
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "p-3 my-3 bg-gray-100 border border-gray-200 rounded-md max-h-40 overflow-y-auto custom-scrollbar",
                            "p-3 my-3 bg-gray-700 border border-gray-600 rounded-md max-h-40 overflow-y-auto custom-scrollbar",
                        ),
                    ),
                    rx.el.form(
                        rx.el.label(
                            "Tu Respuesta:",
                            class_name="font-medium",
                        ),
                        rx.el.textarea(
                            name="reply_message",
                            default_value=AdminMailboxState.reply_message,
                            placeholder="Escribe tu respuesta aquí...",
                            rows=6,
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "w-full p-2 mt-1 border border-sky-300 rounded bg-sky-50 text-sky-800",
                                "w-full p-2 mt-1 border border-gray-600 rounded bg-gray-700 text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Enviar Respuesta",
                                type="submit",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "px-4 py-2 bg-sky-500 text-white rounded hover:bg-sky-600 button-light-interactive",
                                    "px-4 py-2 bg-sky-600 text-white rounded hover:bg-sky-700",
                                ),
                            ),
                            rx.el.button(
                                "Cancelar",
                                on_click=AdminMailboxState.close_reply_modal,
                                type="button",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "ml-2 px-4 py-2 bg-gray-300 text-black rounded hover:bg-gray-400",
                                    "ml-2 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-500",
                                ),
                            ),
                            class_name="flex justify-end mt-4",
                        ),
                        on_submit=AdminMailboxState.handle_reply,
                        reset_on_submit=False,
                    ),
                ),
                rx.el.p("Cargando queja..."),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "bg-white p-6 rounded-lg shadow-xl w-full max-w-2xl text-sky-800",
                "bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-2xl text-white",
            ),
        ),
        open=AdminMailboxState.show_reply_modal,
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "fixed inset-0 bg-sky-700 bg-opacity-30 backdrop-blur-sm open:flex items-center justify-center p-4 z-[100]",
            "fixed inset-0 bg-black bg-opacity-50 dark:bg-opacity-80 backdrop-blur-sm open:flex items-center justify-center p-4 z-[100]",
        ),
    )


def complaint_row(complaint: Complaint) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            complaint.created_at.to_string(),
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm",
        ),
        rx.el.td(
            complaint.name,
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            complaint.subject,
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            rx.el.span(
                complaint.status,
                class_name=rx.cond(
                    complaint.status == "new",
                    "bg-red-200 text-red-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded-full",
                    "bg-green-200 text-green-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded-full",
                ),
            ),
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            rx.el.button(
                "Ver y Responder",
                on_click=lambda: AdminMailboxState.select_complaint(
                    complaint
                ),
                class_name="bg-sky-500 hover:bg-sky-600 text-white px-3 py-1 rounded text-sm",
            ),
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "hover:bg-sky-50/50",
            "hover:bg-gray-700/50",
        ),
    )


def admin_mailbox_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        reply_modal(),
        rx.el.div(
            rx.el.h1(
                "Buzón de Quejas y Reclamos",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl font-bold text-sky-800 mb-8 title-bounce",
                    "text-3xl font-bold text-white mb-8 title-bounce",
                ),
            ),
            rx.cond(
                AdminMailboxState.complaints.length() > 0,
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Fecha",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "De",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Asunto",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Estado",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Acciones",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                AdminMailboxState.complaints,
                                complaint_row,
                            )
                        ),
                        class_name="min-w-full",
                    ),
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "overflow-x-auto shadow-lg rounded-lg bg-white p-4",
                        "overflow-x-auto shadow-lg rounded-lg bg-gray-800 p-4",
                    ),
                ),
                rx.el.p(
                    "No hay quejas o reclamos nuevos.",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-center text-sky-600 text-lg py-10",
                        "text-center text-gray-500 text-lg py-10",
                    ),
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "container mx-auto py-10 px-4 min-h-screen pt-24 bg-white",
                "container mx-auto py-10 px-4 min-h-screen pt-24 bg-slate-900",
            ),
        ),
        on_mount=[
            AuthState.check_admin_session,
            AdminMailboxState.load_complaints,
        ],
        class_name=ThemeState.current_theme,
    )