import reflex as rx
from app.models.models import Complaint
from app.database import engine
from sqlmodel import Session


class ContactState(rx.State):
    name: str = ""
    email: str = ""
    subject: str = ""
    message: str = ""

    @rx.event(background=True)
    async def handle_submit(self, form_data: dict):
        _name = form_data.get("name", "")
        _email = form_data.get("email", "")
        _subject = form_data.get("subject", "")
        _message = form_data.get("message", "")
        if not all([_name, _email, _subject, _message]):
            yield rx.toast(
                "Todos los campos son obligatorios.",
                duration=3000,
            )
            return
        new_complaint = Complaint(
            name=_name,
            email=_email,
            subject=_subject,
            message=_message,
        )
        with Session(engine) as session:
            session.add(new_complaint)
            session.commit()
        yield rx.toast(
            f"¡Mensaje enviado de {_name}! Gracias, lo revisaremos pronto."
        )
        async with self:
            self.name = ""
            self.email = ""
            self.subject = ""
            self.message = ""

    @rx.event
    def set_message(self, message: str):
        self.message = message