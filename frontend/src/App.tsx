import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, History, Settings } from 'lucide-react'
import axios from 'axios'

interface Message {
  id: string
  text: string
  isUser: boolean
  timestamp: Date
}

interface ChatResponse {
  response: string
  conversation_id: string
  data?: any
  metadata?: any
}

interface Conversation {
  conversation_id: string
  title: string
  created_at: string
  updated_at: string
  total_messages: number
  user_messages: number
  ai_messages: number
  is_active: boolean
}

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I\'m your e-commerce customer support assistant. I can help you with:\n\n• Product information and top sellers\n• Order status and tracking\n• Inventory and stock levels\n\nHow can I assist you today?',
      isUser: false,
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [userEmail, setUserEmail] = useState('user@example.com')
  const [showHistory, setShowHistory] = useState(false)
  const [conversations, setConversations] = useState<Conversation[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const suggestions = [
    'What are the top 5 most sold products?',
    'Show me the status of order ID 12345',
    'How many Classic T-Shirts are left in stock?'
  ]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const loadConversations = async () => {
    try {
      const response = await axios.get<Conversation[]>(`${API_BASE_URL}/api/conversations/${userEmail}`)
      setConversations(response.data)
    } catch (error) {
      console.error('Error loading conversations:', error)
    }
  }

  const loadConversationMessages = async (convId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/conversations/${convId}/messages`)
      const conversationMessages = response.data.map((msg: any) => ({
        id: msg.id,
        text: msg.content,
        isUser: msg.is_user_message,
        timestamp: new Date(msg.created_at)
      }))
      setMessages(conversationMessages)
      setConversationId(convId)
      setShowHistory(false)
    } catch (error) {
      console.error('Error loading conversation messages:', error)
    }
  }

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      isUser: true,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await axios.post<ChatResponse>(`${API_BASE_URL}/api/chat`, {
        message: messageText,
        user_email: userEmail,
        conversation_id: conversationId
      })

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.response,
        isUser: false,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
      setConversationId(response.data.conversation_id)
      
      // Refresh conversations list
      await loadConversations()
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I\'m having trouble connecting to the server. Please try again later.',
        isUser: false,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(inputMessage)
  }

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion)
  }

  const startNewConversation = () => {
    setMessages([{
      id: '1',
      text: 'Hello! I\'m your e-commerce customer support assistant. I can help you with:\n\n• Product information and top sellers\n• Order status and tracking\n• Inventory and stock levels\n\nHow can I assist you today?',
      isUser: false,
      timestamp: new Date()
    }])
    setConversationId(null)
    setShowHistory(false)
  }

  useEffect(() => {
    loadConversations()
  }, [userEmail])

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="header-content">
          <h1>🛍️ E-commerce Support Chatbot</h1>
          <p>Your AI assistant for product info, orders, and inventory</p>
        </div>
        <div className="header-actions">
          <button 
            className="history-button"
            onClick={() => setShowHistory(!showHistory)}
            title="View conversation history"
          >
            <History size={20} />
          </button>
          <button 
            className="new-chat-button"
            onClick={startNewConversation}
            title="Start new conversation"
          >
            New Chat
          </button>
        </div>
      </div>

      {showHistory && (
        <div className="conversation-history">
          <h3>Conversation History</h3>
          <div className="conversations-list">
            {conversations.length === 0 ? (
              <p className="no-conversations">No previous conversations found.</p>
            ) : (
              conversations.map((conv) => (
                <div 
                  key={conv.conversation_id} 
                  className={`conversation-item ${conv.conversation_id === conversationId ? 'active' : ''}`}
                  onClick={() => loadConversationMessages(conv.conversation_id)}
                >
                  <div className="conversation-title">{conv.title}</div>
                  <div className="conversation-meta">
                    <span>{conv.total_messages} messages</span>
                    <span>{new Date(conv.updated_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.isUser ? 'user' : 'bot'}`}>
            <div className="message-avatar">
              {message.isUser ? <User size={20} /> : <Bot size={20} />}
            </div>
            <div className="message-content">
              {message.text.split('\n').map((line, index) => (
                <React.Fragment key={index}>
                  {line}
                  {index < message.text.split('\n').length - 1 && <br />}
                </React.Fragment>
              ))}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot">
            <div className="message-avatar">
              <Bot size={20} />
            </div>
            <div className="message-content">
              <div className="loading">
                <span>Thinking</span>
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <form onSubmit={handleSubmit} className="input-container">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me about products, orders, or inventory..."
            disabled={isLoading}
          />
          <button
            type="submit"
            className="send-button"
            disabled={isLoading || !inputMessage.trim()}
          >
            <Send size={20} />
          </button>
        </form>

        <div className="suggestions">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              className="suggestion-button"
              onClick={() => handleSuggestionClick(suggestion)}
              disabled={isLoading}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App 