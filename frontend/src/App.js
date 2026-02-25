import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, Sun, Moon, MapPin, Lock, FileText, ChevronDown } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const MOHI_LOGO = 'https://mohiit.org/static/images/inventorylogo.png';

// Quick action buttons configuration
const QUICK_ACTIONS = [
  {
    id: 'location',
    icon: MapPin,
    label: 'IT Office Location',
    message: 'Where is the IT office located and what are the extensions?'
  },
  {
    id: 'lockout',
    icon: Lock,
    label: 'Portal Lockout Help',
    message: 'My portal account is locked, what should I do?'
  },
  {
    id: 'leave',
    icon: FileText,
    label: 'Apply for Leave',
    message: 'Show me the steps to apply for employee leave.'
  }
];

// Typing indicator component
const TypingIndicator = () => (
  <div className="flex items-center space-x-1 px-4 py-3 bg-mohi-deep-blue rounded-2xl rounded-bl-md max-w-[80px]">
    <div className="w-2 h-2 bg-mohi-green rounded-full typing-dot"></div>
    <div className="w-2 h-2 bg-mohi-green rounded-full typing-dot"></div>
    <div className="w-2 h-2 bg-mohi-green rounded-full typing-dot"></div>
  </div>
);

// Message bubble component
const MessageBubble = ({ message, isUser, isDark }) => (
  <div
    className={`message-bubble flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}
    data-testid={`message-bubble-${isUser ? 'user' : 'assistant'}`}
  >
    <div
      className={`max-w-[85%] px-4 py-3 rounded-2xl ${
        isUser
          ? 'bg-mohi-green text-white rounded-br-md'
          : isDark
          ? 'bg-mohi-dark-surface text-gray-100 rounded-bl-md border border-gray-700'
          : 'bg-mohi-deep-blue text-white rounded-bl-md'
      }`}
    >
      <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
    </div>
  </div>
);

// Quick action button component
const QuickActionButton = ({ action, onClick, isDark }) => {
  const Icon = action.icon;
  return (
    <button
      onClick={() => onClick(action.message)}
      className={`quick-action-btn flex items-center gap-2 px-3 py-2 rounded-full text-xs font-medium transition-all ${
        isDark
          ? 'bg-mohi-dark-surface text-gray-200 hover:bg-gray-700 border border-gray-700'
          : 'bg-gray-100 text-mohi-deep-blue hover:bg-gray-200'
      }`}
      data-testid={`quick-action-${action.id}`}
    >
      <Icon size={14} className="text-mohi-green" />
      <span>{action.label}</span>
    </button>
  );
};

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [isDark, setIsDark] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [history, setHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Load theme preference from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('rafiki-theme');
    if (savedTheme === 'dark') {
      setIsDark(true);
      document.body.classList.add('dark');
    }
  }, []);

  // Toggle theme and persist
  const toggleTheme = () => {
    const newTheme = !isDark;
    setIsDark(newTheme);
    localStorage.setItem('rafiki-theme', newTheme ? 'dark' : 'light');
    if (newTheme) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  };

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 300);
    }
  }, [isOpen]);

  // Send message to backend
  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    const userMessage = { role: 'user', content: messageText.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Update history for API
    const updatedHistory = [...history, userMessage];
    setHistory(updatedHistory);

    try {
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText.trim(),
          history: updatedHistory,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage = { role: 'assistant', content: data.response };
        setMessages((prev) => [...prev, assistantMessage]);
        setHistory((prev) => [...prev, assistantMessage]);
      } else {
        const errorMessage = {
          role: 'assistant',
          content: "I'm having trouble connecting right now. Please try again in a moment, or contact the IT office directly if this persists. God bless!",
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        role: 'assistant',
        content: "I couldn't reach the server. Please check your connection or contact the IT Department if this continues.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputValue);
  };

  // Handle quick action click
  const handleQuickAction = (message) => {
    sendMessage(message);
  };

  // Handle Enter key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className={`min-h-screen ${isDark ? 'bg-mohi-dark-bg' : 'bg-gradient-to-br from-slate-50 to-blue-50'}`}>
      {/* Demo page content */}
      <div className="container mx-auto px-4 py-12">
        <div className={`text-center max-w-2xl mx-auto ${isDark ? 'text-gray-200' : 'text-mohi-deep-blue'}`}>
          <img
            src={MOHI_LOGO}
            alt="MOHI Logo"
            className="w-24 h-24 mx-auto mb-6 object-contain"
          />
          <h1 className="text-3xl font-bold mb-2">MISSIONS OF HOPE INTERNATIONAL</h1>
          <p className="font-caveat text-2xl text-mohi-green mb-8">IT Support</p>
          <div className={`p-6 rounded-xl ${isDark ? 'bg-mohi-dark-surface border border-gray-700' : 'bg-white shadow-lg'}`}>
            <p className="mb-4">
              Welcome to the MOHI Staff Portal. Click the green chat button in the bottom right corner to get IT support from <span className="font-semibold text-mohi-green">Rafiki</span>, your friendly IT assistant.
            </p>
            <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>
              Rafiki can help you with portal access, IT policies, and general support questions.
            </p>
          </div>
        </div>
      </div>

      {/* Floating Action Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 w-16 h-16 bg-mohi-green rounded-full shadow-xl flex items-center justify-center text-white fab-pulse hover:scale-110 transition-transform z-50"
          data-testid="chat-fab-button"
          aria-label="Open chat"
        >
          <MessageCircle size={28} strokeWidth={2} />
        </button>
      )}

      {/* Chat Widget Container */}
      {isOpen && (
        <div
          className={`fixed bottom-6 right-6 w-[400px] max-w-[calc(100vw-48px)] h-[600px] max-h-[calc(100vh-100px)] rounded-2xl shadow-2xl flex flex-col overflow-hidden chat-container-enter z-50 ${
            isDark ? 'bg-mohi-dark-bg border border-gray-700' : 'bg-white'
          }`}
          data-testid="chat-widget-container"
        >
          {/* Header */}
          <div className={`flex items-center justify-between px-4 py-3 border-b ${
            isDark ? 'bg-mohi-dark-surface border-gray-700' : 'bg-mohi-deep-blue'
          }`}>
            <div className="flex items-center gap-3">
              <img
                src={MOHI_LOGO}
                alt="MOHI Logo"
                className="w-10 h-10 object-contain bg-white rounded-lg p-1"
              />
              <div>
                <h2 className={`font-semibold text-sm ${isDark ? 'text-mohi-deep-blue' : 'text-white'}`} style={{ color: isDark ? '#4595d1' : 'white' }}>
                  MISSIONS OF HOPE
                </h2>
                <p className="font-caveat text-mohi-green text-lg leading-none">
                  Rafiki IT
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className={`p-2 rounded-full transition-colors ${
                  isDark ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-mohi-action-blue/20 text-white'
                }`}
                data-testid="theme-toggle-button"
                aria-label="Toggle theme"
              >
                {isDark ? <Sun size={18} /> : <Moon size={18} />}
              </button>
              {/* Close Button */}
              <button
                onClick={() => setIsOpen(false)}
                className={`p-2 rounded-full transition-colors ${
                  isDark ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-mohi-action-blue/20 text-white'
                }`}
                data-testid="chat-close-button"
                aria-label="Close chat"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {/* Messages Area */}
          <div className={`flex-1 overflow-y-auto p-4 chat-messages ${isDark ? 'bg-mohi-dark-bg' : 'bg-gray-50'}`}>
            {/* Welcome message */}
            {messages.length === 0 && (
              <div className="text-center py-6 animate-fade-in">
                <div className={`w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center ${
                  isDark ? 'bg-mohi-dark-surface' : 'bg-mohi-green/10'
                }`}>
                  <MessageCircle className="text-mohi-green" size={32} />
                </div>
                <h3 className={`font-semibold mb-2 ${isDark ? 'text-gray-200' : 'text-mohi-deep-blue'}`}>
                  Hello! I'm Rafiki
                </h3>
                <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                  Your friendly IT assistant. How can I help you today?
                </p>

                {/* Quick Actions */}
                <div className="mt-6 flex flex-wrap justify-center gap-2" data-testid="quick-actions-container">
                  {QUICK_ACTIONS.map((action) => (
                    <QuickActionButton
                      key={action.id}
                      action={action}
                      onClick={handleQuickAction}
                      isDark={isDark}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Message bubbles */}
            {messages.map((msg, index) => (
              <MessageBubble
                key={index}
                message={msg}
                isUser={msg.role === 'user'}
                isDark={isDark}
              />
            ))}

            {/* Typing indicator */}
            {isTyping && (
              <div className="flex justify-start mb-3" data-testid="typing-indicator">
                <TypingIndicator />
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Actions Bar (after conversation started) */}
          {messages.length > 0 && (
            <div className={`px-4 py-2 border-t flex gap-2 overflow-x-auto ${
              isDark ? 'bg-mohi-dark-surface border-gray-700' : 'bg-white border-gray-200'
            }`}>
              {QUICK_ACTIONS.map((action) => (
                <QuickActionButton
                  key={action.id}
                  action={action}
                  onClick={handleQuickAction}
                  isDark={isDark}
                />
              ))}
            </div>
          )}

          {/* Input Area */}
          <div className={`px-4 py-3 border-t ${
            isDark ? 'bg-mohi-dark-surface border-gray-700' : 'bg-white border-gray-200'
          }`}>
            <form onSubmit={handleSubmit} className="flex items-center gap-2">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask Rafiki about IT support..."
                className={`flex-1 px-4 py-3 rounded-full text-sm focus:ring-2 focus:ring-mohi-green transition-all ${
                  isDark
                    ? 'bg-mohi-dark-bg border border-gray-600 text-gray-100 placeholder-gray-500'
                    : 'bg-gray-100 text-mohi-deep-blue placeholder-gray-500'
                }`}
                data-testid="chat-input"
                disabled={isTyping}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isTyping}
                className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${
                  inputValue.trim() && !isTyping
                    ? 'bg-mohi-green text-white hover:bg-opacity-90 hover:scale-105'
                    : isDark
                    ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
                data-testid="chat-send-button"
                aria-label="Send message"
              >
                <Send size={18} />
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
