# Bu script initialProducts ni bir marta backendga yuklaydi
# Ishlatish: python migrate_products.py
# Joyi: backend/ papkasida (app/ bilan bir qatorda)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.product import Product

# Jadvallarni yaratish (yo'q bo'lsa)
Base.metadata.create_all(bind=engine)

products = [
    {
        "name_uz": "Qo'lda chizilgan manzara rasmi",
        "name_ru": "Пейзаж акварелью",
        "desc_uz": "Akvarel bo'yoqda chizilgan, ramkaga joylangan chiroyli manzara rasmi. O'lchami 30x40 sm.",
        "desc_ru": "Красивый пейзаж, нарисованный акварелью в рамке. Размер 30x40 см.",
        "price": 80000, "stock": 1, "category": "paintings",
        "author": "Dilnoza Yusupova", "class_uz": "8-sinf", "class_ru": "8-класс",
        "image": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=500&q=80",
        "is_new": True,
    },
    {
        "name_uz": "Qog'ozdan yasalgan gullar",
        "name_ru": "Цветы из бумаги",
        "desc_uz": "Origami texnikasida yasalgan rangli qog'oz gullar to'plami. 10 ta gul.",
        "desc_ru": "Набор цветных бумажных цветов в технике оригами. 10 штук.",
        "price": 35000, "stock": 5, "category": "crafts",
        "author": "Sardor Mirzayev", "class_uz": "6-sinf", "class_ru": "6-класс",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80",
        "is_new": True,
    },
    {
        "name_uz": "Tikuvli kostyum (bolalar uchun)",
        "name_ru": "Детский вышитый костюм",
        "desc_uz": "O'zbek milliy naqshlari bilan bezatilgan bolalar milliy kostyumi. 3-5 yosh uchun.",
        "desc_ru": "Детский национальный костюм с узбекскими орнаментами. Для детей 3-5 лет.",
        "price": 250000, "stock": 2, "category": "clothes",
        "author": "Malika Toshmatova", "class_uz": "10-sinf", "class_ru": "10-класс",
        "image": "https://images.unsplash.com/photo-1606293926075-69a00dbfde81?w=500&q=80",
        "is_new": False,
    },
    {
        "name_uz": "Sopol idish — qo'lda ishlangan",
        "name_ru": "Керамическая ваза ручной работы",
        "desc_uz": "Gildan yasalgan va bo'yalgan noyob sopol idish. Balandligi 20 sm.",
        "desc_ru": "Уникальная керамическая ваза, расписанная вручную. Высота 20 см.",
        "price": 120000, "stock": 3, "category": "souvenirs",
        "author": "Jasur Qodirov", "class_uz": "9-sinf", "class_ru": "9-класс",
        "image": "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=500&q=80",
        "is_new": False,
    },
    {
        "name_uz": "Yangi yil bezaklari to'plami",
        "name_ru": "Набор новогодних украшений",
        "desc_uz": "Qo'lda ishlangan 12 ta yangi yil bezaklari to'plami.",
        "desc_ru": "Набор из 12 новогодних украшений ручной работы.",
        "price": 90000, "stock": 8, "category": "holiday",
        "author": "Nozima Aliyeva", "class_uz": "7-sinf", "class_ru": "7-класс",
        "image": "https://images.unsplash.com/photo-1512389142860-9c449e58a543?w=500&q=80",
        "is_new": True,
    },
    {
        "name_uz": "Portret rasmi (buyurtma bo'yicha)",
        "name_ru": "Портрет на заказ",
        "desc_uz": "Fotosuratingiz asosida chizilgan portret rasmi. Ishlash muddati 3-5 kun.",
        "desc_ru": "Портрет, нарисованный по вашей фотографии. Срок 3-5 дней.",
        "price": 150000, "stock": 10, "category": "custom",
        "author": "Umid Rahimov", "class_uz": "11-sinf", "class_ru": "11-класс",
        "image": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=500&q=80",
        "is_new": False,
    },
    {
        "name_uz": "Yumshoq o'yinchoq — ayiqcha",
        "name_ru": "Мягкая игрушка — мишка",
        "desc_uz": "Qo'lda tikilgan yumshoq ayiqcha o'yinchoq. Balandligi 30 sm.",
        "desc_ru": "Мягкая игрушка мишка ручной работы. Высота 30 см.",
        "price": 75000, "stock": 4, "category": "toys",
        "author": "Shahlo Tursunova", "class_uz": "8-sinf", "class_ru": "8-класс",
        "image": "https://images.unsplash.com/photo-1559454403-b8fb88521f11?w=500&q=80",
        "is_new": True,
    },
    {
        "name_uz": "O'zbek tili lug'ati — qo'lda yozilgan",
        "name_ru": "Словарь узбекского языка",
        "desc_uz": "O'quvchi tomonidan tuzilgan qo'lda yozilgan O'zbek tili lug'ati.",
        "desc_ru": "Рукописный словарь узбекского языка, составленный учеником.",
        "price": 45000, "stock": 3, "category": "education",
        "author": "Barno Qosimova", "class_uz": "9-sinf", "class_ru": "9-класс",
        "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500&q=80",
        "is_new": False,
    },
    {
        "name_uz": "Logotip dizayni (raqamli)",
        "name_ru": "Дизайн логотипа (цифровой)",
        "desc_uz": "Biznesingiz uchun professional logotip dizayni. Format: PNG, SVG, PDF.",
        "desc_ru": "Профессиональный дизайн логотипа. Форматы: PNG, SVG, PDF.",
        "price": 200000, "stock": 20, "category": "digital",
        "author": "Otabek Yodgorov", "class_uz": "10-sinf", "class_ru": "10-класс",
        "image": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=500&q=80",
        "is_new": True,
    },
    {
        "name_uz": "Rasm darsi (online xizmat)",
        "name_ru": "Урок рисования (онлайн)",
        "desc_uz": "Online rasm darsi. 1 soatlik individual dars. Zoom orqali.",
        "desc_ru": "Онлайн урок рисования. 1 час индивидуально. Через Zoom.",
        "price": 50000, "stock": 15, "category": "services",
        "author": "Feruza Sobirov", "class_uz": "11-sinf", "class_ru": "11-класс",
        "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500&q=80",
        "is_new": False,
    },
    {
        "name_uz": "Ilmiy loyiha — quyosh energiyasi",
        "name_ru": "Научный проект — солнечная энергия",
        "desc_uz": "Maktab ilmiy ko'rgazmasi uchun tayyor qilingan quyosh energiyasi modeli.",
        "desc_ru": "Модель солнечной энергии для школьной выставки.",
        "price": 180000, "stock": 1, "category": "projects",
        "author": "Jasur Toshev", "class_uz": "10-sinf", "class_ru": "10-класс",
        "image": "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=500&q=80",
        "is_new": True,
    },
    {
        "name_uz": "Tabiiy sovun — lavanda",
        "name_ru": "Натуральное мыло — лаванда",
        "desc_uz": "Tabiiy ingredientlardan qo'lda tayyorlangan lavanda xushbo'y sovuni.",
        "desc_ru": "Натуральное мыло с лавандой, приготовленное вручную.",
        "price": 25000, "stock": 12, "category": "eco",
        "author": "Maftuna Xasanova", "class_uz": "7-sinf", "class_ru": "7-класс",
        "image": "https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=500&q=80",
        "is_new": False,
    },
]


def migrate():
    db = SessionLocal()
    try:
        existing = db.query(Product).count()
        if existing > 0:
            print(f"⚠️  Bazada allaqachon {existing} ta mahsulot bor. O'tkazib yuborildi.")
            return

        for p in products:
            product = Product(**p)
            db.add(product)

        db.commit()
        print(f"✅  {len(products)} ta mahsulot muvaffaqiyatli qo'shildi!")

    except Exception as e:
        db.rollback()
        print(f"❌  Xato: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    migrate()