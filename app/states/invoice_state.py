import reflex as rx
import os
import datetime
import uuid
from typing import Optional, Union, cast
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

try:
    from fpdf import FPDF

    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False


class InvoiceItem(rx.Base):
    product_id: int
    name: str
    quantity: int
    price: float
    image_url: str
    stock: int


class OrderDetails(rx.Base):
    customer_name: str = ""
    customer_address: str = ""
    customer_email: str = ""
    customer_document_id: str = ""
    items: list[InvoiceItem] = []
    total_price: float = 0.0
    invoice_number: str = ""
    cufe: str = ""
    subtotal: float = 0.0
    vat: float = 0.0
    invoice_date: str = ""


RawOrderItem = dict[str, Union[str, int, float]]
RawOrderData = dict[
    str, Union[str, float, list[RawOrderItem]]
]


class InvoiceState(rx.State):
    raw_order_data: Optional[RawOrderData] = None
    order_details: OrderDetails = OrderDetails()
    display_items: list[
        dict[str, Union[str, int, float]]
    ] = []
    is_generating_invoice: bool = False
    invoice_pdf_path: Optional[str] = None
    IVA_RATE: float = 0.19
    invoice_email_sent: bool = False

    @rx.var
    def is_fpdf_available(self) -> bool:
        return FPDF_AVAILABLE

    @rx.var
    def has_raw_order_data(self) -> bool:
        return self.raw_order_data is not None

    @rx.event
    def set_raw_order_data(self, data: RawOrderData):
        self.raw_order_data = data
        self.order_details = OrderDetails()
        self.display_items = []
        self.invoice_pdf_path = None
        self.is_generating_invoice = False
        self.invoice_email_sent = False

    @rx.event(background=True)
    async def generate_invoice_details(self):
        async with self:
            if not self.raw_order_data:
                return
            self.is_generating_invoice = True
            import asyncio

            await asyncio.sleep(0.5)
            _raw_data = self.raw_order_data
            self.raw_order_data = None
        _items_data = _raw_data.get("items", [])
        if not isinstance(_items_data, list):
            _items_data = []
        _total_price = float(
            _raw_data.get("total_price", 0.0)
        )
        _subtotal = round(
            _total_price / (1 + self.IVA_RATE), 2
        )
        _vat = round(_total_price - _subtotal, 2)
        _invoice_number = f"INV-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        _cufe = uuid.uuid4().hex
        _invoice_date = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        _customer_name = str(
            _raw_data.get("customer_name", "N/A")
        )
        _customer_address = str(
            _raw_data.get("customer_address", "N/A")
        )
        _customer_email = str(
            _raw_data.get("customer_email", "N/A")
        )
        _customer_document_id = str(
            _raw_data.get("customer_document_id", "N/A")
        )
        _invoice_items = []
        _display_items_temp = []
        for item_data_untyped in _items_data:
            item_data = cast(
                dict[str, Union[str, int, float]],
                item_data_untyped,
            )
            invoice_item_dict = {
                "product_id": int(
                    item_data.get("product_id", 0)
                ),
                "name": str(item_data.get("name", "N/A")),
                "quantity": int(
                    item_data.get("quantity", 0)
                ),
                "price": float(item_data.get("price", 0.0)),
                "image_url": str(
                    item_data.get(
                        "image_url", "/placeholder.svg"
                    )
                ),
                "stock": int(item_data.get("stock", 0)),
            }
            _invoice_items.append(
                InvoiceItem(**invoice_item_dict)
            )
            _display_items_temp.append(invoice_item_dict)
        _current_order_details = OrderDetails(
            customer_name=_customer_name,
            customer_address=_customer_address,
            customer_email=_customer_email,
            customer_document_id=_customer_document_id,
            items=_invoice_items,
            total_price=_total_price,
            invoice_number=_invoice_number,
            cufe=_cufe,
            subtotal=_subtotal,
            vat=_vat,
            invoice_date=_invoice_date,
        )
        async with self:
            self.order_details = _current_order_details
            self.display_items = _display_items_temp
            self.is_generating_invoice = False
        if FPDF_AVAILABLE:
            yield InvoiceState.generate_invoice_pdf()

    @rx.event(background=True)
    async def generate_invoice_pdf(self):
        if not FPDF_AVAILABLE:
            async with self:
                self.invoice_pdf_path = None
            yield rx.toast(
                "FPDF library not found. PDF generation disabled.",
                duration=3000,
            )
            return
        async with self:
            if not self.order_details.invoice_number:
                return
            _details = self.order_details.copy()
            self.is_generating_invoice = True
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        try:
            pdf.add_font(
                "DejaVu",
                "",
                "assets/DejaVuSansCondensed.ttf",
                uni=True,
            )
            pdf.add_font(
                "DejaVu",
                "B",
                "assets/DejaVuSansCondensed-Bold.ttf",
                uni=True,
            )
            font_family = "DejaVu"
        except RuntimeError as e:
            print(
                f"FPDF Font Error: {e}. Using fallback Arial."
            )
            font_family = "Arial"
        pdf.set_font(font_family, "B", 20)
        pdf.set_fill_color(7, 89, 133)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(
            0,
            15,
            "TechStore - Factura Electrónica",
            0,
            1,
            "C",
            fill=True,
        )
        pdf.ln(10)
        pdf.set_font(font_family, "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.set_x(pdf.w - 10 - 60)
        pdf.cell(
            60,
            6,
            f"Factura No: {_details.invoice_number}",
            0,
            1,
            "L",
        )
        pdf.set_x(pdf.w - 10 - 60)
        pdf.cell(
            60,
            6,
            f"Fecha: {_details.invoice_date}",
            0,
            1,
            "L",
        )
        pdf.set_x(pdf.w - 10 - 60)
        pdf.multi_cell(
            60, 6, f"CUFE: {_details.cufe}", 0, "L"
        )
        pdf.set_y(pdf.get_y() - 18)
        pdf.ln(5)
        pdf.set_font(font_family, "B", 12)
        pdf.cell(
            (pdf.w - 20) / 2,
            8,
            "Información del Cliente:",
            0,
            0,
        )
        pdf.ln(8)
        pdf.set_font(font_family, "", 10)
        pdf.cell(
            0, 6, f"Nombre: {_details.customer_name}", 0, 1
        )
        pdf.cell(
            0,
            6,
            f"Dirección: {_details.customer_address}",
            0,
            1,
        )
        pdf.cell(
            0, 6, f"Email: {_details.customer_email}", 0, 1
        )
        pdf.cell(
            0,
            6,
            f"Documento: {_details.customer_document_id}",
            0,
            1,
        )
        pdf.ln(10)
        pdf.set_font(font_family, "B", 11)
        pdf.set_fill_color(224, 236, 249)
        pdf.cell(100, 8, "Producto", 1, 0, "C", fill=True)
        pdf.cell(30, 8, "Cantidad", 1, 0, "C", fill=True)
        pdf.cell(
            30, 8, "Precio Unit.", 1, 0, "C", fill=True
        )
        pdf.cell(30, 8, "Total", 1, 1, "C", fill=True)
        pdf.set_font(font_family, "", 10)
        for item in _details.items:
            pdf.cell(100, 7, item.name, 1)
            pdf.cell(30, 7, item.quantity, 1, 0, "C")
            pdf.cell(30, 7, f"{item.price:,.0f}", 1, 0, "R")
            pdf.cell(
                30,
                7,
                f"{item.price * item.quantity:,.0f}",
                1,
                1,
                "R",
            )
        pdf.ln(10)
        total_y_pos = pdf.get_y()
        pdf.set_x(pdf.w - 10 - 70)
        pdf.set_font(font_family, "B", 10)
        pdf.cell(40, 7, "Subtotal:", 0, 0, "R")
        pdf.set_font(font_family, "", 10)
        pdf.cell(
            30,
            7,
            f"COP {_details.subtotal:,.0f}",
            0,
            1,
            "R",
        )
        pdf.set_x(pdf.w - 10 - 70)
        pdf.set_font(font_family, "B", 10)
        pdf.cell(
            40,
            7,
            f"IVA ({self.IVA_RATE * 100:.0f}%):",
            0,
            0,
            "R",
        )
        pdf.set_font(font_family, "", 10)
        pdf.cell(
            30, 7, f"COP {_details.vat:,.0f}", 0, 1, "R"
        )
        pdf.set_x(pdf.w - 10 - 70)
        pdf.set_font(font_family, "B", 12)
        pdf.cell(40, 8, "TOTAL:", 0, 0, "R")
        pdf.cell(
            30,
            8,
            f"COP {_details.total_price:,.0f}",
            0,
            1,
            "R",
        )
        invoice_dir = "assets/invoices"
        os.makedirs(invoice_dir, exist_ok=True)
        _invoice_pdf_path_local = os.path.join(
            invoice_dir, f"{_details.invoice_number}.pdf"
        )
        try:
            pdf.output(_invoice_pdf_path_local, "F")
            _invoice_pdf_relative_path = (
                f"/invoices/{_details.invoice_number}.pdf"
            )
            async with self:
                self.invoice_pdf_path = (
                    _invoice_pdf_relative_path
                )
                self.is_generating_invoice = False
            yield InvoiceState.send_invoice_email(
                pdf_path=_invoice_pdf_relative_path,
                recipient_email=_details.customer_email,
                invoice_number=_details.invoice_number,
            )
        except Exception as e:
            print(f"Failed to save PDF: {e}")
            async with self:
                self.is_generating_invoice = False
                self.invoice_pdf_path = None

    @rx.event(background=True)
    async def send_invoice_email(
        self,
        pdf_path: str,
        recipient_email: str,
        invoice_number: str,
    ):
        sender_email = os.getenv(
            "SENDER_EMAIL", "noreply@techstore.com"
        )
        smtp_server = os.getenv(
            "SMTP_SERVER", "smtp.example.com"
        )
        if not sender_email or not smtp_server:
            print(
                "Email configuration missing. Skipping email."
            )
            async with self:
                self.invoice_email_sent = False
            yield rx.toast(
                "Configuración de correo incompleta. No se pudo enviar la factura por email.",
                duration=3000,
            )
            return
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = (
            f"Tu factura de TechStore - No. {invoice_number}"
        )
        body = f"Hola,\n\nAdjunto encontrarás tu factura No. {invoice_number} de tu reciente compra en TechStore.\n\nGracias por tu preferencia.\n\nSaludos,\nEl equipo de TechStore"
        msg.attach(MIMEText(body, "plain"))
        actual_pdf_path = os.path.join(
            "assets", pdf_path.lstrip("/")
        )
        try:
            if os.path.exists(actual_pdf_path):
                with open(
                    actual_pdf_path, "rb"
                ) as attachment:
                    part = MIMEApplication(
                        attachment.read(),
                        Name=os.path.basename(
                            actual_pdf_path
                        ),
                    )
                part["Content-Disposition"] = (
                    f'attachment; filename="{os.path.basename(actual_pdf_path)}"'
                )
                msg.attach(part)
            else:
                print(
                    f"PDF file not found at {actual_pdf_path}. Cannot attach to email."
                )
            print(
                f"Simulating sending email with invoice {invoice_number} to {recipient_email}"
            )
            async with self:
                self.invoice_email_sent = True
            yield rx.toast(
                f"Factura (simulada) enviada por correo a {recipient_email}",
                duration=3000,
            )
        except Exception as e:
            print(f"Error preparing or sending email: {e}")
            async with self:
                self.invoice_email_sent = False
            yield rx.toast(
                f"Error al enviar factura por email: {str(e)}",
                duration=4000,
            )

    @rx.event
    def download_invoice(self):
        if self.invoice_pdf_path:
            return rx.download(url=self.invoice_pdf_path)
        else:
            return rx.toast(
                "La factura no está disponible para descargar.",
                duration=3000,
            )

    @rx.event
    def debug_download_info(self):
        info_str = f"\n        Debug Info - Invoice State:\n        Raw Order Data Present: {self.raw_order_data is not None}\n        Order Details Populated: {self.order_details.invoice_number != ''}\n        Invoice Number: {self.order_details.invoice_number}\n        CUFE: {self.order_details.cufe}\n        Total Price: {self.order_details.total_price}\n        Subtotal: {self.order_details.subtotal}\n        VAT: {self.order_details.vat}\n        Items Count: {len(self.order_details.items)}\n        Display Items Count: {len(self.display_items)}\n        Is Generating Invoice: {self.is_generating_invoice}\n        Invoice PDF Path: {self.invoice_pdf_path}\n        FPDF Available: {FPDF_AVAILABLE}\n        Invoice Email Sent: {self.invoice_email_sent}\n        Customer Email: {self.order_details.customer_email}\n        "
        print(info_str)
        yield rx.toast(
            "Información de depuración impresa en la consola.",
            duration=4000,
        )