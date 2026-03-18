from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    did = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    owner_id = Column(Integer)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    buyer_id = Column(Integer)
    seller_id = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Seed data
def seed_data():
    db = SessionLocal()
    if not db.query(User).first():
        user1 = User(name="Alice", did="did:example:123", email="alice@example.com")
        user2 = User(name="Bob", did="did:example:456", email="bob@example.com")
        db.add(user1)
        db.add(user2)
        db.commit()

    if not db.query(Product).first():
        product1 = Product(name="Laptop", description="A powerful laptop", price=999.99, owner_id=1)
        product2 = Product(name="Smartphone", description="A modern smartphone", price=499.99, owner_id=2)
        db.add(product1)
        db.add(product2)
        db.commit()

    if not db.query(Transaction).first():
        transaction1 = Transaction(product_id=1, buyer_id=2, seller_id=1)
        transaction2 = Transaction(product_id=2, buyer_id=1, seller_id=2)
        db.add(transaction1)
        db.add(transaction2)
        db.commit()

    db.close()

seed_data()

# Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_home(request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def read_profile(request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/products", response_class=HTMLResponse)
async def read_products(request):
    return templates.TemplateResponse("products.html", {"request": request})

@app.get("/product/{id}", response_class=HTMLResponse)
async def read_product_detail(request, id: int):
    return templates.TemplateResponse("product_detail.html", {"request": request, "id": id})

@app.get("/transactions", response_class=HTMLResponse)
async def read_transactions(request):
    return templates.TemplateResponse("transactions.html", {"request": request})

@app.get("/api/users")
async def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@app.post("/api/users")
async def create_user(user: User):
    db = SessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@app.get("/api/products")
async def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.get("/api/transactions")
async def get_transactions():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    db.close()
    return transactions

