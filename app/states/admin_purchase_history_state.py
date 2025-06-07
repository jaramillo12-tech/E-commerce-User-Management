import reflex as rx
from typing import Optional
from app.states.admin_stats_state import (
    AdminStatsState,
    SalesRecord,
)
from app.states.invoice_state import InvoiceState
import datetime
import os

try:
    from fpdf import FPDF

    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False


class PurchaseGroup(rx.Base):
    timestamp: float
    customer_name: str
    customer_email: str
    total_amount: float
    items: list[SalesRecord]
    invoice_path: Optional[str] = None


class AdminPurchaseHistoryState(rx.State):
    purchase_groups: list[PurchaseGroup] = []
    selected_purchase_invoice_url: Optional[str] = None

    @rx.event(background=True)
    async def load_purchase_history(self):
        sales_records_local = []
        async with self:
            admin_stats_s = await self.get_state(
                AdminStatsState
            )
            sales_records_local = list(
                admin_stats_s.sales_records
            )
        grouped_sales: dict[float, list[SalesRecord]] = {}
        for record in sales_records_local:
            if record.timestamp not in grouped_sales:
                grouped_sales[record.timestamp] = []
            grouped_sales[record.timestamp].append(record)
        _purchase_groups = []
        for ts, records_list in grouped_sales.items():
            total = sum(
                (
                    r.quantity_sold * r.price_at_sale
                    for r in records_list
                )
            )
            invoice_filename = f"ORDER_{datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')}.pdf"
            invoice_path = os.path.join(
                "assets/invoices", invoice_filename
            )
            relative_invoice_path = (
                f"/invoices/{invoice_filename}"
            )
            if (
                not os.path.exists(invoice_path)
                and FPDF_AVAILABLE
            ):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(
                    0,
                    10,
                    f"Factura Pedido - {datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')}",
                    0,
                    1,
                    "C",
                )
                pdf.set_font("Arial", "", 10)
                for item_record in records_list:
                    pdf.cell(
                        0,
                        7,
                        f"{item_record.name} - Cant: {item_record.quantity_sold} - Precio: {item_record.price_at_sale:,.0f} COP - Total: {item_record.quantity_sold * item_record.price_at_sale:,.0f} COP",
                        0,
                        1,
                    )
                pdf.cell(
                    0,
                    10,
                    f"Total Pedido: {total:,.0f} COP",
                    0,
                    1,
                    "R",
                )
                os.makedirs(
                    os.path.dirname(invoice_path),
                    exist_ok=True,
                )
                try:
                    pdf.output(invoice_path, "F")
                except Exception as e:
                    print(
                        f"Error generating admin invoice PDF for {invoice_filename}: {e}"
                    )
                    relative_invoice_path = None
            elif not FPDF_AVAILABLE:
                relative_invoice_path = None
            _purchase_groups.append(
                PurchaseGroup(
                    timestamp=ts,
                    customer_name="Cliente Placeholder",
                    customer_email="email@placeholder.com",
                    total_amount=total,
                    items=records_list,
                    invoice_path=(
                        relative_invoice_path
                        if os.path.exists(invoice_path)
                        else None
                    ),
                )
            )
        _purchase_groups.sort(
            key=lambda x: x.timestamp, reverse=True
        )
        async with self:
            self.purchase_groups = _purchase_groups
        yield

    @rx.event
    def view_invoice_pdf(self, invoice_url: str):
        self.selected_purchase_invoice_url = invoice_url
        yield rx.redirect(invoice_url, external=True)

    @rx.var
    def formatted_purchase_groups(self) -> list[dict]:
        return [
            {
                "id": pg.timestamp,
                "date": datetime.datetime.fromtimestamp(
                    pg.timestamp
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "customer": pg.customer_name,
                "email": pg.customer_email,
                "total": f"{pg.total_amount:,.0f} COP",
                "item_count": sum(
                    (
                        item.quantity_sold
                        for item in pg.items
                    )
                ),
                "invoice_available": pg.invoice_path
                is not None,
                "invoice_url": pg.invoice_path,
            }
            for pg in self.purchase_groups
        ]