import {
    useRef,
    useState,
    type FormEvent,
    type KeyboardEvent,
  } from "react";
  
  import {
    ArrowUp,
    FileSearch,
    Paperclip,
    Square,
    X,
  } from "lucide-react";
  
  interface InputBoxProps {
    onSend: (message: string) => void;
    disabled?: boolean;
    loading?: boolean;
    placeholder?: string;
    selectedDocumentCount?: number;
    onClearDocuments?: () => void;
  }
  
  export default function InputBox({
    onSend,
    disabled = false,
    loading = false,
    placeholder = "Ask a question about your documents...",
    selectedDocumentCount = 0,
    onClearDocuments,
  }: InputBoxProps) {
    const [value, setValue] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);
  
    function resizeTextarea() {
      const textarea = textareaRef.current;
  
      if (!textarea) return;
  
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 180)}px`;
    }
  
    function submit(event: FormEvent<HTMLFormElement>) {
      event.preventDefault();
  
      const message = value.trim();
  
      if (!message || disabled || loading) {
        return;
      }
  
      onSend(message);
      setValue("");
  
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  
    function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
      if (
        event.key === "Enter" &&
        !event.shiftKey &&
        !event.nativeEvent.isComposing
      ) {
        event.preventDefault();
        textareaRef.current?.form?.requestSubmit();
      }
    }
  
    return (
      <div className="chat-composer-wrap">
        {selectedDocumentCount > 0 && (
          <div className="composer-filter">
            <span>
              <FileSearch size={15} />
              Searching {selectedDocumentCount} selected document(s)
            </span>
  
            <button
              type="button"
              onClick={onClearDocuments}
              aria-label="Clear document filter"
            >
              <X size={14} />
              Clear
            </button>
          </div>
        )}
  
        <form className="chat-composer" onSubmit={submit}>
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(event) => {
              setValue(event.target.value);
              resizeTextarea();
            }}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            rows={1}
            maxLength={12000}
            disabled={disabled || loading}
            aria-label="Your question"
          />
  
          <div className="composer-toolbar">
            <div className="composer-toolbar-left">
              <span className="composer-hint">
                <Paperclip size={14} />
                Answers grounded in your files
              </span>
            </div>
  
            <div className="composer-toolbar-right">
              <span className="composer-character-count">
                {value.length.toLocaleString()} / 12,000
              </span>
  
              <button
                type="submit"
                className="composer-send-button"
                disabled={!value.trim() || disabled || loading}
                aria-label={loading ? "Generating answer" : "Send message"}
                title="Send message"
              >
                {loading ? (
                  <Square size={15} />
                ) : (
                  <ArrowUp size={19} />
                )}
              </button>
            </div>
          </div>
        </form>
  
        <p className="composer-disclaimer">
          AI-generated answers may be inaccurate. Verify important claims
          against the cited sources.
        </p>
      </div>
    );
  }