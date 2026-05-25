from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from typing import List
from app.email_utils import send_email

router = APIRouter(prefix="/customer", tags=["Customer"])

# ---------------------------
# DB Dependency
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Register / Login
# ---------------------------
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.role != "customer":
        raise HTTPException(status_code=403, detail="Invalid role for customer registration")
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        role="customer",
        status="active"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Customer registered successfully", "user_id": new_user.id}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or user.password != db_user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_user.role != "customer":
        raise HTTPException(status_code=403, detail="Unauthorized")

    return {"message": "Login successful", "user_id": db_user.id}

# ---------------------------
# Cities / Retailers / Products
# ---------------------------
@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    locations = db.query(models.Retailer.location).distinct().all()
    return {"cities": [loc[0] for loc in locations]}

@router.get("/retailers/{city}")
def get_retailers_by_city(city: str, db: Session = Depends(get_db)):
    shops = db.query(models.Retailer).filter(models.Retailer.location == city).all()
    return [{"id": s.id, "name": s.name} for s in shops]

@router.get("/products/{retailer_id}", response_model=list[schemas.ProductOut])
def get_products(retailer_id: int, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.retailer_id == retailer_id).all()
    return [p for p in products if p.price is not None and p.category is not None]

# ---------------------------
# Place Order (fixed version)
# ---------------------------
@router.post("/order")
def place_multiple_orders(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Handles placing a new order for a customer with multiple order items.
    Updates inventory, creates order + order items, sends email + Telegram notifications.
    """

    try:
        print("📩 Received Order Payload:", order.dict())
        total = 0

        # ✅ Step 1: Create Order entry first
        new_order = models.Order(
            customer_id=order.customer_id,
            retailer_id=order.retailer_id,
            address_id=order.address_id,
            total_price=0.0,
            status="placed",
            payment_status="pending"
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # ✅ Step 2: Add each order item
        for item in order.order_items:
            product = db.query(models.Product).filter(
                models.Product.id == item.product_id,
                models.Product.retailer_id == order.retailer_id
            ).first()

            if not product:
                raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")
            if product.quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

            product.quantity -= item.quantity
            subtotal = item.price * item.quantity
            total += subtotal

            order_item = models.OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )
            db.add(order_item)

        # ✅ Step 3: Update total after adding all items
        new_order.total_price = total
        db.commit()

        # ✅ Step 4: Add retailer notification
        notification = models.Notification(
            retailer_id=order.retailer_id,
            user_id=order.customer_id,
            message=f"New order #{new_order.id} placed — Total ₹{total:.2f}"
        )
        db.add(notification)
        db.commit()

        # ✅ Step 5: Send Telegram update
        from app.utils import telegram_utils
        try:
            telegram_data = {
                "order_no": f"ORD-{new_order.id}",
                "customer_id": order.customer_id,
                "retailer_id": order.retailer_id,
                "total": total,
                "address_id": order.address_id,
                "status": "Placed",
                "items": [
                    {
                        "product_id": i.product_id,
                        "quantity": i.quantity,
                        "price": i.price
                    } for i in order.order_items
                ]
            }
            telegram_utils.send_telegram_notification(telegram_data)
        except Exception as tg_err:
            print("⚠️ Telegram notification failed:", tg_err)

        # ✅ Step 6: Send confirmation email (non-blocking)
        try:
            send_email(
                to_email="bsarathy2241@gmail.com",
                subject="Your Smart Market Order Confirmation",
                body=f"Your order #{new_order.id} has been placed successfully.\nTotal: ₹{total:.2f}"
            )
        except Exception as mail_err:
            print("⚠️ Email send failed:", mail_err)

        print("✅ Order placed successfully:", new_order.id)
        return {"message": "Order placed successfully", "order_id": new_order.id, "total": total}

    except Exception as e:
        db.rollback()
        print("❌ Order placement failed:", e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



# ---------------------------
# Addresses
# ---------------------------
@router.get("/addresses/{user_id}")
def get_addresses(user_id: int, db: Session = Depends(get_db)):
    addresses = db.query(models.Address).filter(models.Address.user_id == user_id).all()
    return {"addresses": addresses}

@router.post("/addresses/")
def add_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    new_address = models.Address(
        user_id=address.user_id,
        address_line1=address.address_line1,
        city=address.city,
        state=address.state,
        pincode=address.pincode
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return {"message": "Address added successfully", "address": new_address}
