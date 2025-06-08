import reflex as rx
from app.models.models import Purchase, PurchaseItem
from sqlmodel import Session, select, func
from app.database import engine


class AdminStatsState(rx.State):
    product_purchase_summary: list[dict] = []

    @rx.event(background=True)
    async def load_sales_summary(self):
        summary: dict[int, dict] = {}
        with Session(engine) as session:
            purchase_items = session.exec(
                select(PurchaseItem)
            ).all()
            for item in purchase_items:
                pid = item.product_id
                if pid not in summary:
                    summary[pid] = {
                        "name": item.name,
                        "total_sold": 0,
                        "total_revenue": 0.0,
                    }
                summary[pid]["total_sold"] += item.quantity
                summary[pid]["total_revenue"] += (
                    item.quantity * item.price_at_sale
                )
        summary_list = [
            {
                "product_id": pid,
                "name": data["name"],
                "total_sold": data["total_sold"],
                "total_revenue": round(
                    data["total_revenue"], 2
                ),
            }
            for pid, data in summary.items()
        ]
        summary_list.sort(
            key=lambda x: x["total_sold"], reverse=True
        )
        async with self:
            self.product_purchase_summary = summary_list

    @rx.var
    def chart_data(self) -> list[dict[str, str | int]]:
        return [
            {
                "name": item["name"],
                "Vendidos": item["total_sold"],
            }
            for item in self.product_purchase_summary
        ]