import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Welcome message
    setMessages([
      {
        sender: 'bot',
        text: `Hello! 👋 I'm your Windows Automation Assistant.

I can help you with:
• Opening applications (WhatsApp, Calculator, Notepad, etc.)
• System information (CPU, memory, battery, storage)
• Controlling volume and Bluetooth
• Managing files and folders
• And much more!

💡 Type 'help' to see all available commands, or just ask me naturally!
Example: 'open calculator' or 'check my battery status'`,
        timestamp: new Date()
      }
    ]);
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      sender: 'user',
      text: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: inputValue
      });

      const botMessage = {
        sender: 'bot',
        text: response.data.response || 'No response from server',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);

      // Handle special responses
      if (response.data.special === 'CLEAR') {
        setTimeout(() => {
          setMessages([botMessage]);
        }, 1000);
      }

    } catch (error) {
      const errorMessage = {
        sender: 'bot',
        text: `❌ Error: ${error.response?.data?.error || error.message || 'Failed to process command'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-content">
          <div className="header-icon">🤖</div>
          <div className="header-text">
            <h1>Windows Automation Assistant</h1>
            <p>AI-powered Windows automation at your command</p>
          </div>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div className="message-avatar">
              {message.sender === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <div className="message-sender">
                {message.sender === 'user' ? 'You' : 'Assistant'}
              </div>
              <div className="message-text">{message.text}</div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString([], { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot loading">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="message-sender">Assistant</div>
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

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <input
            type="text"
            className="chat-input"
            placeholder="Type your command here... (e.g., 'open calculator')"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button
            className="send-button"
            onClick={sendMessage}
            disabled={isLoading || !inputValue.trim()}
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
