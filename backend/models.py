from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.dialects.mysql import JSON as MySQLJSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String(50))
    state = Column(String(100))
    street_address = Column(Text)
    postal_code = Column(String(20))
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    traffic_source = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_user_message = Column(Boolean, nullable=False)  # True for user, False for AI
    created_at = Column(DateTime, server_default=func.now())
    message_metadata = Column(MySQLJSON)  # Store additional data like query type, confidence, etc.
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

# E-commerce data models
class EcommerceUser(Base):
    __tablename__ = "ecommerce_users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    age = Column(Integer)
    gender = Column(String(50))
    state = Column(String(100))
    street_address = Column(Text)
    postal_code = Column(String(20))
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    traffic_source = Column(String(100))
    created_at = Column(DateTime)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    cost = Column(Float)
    category = Column(String(100))
    name = Column(String(255), nullable=True)
    brand = Column(String(100))
    retail_price = Column(Float)
    department = Column(String(100))
    sku = Column(String(100))
    distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"))

class DistributionCenter(Base):
    __tablename__ = "distribution_centers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime)
    sold_at = Column(DateTime)
    cost = Column(Float)
    product_category = Column(String(100))
    product_name = Column(String(255))
    product_brand = Column(String(100))
    product_retail_price = Column(Float)
    product_department = Column(String(100))
    product_sku = Column(String(100))
    product_distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"))

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ecommerce_users.id"))
    status = Column(String(50))
    gender = Column(String(50))
    created_at = Column(DateTime)
    returned_at = Column(DateTime)
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    num_of_item = Column(Integer)

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    user_id = Column(Integer, ForeignKey("ecommerce_users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"))
    status = Column(String(50))
    created_at = Column(DateTime)
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    returned_at = Column(DateTime) 