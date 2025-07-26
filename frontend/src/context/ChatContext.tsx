import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { MessageType, ConversationType, ChatRequest, ChatResponse } from '../types/chat';
import { chatService } from '../services/chatService';

// State interface
interface ChatState {
  messages: MessageType[];
  loading: boolean;
  conversations: ConversationType[];
  currentConversationId: string | null;
  error: string | null;
}

// Action types
type ChatAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'ADD_MESSAGE'; payload: MessageType }
  | { type: 'SET_MESSAGES'; payload: MessageType[] }
  | { type: 'SET_CONVERSATIONS'; payload: ConversationType[] }
  | { type: 'SET_CURRENT_CONVERSATION'; payload: string | null }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_MESSAGES' };

// Initial state
const initialState: ChatState = {
  messages: [],
  loading: false,
  conversations: [],
  currentConversationId: null,
  error: null,
};

// Reducer function
const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    
    case 'ADD_MESSAGE':
      return { 
        ...state, 
        messages: [...state.messages, action.payload],
        error: null 
      };
    
    case 'SET_MESSAGES':
      return { ...state, messages: action.payload };
    
    case 'SET_CONVERSATIONS':
      return { ...state, conversations: action.payload };
    
    case 'SET_CURRENT_CONVERSATION':
      return { ...state, currentConversationId: action.payload };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    
    case 'CLEAR_MESSAGES':
      return { ...state, messages: [] };
    
    default:
      return state;
  }
};

// Context interface
interface ChatContextType {
  messages: MessageType[];
  loading: boolean;
  conversations: ConversationType[];
  currentConversationId: string | null;
  error: string | null;
  sendMessage: (message: string) => Promise<void>;
  loadConversations: () => Promise<void>;
  selectConversation: (conversationId: string) => Promise<void>;
  createNewConversation: () => void;
  clearError: () => void;
}

// Create context
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Provider component
interface ChatProviderProps {
  children: ReactNode;
}

export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const sendMessage = async (message: string) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      dispatch({ type: 'SET_ERROR', payload: null });

      // Add user message immediately
      const userMessage: MessageType = {
        content: message,
        isUserMessage: true,
        createdAt: new Date().toISOString(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: userMessage });

      // Prepare request
      const request: ChatRequest = {
        message,
        conversation_id: state.currentConversationId || undefined,
      };

      // Send to API
      const response: ChatResponse = await chatService.sendMessage(request);

      // Add AI response
      const aiMessage: MessageType = {
        content: response.response,
        isUserMessage: false,
        createdAt: new Date().toISOString(),
        metadata: response.metadata,
      };
      dispatch({ type: 'ADD_MESSAGE', payload: aiMessage });

      // Update current conversation
      if (response.conversation_id !== state.currentConversationId) {
        dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: response.conversation_id });
      }

      // Reload conversations to get updated list
      await loadConversations();

    } catch (error) {
      console.error('Error sending message:', error);
      dispatch({ 
        type: 'SET_ERROR', 
        payload: error instanceof Error ? error.message : 'Failed to send message' 
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const loadConversations = async () => {
    try {
      const conversations = await chatService.getConversations();
      dispatch({ type: 'SET_CONVERSATIONS', payload: conversations });
    } catch (error) {
      console.error('Error loading conversations:', error);
      dispatch({ 
        type: 'SET_ERROR', 
        payload: error instanceof Error ? error.message : 'Failed to load conversations' 
      });
    }
  };

  const selectConversation = async (conversationId: string) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      dispatch({ type: 'SET_ERROR', payload: null });

      const messages = await chatService.getConversationMessages(conversationId);
      dispatch({ type: 'SET_MESSAGES', payload: messages });
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: conversationId });

    } catch (error) {
      console.error('Error selecting conversation:', error);
      dispatch({ 
        type: 'SET_ERROR', 
        payload: error instanceof Error ? error.message : 'Failed to load conversation' 
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const createNewConversation = () => {
    dispatch({ type: 'CLEAR_MESSAGES' });
    dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: null });
    dispatch({ type: 'SET_ERROR', payload: null });
  };

  const clearError = () => {
    dispatch({ type: 'SET_ERROR', payload: null });
  };

  const value: ChatContextType = {
    messages: state.messages,
    loading: state.loading,
    conversations: state.conversations,
    currentConversationId: state.currentConversationId,
    error: state.error,
    sendMessage,
    loadConversations,
    selectConversation,
    createNewConversation,
    clearError,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the context
export const useChatContext = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
}; 