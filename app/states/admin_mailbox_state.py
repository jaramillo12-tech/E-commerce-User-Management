import reflex as rx
from sqlmodel import Session, select
from app.database import engine
from app.models.models import Complaint
import datetime
from typing import Optional


class AdminMailboxState(rx.State):
    complaints: list[Complaint] = []
    selected_complaint: Optional[Complaint] = None
    reply_message: str = ""
    show_reply_modal: bool = False

    @rx.event
    async def load_complaints(self):
        with Session(engine) as session:
            self.complaints = session.exec(
                select(Complaint).order_by(
                    Complaint.created_at.desc()
                )
            ).all()

    @rx.event
    def select_complaint(self, complaint: Complaint):
        self.selected_complaint = complaint
        self.reply_message = ""
        self.show_reply_modal = True

    @rx.event
    def close_reply_modal(self):
        self.show_reply_modal = False
        self.selected_complaint = None
        self.reply_message = ""

    @rx.event(background=True)
    async def handle_reply(self, form_data: dict):
        reply_text = form_data.get("reply_message", "")
        async with self:
            if (
                not self.selected_complaint
                or not reply_text
            ):
                yield rx.toast(
                    "La respuesta no puede estar vacía.",
                    duration=3000,
                )
                return
            self.reply_message = reply_text
        print(f"--- SIMULATING EMAIL ---")
        print(f"To: {self.selected_complaint.email}")
        print(
            f"Subject: Re: {self.selected_complaint.subject}"
        )
        print(f"Body: {self.reply_message}")
        print(f"--- END SIMULATION ---")
        with Session(engine) as session:
            db_complaint = session.get(
                Complaint, self.selected_complaint.id
            )
            if db_complaint:
                db_complaint.status = "replied"
                db_complaint.reply_message = (
                    self.reply_message
                )
                db_complaint.replied_at = (
                    datetime.datetime.utcnow()
                )
                session.add(db_complaint)
                session.commit()
        async with self:
            self.show_reply_modal = False
            self.selected_complaint = None
            self.reply_message = ""
        yield rx.toast(
            "Respuesta enviada (simulada).", duration=3000
        )
        yield AdminMailboxState.load_complaints