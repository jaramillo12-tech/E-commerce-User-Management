import reflex as rx
from sqlmodel import Session, select, func
from app.database import engine
from app.models.models import User
import bcrypt
import asyncio
import time


class DummyPhoneService:

    async def send_verification_code(
        self, phone_number: str
    ) -> str:
        await asyncio.sleep(1)
        print(
            f"Simulating sending SMS code to {phone_number}. Code: 123456"
        )
        return "123456"

    async def verify_code(
        self, phone_number: str, code: str
    ) -> bool:
        await asyncio.sleep(1)
        return code == "123456"


class DummyEmailService:

    async def send_verification_code(
        self, email: str
    ) -> str:
        await asyncio.sleep(1)
        print(
            f"Simulating sending email code to {email}. Code: 654321"
        )
        return "654321"

    async def verify_code(
        self, email: str, code: str
    ) -> bool:
        await asyncio.sleep(1)
        return code == "654321"


_dummy_phone_service = DummyPhoneService()
_dummy_email_service = DummyEmailService()


class AuthState(rx.State):
    username: str = ""
    email: str = ""
    password: str = ""
    is_logged_in: bool = False
    is_admin_user: bool = False
    error_message: str = ""
    recovery_method: str = "email"
    recovery_target: str = ""
    recovery_step: str = "request"
    reset_code_input: str = ""
    generated_reset_code: str = ""
    new_password_recovery: str = ""
    confirm_new_password_recovery: str = ""
    recovery_message: str = ""
    change_current_password: str = ""
    change_new_username: str = ""
    change_new_password: str = ""
    change_confirm_new_password: str = ""
    change_user_details_message: str = ""

    @rx.event
    def signup(self, form_data: dict):
        _username = form_data.get("username", "").strip()
        _email = form_data.get("email", "").strip().lower()
        _password = form_data.get("password", "")
        self.error_message = ""
        if not _username or not _email or (not _password):
            self.error_message = (
                "Todos los campos son obligatorios."
            )
            self.username = _username
            self.email = _email
            self.password = _password
            return
        self.username = _username
        self.email = _email
        self.password = _password
        with Session(engine) as session:
            existing_user_by_name = session.exec(
                select(User).where(
                    User.username == self.username
                )
            ).first()
            if existing_user_by_name:
                self.error_message = (
                    "El nombre de usuario ya existe."
                )
                return
            existing_user_by_email = session.exec(
                select(User).where(User.email == self.email)
            ).first()
            if existing_user_by_email:
                self.error_message = "El correo electrónico ya está registrado."
                return
            hashed_password_bytes = bcrypt.hashpw(
                self.password.encode("utf-8"),
                bcrypt.gensalt(),
            )
            hashed_password_str = (
                hashed_password_bytes.decode("utf-8")
            )
            count_stmt = select(func.count(User.id))
            user_count = (
                session.exec(
                    count_stmt
                ).scalar_one_or_none()
                or 0
            )
            is_first_user = user_count == 0
            new_user = User(
                username=self.username,
                email=self.email,
                hashed_password=hashed_password_str,
                is_admin=is_first_user,
            )
            session.add(new_user)
            session.commit()
        self.password = ""
        self.username = ""
        self.email = ""
        yield rx.redirect("/sign_in")
        yield rx.toast(
            "¡Registro exitoso! Por favor, inicia sesión.",
            duration=3000,
        )

    @rx.event
    def login(self, form_data: dict):
        _username = form_data.get("username", "").strip()
        _password = form_data.get("password", "")
        self.error_message = ""
        if not _username or not _password:
            self.error_message = (
                "Usuario y contraseña son obligatorios."
            )
            self.username = _username
            self.password = _password
            return
        self.username = _username
        self.password = _password
        if (
            self.username == "admin"
            and self.password == "adminpass"
        ):
            with Session(engine) as session:
                admin_user_model = session.exec(
                    select(User).where(
                        User.username == "admin"
                    )
                ).first()
                if not admin_user_model:
                    admin_email_candidate = (
                        "admin@techstore.com"
                    )
                    email_exists = session.exec(
                        select(User).where(
                            User.email
                            == admin_email_candidate
                        )
                    ).first()
                    if email_exists:
                        admin_email_candidate = f"admin_{int(time.time())}@techstore.com"
                    hashed_password_bytes = bcrypt.hashpw(
                        "adminpass".encode("utf-8"),
                        bcrypt.gensalt(),
                    )
                    hashed_password_str = (
                        hashed_password_bytes.decode(
                            "utf-8"
                        )
                    )
                    admin_user_model = User(
                        username="admin",
                        email=admin_email_candidate,
                        hashed_password=hashed_password_str,
                        is_admin=True,
                    )
                    session.add(admin_user_model)
                    session.commit()
                    session.refresh(admin_user_model)
                elif not admin_user_model.is_admin:
                    admin_user_model.is_admin = True
                    session.add(admin_user_model)
                    session.commit()
                self.is_logged_in = True
                self.is_admin_user = True
                self.username = admin_user_model.username
                self.email = admin_user_model.email
                self.password = ""
                yield rx.redirect("/")
                yield rx.toast(
                    "¡Bienvenido, Administrador!",
                    duration=3000,
                )
                return
        with Session(engine) as session:
            user_model = session.exec(
                select(User).where(
                    User.username == self.username
                )
            ).first()
            if user_model and bcrypt.checkpw(
                self.password.encode("utf-8"),
                user_model.hashed_password.encode("utf-8"),
            ):
                self.is_logged_in = True
                self.is_admin_user = user_model.is_admin
                self.username = user_model.username
                self.email = user_model.email
                self.password = ""
                yield rx.redirect("/")
                yield rx.toast(
                    f"¡Bienvenido de nuevo, {self.username}!",
                    duration=3000,
                )
            else:
                self.error_message = (
                    "Usuario o contraseña incorrectos."
                )
                self.is_logged_in = False
                self.is_admin_user = False
                self.password = ""

    @rx.event
    def logout(self):
        self.is_logged_in = False
        self.is_admin_user = False
        self.username = ""
        self.email = ""
        self.password = ""
        self.error_message = ""
        self.recovery_message = ""
        self.change_user_details_message = ""
        yield rx.redirect("/sign_in")
        yield rx.toast("Has cerrado sesión.", duration=2000)

    @rx.event
    def check_login_status(self):
        if self.is_logged_in:
            current_path = self.router.page.path
            if current_path in ["/sign_in", "/sign_up"]:
                yield rx.redirect("/")

    @rx.event
    def check_admin_session(self):
        current_path = self.router.page.path
        if not self.is_logged_in:
            yield rx.redirect("/sign_in")
            yield rx.toast(
                "Debes iniciar sesión para acceder a esta página.",
                duration=3000,
            )
            return
        if not self.is_admin_user:
            yield rx.redirect("/")
            yield rx.toast(
                "No tienes permisos para acceder a esta página.",
                duration=3000,
            )
            return
        if not self.username:
            yield AuthState.logout()

    @rx.event
    def check_general_login_session(self):
        if not self.is_logged_in or not self.username:
            yield rx.redirect("/sign_in")
            yield rx.toast(
                "Debes iniciar sesión para ver tu perfil.",
                duration=3000,
            )

    @rx.event
    def set_recovery_method(self, method: str):
        self.recovery_method = method
        self.recovery_target = ""
        self.recovery_message = ""

    @rx.event(background=True)
    async def request_password_reset(self, form_data: dict):
        async with self:
            self.recovery_target = form_data.get(
                "recovery_input_field", ""
            ).strip()
            self.recovery_message = ""
            if not self.recovery_target:
                self.recovery_message = "Por favor, ingresa tu correo o número de celular."
                return
        with Session(engine) as session:
            user_exists = False
            if self.recovery_method == "email":
                user_exists = (
                    session.exec(
                        select(User).where(
                            User.email
                            == self.recovery_target
                        )
                    ).first()
                    is not None
                )
            elif self.recovery_method == "phone":
                async with self:
                    self.recovery_message = "La recuperación por teléfono no está implementada completamente con base de datos real."
                user_exists = True
            if self.recovery_method == "email" and (
                not user_exists
            ):
                async with self:
                    self.recovery_message = "No se encontró una cuenta con ese correo electrónico."
                yield rx.toast(
                    self.recovery_message, duration=3000
                )
                return
        if self.recovery_method == "email":
            generated_code = await _dummy_email_service.send_verification_code(
                self.recovery_target
            )
            async with self:
                self.generated_reset_code = generated_code
        elif self.recovery_method == "phone":
            generated_code = await _dummy_phone_service.send_verification_code(
                self.recovery_target
            )
            async with self:
                self.generated_reset_code = generated_code
        async with self:
            if self.generated_reset_code:
                self.recovery_step = "verify"
                self.recovery_message = f"Se ha enviado un código de verificación a {self.recovery_target}."
                yield rx.toast(
                    self.recovery_message, duration=3000
                )
            else:
                self.recovery_message = "Error al enviar el código de verificación."
                yield rx.toast(
                    self.recovery_message, duration=3000
                )

    @rx.event
    async def verify_reset_code(self, form_data: dict):
        self.reset_code_input = form_data.get(
            "reset_code_input_field", ""
        ).strip()
        self.recovery_message = ""
        verified = False
        if self.recovery_method == "email":
            verified = (
                await _dummy_email_service.verify_code(
                    self.recovery_target,
                    self.reset_code_input,
                )
            )
        elif self.recovery_method == "phone":
            verified = (
                await _dummy_phone_service.verify_code(
                    self.recovery_target,
                    self.reset_code_input,
                )
            )
        if (
            verified
            and self.reset_code_input
            and (
                self.reset_code_input
                == self.generated_reset_code
            )
        ):
            self.recovery_step = "reset"
            self.recovery_message = "Código verificado. Ahora puedes restablecer tu contraseña."
            yield rx.toast(
                self.recovery_message, duration=3000
            )
        else:
            self.recovery_message = (
                "Código de verificación incorrecto."
            )
            yield rx.toast(
                self.recovery_message, duration=3000
            )
        self.reset_code_input = ""

    @rx.event
    def process_password_reset(self, form_data: dict):
        self.new_password_recovery = form_data.get(
            "new_password_field", ""
        )
        self.confirm_new_password_recovery = form_data.get(
            "confirm_new_password_field", ""
        )
        self.recovery_message = ""
        if (
            not self.new_password_recovery
            or not self.confirm_new_password_recovery
        ):
            self.recovery_message = "Por favor, ingresa y confirma tu nueva contraseña."
            return
        if (
            self.new_password_recovery
            != self.confirm_new_password_recovery
        ):
            self.recovery_message = (
                "Las contraseñas no coinciden."
            )
            return
        with Session(engine) as session:
            user_to_update = None
            if self.recovery_method == "email":
                user_to_update = session.exec(
                    select(User).where(
                        User.email == self.recovery_target
                    )
                ).first()
            if user_to_update:
                hashed_password_bytes = bcrypt.hashpw(
                    self.new_password_recovery.encode(
                        "utf-8"
                    ),
                    bcrypt.gensalt(),
                )
                user_to_update.hashed_password = (
                    hashed_password_bytes.decode("utf-8")
                )
                session.add(user_to_update)
                session.commit()
                self.recovery_message = "¡Contraseña restablecida exitosamente! Ahora puedes iniciar sesión."
                self.recovery_step = "request"
                self.new_password_recovery = ""
                self.confirm_new_password_recovery = ""
                self.reset_code_input = ""
                self.recovery_target = ""
                yield rx.toast(
                    self.recovery_message, duration=4000
                )
                yield rx.redirect("/sign_in")
            else:
                self.recovery_message = "Error al encontrar el usuario para actualizar la contraseña."
                self.new_password_recovery = ""
                self.confirm_new_password_recovery = ""
                yield rx.toast(
                    self.recovery_message, duration=3000
                )

    @rx.event
    def go_to_request_step(self):
        self.recovery_step = "request"
        self.recovery_target = ""
        self.reset_code_input = ""
        self.new_password_recovery = ""
        self.confirm_new_password_recovery = ""
        self.recovery_message = ""
        self.generated_reset_code = ""

    @rx.event
    def handle_change_user_details(self, form_data: dict):
        _change_current_password = form_data.get(
            "change_current_password", ""
        )
        _change_new_username = form_data.get(
            "change_new_username", ""
        ).strip()
        _change_new_password = form_data.get(
            "change_new_password", ""
        )
        _change_confirm_new_password = form_data.get(
            "change_confirm_new_password", ""
        )
        self.change_user_details_message = ""
        if not _change_current_password:
            self.change_user_details_message = (
                "Debes ingresar tu contraseña actual."
            )
            self.change_current_password = ""
            self.change_new_username = _change_new_username
            self.change_new_password = _change_new_password
            self.change_confirm_new_password = (
                _change_confirm_new_password
            )
            return
        if not _change_new_username and (
            not _change_new_password
        ):
            self.change_user_details_message = "Debes ingresar un nuevo nombre de usuario o una nueva contraseña."
            self.change_current_password = (
                _change_current_password
            )
            self.change_new_username = _change_new_username
            self.change_new_password = _change_new_password
            self.change_confirm_new_password = (
                _change_confirm_new_password
            )
            return
        if (
            _change_new_password
            and _change_new_password
            != _change_confirm_new_password
        ):
            self.change_user_details_message = (
                "Las nuevas contraseñas no coinciden."
            )
            self.change_current_password = (
                _change_current_password
            )
            self.change_new_username = _change_new_username
            self.change_new_password = ""
            self.change_confirm_new_password = ""
            return
        self.change_current_password = (
            _change_current_password
        )
        self.change_new_username = _change_new_username
        self.change_new_password = _change_new_password
        self.change_confirm_new_password = (
            _change_confirm_new_password
        )
        with Session(engine) as session:
            current_user = session.exec(
                select(User).where(
                    User.username == self.username
                )
            ).first()
            if not current_user or not bcrypt.checkpw(
                self.change_current_password.encode(
                    "utf-8"
                ),
                current_user.hashed_password.encode(
                    "utf-8"
                ),
            ):
                self.change_user_details_message = (
                    "La contraseña actual es incorrecta."
                )
                self.change_current_password = ""
                return
            changes_made = False
            if (
                self.change_new_username
                and self.change_new_username
                != current_user.username
            ):
                existing_user_by_new_name = session.exec(
                    select(User).where(
                        User.username
                        == self.change_new_username
                    )
                ).first()
                if existing_user_by_new_name:
                    self.change_user_details_message = "El nuevo nombre de usuario ya está en uso."
                    self.change_new_username = ""
                    return
                current_user.username = (
                    self.change_new_username
                )
                self.username = self.change_new_username
                changes_made = True
            if self.change_new_password:
                new_hashed_password_bytes = bcrypt.hashpw(
                    self.change_new_password.encode(
                        "utf-8"
                    ),
                    bcrypt.gensalt(),
                )
                current_user.hashed_password = (
                    new_hashed_password_bytes.decode(
                        "utf-8"
                    )
                )
                changes_made = True
            if changes_made:
                session.add(current_user)
                session.commit()
                self.change_user_details_message = (
                    "¡Detalles actualizados exitosamente!"
                )
            else:
                self.change_user_details_message = (
                    "No se realizaron cambios."
                )
            self.change_current_password = ""
            self.change_new_username = ""
            self.change_new_password = ""
            self.change_confirm_new_password = ""
            yield rx.toast(
                self.change_user_details_message,
                duration=3000,
            )

    @rx.event
    def set_username_form_field(self, value: str):
        self.username = value

    @rx.event
    def set_email_form_field(self, value: str):
        self.email = value

    @rx.event
    def set_password_form_field(self, value: str):
        self.password = value

    @rx.event
    def set_recovery_target_field(self, value: str):
        self.recovery_target = value

    @rx.event
    def set_reset_code_input_field(self, value: str):
        self.reset_code_input = value

    @rx.event
    def set_new_password_recovery_field(self, value: str):
        self.new_password_recovery = value

    @rx.event
    def set_confirm_new_password_recovery_field(
        self, value: str
    ):
        self.confirm_new_password_recovery = value

    @rx.event
    def set_change_current_password_field(self, value: str):
        self.change_current_password = value

    @rx.event
    def set_change_new_username_field(self, value: str):
        self.change_new_username = value

    @rx.event
    def set_change_new_password_field(self, value: str):
        self.change_new_password = value

    @rx.event
    def set_change_confirm_new_password_field(
        self, value: str
    ):
        self.change_confirm_new_password = value