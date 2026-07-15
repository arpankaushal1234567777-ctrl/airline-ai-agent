import React, { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  fileName?: string;
  fileType?: 'pdf' | 'image';
  toolCalls?: any[];
  ragSources?: any[];
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'ai',
      text: 'Hello! ✈️ I am your Emirates Customer Support Assistant. You can ask me questions about flight schedules, baggage policies, cancellations, check-in, or get live weather updates.\n\nYou can also upload an itinerary PDF or luggage/boarding pass images directly here!',
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      const ext = file.name.split('.').pop()?.toLowerCase();
      
      if (['pdf', 'png', 'jpg', 'jpeg', 'webp'].includes(ext || '')) {
        setSelectedFile(file);
      } else {
        alert("Unsupported file type. Please upload a PDF, PNG, JPG, JPEG, or WEBP file.");
        if (fileInputRef.current) fileInputRef.current.value = '';
      }
    }
  };

  // Trigger file upload selector
  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  // Clear selected file
  const removeSelectedFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // Submit chat query
  const handleSendMessage = async (e?: React.FormEvent, textOverride?: string) => {
    if (e) e.preventDefault();
    
    const messageToSend = textOverride || inputText;
    if (!messageToSend.trim() && !selectedFile) return;

    // 1. Add User Message Locally
    const fileType = selectedFile 
      ? (selectedFile.name.toLowerCase().endsWith('.pdf') ? 'pdf' : 'image') 
      : undefined;

    const userMessageId = `user-${Date.now()}`;
    const userMessage: Message = {
      id: userMessageId,
      sender: 'user',
      text: messageToSend,
      fileName: selectedFile ? selectedFile.name : undefined,
      fileType: fileType
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setSelectedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
    setIsLoading(true);

    // 2. Prepare FormData
    const formData = new FormData();
    formData.append('message', messageToSend);
    if (selectedFile) {
      formData.append('file', selectedFile);
    }

    try {
      // 3. Post to backend API
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Internal server error');
      }

      const data = await res.json();

      // 4. Add AI Message Locally
      setMessages((prev) => [
        ...prev,
        {
          id: `ai-${Date.now()}`,
          sender: 'ai',
          text: data.answer,
          toolCalls: data.tool_calls,
          ragSources: data.rag_sources
        },
      ]);

    } catch (error: any) {
      console.error('API Error:', error);
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          sender: 'ai',
          text: `⚠️ Error communicating with agent: ${error.message}. Please verify the backend is running.`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Reset Session History
  const handleResetHistory = async () => {
    if (!window.confirm("Are you sure you want to clear the conversation history?")) return;
    
    setIsLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/reset', {
        method: 'POST',
      });

      if (res.ok) {
        setMessages([
          {
            id: 'welcome',
            sender: 'ai',
            text: 'Conversation history reset successfully. How can I help you today? ✈️',
          },
        ]);
        removeSelectedFile();
      } else {
        alert("Failed to reset session history.");
      }
    } catch (error) {
      console.error('Reset Error:', error);
      alert("Failed to connect to backend server to reset.");
    } finally {
      setIsLoading(false);
    }
  };

  // Shortcut queries
  const handleShortcutClick = (text: string) => {
    handleSendMessage(undefined, text);
  };

  return (
    <div className="app-container">
      {/* Background Orbs */}
      <div className="ambient-glow-1"></div>
      <div className="ambient-glow-2"></div>

      {/* Sidebar Panel */}
      <aside className="sidebar">
        <div>
          <div className="logo-section">
            <svg className="logo-icon" viewBox="0 0 24 24">
              <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L14 19v-5.5l8 2.5z"/>
            </svg>
            <div>
              <div className="brand-title">Emirates</div>
              <div className="brand-subtitle">AI Assistant</div>
            </div>
          </div>

          <div className="status-badge">
            <div className="status-dot"></div>
            <span>Support Online</span>
          </div>

          <div className="sidebar-shortcuts">
            <div className="shortcut-label">Quick Actions</div>
            <div 
              className="shortcut-card" 
              onClick={() => handleShortcutClick("Find flights from Dubai to London")}
            >
              ✈️ Search Flights
            </div>
            <div 
              className="shortcut-card" 
              onClick={() => handleShortcutClick("What is the flight status of EK200?")}
            >
              📊 Check Flight Status
            </div>
            <div 
              className="shortcut-card" 
              onClick={() => handleShortcutClick("What is the weather in Dubai?")}
            >
              ☀️ Dubai Weather
            </div>
            <div 
              className="shortcut-card" 
              onClick={() => handleShortcutClick("What is the refund policy for Fully Refundable?")}
            >
              📄 Refund Policy
            </div>
          </div>
        </div>

        <div className="sidebar-footer">
          <button className="reset-button" onClick={handleResetHistory} disabled={isLoading}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
              <path d="M16 3h5v5"/>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
              <path d="M8 21H3v-5"/>
            </svg>
            Reset Session
          </button>
        </div>
      </aside>

      {/* Main Chat Panel */}
      <main className="chat-main">
        {/* Chat Header */}
        <header className="chat-header">
          <div className="chat-header-title">Multimodal Flight Support Desk</div>
          {isLoading && (
            <div className="logs-panel">
              <div className="log-indicator">
                <div className="log-spinner"></div>
                <span>Executing Pipeline...</span>
              </div>
            </div>
          )}
        </header>

        {/* Scrollable Message Box */}
        <div className="messages-container">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
              <div className={`avatar-container ${msg.sender}`}>
                {msg.sender === 'user' ? (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                ) : (
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M22 2L2 22M2 2l20 20" />
                  </svg>
                )}
              </div>
              <div className="message-bubble">
                {msg.text.split('\n').map((line, idx) => (
                  <p key={idx}>{line}</p>
                ))}
                
                {msg.fileName && (
                  <div className="message-file-tag">
                    <svg className="message-file-icon" viewBox="0 0 24 24">
                      {msg.fileType === 'pdf' ? (
                        <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
                      ) : (
                        <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                      )}
                    </svg>
                    <span>{msg.fileName}</span>
                  </div>
                )}

                {/* Collapsible Pipeline Trace for results display */}
                {((msg.toolCalls && msg.toolCalls.length > 0) || (msg.ragSources && msg.ragSources.length > 0)) && (
                  <details className="pipeline-trace">
                    <summary className="trace-summary">
                      <span>🔍 Inspect Execution Trace</span>
                      <span className="trace-arrow">▼</span>
                    </summary>
                    <div className="trace-content">
                      {msg.toolCalls && msg.toolCalls.length > 0 && (
                        <div className="trace-section">
                          <div className="trace-section-title">🛠️ Tool Invocations</div>
                          {msg.toolCalls.map((tc, idx) => (
                            <div key={idx} className="trace-item">
                              <div className="trace-item-header">Executed: <code>{tc.name}</code></div>
                              <pre className="trace-code">Arguments: {JSON.stringify(tc.args, null, 2)}</pre>
                              <pre className="trace-code">Result: {JSON.stringify(tc.result, null, 2)}</pre>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {msg.ragSources && msg.ragSources.length > 0 && (
                        <div className="trace-section">
                          <div className="trace-section-title">📂 Retrieved Knowledge Base Chunks</div>
                          {msg.ragSources.map((source, idx) => (
                            <div key={idx} className="trace-item">
                              <div className="trace-item-header">Source: <code>{source.source.split('/').pop()}</code></div>
                              <blockquote className="trace-quote">"{source.content}"</blockquote>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </details>
                )}
              </div>
            </div>
          ))}

          {/* Loader Dots */}
          {isLoading && (
            <div className="message-wrapper ai">
              <div className="avatar-container ai">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 2L2 22M2 2l20 20" />
                </svg>
              </div>
              <div className="message-bubble">
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Footer Input Strip */}
        <footer className="chat-footer">
          {/* File Selected Indicator */}
          {selectedFile && (
            <div className="file-preview-strip">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c5a059" strokeWidth="2">
                {selectedFile.name.toLowerCase().endsWith('.pdf') ? (
                  <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
                ) : (
                  <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                )}
              </svg>
              <span className="file-preview-name">{selectedFile.name}</span>
              <button className="remove-file-button" onClick={removeSelectedFile}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          )}

          {/* Form */}
          <form className="input-form" onSubmit={(e) => handleSendMessage(e)}>
            <input 
              type="text" 
              className="text-input" 
              placeholder="Ask about flights, policies, weather, or upload documents..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={isLoading}
            />

            <input 
              type="file" 
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: 'none' }}
              accept=".pdf,.png,.jpg,.jpeg,.webp"
            />

            <div className="input-actions">
              <button 
                type="button" 
                className="action-btn"
                onClick={triggerFileSelect}
                disabled={isLoading}
                title="Attach Itinerary or Image"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                </svg>
              </button>

              <button 
                type="submit" 
                className="action-btn send-btn"
                disabled={isLoading || (!inputText.trim() && !selectedFile)}
                title="Send Message"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              </button>
            </div>
          </form>
        </footer>
      </main>
    </div>
  );
}

export default App;
