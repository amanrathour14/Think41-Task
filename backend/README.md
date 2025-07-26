# E-commerce Customer Support Chatbot - Backend

This is the backend service for the E-commerce Customer Support Chatbot. It provides a FastAPI-based REST API that can answer customer queries about products, orders, and inventory.

## Features

- **Product Information**: Get top selling products
- **Order Status**: Check order status by order ID
- **Inventory Status**: Check stock levels for specific products
- **RESTful API**: Clean API endpoints for frontend integration

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Dataset**:
   - Download the e-commerce dataset from: `github.com/recruit41/ecommerce-dataset`
   - Extract the CSV files to a `data/` directory in the backend folder
   - The following files should be in the `data/` directory:
     - `products.csv`
     - `orders.csv`
     - `inventory_items.csv`
     - `users.csv`
     - `distribution_centers.csv`
     - `order_items.csv`

3. **Run the Application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Health Check
- **GET** `/health` - Check if the service is running

### Chat Endpoint
- **POST** `/chat` - Main chat endpoint for processing customer queries

#### Request Body:
```json
{
  "message": "What are the top 5 most sold products?",
  "user_id": "optional_user_id"
}
```

#### Response:
```json
{
  "response": "Here are the top 5 most sold products:\n1. Product A: 150 units sold\n2. Product B: 120 units sold\n...",
  "data": {
    "top_products": {
      "Product A": 150,
      "Product B": 120
    }
  }
}
```

## Supported Queries

The chatbot can handle the following types of queries:

1. **Top Products**: "What are the top 5 most sold products?"
2. **Order Status**: "Show me the status of order ID 12345"
3. **Inventory**: "How many Classic T-Shirts are left in stock?"

## Data Structure

The backend loads data from CSV files and provides intelligent responses based on the e-commerce dataset structure:

- **Products**: Product information, categories, brands, pricing
- **Orders**: Order status, shipping, delivery information
- **Inventory**: Stock levels, sold items, availability
- **Users**: Customer information and demographics
- **Distribution Centers**: Warehouse locations and logistics

## Development

The application uses:
- **FastAPI**: Modern Python web framework
- **Pandas**: Data manipulation and analysis
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for running the application

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (React development server)
- `http://localhost:5173` (Vite development server)

## Error Handling

The API includes comprehensive error handling for:
- Missing data files
- Invalid order IDs
- Product not found scenarios
- General server errors