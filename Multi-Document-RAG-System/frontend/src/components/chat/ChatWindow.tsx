import {
    useEffect,
    useRef,
    useState,
  } from "react";
  
  import {
    Bot,
    FileSearch,
    Library,
    MessageSquareText,
    Sparkles,
  } from "lucide-react";
  
  import type { ChatMessage, ChatRequest } from "../../types";
  import Message from "./Message";
  import InputBox from "./InputBox";
  import Loader from "../common/Loader";
  
  interface ChatWindowProps {
    messages: ChatMessage[];
    loading?: boolean;
    error?: string | null;
    onSend: (payload: ChatRequest) => void;
    collectionId?: string | null;
    conversationId?: string | null;
    selectedDocumentIds?: string[];
    onClearDocumentFilter?: () => void;
  }
  
  const suggestedQuestions = [
    {
      icon: FileSearch,
      title: "Summarize my documents",
      prompt: "Summarize the main findings across my uploaded documents.",
    },
    {
      icon: Library,
      title: "Compare key information",
      prompt: "Compare the key information and differences across my documents.",
    },
    {
      icon: Sparkles,
      title: "Find important insights",
      prompt: "What are the most important insights supported by my documents?",
    },
    {
      icon: MessageSquareText,
      title: "Ask a specific question",
      prompt: "What are the main conclusions in the available documents?",
    },
  ];
  
  export default function ChatWindow({
    messages,
    loading = false,
    error,
    onSend,
    collectionId,
    conversationId,
    selectedDocumentIds = [],
    onClearDocumentFilter,
  }: ChatWindowProps) {
    const scrollRef = useRef<HTMLDivElement>(null);
    const [lastQuestion, setLastQuestion] = useState("");
  
    useEffect(() => {
      const container = scrollRef.current;
  
      if (!container) return;
  
      container.scrollTo({
        top: container.scrollHeight,
        behavior: "smooth",
      });
    }, [messages, loading]);
  
    function sendQuestion(question: string) {
      const normalized = question.trim();
  
      if (!normalized || loading) return;
  
      setLastQuestion(normalized);
  
      onSend({
        question: normalized,
        conversation_id: conversationId || null,
        collection_id: collectionId || null,
        document_ids:
          selectedDocumentIds.length > 0
            ? selectedDocumentIds
            : null,
        include_sources: true,
      });
    }
  
    return (
      <div className="chat-window">
        <div className="chat-scroll-area" ref={scrollRef}>
          {messages.length === 0 && !loading ? (
            <div className="chat-welcome">
              <div className="welcome-mark">
                <Bot size={30} />
              </div>
  
              <span className="eyebrow">DOCUMENT INTELLIGENCE</span>
  
              <h2>What would you like to know?</h2>
  
              <p>
                Ask questions across your documents. Get clear answers
                with citations pointing back to the original sources.
              </p>
  
              <div className="suggested-question-grid">
                {suggestedQuestions.map((item) => {
                  const Icon = item.icon;
  
                  return (
                    <button
                      type="button"
                      key={item.title}
                      className="suggested-question"
                      onClick={() => sendQuestion(item.prompt)}
                    >
                      <span className="suggested-question-icon">
                        <Icon size={18} />
                      </span>
                      <span>
                        <strong>{item.title}</strong>
                        <small>{item.prompt}</small>
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          ) : (
            <div className="chat-messages">
              {messages.map((message) => (
                <Message
                  key={message.id}
                  message={message}
                />
              ))}
  
              {loading && (
                <div className="assistant-thinking">
                  <div className="message-avatar">
                    <Bot size={18} />
                  </div>
  
                  <div className="thinking-content">
                    <strong>DocuMind AI</strong>
                    <Loader
                      label={
                        lastQuestion
                          ? "Searching sources and preparing an answer..."
                          : "Thinking..."
                      }
                      size={17}
                    />
                  </div>
                </div>
              )}
  
              {error && (
                <div className="inline-alert alert-error chat-error">
                  <span>{error}</span>
                </div>
              )}
            </div>
          )}
        </div>
  
        <div className="chat-input-area">
          <InputBox
            onSend={sendQuestion}
            loading={loading}
            disabled={loading}
            selectedDocumentCount={selectedDocumentIds.length}
            onClearDocuments={onClearDocumentFilter}
          />
        </div>
      </div>
    );
  }