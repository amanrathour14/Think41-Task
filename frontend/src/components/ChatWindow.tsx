import React, { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistory from './ConversationHistory';
import { useChatContext } from '../context/ChatContext';

const ChatWindow: React.FC = () => {
  const { 
    messages, 
    loading, 
    sendMessage, 
    conversations, 
    currentConversationId,
    selectConversation,
    createNewConversation,
    loadConversations
  } = useChatContext();
  
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversations on component mount
  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    if (message.trim()) {
      await sendMessage(message);
    }
  };

  const handleNewChat = () => {
    createNewConversation();
    setShowHistory(false);
  };

  const handleSelectConversation = (conversationId: string) => {
    selectConversation(conversationId);
    setShowHistory(false);
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Conversation History Panel - Milestone 8 */}
      <div className={`${showHistory ? 'w-80' : 'w-0'} transition-all duration-300 ease-in-out overflow-hidden bg-white shadow-lg`}>
        <ConversationHistory 
          conversations={conversations}
          currentConversationId={currentConversationId}
          onSelectConversation={handleSelectConversation}
          onNewChat={handleNewChat}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              title="Toggle conversation history"
            >
              <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div>
              <h1 className="text-xl font-semibold text-gray-800">🛍️ E-commerce Support Chat</h1>
              <p className="text-sm text-gray-500">AI-powered customer support assistant</p>
            </div>
          </div>
          
          <button
            onClick={handleNewChat}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            <span>New Chat</span>
          </button>
        </div>

        {/* Messages Area - Milestone 6: MessageList component */}
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} loading={loading} />
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area - Milestone 6: UserInput component */}
        <div className="bg-white border-t border-gray-200 p-4">
          <UserInput onSendMessage={handleSendMessage} loading={loading} />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow; 