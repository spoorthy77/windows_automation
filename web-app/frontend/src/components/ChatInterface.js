import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOffline, setIsOffline] = useState(false);
  const [serverStatus, setServerStatus] = useState('checking');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Backend URL
  const API_URL = 'http://localhost:5000';

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check server status on mount
  useEffect(() => {
    checkServerStatus();
    
    // Add welcome message
    setMessages([{
      id: Date.now(),
      type: 'bot',
      text: `🤖 Welcome to Windows Automation Chatbot!

✅ 100% Offline - No internet required
✅ Fuzzy matching - Typos are okay!
✅ Natural language understanding

Try commands like:
• "open calculator"
• "check battery"
• "show cpu usage"
• Or even with typos: "opn calc", "chk baterry"

Type 'help' to see all available commands!`,
      timestamp: new Date().toISOString()
    }]);
  }, []);

  // Check if backend server is running
  const checkServerStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/status`);
      if (response.ok) {
        setServerStatus('online');
        setIsOffline(false);
      } else {
        setServerStatus('offline');
        setIsOffline(true);
      }
    } catch (error) {
      setServerStatus('offline');
      setIsOffline(true);
    }
  };

  // Send message to backend
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    const userMessageObj = {
      id: Date.now(),
      type: 'user',
      text: userMessage,
      timestamp: new Date().toISOString()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessageObj]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send to backend
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      // Add bot response to chat
      const botMessageObj = {
        id: Date.now() + 1,
        type: 'bot',
        text: data.response,
        intent: data.intent,
        confidence: data.confidence,
        timestamp: data.timestamp
      };

      setMessages(prev => [...prev, botMessageObj]);
      setServerStatus('online');
      setIsOffline(false);

    } catch (error) {
      console.error('Error:', error);
      
      // Add error message
      const errorMessageObj = {
        id: Date.now() + 1,
        type: 'bot',
        text: `❌ Error: Could not connect to server.
        
Please make sure the backend server is running:
1. Open a terminal in the web-app folder
2. Activate the virtual environment
3. Run: python offline_app.py

Server should be running on http://localhost:5000`,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessageObj]);
      setServerStatus('offline');
      setIsOffline(true);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Quick action buttons
  const quickActions = [
    { label: '🔢 Calculator', command: 'open calculator' },
    { label: '📝 Notepad', command: 'open notepad' },
    { label: '⚙️ Settings', command: 'open settings' },
    { label: '📊 System Info', command: 'system summary' },
    { label: '🔋 Battery', command: 'battery status' },
    { label: '💾 Storage', command: 'check storage' },
  ];

  const handleQuickAction = (command) => {
    setInputMessage(command);
    inputRef.current?.focus();
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="header-title">
          <h1>🤖 Windows Automation Chatbot</h1>
          <span className="subtitle">100% Offline • Fuzzy Matching • Local Automation</span>
        </div>
        <div className="header-status">
          <div className={`status-indicator ${serverStatus}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {serverStatus === 'online' ? '✅ Online' : 
               serverStatus === 'offline' ? '❌ Offline' : 
               '⏳ Checking...'}
            </span>
          </div>
          {isOffline && (
            <button 
              className="retry-button"
              onClick={checkServerStatus}
              title="Retry connection"
            >
              🔄 Retry
            </button>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <div className="quick-actions-title">Quick Actions:</div>
        <div className="quick-actions-buttons">
          {quickActions.map((action, index) => (
            <button
              key={index}
              className="quick-action-btn"
              onClick={() => handleQuickAction(action.command)}
            >
              {action.label}
            </button>
          ))}
        </div>
      </div>

      {/* Messages Area */}
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-content">
              <div className="message-text">
                {message.text.split('\n').map((line, i) => (
                  <React.Fragment key={i}>
                    {line}
                    {i < message.text.split('\n').length - 1 && <br />}
                  </React.Fragment>
                ))}
              </div>
              {message.intent && (
                <div className="message-meta">
                  Intent: {message.intent} | Confidence: {message.confidence}%
                </div>
              )}
              <div className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          <input
            ref={inputRef}
            type="text"
            className="message-input"
            placeholder="Type a command... (typos are okay!)"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button
            className="send-button"
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim()}
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
        <div className="input-hint">
          💡 Try: "open calculator", "check battery", "write program factorial" (typos okay!)
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
