from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from coffee_pos.db import Base, MenuItem, Order, OrderItem, engine, get_session

Money = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]
DB = Annotated[Session, Depends(get_session)]


class MenuItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: Money


class MenuItemOut(MenuItemIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class OrderLineIn(BaseModel):
    menu_item_id: int
    quantity: int = Field(ge=1, le=100)


class OrderIn(BaseModel):
    items: list[OrderLineIn] = Field(min_length=1, max_length=50)


class OrderLineOut(OrderLineIn):
    model_config = ConfigDict(from_attributes=True)
    unit_price: Money


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    total: Money
    items: list[OrderLineOut]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # shortcut: create_all instead of migrations; switch to Alembic once the schema changes after deploy
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Coffee POS", lifespan=lifespan)
Instrumentator().instrument(app).expose(app, include_in_schema=False)


@app.get("/health")
def health(db: DB, response: Response):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        response.status_code = 503
        return {"status": "db_unavailable"}
    return {"status": "ok"}


@app.get("/menu", response_model=list[MenuItemOut])
def list_menu(db: DB):
    return db.scalars(select(MenuItem).order_by(MenuItem.id)).all()


@app.post("/menu", response_model=MenuItemOut, status_code=201)
def create_menu_item(body: MenuItemIn, db: DB):
    item = MenuItem(**body.model_dump())
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Menu item name already exists") from None
    return item


@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(body: OrderIn, db: DB):
    ids = {line.menu_item_id for line in body.items}
    prices = {i: p for i, p in db.execute(select(MenuItem.id, MenuItem.price).where(MenuItem.id.in_(ids)))}
    if missing := ids - prices.keys():
        raise HTTPException(404, f"Menu item(s) not found: {sorted(missing)}")
    lines = [
        OrderItem(menu_item_id=x.menu_item_id, quantity=x.quantity, unit_price=prices[x.menu_item_id])
        for x in body.items
    ]
    order = Order(items=lines, total=sum((li.unit_price * li.quantity for li in lines), Decimal("0")))
    db.add(order)
    db.commit()
    return order


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: DB):
    if order := db.get(Order, order_id):
        return order
    raise HTTPException(404, "Order not found")
