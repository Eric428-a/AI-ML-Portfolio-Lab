import { useMemo } from "react";
import { Link } from "react-router-dom";

import {
  ArrowRight,
  ArrowUpRight,
  BookOpen,
  CheckCircle2,
  Clock3,
  FileSearch,
  FileText,
  FolderOpen,
  MessageSquareText,
  Plus,
  Sparkles,
  UploadCloud,
} from "lucide-react";

import Button from "../components/common/Button";
import Loader from "../components/common/Loader";
import EmptyState from "../components/common/EmptyState";

import {
  useCollections,
  useDocuments,
} from "../hooks/useDocuments";

import { useConversations } from "../hooks/useChat";

import {
  formatDate,
  formatFileSize,
  formatRelativeDate,
} from "../utils/formatters";

export default function Dashboard() {
  const documentsQuery = useDocuments(1, 100);
  const collectionsQuery = useCollections();
  const conversationsQuery = useConversations();

  const documents = documentsQuery.data?.items ?? [];
  const collections = collectionsQuery.data?.items ?? [];
  const conversations = conversationsQuery.data ?? [];

  const stats = useMemo(
    () => ({
      documents: documentsQuery.data?.total ?? 0,
      ready: documents.filter((item) => item.status === "ready").length,
      chunks: documents.reduce(
        (sum, item) => sum + item.chunk_count,
        0,
      ),
      collections: collectionsQuery.data?.total ?? 0,
    }),
    [documents, documentsQuery.data, collectionsQuery.data],
  );

  const isLoading =
    documentsQuery.isLoading ||
    collectionsQuery.isLoading ||
    conversationsQuery.isLoading;

  const hasError =
    documentsQuery.isError ||
    collectionsQuery.isError ||
    conversationsQuery.isError;

  if (isLoading) {
    return <Loader label="Loading your workspace..." fullPage />;
  }

  return (
    <div className="dashboard-page">
      <section className="welcome-banner">
        <div className="welcome-banner-content">
          <div className="welcome-kicker">
            <Sparkles size={14} />
            YOUR DOCUMENT WORKSPACE
          </div>

          <h1>Turn your documents into answers.</h1>

          <p>
            Bring your research, reports, and files together.
            Ask questions and explore insights grounded in your sources.
          </p>

          <div className="welcome-actions">
            <Button
              icon={<MessageSquareText size={16} />}
              onClick={() => {
                window.location.assign("/chat");
              }}
            >
              Start a conversation
            </Button>

            <Link to="/documents" className="welcome-secondary-link">
              <UploadCloud size={16} />
              Upload documents
              <ArrowRight size={15} />
            </Link>
          </div>
        </div>

        <div className="welcome-illustration" aria-hidden="true">
          <div className="illustration-orbit orbit-one" />
          <div className="illustration-orbit orbit-two" />

          <div className="illustration-document illustration-document-back">
            <span />
            <span />
            <span />
          </div>

          <div className="illustration-document illustration-document-front">
            <div className="illustration-document-symbol">
              <BookOpen size={28} />
            </div>
            <span />
            <span />
            <span className="illustration-short-line" />
          </div>

          <div className="illustration-sparkle sparkle-one">
            <Sparkles size={19} />
          </div>
          <div className="illustration-sparkle sparkle-two">
            <CheckCircle2 size={18} />
          </div>
        </div>
      </section>

      {hasError && (
        <div className="inline-alert alert-error">
          Some workspace data could not be loaded. Check the API connection.
        </div>
      )}

      <section className="stats-grid">
        <article className="stat-card">
          <div className="stat-icon stat-icon-blue">
            <FileText size={20} />
          </div>
          <p className="stat-label">Total documents</p>
          <div className="stat-value-row">
            <strong>{stats.documents.toLocaleString()}</strong>
            <span className="stat-caption">Uploaded files</span>
          </div>
          <Link to="/documents" className="stat-link">
            View library <ArrowUpRight size={14} />
          </Link>
        </article>

        <article className="stat-card">
          <div className="stat-icon stat-icon-green">
            <CheckCircle2 size={20} />
          </div>
          <p className="stat-label">Indexed documents</p>
          <div className="stat-value-row">
            <strong>{stats.ready.toLocaleString()}</strong>
            <span className="stat-caption">Ready for retrieval</span>
          </div>
          <span className="stat-footnote">
            {stats.documents > 0
              ? `${Math.round((stats.ready / stats.documents) * 100)}% of all files`
              : "Upload your first document"}
          </span>
        </article>

        <article className="stat-card">
          <div className="stat-icon stat-icon-purple">
            <FileSearch size={20} />
          </div>
          <p className="stat-label">Knowledge chunks</p>
          <div className="stat-value-row">
            <strong>{stats.chunks.toLocaleString()}</strong>
            <span className="stat-caption">Searchable passages</span>
          </div>
          <span className="stat-footnote">
            Generated during document processing
          </span>
        </article>

        <article className="stat-card">
          <div className="stat-icon stat-icon-amber">
            <FolderOpen size={20} />
          </div>
          <p className="stat-label">Knowledge bases</p>
          <div className="stat-value-row">
            <strong>{stats.collections.toLocaleString()}</strong>
            <span className="stat-caption">Organized collections</span>
          </div>
          <Link to="/collections" className="stat-link">
            Manage collections <ArrowUpRight size={14} />
          </Link>
        </article>
      </section>

      <div className="dashboard-content-grid">
        <section className="panel dashboard-documents-panel">
          <div className="panel-heading">
            <div>
              <h2>Recent documents</h2>
              <p>Your latest files and processing status.</p>
            </div>

            <Link to="/documents" className="panel-heading-link">
              View all <ArrowRight size={15} />
            </Link>
          </div>

          {documents.length === 0 ? (
            <EmptyState
              icon={<FileText size={24} />}
              title="Your library is empty"
              description="Upload PDF, DOCX, TXT, Markdown, or CSV files to get started."
              action={
                <Link to="/documents" className="button button-primary">
                  <Plus size={16} />
                  Upload documents
                </Link>
              }
            />
          ) : (
            <div className="recent-document-list">
              {documents.slice(0, 5).map((document) => (
                <div
                  key={document.id}
                  className="recent-document-item"
                >
                  <div className="recent-document-icon">
                    <FileText size={19} />
                  </div>

                  <div className="recent-document-info">
                    <strong title={document.original_filename}>
                      {document.original_filename}
                    </strong>
                    <small>
                      {formatFileSize(document.file_size)}
                      {" · "}
                      {formatRelativeDate(document.created_at)}
                    </small>
                  </div>

                  <div
                    className={`mini-status mini-status-${document.status}`}
                  >
                    <span />
                    {document.status}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="panel dashboard-activity-panel">
          <div className="panel-heading">
            <div>
              <h2>Recent conversations</h2>
              <p>Continue your document research.</p>
            </div>

            <Link to="/chat" className="panel-heading-link">
              Open chat <ArrowRight size={15} />
            </Link>
          </div>

          {conversations.length === 0 ? (
            <EmptyState
              icon={<MessageSquareText size={24} />}
              title="No conversations yet"
              description="Start a chat to ask questions across your uploaded documents."
              action={
                <Link to="/chat" className="button button-secondary">
                  Start a chat
                </Link>
              }
            />
          ) : (
            <div className="recent-document-list">
              {conversations.slice(0, 5).map((conversation) => (
                <Link
                  key={conversation.id}
                  to={`/chat/${conversation.id}`}
                  className="recent-document-item recent-conversation-item"
                >
                  <div className="recent-document-icon conversation-icon">
                    <MessageSquareText size={18} />
                  </div>

                  <div className="recent-document-info">
                    <strong>{conversation.title}</strong>
                    <small>
                      {formatDate(conversation.updated_at)}
                    </small>
                  </div>

                  <ArrowRight size={15} className="recent-item-arrow" />
                </Link>
              ))}
            </div>
          )}
        </section>
      </div>

      <section className="quick-start-section">
        <div className="quick-start-heading">
          <div>
            <h2>Make the most of your workspace</h2>
            <p>Three steps to get useful answers from your documents.</p>
          </div>
        </div>

        <div className="quick-start-grid">
          <Link to="/documents" className="quick-start-card">
            <div className="quick-start-number">01</div>
            <div className="quick-start-icon">
              <UploadCloud size={21} />
            </div>
            <h3>Add your documents</h3>
            <p>
              Upload reports, research papers, notes, and datasets.
            </p>
            <span>
              Upload files <ArrowRight size={14} />
            </span>
          </Link>

          <Link to="/collections" className="quick-start-card">
            <div className="quick-start-number">02</div>
            <div className="quick-start-icon">
              <FolderOpen size={21} />
            </div>
            <h3>Organize your knowledge</h3>
            <p>
              Group related documents into dedicated collections.
            </p>
            <span>
              Create a collection <ArrowRight size={14} />
            </span>
          </Link>

          <Link to="/chat" className="quick-start-card">
            <div className="quick-start-number">03</div>
            <div className="quick-start-icon">
              <MessageSquareText size={21} />
            </div>
            <h3>Ask better questions</h3>
            <p>
              Explore ideas and trace answers back to source excerpts.
            </p>
            <span>
              Start asking <ArrowRight size={14} />
            </span>
          </Link>
        </div>
      </section>

      <footer className="dashboard-footer">
        <span>
          <Clock3 size={14} />
          Your workspace data is retrieved from your connected backend.
        </span>
        <Link to="/settings">Workspace settings</Link>
      </footer>
    </div>
  );
}