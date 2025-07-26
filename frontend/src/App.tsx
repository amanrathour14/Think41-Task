import React, { useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import { ChatProvider, useChatContext } from './context/ChatContext';
import './index.css';

const AppContent: React.FC = () => {
  const { loadConversations } = useChatContext();

  useEffect(() => {
    // Load conversations when the app starts
    loadConversations();
  }, [loadConversations]);

  return <ChatWindow />;
};

const App: React.FC = () => {
  return (
    <ChatProvider>
      <AppContent />
    </ChatProvider>
  );
};

export default App; 