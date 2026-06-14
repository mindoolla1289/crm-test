"""Заполняет базу тестовыми данными при первом запуске."""
from app.database import SessionLocal, engine, Base
from app.models.models import Client, Equipment, Order, OrderStatus

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if db.query(Client).count() == 0:
    clients = [
        Client(name="Иванов Алексей Петрович", phone="+7 701 123 45 67", email="ivanov@mail.ru"),
        Client(name="ТОО «СтройМаш»", phone="+7 727 234 56 78", email="info@stroymash.kz"),
        Client(name="Петренко Сергей Николаевич", phone="+7 705 987 65 43"),
    ]
    db.add_all(clients)
    db.commit()

if db.query(Equipment).count() == 0:
    equipment = [
        Equipment(name="Экскаватор KOMATSU PC200", category="Земляные работы", description="Гусеничный экскаватор 20 тонн"),
        Equipment(name="Автокран XCMG QY25K5", category="Грузоподъёмная техника", description="Автокран 25 тонн"),
        Equipment(name="Бульдозер CAT D6T", category="Земляные работы", description="Гусеничный бульдозер"),
        Equipment(name="Самосвал КАМАЗ 65115", category="Грузовой транспорт", description="Самосвал 15 куб.м"),
        Equipment(name="Вибрационный каток BOMAG BW213", category="Дорожные работы", description="Грунтовый каток"),
    ]
    db.add_all(equipment)
    db.commit()

if db.query(Order).count() == 0:
    orders = [
        Order(client_id=1, equipment_id=1, comment="Нужен экскаватор на 3 дня для рытья котлована", status=OrderStatus.new),
        Order(client_id=2, equipment_id=2, comment="Монтаж металлоконструкций, высота 12м", status=OrderStatus.in_progress),
        Order(client_id=3, equipment_id=4, comment="Вывоз грунта, 5 рейсов", status=OrderStatus.completed),
        Order(client_id=1, equipment_id=3, comment="Планировка участка 2 га", status=OrderStatus.new),
        Order(client_id=2, equipment_id=5, comment="Уплотнение основания под дорогу", status=OrderStatus.in_progress),
    ]
    db.add_all(orders)
    db.commit()
    print("✅ Тестовые данные загружены")
else:
    print("ℹ️  База данных уже заполнена")

db.close()