import reflex as rx
from sqlmodel import Session, select
from app.database import engine
from app.models.models import (
    Product as ProductModel,
    Review as ReviewModel,
    CartItem,
    DisplayReview,
)
from app.states.cart_state import CartState
from app.states.feedback_state import FeedbackState
from typing import Optional, cast
import datetime


class ProductState(rx.State):
    products: list[ProductModel] = []
    selected_product: Optional[ProductModel] = None
    show_selected_product_modal: bool = False
    selected_product_quantity: int = 1
    search_query: str = ""
    selected_category: str = "All"
    selected_product_reviews: list[DisplayReview] = []

    @rx.event
    def load_products(self):
        with Session(engine) as session:
            self.products = session.exec(
                select(ProductModel).order_by(
                    ProductModel.name
                )
            ).all()
            if not self.products:
                default_products_data = [
                    {
                        "name": "Laptop Pro X1",
                        "description": "Potente laptop para profesionales y creativos, con chip M3.",
                        "price": 4500000,
                        "image_url": "/placeholder.svg",
                        "category": "Portátiles",
                        "stock": 15,
                    },
                    {
                        "name": "Smartphone Galaxy S25 Ultra",
                        "description": "El último smartphone con cámara IA de 200MP y pantalla AMOLED dinámica.",
                        "price": 5200000,
                        "image_url": "/placeholder.svg",
                        "category": "Celulares",
                        "stock": 25,
                    },
                    {
                        "name": "Auriculares Quantum Sound Pro",
                        "description": "Auriculares con cancelación de ruido adaptativa y sonido Hi-Fi espacial.",
                        "price": 950000,
                        "image_url": "/placeholder.svg",
                        "category": "Audio",
                        "stock": 30,
                    },
                    {
                        "name": "Smartwatch Vitality Fit 3",
                        "description": "Reloj inteligente con monitoreo de salud avanzado, ECG y GPS.",
                        "price": 1350000,
                        "image_url": "/placeholder.svg",
                        "category": "Wearables",
                        "stock": 20,
                    },
                    {
                        "name": "Tablet DrawPad Pro 11",
                        "description": "Tablet con pantalla Liquid Retina XDR, ideal para diseño gráfico y ProMotion.",
                        "price": 3100000,
                        "image_url": "/placeholder.svg",
                        "category": "Tablets",
                        "stock": 10,
                    },
                    {
                        "name": "Teclado Mecánico RGB K-Force Elite",
                        "description": "Teclado gamer inalámbrico con switches ópticos personalizables e iluminación RGB por tecla.",
                        "price": 650000,
                        "image_url": "/placeholder.svg",
                        "category": "Periféricos",
                        "stock": 40,
                    },
                    {
                        "name": "Mouse Ergonómico ProGlide Vertical",
                        "description": "Mouse vertical diseñado para reducir la tensión y mejorar la postura.",
                        "price": 320000,
                        "image_url": "/placeholder.svg",
                        "category": "Periféricos",
                        "stock": 50,
                    },
                    {
                        "name": "Monitor UltraWide 34'' QHD OLED",
                        "description": "Monitor curvo OLED para negros perfectos y colores vibrantes, 165Hz.",
                        "price": 4800000,
                        "image_url": "/placeholder.svg",
                        "category": "Monitores",
                        "stock": 12,
                    },
                    {
                        "name": "Cámara Mirrorless Alpha Z",
                        "description": "Cámara full-frame con sensor de 50MP y video 8K.",
                        "price": 12500000,
                        "image_url": "/placeholder.svg",
                        "category": "Cámaras",
                        "stock": 8,
                    },
                    {
                        "name": "Drone Explorer Pro 4K",
                        "description": "Drone con cámara 4K, gimbal de 3 ejes y 30 min de vuelo.",
                        "price": 3800000,
                        "image_url": "/placeholder.svg",
                        "category": "Drones",
                        "stock": 18,
                    },
                    {
                        "name": "Proyector CineHome X500",
                        "description": "Proyector 4K nativo con HDR10+ y 3000 lúmenes.",
                        "price": 6200000,
                        "image_url": "/placeholder.svg",
                        "category": "Proyectores",
                        "stock": 7,
                    },
                    {
                        "name": "SSD NVMe FireStorm 2TB",
                        "description": "Unidad de estado sólido ultrarrápida, Gen4, hasta 7000MB/s.",
                        "price": 900000,
                        "image_url": "/placeholder.svg",
                        "category": "Almacenamiento",
                        "stock": 35,
                    },
                    {
                        "name": "Memoria RAM Vengeance DDR5 32GB",
                        "description": "Kit de memoria RAM DDR5 6000MHz (2x16GB) para alto rendimiento.",
                        "price": 700000,
                        "image_url": "/placeholder.svg",
                        "category": "Componentes PC",
                        "stock": 22,
                    },
                    {
                        "name": "Router WiFi 6E Mesh System",
                        "description": "Sistema Mesh de 3 nodos para cobertura total y velocidades gigabit.",
                        "price": 1500000,
                        "image_url": "/placeholder.svg",
                        "category": "Redes",
                        "stock": 15,
                    },
                    {
                        "name": "Impresora Multifuncional EcoTank L500",
                        "description": "Impresora con tanques de tinta de alta capacidad, WiFi y dúplex.",
                        "price": 1100000,
                        "image_url": "/placeholder.svg",
                        "category": "Impresoras",
                        "stock": 19,
                    },
                    {
                        "name": "Altavoz Inteligente EchoSphere",
                        "description": "Altavoz con asistente virtual, sonido 360 y control de hogar.",
                        "price": 480000,
                        "image_url": "/placeholder.svg",
                        "category": "Hogar Inteligente",
                        "stock": 28,
                    },
                    {
                        "name": "Webcam ProStream 4K",
                        "description": "Webcam con sensor 4K, autoenfoque y micrófonos duales.",
                        "price": 600000,
                        "image_url": "/placeholder.svg",
                        "category": "Periféricos",
                        "stock": 33,
                    },
                    {
                        "name": "Consola de Videojuegos NextGen X",
                        "description": "La última generación en consolas, con gráficos 8K y SSD ultrarrápido.",
                        "price": 2900000,
                        "image_url": "/placeholder.svg",
                        "category": "Videojuegos",
                        "stock": 10,
                    },
                    {
                        "name": "Silla Gamer ErgoMax Pro",
                        "description": "Silla ergonómica con soporte lumbar ajustable y materiales premium.",
                        "price": 1300000,
                        "image_url": "/placeholder.svg",
                        "category": "Muebles Tech",
                        "stock": 14,
                    },
                    {
                        "name": "Power Bank Solar 30000mAh",
                        "description": "Batería externa de alta capacidad con panel solar integrado.",
                        "price": 250000,
                        "image_url": "/placeholder.svg",
                        "category": "Accesorios",
                        "stock": 40,
                    },
                    {
                        "name": "Lector de Ebooks PaperGlow 7",
                        "description": "Lector con pantalla E-ink de 7 pulgadas, luz cálida y resistente al agua.",
                        "price": 700000,
                        "image_url": "/placeholder.svg",
                        "category": "Lectores",
                        "stock": 20,
                    },
                    {
                        "name": "Tarjeta Gráfica RTX 5080",
                        "description": "Potente GPU para gaming y creación de contenido en 4K/8K.",
                        "price": 5500000,
                        "image_url": "/placeholder.svg",
                        "category": "Componentes PC",
                        "stock": 5,
                    },
                    {
                        "name": "Micrófono de Condensador Studio Pro",
                        "description": "Micrófono USB para podcasting, streaming y grabación de voz.",
                        "price": 550000,
                        "image_url": "/placeholder.svg",
                        "category": "Audio",
                        "stock": 26,
                    },
                    {
                        "name": "Hub USB-C 10-en-1 HyperPort",
                        "description": "Adaptador multipuerto con HDMI 4K, Ethernet, USB 3.0, PD.",
                        "price": 280000,
                        "image_url": "/placeholder.svg",
                        "category": "Accesorios",
                        "stock": 38,
                    },
                    {
                        "name": "Gafas VR Quantum Rift 2",
                        "description": "Gafas de realidad virtual de alta resolución con seguimiento inside-out.",
                        "price": 2200000,
                        "image_url": "/placeholder.svg",
                        "category": "VR/AR",
                        "stock": 9,
                    },
                    {
                        "name": "Sistema de Sonido SoundBar Atmos 5.1",
                        "description": "Barra de sonido con subwoofer inalámbrico y Dolby Atmos.",
                        "price": 1800000,
                        "image_url": "/placeholder.svg",
                        "category": "Audio",
                        "stock": 13,
                    },
                    {
                        "name": "Disco Duro Externo ArmorShield 4TB",
                        "description": "Disco duro portátil resistente a golpes y agua, USB 3.2.",
                        "price": 600000,
                        "image_url": "/placeholder.svg",
                        "category": "Almacenamiento",
                        "stock": 24,
                    },
                    {
                        "name": "NAS Synology DS225+",
                        "description": "Servidor NAS de 2 bahías para nube privada y copias de seguridad.",
                        "price": 1700000,
                        "image_url": "/placeholder.svg",
                        "category": "Redes",
                        "stock": 11,
                    },
                    {
                        "name": "Teclado Inalámbrico ErgoWave",
                        "description": "Teclado ergonómico dividido con reposamuñecas integrado.",
                        "price": 420000,
                        "image_url": "/placeholder.svg",
                        "category": "Periféricos",
                        "stock": 17,
                    },
                    {
                        "name": "Purificador de Aire SmartClean Pro",
                        "description": "Purificador con filtro HEPA, carbón activado y control por app.",
                        "price": 950000,
                        "image_url": "/placeholder.svg",
                        "category": "Hogar Inteligente",
                        "stock": 16,
                    },
                    {
                        "name": "Luz LED Inteligente ColorHue Strip",
                        "description": "Tira LED RGBIC de 5m, compatible con Alexa/Google Home.",
                        "price": 180000,
                        "image_url": "/placeholder.svg",
                        "category": "Hogar Inteligente",
                        "stock": 45,
                    },
                    {
                        "name": "Mochila TechTravel Anti-robo",
                        "description": "Mochila para laptop de hasta 17'' con puerto USB y diseño seguro.",
                        "price": 350000,
                        "image_url": "/placeholder.svg",
                        "category": "Accesorios",
                        "stock": 23,
                    },
                    {
                        "name": "Smartphone Pixel Fold 2",
                        "description": "Teléfono plegable con pantalla interna de 7.8 pulgadas y software optimizado.",
                        "price": 7500000,
                        "image_url": "/placeholder.svg",
                        "category": "Celulares",
                        "stock": 7,
                    },
                    {
                        "name": "Audífonos In-Ear TrueWireless Elite 8",
                        "description": "Audífonos TWS con ANC, Bluetooth 5.3 y estuche de carga inalámbrica.",
                        "price": 680000,
                        "image_url": "/placeholder.svg",
                        "category": "Audio",
                        "stock": 29,
                    },
                    {
                        "name": "Smart Display HomeHub Max",
                        "description": "Pantalla inteligente de 10'' con cámara para videollamadas y control del hogar.",
                        "price": 900000,
                        "image_url": "/placeholder.svg",
                        "category": "Hogar Inteligente",
                        "stock": 18,
                    },
                    {
                        "name": "Monitor Gamer Curvo 27'' 2K 240Hz",
                        "description": "Monitor de 27 pulgadas, resolución QHD, 240Hz y 1ms de respuesta.",
                        "price": 2100000,
                        "image_url": "/placeholder.svg",
                        "category": "Monitores",
                        "stock": 14,
                    },
                    {
                        "name": "Laptop Gamer Titan X",
                        "description": "Laptop para juegos con GPU RTX 5090 y CPU Core i9 de última generación.",
                        "price": 11500000,
                        "image_url": "/placeholder.svg",
                        "category": "Portátiles",
                        "stock": 6,
                    },
                    {
                        "name": "Docking Station Thunderbolt 4 Pro",
                        "description": "Estación de acoplamiento con múltiples puertos Thunderbolt 4, USB-A, HDMI y Ethernet.",
                        "price": 1200000,
                        "image_url": "/placeholder.svg",
                        "category": "Accesorios",
                        "stock": 10,
                    },
                ]
                for prod_data in default_products_data:
                    session.add(ProductModel(**prod_data))
                session.commit()
                self.products = session.exec(
                    select(ProductModel).order_by(
                        ProductModel.name
                    )
                ).all()
        yield

    @rx.event
    def load_reviews_for_selected_product(
        self, product_id: int
    ):
        with Session(engine) as session:
            reviews_db = session.exec(
                select(ReviewModel)
                .where(ReviewModel.product_id == product_id)
                .order_by(ReviewModel.created_at.desc())
            ).all()
            self.selected_product_reviews = [
                DisplayReview(
                    id=review.id,
                    product_id=review.product_id,
                    reviewer_name=review.reviewer_name,
                    rating=review.rating,
                    comment=review.comment,
                    image_url=review.image_url,
                    created_at_formatted=review.created_at.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                )
                for review in reviews_db
                if review.id is not None
            ]
        yield FeedbackState.set_selected_product_for_review(
            product_id
        )

    @rx.event
    def select_product(self, product: ProductModel):
        self.selected_product = product
        self.selected_product_quantity = 1
        self.show_selected_product_modal = True
        if product and product.id is not None:
            yield ProductState.load_reviews_for_selected_product(
                cast(int, product.id)
            )
        else:
            self.selected_product_reviews = []
            yield FeedbackState.set_selected_product_for_review(
                None
            )

    @rx.event
    def close_selected_product_modal(self):
        self.show_selected_product_modal = False
        self.selected_product = None
        self.selected_product_reviews = []
        yield FeedbackState.set_selected_product_for_review(
            None
        )

    @rx.event
    def set_selected_product_quantity(
        self, quantity_str: str
    ):
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                self.selected_product_quantity = 1
            elif (
                self.selected_product
                and quantity > self.selected_product.stock
            ):
                self.selected_product_quantity = (
                    self.selected_product.stock
                )
                yield rx.toast(
                    f"Máximo stock disponible: {self.selected_product.stock}",
                    duration=2000,
                )
            else:
                self.selected_product_quantity = quantity
        except ValueError:
            self.selected_product_quantity = 1

    @rx.event
    async def add_selected_to_cart(self):
        if (
            self.selected_product
            and self.selected_product_quantity > 0
        ):
            cart_s = await self.get_state(CartState)
            if self.selected_product.id is None:
                yield rx.toast(
                    "Error: ID de producto no válido.",
                    duration=3000,
                )
                return
            product_data = {
                "product_id": self.selected_product.id,
                "name": self.selected_product.name,
                "price": self.selected_product.price,
                "quantity": self.selected_product_quantity,
                "image_url": self.selected_product.image_url,
                "stock": self.selected_product.stock,
            }
            yield CartState.add_item(
                product_data, self.selected_product_quantity
            )

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_selected_category(self, category: str):
        self.selected_category = category

    @rx.var
    def categories(self) -> list[str]:
        if not self.products:
            return ["All"]
        unique_categories = {"All"}
        for product in self.products:
            unique_categories.add(product.category)
        return sorted(list(unique_categories))

    @rx.var
    def filtered_products(self) -> list[ProductModel]:
        if not self.products:
            return []
        products_to_filter = self.products
        if self.selected_category != "All":
            products_to_filter = [
                p
                for p in products_to_filter
                if p.category == self.selected_category
            ]
        if self.search_query:
            query = self.search_query.lower()
            products_to_filter = [
                p
                for p in products_to_filter
                if query in p.name.lower()
            ]
        return products_to_filter

    @rx.var
    def products_by_category(
        self,
    ) -> dict[str, list[ProductModel]]:
        categorized = {}
        for product in self.filtered_products:
            if product.category not in categorized:
                categorized[product.category] = []
            categorized[product.category].append(product)
        return categorized

    @rx.var
    def products_by_category_keys(self) -> list[str]:
        return list(self.products_by_category.keys())

    @rx.event(background=True)
    async def refresh_selected_product_reviews(self):
        if (
            self.selected_product
            and self.selected_product.id is not None
        ):
            async with self:
                pass
            yield ProductState.load_reviews_for_selected_product(
                cast(int, self.selected_product.id)
            )