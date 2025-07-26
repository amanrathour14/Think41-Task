import pandas as pd
import os
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from models import (
    User, EcommerceUser, Product, DistributionCenter, InventoryItem, 
    Order, OrderItem, Base
)
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_datetime(date_str):
    """Parse datetime string to datetime object"""
    if pd.isna(date_str) or date_str == '':
        return None
    try:
        return pd.to_datetime(date_str)
    except:
        return None

def load_distribution_centers(db: Session, data_dir: str):
    """Load distribution centers data"""
    try:
        df = pd.read_csv(os.path.join(data_dir, 'distribution_centers.csv'))
        logger.info(f"Loading {len(df)} distribution centers")
        
        for _, row in df.iterrows():
            center = DistributionCenter(
                id=row['id'],
                name=row['name'] if pd.notna(row['name']) else None,
                latitude=row['latitude'] if pd.notna(row['latitude']) else None,
                longitude=row['longitude'] if pd.notna(row['longitude']) else None
            )
            db.add(center)
        
        db.commit()
        logger.info("Distribution centers loaded successfully")
    except Exception as e:
        logger.error(f"Error loading distribution centers: {e}")
        db.rollback()

def load_products(db: Session, data_dir: str):
    """Load products data"""
    try:
        df = pd.read_csv(os.path.join(data_dir, 'products.csv'))
        logger.info(f"Loading {len(df)} products")
        
        for _, row in df.iterrows():
            product = Product(
                id=row['id'],
                cost=row['cost'] if pd.notna(row['cost']) else None,
                category=row['category'] if pd.notna(row['category']) else None,
                name=row['name'] if pd.notna(row['name']) else None,
                brand=row['brand'] if pd.notna(row['brand']) else None,
                retail_price=row['retail_price'] if pd.notna(row['retail_price']) else None,
                department=row['department'] if pd.notna(row['department']) else None,
                sku=row['sku'] if pd.notna(row['sku']) else None,
                distribution_center_id=row['distribution_center_id'] if pd.notna(row['distribution_center_id']) else None
            )
            db.add(product)
        
        db.commit()
        logger.info("Products loaded successfully")
    except Exception as e:
        logger.error(f"Error loading products: {e}")
        db.rollback()

def load_ecommerce_users(db: Session, data_dir: str):
    """Load users data"""
    try:
        df = pd.read_csv(os.path.join(data_dir, 'users.csv'))
        logger.info(f"Loading {len(df)} users")
        
        for _, row in df.iterrows():
            user = EcommerceUser(
                id=row['id'],
                first_name=row['first_name'] if pd.notna(row['first_name']) else None,
                last_name=row['last_name'] if pd.notna(row['last_name']) else None,
                email=row['email'] if pd.notna(row['email']) else None,
                age=row['age'] if pd.notna(row['age']) else None,
                gender=row['gender'] if pd.notna(row['gender']) else None,
                state=row['state'] if pd.notna(row['state']) else None,
                street_address=row['street_address'] if pd.notna(row['street_address']) else None,
                postal_code=row['postal_code'] if pd.notna(row['postal_code']) else None,
                city=row['city'] if pd.notna(row['city']) else None,
                country=row['country'] if pd.notna(row['country']) else None,
                latitude=row['latitude'] if pd.notna(row['latitude']) else None,
                longitude=row['longitude'] if pd.notna(row['longitude']) else None,
                traffic_source=row['traffic_source'] if pd.notna(row['traffic_source']) else None,
                created_at=parse_datetime(row['created_at']) if pd.notna(row['created_at']) else None
            )
            db.add(user)
        
        db.commit()
        logger.info("Users loaded successfully")
    except Exception as e:
        logger.error(f"Error loading users: {e}")
        db.rollback()

def load_inventory_items(db: Session, data_dir: str):
    """Load inventory items data"""
    try:
        df = pd.read_csv(os.path.join(data_dir, 'inventory_items.csv'))
        logger.info(f"Loading {len(df)} inventory items")
        
        for _, row in df.iterrows():
            inventory_item = InventoryItem(
                id=row['id'],
                product_id=row['product_id'] if pd.notna(row['product_id']) else None,
                created_at=parse_datetime(row['created_at']) if pd.notna(row['created_at']) else None,
                sold_at=parse_datetime(row['sold_at']) if pd.notna(row['sold_at']) else None,
                cost=row['cost'] if pd.notna(row['cost']) else None,
                product_category=row['product_category'] if pd.notna(row['product_category']) else None,
                product_name=row['product_name'] if pd.notna(row['product_name']) else None,
                product_brand=row['product_brand'] if pd.notna(row['product_brand']) else None,
                product_retail_price=row['product_retail_price'] if pd.notna(row['product_retail_price']) else None,
                product_department=row['product_department'] if pd.notna(row['product_department']) else None,
                product_sku=row['product_sku'] if pd.notna(row['product_sku']) else None,
                product_distribution_center_id=row['product_distribution_center_id'] if pd.notna(row['product_distribution_center_id']) else None
            )
            db.add(inventory_item)
        
        db.commit()
        logger.info("Inventory items loaded successfully")
    except Exception as e:
        logger.error(f"Error loading inventory items: {e}")
        db.rollback()

def load_orders(db: Session, data_dir: str):
    """Load orders data"""
    try:
        df = pd.read_csv(os.path.join(data_dir, 'orders.csv'))
        logger.info(f"Loading {len(df)} orders")
        
        for _, row in df.iterrows():
            order = Order(
                order_id=row['order_id'],
                user_id=row['user_id'] if pd.notna(row['user_id']) else None,
                status=row['status'] if pd.notna(row['status']) else None,
                gender=row['gender'] if pd.notna(row['gender']) else None,
                created_at=parse_datetime(row['created_at']) if pd.notna(row['created_at']) else None,
                returned_at=parse_datetime(row['returned_at']) if pd.notna(row['returned_at']) else None,
                shipped_at=parse_datetime(row['shipped_at']) if pd.notna(row['shipped_at']) else None,
                delivered_at=parse_datetime(row['delivered_at']) if pd.notna(row['delivered_at']) else None,
                num_of_item=row['num_of_item'] if pd.notna(row['num_of_item']) else None
            )
            db.add(order)
        
        db.commit()
        logger.info("Orders loaded successfully")
    except Exception as e:
        logger.error(f"Error loading orders: {e}")
        db.rollback()

def load_order_items(db: Session, data_dir: str):
    """Load order items data"""
    try:
        df = pd.read_csv(os.path.join(data_dir, 'order_items.csv'))
        logger.info(f"Loading {len(df)} order items")
        
        for _, row in df.iterrows():
            order_item = OrderItem(
                id=row['id'],
                order_id=row['order_id'] if pd.notna(row['order_id']) else None,
                user_id=row['user_id'] if pd.notna(row['user_id']) else None,
                product_id=row['product_id'] if pd.notna(row['product_id']) else None,
                inventory_item_id=row['inventory_item_id'] if pd.notna(row['inventory_item_id']) else None,
                status=row['status'] if pd.notna(row['status']) else None,
                created_at=parse_datetime(row['created_at']) if pd.notna(row['created_at']) else None,
                shipped_at=parse_datetime(row['shipped_at']) if pd.notna(row['shipped_at']) else None,
                delivered_at=parse_datetime(row['delivered_at']) if pd.notna(row['delivered_at']) else None,
                returned_at=parse_datetime(row['returned_at']) if pd.notna(row['returned_at']) else None
            )
            db.add(order_item)
        
        db.commit()
        logger.info("Order items loaded successfully")
    except Exception as e:
        logger.error(f"Error loading order items: {e}")
        db.rollback()

def main():
    """Main function to load all data"""
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        logger.error(f"Data directory '{data_dir}' not found!")
        logger.info("Please download the dataset and extract CSV files to the 'data' directory")
        return
    
    # Check if required files exist
    required_files = [
        'distribution_centers.csv',
        'products.csv', 
        'users.csv',
        'inventory_items.csv',
        'orders.csv',
        'order_items.csv'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(data_dir, f))]
    if missing_files:
        logger.error(f"Missing required files: {missing_files}")
        return
    
    # Create tables
    logger.info("Creating database tables...")
    create_tables()
    
    # Load data
    db = SessionLocal()
    try:
        logger.info("Starting data loading process...")
        
        # Load in order to respect foreign key constraints
        load_distribution_centers(db, data_dir)
        load_products(db, data_dir)
        load_ecommerce_users(db, data_dir)
        load_inventory_items(db, data_dir)
        load_orders(db, data_dir)
        load_order_items(db, data_dir)
        
        logger.info("All data loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 