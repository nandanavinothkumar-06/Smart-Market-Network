from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from datetime import datetime

router = APIRouter(prefix="/retailer", tags=["Retailer"])

# -------------------------------------------------------------
# Database Dependency
# -------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------------
# 🧾 Retailer Registration
# -------------------------------------------------------------
@router.post("/register")
def register_retailer(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new retailer account."""
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    if user.role != "retailer":
        raise HTTPException(status_code=403, detail="Role must be 'retailer'")

    # Create new user entry
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        role="retailer",
        status="active"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create corresponding retailer entry
    retailer = models.Retailer(
        user_id=new_user.id,
        name=user.username,
        location="Default Location",
        deliverable=True
    )
    db.add(retailer)
    db.commit()
    db.refresh(retailer)

    return {
        "message": "Retailer registered successfully",
        "user_id": new_user.id,
        "retailer_id": retailer.id
    }


# -------------------------------------------------------------
# 🔑 Retailer Login
# -------------------------------------------------------------
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Retailer login with username and password."""
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")
    if db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    if db_user.role != "retailer":
        raise HTTPException(status_code=403, detail="Not a retailer account")
    if db_user.status != "active":
        raise HTTPException(status_code=403, detail="Retailer account not active")

    retailer = db.query(models.Retailer).filter(models.Retailer.user_id == db_user.id).first()

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "retailer_id": retailer.id if retailer else None
    }


# -------------------------------------------------------------
# 🏷️ Get Retailer Inventory (by retailer ID)
# -------------------------------------------------------------
@router.get("/{retailer_id}/inventory")
def get_retailer_inventory(retailer_id: int, db: Session = Depends(get_db)):
    """Get all products for a specific retailer."""
    products = db.query(models.Product).filter(models.Product.retailer_id == retailer_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this retailer")
    return products


# -------------------------------------------------------------
# 📦 Inventory Update
# -------------------------------------------------------------
@router.put("/inventory/update")
def update_inventory(update: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    """Update product quantity, price, or category."""
    product = db.query(models.Product).filter(
        models.Product.retailer_id == update.retailer_id,
        models.Product.name == update.product_name
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update quantity
    product.quantity = update.new_qty

    # Optional updates
    if update.price is not None:
        product.price = update.price
    if update.category is not None:
        product.category = update.category

    db.commit()
    db.refresh(product)

    return {"message": "Inventory updated successfully"}


# -------------------------------------------------------------
# 🚚 Dispatch Order
# -------------------------------------------------------------
@router.put("/order/{order_id}/dispatch")
def dispatch_order(order_id: int, db: Session = Depends(get_db)):
    """Mark an order as dispatched."""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "Dispatched"
    db.commit()

    return {"message": f"Order {order_id} dispatched successfully"}


# -------------------------------------------------------------
# 📬 Deliver Order
# -------------------------------------------------------------
@router.put("/order/{order_id}/deliver")
def deliver_order(order_id: int, db: Session = Depends(get_db)):
    """Mark an order as delivered."""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "Delivered"
    order.delivery_timestamp = datetime.utcnow()
    order.email_sent = True

    db.commit()

    return {"message": f"Order {order_id} delivered successfully"}
