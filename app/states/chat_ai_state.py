import reflex as rx
import os
import openai
from typing import cast

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print(
        "WARNING: DEEPSEEK_API_KEY environment variable not set. Chat AI will not function."
    )
    client = None
else:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
    )


class ChatAIState(rx.State):
    is_chat_open: bool = False
    is_processing: bool = False
    messages: list[dict[str, str]] = []

    @rx.event
    def toggle_chat(self):
        self.is_chat_open = not self.is_chat_open
        if self.is_chat_open and (not self.messages):
            self.messages = [
                {
                    "role": "assistant",
                    "content": "¡Hola! Soy tu asistente de compras de TechStore. ¿Cómo puedo ayudarte a encontrar el producto perfecto hoy?",
                }
            ]

    @rx.event(background=True)
    async def handle_submit(self, form_data: dict):
        question = form_data.get("question", "").strip()
        if not question:
            return
        if not client:
            async with self:
                self.messages.append(
                    {"role": "user", "content": question}
                )
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": "Lo siento, el servicio de IA no está configurado. Por favor, contacta al administrador.",
                    }
                )
            yield rx.toast(
                "La IA del chat no está configurada.",
                duration=3000,
            )
            return
        async with self:
            self.messages.append(
                {"role": "user", "content": question}
            )
            self.is_processing = True
        yield
        try:
            system_prompt = {
                "role": "system",
                "content": "Eres un asistente de IA amigable y servicial para TechStore, una tienda de electrónica en línea. Tu objetivo es ayudar a los usuarios a encontrar productos, responder sus preguntas sobre especificaciones y guiarlos a través del sitio web. Sé conciso y útil. Responde en español.",
            }
            api_messages = [system_prompt] + [
                cast(dict, msg) for msg in self.messages
            ]
            response = await client.chat.completions.create(
                model="deepseek-chat",
                messages=api_messages,
                max_tokens=1024,
                temperature=0.7,
                stream=False,
            )
            assistant_response = response.choices[
                0
            ].message.content
            async with self:
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response,
                    }
                )
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            async with self:
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": "Lo siento, estoy teniendo problemas para conectarme. Por favor, inténtalo de nuevo más tarde.",
                    }
                )
        finally:
            async with self:
                self.is_processing = False
            yield