import { useState } from "react";
import {
  Bot,
  Check,
  Copy,
  FileSearch,
  UserRound,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { ChatMessage } from "../../types";
import Citation from "./Citation";
import { formatDate } from "../../utils/formatters";

interface MessageProps {
  message: ChatMessage;
}

export default function Message({ message }: MessageProps) {
  const isAssistant = message.role === "assistant";
  const [copied, setCopied] = useState(false);

  async function copyMessage() {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  }

  return (
    <article
      className={`chat-message ${isAssistant ? "message-assistant" : "message-user"}`}
    >
      <div className="message-avatar">
        {isAssistant ? (
          <Bot size={18} />
        ) : (
          <UserRound size={18} />
        )}
      </div>

      <div className="message-body">
        <div className="message-heading">
          <strong>{isAssistant ? "DocuMind AI" : "You"}</strong>
          <time dateTime={message.created_at}>
            {formatDate(message.created_at, {
              hour: "numeric",
              minute: "2-digit",
            })}
          </time>
        </div>

        <div className="message-content markdown-content">
          {isAssistant ? (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          ) : (
            <p>{message.content}</p>
          )}
        </div>

        {isAssistant && message.citations.length > 0 && (
          <div className="message-citations">
            <div className="message-citations-heading">
              <FileSearch size={15} />
              <strong>Sources</strong>
              <span>{message.citations.length}</span>
            </div>

            <div className="citation-list">
              {message.citations.map((citation, index) => (
                <Citation
                  key={citation.chunk_id}
                  citation={citation}
                  index={index}
                />
              ))}
            </div>
          </div>
        )}

        <div className="message-toolbar">
          <button
            type="button"
            className="message-tool-button"
            onClick={copyMessage}
            aria-label="Copy message"
          >
            {copied ? <Check size={14} /> : <Copy size={14} />}
            {copied ? "Copied" : "Copy"}
          </button>
        </div>
      </div>
    </article>
  );
}