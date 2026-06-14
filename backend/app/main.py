from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import clients, equipment, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Мини-CRM Спецтехника", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients.router, prefix="/api/clients", tags=["Клиенты"])
app.include_router(equipment.router, prefix="/api/equipment", tags=["Спецтехника"])
app.include_router(orders.router, prefix="/api/orders", tags=["Заявки"])

@app.get("/")
def root():
    return {"message": "CRM API работает"}