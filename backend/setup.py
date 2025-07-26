#!/usr/bin/env python3
"""
Setup script for the E-commerce Customer Support Chatbot
This script initializes the database and loads the e-commerce dataset.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        sys.exit(1)
    logger.info(f"Python version: {sys.version}")

def install_dependencies():
    """Install Python dependencies"""
    logger.info("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        sys.exit(1)

def check_database_connection():
    """Check database connection"""
    logger.info("Checking database connection...")
    try:
        from database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.info("Please ensure MySQL is running and DATABASE_URL is configured correctly")
        return False

def create_database_tables():
    """Create database tables"""
    logger.info("Creating database tables...")
    try:
        from database import create_tables
        create_tables()
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        return False

def check_dataset_files():
    """Check if dataset files exist"""
    data_dir = Path("data")
    required_files = [
        "distribution_centers.csv",
        "products.csv",
        "users.csv",
        "inventory_items.csv",
        "orders.csv",
        "order_items.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not (data_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"Missing dataset files: {missing_files}")
        logger.info("Please download the dataset from: github.com/recruit41/ecommerce-dataset")
        logger.info("Extract the CSV files to the 'data' directory")
        return False
    
    logger.info("All dataset files found")
    return True

def load_dataset():
    """Load dataset into database"""
    logger.info("Loading dataset into database...")
    try:
        from load_data import main as load_data_main
        load_data_main()
        logger.info("Dataset loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return False

def check_environment():
    """Check environment configuration"""
    logger.info("Checking environment configuration...")
    
    # Check for .env file
    if not Path(".env").exists():
        logger.warning(".env file not found. Creating from template...")
        try:
            with open("env.example", "r") as f:
                env_content = f.read()
            with open(".env", "w") as f:
                f.write(env_content)
            logger.info("Created .env file from template")
            logger.info("Please update .env file with your configuration")
        except Exception as e:
            logger.error(f"Failed to create .env file: {e}")
    
    # Check for required environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["DATABASE_URL", "GROQ_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.info("Please update your .env file with the required variables")
        return False
    
    logger.info("Environment configuration looks good")
    return True

def main():
    """Main setup function"""
    logger.info("Starting E-commerce Customer Support Chatbot setup...")
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Check environment
    if not check_environment():
        logger.warning("Environment configuration incomplete. Please update .env file")
        logger.info("You can continue with setup, but some features may not work")
    
    # Check database connection
    if not check_database_connection():
        logger.error("Cannot proceed without database connection")
        sys.exit(1)
    
    # Create database tables
    if not create_database_tables():
        logger.error("Cannot proceed without database tables")
        sys.exit(1)
    
    # Check dataset files
    if not check_dataset_files():
        logger.error("Cannot proceed without dataset files")
        sys.exit(1)
    
    # Load dataset
    if not load_dataset():
        logger.error("Failed to load dataset")
        sys.exit(1)
    
    logger.info("Setup completed successfully!")
    logger.info("You can now start the backend server with: python main.py")

if __name__ == "__main__":
    main() 