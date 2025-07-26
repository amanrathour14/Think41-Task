# E-commerce Customer Support Chatbot

A sophisticated customer support chatbot for e-commerce platforms, built with FastAPI backend and React frontend, powered by Groq LLM integration.

## 🚀 Features

- **Intelligent Chat Interface**: Modern React-based chat UI with real-time messaging
- **LLM-Powered Responses**: Groq integration for intelligent, context-aware responses
- **E-commerce Data Integration**: Full access to products, orders, inventory, and customer data
- **Conversation History**: Persistent chat history with multi-user support
- **Database Management**: MySQL database with comprehensive e-commerce schema
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Real-time Updates**: Live chat interface with instant responses

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **MySQL** - Database (with PyMySQL driver)
- **Groq** - LLM API for intelligent responses
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## 📋 Prerequisites

1. **Python 3.8+**
2. **Node.js 16+**
3. **MySQL 8.0+**
4. **Groq API Key** - Get from [https://console.groq.com/](https://console.groq.com/)

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd Think41-Task

# Set up environment variables
copy docker.env .env
# Edit .env and add your GROQ_API_KEY

# Run the setup script
# On Windows:
.\docker-setup.ps1

# On Linux/Mac:
chmod +x docker-setup.sh
./docker-setup.sh

# Or manually:
docker-compose up --build -d
```

### Option 2: Manual Setup

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Think41-Task
```

#### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
copy env.example .env
# Edit .env and add your GROQ_API_KEY

# Create MySQL database
mysql -u root -p
# Enter your MySQL password
# In MySQL prompt:
CREATE DATABASE ecommerce_chatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Load sample data (if available)
python load_data.py

# Start the backend server
python main.py
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 4. Access the Application

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📊 Database Schema

### Chat System Tables
- `users` - Chat system users
- `conversations` - Chat conversations
- `messages` - Individual chat messages

### E-commerce Tables
- `ecommerce_users` - Customer data
- `products` - Product catalog
- `orders` - Order information
- `order_items` - Order line items
- `inventory_items` - Inventory tracking
- `distribution_centers` - Warehouse locations

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/ecommerce_chatbot

# LLM Configuration (Groq)
GROQ_API_KEY=your_groq_api_key_here

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📡 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send a message and get AI response
- `GET /api/conversations` - Get user conversations
- `GET /api/conversations/{id}/messages` - Get conversation messages
- `POST /api/conversations` - Create new conversation

### Health Check
- `GET /health` - API health status

## 🎯 Usage Examples

### Chat with the Bot

Ask questions like:
- "What products do you have in the Women's department?"
- "Show me orders for user ID 12345"
- "What's the status of order #1001?"
- "How many products are in stock?"
- "What are your return policies?"

### API Usage

```bash
# Send a chat message
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What products do you have?", "user_id": "user123"}'

# Get conversation history
curl "http://localhost:8000/api/conversations/user123/messages"
```

## 🔍 Project Structure

```
Think41-Task/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── database.py             # Database configuration
│   ├── llm_service.py          # Groq LLM integration
│   ├── conversation_service.py # Chat management
│   ├── load_data.py            # Data loading script
│   ├── requirements.txt        # Python dependencies
│   └── env.example             # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main React component
│   │   ├── components/        # React components
│   │   └── services/          # API services
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite configuration
└── README.md                  # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in `.env`
   - Verify database exists

2. **Groq API Error**
   - Verify API key is correct
   - Check API key permissions
   - Ensure internet connection

3. **Frontend Build Issues**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

4. **CORS Errors**
   - Verify ALLOWED_ORIGINS in `.env`
   - Check frontend URL matches configuration

### Docker Issues

1. **Docker Not Starting**
   - Ensure Docker Desktop is running
   - Check Docker service status
   - Verify Docker Compose is installed

2. **Port Conflicts**
   - Check if ports 3000, 8000, or 3306 are already in use
   - Stop conflicting services or change ports in docker-compose.yml

3. **Container Build Failures**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild containers: `docker-compose build --no-cache`

4. **Environment Variables**
   - Ensure `.env` file exists and contains valid GROQ_API_KEY
   - Check file permissions on `.env` file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Groq for LLM API
- FastAPI for the backend framework
- React team for the frontend framework
- MySQL for the database system 