import os
import groq
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from models import Product, Order, InventoryItem, User, EcommerceUser
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-8b-8192"  # Using Llama3 model via Groq
        
    def generate_response(self, user_message: str, conversation_history: List[Dict], db: Session) -> Dict[str, Any]:
        """Generate intelligent response using LLM and database queries"""
        
        # Analyze user intent
        intent = self._analyze_intent(user_message)
        
        # Get relevant data based on intent
        data = self._get_relevant_data(intent, user_message, db)
        
        # Generate response using LLM
        response = self._generate_llm_response(user_message, intent, data, conversation_history)
        
        return {
            "response": response,
            "intent": intent,
            "data": data,
            "metadata": {
                "model": self.model,
                "confidence": 0.9
            }
        }
    
    def _analyze_intent(self, message: str) -> str:
        """Analyze user intent from message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["top", "popular", "best", "most sold"]):
            return "top_products"
        elif any(word in message_lower for word in ["order", "status", "tracking"]):
            return "order_status"
        elif any(word in message_lower for word in ["stock", "inventory", "available", "left"]):
            return "inventory"
        elif any(word in message_lower for word in ["help", "what can you do", "capabilities"]):
            return "help"
        else:
            return "general"
    
    def _get_relevant_data(self, intent: str, message: str, db: Session) -> Dict[str, Any]:
        """Get relevant data from database based on intent"""
        try:
            if intent == "top_products":
                return self._get_top_products(db)
            elif intent == "order_status":
                return self._get_order_status(message, db)
            elif intent == "inventory":
                return self._get_inventory_status(message, db)
            else:
                return {}
        except Exception as e:
            logger.error(f"Error getting data: {e}")
            return {}
    
    def _get_top_products(self, db: Session) -> Dict[str, Any]:
        """Get top selling products"""
        # Count products by name
        from sqlalchemy import func
        top_products = db.query(
            Product.name,
            func.count(Product.id).label('count')
        ).group_by(Product.name).order_by(func.count(Product.id).desc()).limit(5).all()
        
        return {
            "top_products": [{"name": p.name, "count": p.count} for p in top_products]
        }
    
    def _get_order_status(self, message: str, db: Session) -> Dict[str, Any]:
        """Get order status by order ID"""
        import re
        order_id_match = re.search(r'(\d+)', message)
        if not order_id_match:
            return {"error": "No order ID found in message"}
        
        order_id = int(order_id_match.group(1))
        order = db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            return {"error": f"Order {order_id} not found"}
        
        return {
            "order": {
                "order_id": order.order_id,
                "status": order.status,
                "created_at": order.created_at,
                "shipped_at": order.shipped_at,
                "delivered_at": order.delivered_at,
                "num_of_item": order.num_of_item
            }
        }
    
    def _get_inventory_status(self, message: str, db: Session) -> Dict[str, Any]:
        """Get inventory status for products"""
        import re
        
        # Extract product name from message
        product_name_match = re.search(r'([A-Za-z\s]+)', message)
        if not product_name_match:
            return {"error": "No product name found in message"}
        
        product_name = product_name_match.group(1).strip()
        
        # Query inventory items
        inventory_items = db.query(InventoryItem).filter(
            InventoryItem.product_name.ilike(f"%{product_name}%")
        ).all()
        
        if not inventory_items:
            return {"error": f"No inventory found for '{product_name}'"}
        
        # Calculate availability
        total_items = len(inventory_items)
        available_items = len([item for item in inventory_items if item.sold_at is None])
        sold_items = total_items - available_items
        
        return {
            "inventory": {
                "product_name": product_name,
                "total_items": total_items,
                "available_items": available_items,
                "sold_items": sold_items
            }
        }
    
    def _generate_llm_response(self, user_message: str, intent: str, data: Dict, conversation_history: List[Dict]) -> str:
        """Generate response using LLM"""
        
        # Build context from conversation history
        context = self._build_context(conversation_history)
        
        # Build system prompt
        system_prompt = self._build_system_prompt(intent, data)
        
        # Build user prompt
        user_prompt = f"User message: {user_message}\n\nPlease provide a helpful and informative response."
        
        try:
            # Generate response using Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context + "\n\n" + user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._fallback_response(intent, data)
    
    def _build_context(self, conversation_history: List[Dict]) -> str:
        """Build context from conversation history"""
        if not conversation_history:
            return ""
        
        context = "Previous conversation:\n"
        for msg in conversation_history[-5:]:  # Last 5 messages
            role = "User" if msg.get("is_user_message") else "Assistant"
            context += f"{role}: {msg.get('content', '')}\n"
        
        return context
    
    def _build_system_prompt(self, intent: str, data: Dict) -> str:
        """Build system prompt based on intent and data"""
        
        base_prompt = """You are a helpful customer support assistant for an e-commerce clothing store. 
        You have access to product information, order status, and inventory data. 
        Be friendly, professional, and provide accurate information based on the available data."""
        
        if intent == "top_products":
            products = data.get("top_products", [])
            if products:
                product_list = "\n".join([f"{i+1}. {p['name']}: {p['count']} units" for i, p in enumerate(products)])
                return f"{base_prompt}\n\nTop selling products data:\n{product_list}\n\nProvide a clear list of the top products with their sales numbers."
        
        elif intent == "order_status":
            order = data.get("order")
            if order:
                order_info = f"""
                Order ID: {order['order_id']}
                Status: {order['status']}
                Created: {order['created_at']}
                Items: {order['num_of_item']}
                """
                if order.get('shipped_at'):
                    order_info += f"Shipped: {order['shipped_at']}\n"
                if order.get('delivered_at'):
                    order_info += f"Delivered: {order['delivered_at']}\n"
                
                return f"{base_prompt}\n\nOrder information:\n{order_info}\n\nProvide a clear status update for this order."
            elif data.get("error"):
                return f"{base_prompt}\n\nError: {data['error']}\n\nAsk the user to provide a valid order ID."
        
        elif intent == "inventory":
            inventory = data.get("inventory")
            if inventory:
                inventory_info = f"""
                Product: {inventory['product_name']}
                Total items: {inventory['total_items']}
                Available in stock: {inventory['available_items']}
                Sold items: {inventory['sold_items']}
                """
                return f"{base_prompt}\n\nInventory information:\n{inventory_info}\n\nProvide a clear inventory status for this product."
            elif data.get("error"):
                return f"{base_prompt}\n\nError: {data['error']}\n\nAsk the user to specify a product name."
        
        elif intent == "help":
            return f"""{base_prompt}
            
            You can help with:
            1. Product information and top sellers
            2. Order status and tracking (provide order ID)
            3. Inventory and stock levels (specify product name)
            
            Ask clarifying questions if you need more information from the user."""
        
        return base_prompt
    
    def _fallback_response(self, intent: str, data: Dict) -> str:
        """Provide fallback response when LLM fails"""
        
        if intent == "top_products":
            products = data.get("top_products", [])
            if products:
                response = "Here are the top 5 most sold products:\n"
                for i, product in enumerate(products, 1):
                    response += f"{i}. {product['name']}: {product['count']} units sold\n"
                return response
            return "I can help you find information about our top selling products. Please try asking again."
        
        elif intent == "order_status":
            if data.get("order"):
                order = data["order"]
                response = f"Order ID {order['order_id']} status: {order['status']}\n"
                response += f"Created: {order['created_at']}\n"
                response += f"Items: {order['num_of_item']}\n"
                if order.get('shipped_at'):
                    response += f"Shipped: {order['shipped_at']}\n"
                if order.get('delivered_at'):
                    response += f"Delivered: {order['delivered_at']}\n"
                return response
            return "I can help you check order status. Please provide an order ID."
        
        elif intent == "inventory":
            if data.get("inventory"):
                inventory = data["inventory"]
                response = f"Inventory status for {inventory['product_name']}:\n"
                response += f"Available in stock: {inventory['available_items']} items\n"
                response += f"Total items: {inventory['total_items']}\n"
                response += f"Sold items: {inventory['sold_items']}\n"
                return response
            return "I can help you check inventory levels. Please specify a product name."
        
        elif intent == "help":
            return """I'm your e-commerce customer support assistant! I can help you with:

• Product information and top sellers
• Order status and tracking (provide order ID)
• Inventory and stock levels (specify product name)

How can I assist you today?"""
        
        return "I'm here to help! I can provide information about products, orders, and inventory. What would you like to know?" 