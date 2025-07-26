-- MySQL Setup Script for E-commerce Chatbot
-- Run this script as root user

-- Create the database
CREATE DATABASE IF NOT EXISTS ecommerce_chatbot 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE ecommerce_chatbot;

-- Show confirmation
SELECT 'Database ecommerce_chatbot created successfully!' as status;

-- Show current database
SELECT DATABASE() as current_database; 