import React from 'react';
import ChatWindow from './components/ChatWindow';
import { ChatProvider } from './context/ChatContext';
import './index.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <ChatProvider>
        <ChatWindow />
      </ChatProvider>
    </div>
  );
};

export default App; 