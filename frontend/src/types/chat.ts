export interface MessageType {
  id?: string;
  content: string;
  isUserMessage: boolean;
  createdAt?: string;
  metadata?: {
    model?: string;
    confidence?: number;
    [key: string]: any;
  };
}

export interface ConversationType {
  id: string;
  title?: string;
  createdAt?: string;
  updatedAt?: string;
  isActive?: boolean;
  messages?: MessageType[];
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  metadata?: {
    model?: string;
    confidence?: number;
    [key: string]: any;
  };
}

export interface ChatRequest {
  message: string;
  user_id?: string;
  conversation_id?: string;
} 