import reflex as rx
from app.states.chat_ai_state import ChatAIState
from app.states.theme_state import ThemeState


def chat_message(message: dict) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.p(
            message["content"],
            class_name=rx.cond(
                is_user,
                "bg-sky-500 text-white rounded-t-lg rounded-bl-lg",
                "bg-gray-200 text-gray-800 rounded-t-lg rounded-br-lg",
            ),
            padding="0.75rem",
            max_width="80%",
        ),
        class_name=rx.cond(
            is_user,
            "flex justify-end",
            "flex justify-start",
        ),
    )


def chat_ai_widget() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                ChatAIState.is_chat_open,
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Asistente IA",
                            class_name="font-bold",
                        ),
                        rx.el.button(
                            "X",
                            on_click=ChatAIState.toggle_chat,
                        ),
                        class_name="flex justify-between items-center p-4 bg-sky-600 text-white rounded-t-lg",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ChatAIState.messages,
                            chat_message,
                        ),
                        class_name="flex-grow p-4 space-y-4 overflow-y-auto custom-scrollbar",
                    ),
                    rx.cond(
                        ChatAIState.is_processing,
                        rx.el.div(
                            rx.spinner(size="2"),
                            class_name="p-4",
                        ),
                        rx.el.div(),
                    ),
                    rx.el.form(
                        rx.el.input(
                            placeholder="Pregunta sobre productos...",
                            name="question",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "flex-grow p-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-sky-500",
                                "flex-grow p-2 bg-gray-700 border border-gray-600 rounded-l-md text-white focus:outline-none focus:ring-2 focus:ring-sky-500",
                            ),
                        ),
                        rx.el.button(
                            "Enviar",
                            type="submit",
                            class_name="p-2 bg-sky-500 text-white rounded-r-md hover:bg-sky-600",
                        ),
                        on_submit=ChatAIState.handle_submit,
                        class_name="flex p-4 border-t border-gray-200 dark:border-gray-700",
                        reset_on_submit=True,
                    ),
                    class_name="fixed bottom-24 right-5 w-96 h-[500px] bg-white dark:bg-gray-800 rounded-lg shadow-2xl flex flex-col z-[100]",
                ),
                rx.el.div(),
            ),
            rx.el.button(
                rx.icon(
                    tag="message_circle",
                    class_name="h-8 w-8 text-white",
                ),
                on_click=ChatAIState.toggle_chat,
                class_name="bg-sky-500 hover:bg-sky-600 rounded-full p-4 shadow-lg",
            ),
            class_name="fixed bottom-5 right-5 z-[100]",
        )
    )