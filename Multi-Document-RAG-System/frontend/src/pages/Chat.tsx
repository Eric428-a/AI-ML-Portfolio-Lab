import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  AlertCircle,
  Bot,
  ChevronDown,
  FileText,
  MessageSquarePlus,
  PanelLeftClose,
  PanelLeftOpen,
  Plus,
  Search,
  Trash2,
} from "lucide-react";

import ChatWindow from "../components/chat/ChatWindow";
import Button from "../components/common/Button";
import Loader from "../components/common/Loader";
import Modal from "../components/common/Modal";

import {
  useConversation,
  useConversations,
  useDeleteConversation,
  useSendMessage,
} from "../hooks/useChat";

import { useCollections, useDocuments } from "../hooks/useDocuments";
import { getAPIErrorMessage } from "../api/client";
import type { ChatMessage, ChatRequest } from "../types";
import { formatRelativeDate } from "../utils/formatters";

export default function Chat() {
  const { conversationId: routeConversationId } = useParams();
  const navigate = useNavigate();

  const [activeConversationId, setActiveConversationId] =
    useState<string | null>(routeConversationId ?? null);

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversationSearch, setConversationSearch] = useState("");
  const [collectionId, setCollectionId] = useState("");
  const [documentId, setDocumentId] = useState("");
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null);
  const [actionError, setActionError] = useState("");
  const [localMessages, setLocalMessages] = useState<ChatMessage[]>([]);

  const conversationsQuery = useConversations();
  const conversationQuery = useConversation(activeConversationId);
  const collectionsQuery = useCollections();
  const documentsQuery = useDocuments(1, 100, collectionId || null);

  const sendMutation = useSendMessage();
  const deleteMutation = useDeleteConversation();

  const conversations = conversationsQuery.data ?? [];
  const selectedConversation = conversationQuery.data;

  useEffect(() => {
    setActiveConversationId(routeConversationId ?? null);
  }, [routeConversationId]);

  useEffect(() => {
    setLocalMessages(selectedConversation?.messages ?? []);
  }, [selectedConversation]);

  useEffect(() => {
    if (!activeConversationId) {
      setLocalMessages([]);
    }
  }, [activeConversationId]);

  const filteredConversations = useMemo(() => {
    const query = conversationSearch.toLowerCase().trim();

    if (!query) return conversations;

    return conversations.filter((conversation) =>
      conversation.title.toLowerCase().includes(query),
    );
  }, [conversations, conversationSearch]);

  function startNewChat() {
    setActiveConversationId(null);
    setLocalMessages([]);
    setCollectionId("");
    setDocumentId("");
    setActionError("");
    navigate("/chat");
  }

  async function handleSend(payload: ChatRequest) {
    setActionError("");

    const question = payload.question;

    const optimisticUserMessage: ChatMessage = {
      id: `pending-${Date.now()}`,
      conversation_id: activeConversationId ?? "",
      role: "user",
      content: question,
      citations: [],
      created_at: new Date().toISOString(),
    };

    setLocalMessages((previous) => [
      ...previous,
      optimisticUserMessage,
    ]);

    try {
      const response = await sendMutation.mutateAsync({
        ...payload,
        conversation_id: activeConversationId,
        collection_id: collectionId || null,
        document_ids: documentId ? [documentId] : null,
      });

      const newConversationId = response.conversation_id;

      const userMessage: ChatMessage = {
        id: `user-${response.message_id}`,
        conversation_id: newConversationId,
        role: "user",
        content: question,
        citations: [],
        created_at: optimisticUserMessage.created_at,
      };

      const assistantMessage: ChatMessage = {
        id: response.message_id,
        conversation_id: newConversationId,
        role: "assistant",
        content: response.answer,
        citations: response.citations ?? [],
        created_at: response.created_at,
      };

      setActiveConversationId(newConversationId);
      setLocalMessages((previous) => [
        ...previous.filter(
          (message) => message.id !== optimisticUserMessage.id,
        ),
        userMessage,
        assistantMessage,
      ]);

      navigate(`/chat/${newConversationId}`, { replace: true });
    } catch (error) {
      setLocalMessages((previous) =>
        previous.filter(
          (message) => message.id !== optimisticUserMessage.id,
        ),
      );

      setActionError(getAPIErrorMessage(error));
    }
  }

  async function handleDeleteConversation() {
    if (!deleteTarget) return;

    setActionError("");

    try {
      await deleteMutation.mutateAsync(deleteTarget);

      if (activeConversationId === deleteTarget) {
        setActiveConversationId(null);
        setLocalMessages([]);
        navigate("/chat");
      }

      setDeleteTarget(null);
    } catch (error) {
      setActionError(getAPIErrorMessage(error));
    }
  }

  if (
    activeConversationId &&
    conversationQuery.isLoading
  ) {
    return <Loader label="Loading conversation..." fullPage />;
  }

  return (
    <div
      className={`chat-page ${sidebarOpen ? "" : "chat-page-sidebar-hidden"}`}
    >
      <aside className="chat-history-sidebar">
        <div className="chat-history-header">
          <div className="chat-history-heading">
            <span className="chat-history-heading-icon">
              <MessageSquarePlus size={19} />
            </span>
            <strong>Conversations</strong>
          </div>

          <button
            type="button"
            className="icon-button"
            onClick={() => setSidebarOpen(false)}
            aria-label="Hide conversation history"
          >
            <PanelLeftClose size={17} />
          </button>
        </div>

        <Button
          fullWidth
          variant="secondary"
          icon={<Plus size={16} />}
          onClick={startNewChat}
        >
          New conversation
        </Button>

        <label className="conversation-search">
          <Search size={15} />
          <input
            value={conversationSearch}
            onChange={(event) =>
              setConversationSearch(event.target.value)
            }
            placeholder="Find a conversation..."
            aria-label="Search conversations"
          />
        </label>

        <div className="conversation-list">
          {conversationsQuery.isLoading ? (
            <Loader label="Loading history..." size={17} />
          ) : filteredConversations.length === 0 ? (
            <div className="conversation-empty">
              <MessageSquarePlus size={22} />
              <p>No conversations found.</p>
            </div>
          ) : (
            filteredConversations.map((conversation) => (
              <div
                key={conversation.id}
                className={`conversation-list-item ${
                  activeConversationId === conversation.id
                    ? "conversation-list-item-active"
                    : ""
                }`}
              >
                <button
                  type="button"
                  className="conversation-select"
                  onClick={() =>
                    navigate(`/chat/${conversation.id}`)
                  }
                >
                  <MessageSquarePlus size={16} />
                  <span>
                    <strong>{conversation.title}</strong>
                    <small>
                      {formatRelativeDate(conversation.updated_at)}
                    </small>
                  </span>
                </button>

                <button
                  type="button"
                  className="conversation-delete"
                  title="Delete conversation"
                  aria-label={`Delete ${conversation.title}`}
                  onClick={() => setDeleteTarget(conversation.id)}
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))
          )}
        </div>

        <div className="chat-history-footer">
          <div className="chat-history-footer-icon">
            <Bot size={19} />
          </div>
          <div>
            <strong>Document intelligence</strong>
            <small>Answers with source citations</small>
          </div>
        </div>
      </aside>

      <section className="chat-main-panel">
        <header className="chat-page-toolbar">
          <div className="chat-page-toolbar-left">
            {!sidebarOpen && (
              <button
                type="button"
                className="icon-button"
                onClick={() => setSidebarOpen(true)}
                aria-label="Show conversation history"
              >
                <PanelLeftOpen size={18} />
              </button>
            )}

            <div>
              <h1>
                {selectedConversation?.title ?? "New conversation"}
              </h1>
              <span className="chat-toolbar-subtitle">
                <span className="connection-dot" />
                Document-grounded assistant
              </span>
            </div>
          </div>

          <div className="chat-scope-controls">
            <label className="chat-scope-select">
              <FileText size={15} />
              <select
                value={collectionId}
                onChange={(event) => {
                  setCollectionId(event.target.value);
                  setDocumentId("");
                }}
                aria-label="Choose knowledge base"
                disabled={sendMutation.isPending}
              >
                <option value="">All documents</option>
                {collectionsQuery.data?.items.map((collection) => (
                  <option key={collection.id} value={collection.id}>
                    {collection.name}
                  </option>
                ))}
              </select>
              <ChevronDown size={13} />
            </label>

            <label className="chat-scope-select chat-document-scope">
              <select
                value={documentId}
                onChange={(event) => setDocumentId(event.target.value)}
                aria-label="Limit search to a document"
                disabled={sendMutation.isPending}
              >
                <option value="">Every document</option>
                {documentsQuery.data?.items
                  .filter((document) => document.status === "ready")
                  .map((document) => (
                    <option key={document.id} value={document.id}>
                      {document.original_filename}
                    </option>
                  ))}
              </select>
              <ChevronDown size={13} />
            </label>
          </div>
        </header>

        {actionError && (
          <div className="inline-alert alert-error chat-page-error">
            <AlertCircle size={16} />
            <span>{actionError}</span>
            <button
              type="button"
              className="icon-button"
              onClick={() => setActionError("")}
              aria-label="Dismiss error"
            >
              ×
            </button>
          </div>
        )}

        {conversationQuery.isError && activeConversationId && (
          <div className="inline-alert alert-error chat-page-error">
            Could not load this conversation. Try returning to the chat list.
            <Link to="/chat">Return to chat</Link>
          </div>
        )}

        <ChatWindow
          messages={localMessages}
          loading={sendMutation.isPending}
          onSend={handleSend}
          conversationId={activeConversationId}
          collectionId={collectionId || null}
          selectedDocumentIds={documentId ? [documentId] : []}
          onClearDocumentFilter={() => setDocumentId("")}
          error={null}
        />
      </section>

      <Modal
        open={Boolean(deleteTarget)}
        title="Delete conversation"
        description="The conversation history will be permanently removed."
        onClose={() => setDeleteTarget(null)}
        width="440px"
      >
        <p className="delete-confirm-description">
          Are you sure you want to delete this conversation? This action
          cannot be undone.
        </p>

        <div className="modal-actions">
          <Button
            variant="secondary"
            onClick={() => setDeleteTarget(null)}
            disabled={deleteMutation.isPending}
          >
            Cancel
          </Button>

          <Button
            variant="danger"
            loading={deleteMutation.isPending}
            onClick={handleDeleteConversation}
          >
            Delete conversation
          </Button>
        </div>
      </Modal>
    </div>
  );
}