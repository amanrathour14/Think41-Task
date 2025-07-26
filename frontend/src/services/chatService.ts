import { ChatRequest, ChatResponse, MessageType, ConversationType } from '../types/chat';

const API_BASE_URL = 'http://localhost:8000';

class ChatService {
  private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    return this.makeRequest<ChatResponse>('/api/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getConversations(): Promise<ConversationType[]> {
    return this.makeRequest<ConversationType[]>('/api/conversations');
  }

  async getConversationMessages(conversationId: string): Promise<MessageType[]> {
    return this.makeRequest<MessageType[]>(`/api/conversations/${conversationId}/messages`);
  }

  async createConversation(): Promise<ConversationType> {
    return this.makeRequest<ConversationType>('/api/conversations', {
      method: 'POST',
    });
  }

  async updateConversationTitle(conversationId: string, title: string): Promise<void> {
    return this.makeRequest<void>(`/api/conversations/${conversationId}/title`, {
      method: 'PUT',
      body: JSON.stringify({ title }),
    });
  }

  async deleteConversation(conversationId: string): Promise<void> {
    return this.makeRequest<void>(`/api/conversations/${conversationId}`, {
      method: 'DELETE',
    });
  }

  async getHealth(): Promise<{ status: string }> {
    return this.makeRequest<{ status: string }>('/health');
  }
}

export const chatService = new ChatService(); 