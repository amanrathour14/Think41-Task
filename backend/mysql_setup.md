# MySQL Setup Guide

This guide will help you set up MySQL for the E-commerce Customer Support Chatbot.

## Prerequisites

- MySQL Server installed (version 5.7 or higher)
- MySQL client tools
- Python with mysqlclient package

## Installation

### 1. Install MySQL Server

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server mysql-client
```

**macOS (using Homebrew):**
```bash
brew install mysql
```

**Windows:**
Download and install from: https://dev.mysql.com/downloads/mysql/

### 2. Start MySQL Service

**Ubuntu/Debian:**
```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

**macOS:**
```bash
brew services start mysql
```

**Windows:**
MySQL service should start automatically after installation.

### 3. Secure MySQL Installation

```bash
sudo mysql_secure_installation
```

Follow the prompts to:
- Set root password
- Remove anonymous users
- Disallow root login remotely
- Remove test database
- Reload privilege tables

## Database Setup

### 1. Create Database and User

Connect to MySQL as root:
```bash
mysql -u root -p
```

Create the database and user:
```sql
-- Create database
CREATE DATABASE ecommerce_chatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (replace 'your_password' with a secure password)
CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON ecommerce_chatbot.* TO 'chatbot_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

### 2. Update Environment Configuration

Edit your `.env` file:
```bash
# Database Configuration
DATABASE_URL=mysql://chatbot_user:your_password@localhost:3306/ecommerce_chatbot

# LLM Configuration (Groq)
GROQ_API_KEY=your_groq_api_key_here

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Python Dependencies

### 1. Install mysqlclient

**Ubuntu/Debian:**
```bash
sudo apt install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

**macOS:**
```bash
brew install mysql-connector-c
pip install mysqlclient
```

**Windows:**
```bash
pip install mysqlclient
```

If you encounter issues with mysqlclient installation, you can use PyMySQL as an alternative:

```bash
pip install PyMySQL
```

Then update the DATABASE_URL in your `.env` file:
```
DATABASE_URL=mysql+pymysql://chatbot_user:your_password@localhost:3306/ecommerce_chatbot
```

### 2. Install Other Dependencies

```bash
pip install -r requirements.txt
```

## Testing the Connection

### 1. Test Database Connection

```bash
python -c "
from database import engine
with engine.connect() as conn:
    result = conn.execute('SELECT 1')
    print('Database connection successful!')
"
```

### 2. Run Setup Script

```bash
python setup.py
```

This will:
- Check database connection
- Create tables
- Load the e-commerce dataset

## Troubleshooting

### Common Issues

1. **Connection Error:**
   - Verify MySQL is running
   - Check username/password in DATABASE_URL
   - Ensure database exists

2. **mysqlclient Installation Issues:**
   - Install system dependencies first
   - Use PyMySQL as alternative
   - On Windows, download pre-compiled wheels

3. **Character Set Issues:**
   - Ensure database uses utf8mb4 character set
   - Check MySQL configuration for proper encoding

4. **Permission Issues:**
   - Verify user has proper privileges
   - Check MySQL user permissions

### Useful MySQL Commands

```sql
-- Show databases
SHOW DATABASES;

-- Use database
USE ecommerce_chatbot;

-- Show tables
SHOW TABLES;

-- Check table structure
DESCRIBE users;
DESCRIBE conversations;
DESCRIBE messages;

-- Check data
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM conversations;
SELECT COUNT(*) FROM messages;
```

## Next Steps

After successful MySQL setup:

1. Download the e-commerce dataset
2. Run the setup script: `python setup.py`
3. Start the backend server: `python main.py`
4. Start the frontend: `npm run dev`

Your chatbot should now be running with MySQL as the database backend! 