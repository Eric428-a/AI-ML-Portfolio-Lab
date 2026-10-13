import { Link } from "react-router-dom";
import {
  Activity as ActivityIcon,
  ArrowRight,
  CheckCircle2,
  Clock3,
  FileText,
  MessageSquareText,
  XCircle,
} from "lucide-react";

import Loader from "../components/common/Loader";
import EmptyState from "../components/common/EmptyState";
import { useDocuments } from "../hooks/useDocuments";
import { useConversations } from "../hooks/useChat";
import {
  formatDate,
  formatRelativeDate,
} from "../utils/formatters";

export default function Activity() {
  const documentsQuery = useDocuments(1, 100);
  const conversationsQuery = useConversations();

  const documents = documentsQuery.data?.items ?? [];
  const conversations = conversationsQuery.data ?? [];

  if (documentsQuery.isLoading || conversationsQuery.isLoading) {
    return <Loader label="Loading recent activity..." fullPage />;
  }

  const activityItems = [
    ...documents.map((document) => ({
      id: `document-${document.id}`,
      title: document.original_filename,
      description:
        document.status === "ready"
          ? `${document.chunk_count} chunks indexed successfully`
          : document.status === "failed"
            ? document.error_message || "Document processing failed"
            : "Document processing is in progress",
      date: document.updated_at,
      kind: "document" as const,
      status: document.status,
      href: "/documents",
    })),

    ...conversations.map((conversation) => ({
      id: `conversation-${conversation.id}`,
      title: conversation.title,
      description: "Conversation updated",
      date: conversation.updated_at,
      kind: "conversation" as const,
      status: "ready",
      href: `/chat/${conversation.id}`,
    })),
  ].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  );

  return (
    <div className="activity-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">WORKSPACE HISTORY</span>
          <h1>Activity</h1>
          <p>
            Review recent document processing and conversation activity.
          </p>
        </div>
      </div>

      <section className="panel activity-panel">
        <div className="panel-heading">
          <div>
            <h2>Recent activity</h2>
            <p>Latest events from your workspace.</p>
          </div>

          <ActivityIcon size={20} className="panel-heading-icon" />
        </div>

        {activityItems.length === 0 ? (
          <EmptyState
            icon={<ActivityIcon size={25} />}
            title="No activity yet"
            description="Upload a document or start a conversation to see activity here."
            action={
              <Link to="/documents" className="button button-primary">
                Upload documents <ArrowRight size={15} />
              </Link>
            }
          />
        ) : (
          <div className="activity-timeline">
            {activityItems.map((item) => {
              const isDocument = item.kind === "document";

              return (
                <article className="activity-item" key={item.id}>
                  <div
                    className={`activity-item-icon ${
                      item.status === "failed"
                        ? "activity-icon-failed"
                        : item.status === "ready"
                          ? "activity-icon-ready"
                          : "activity-icon-processing"
                    }`}
                  >
                    {isDocument ? (
                      item.status === "failed" ? (
                        <XCircle size={18} />
                      ) : item.status === "ready" ? (
                        <CheckCircle2 size={18} />
                      ) : (
                        <Clock3 size={18} />
                      )
                    ) : (
                      <MessageSquareText size={18} />
                    )}
                  </div>

                  <div className="activity-item-content">
                    <Link to={item.href} className="activity-item-title">
                      {item.title}
                    </Link>

                    <p>{item.description}</p>

                    <div className="activity-item-meta">
                      {isDocument ? (
                        <FileText size={13} />
                      ) : (
                        <MessageSquareText size={13} />
                      )}
                      <span>
                        {isDocument ? "Document" : "Conversation"}
                      </span>
                      <span>·</span>
                      <time dateTime={item.date}>
                        {formatDate(item.date, {
                          month: "short",
                          day: "numeric",
                          hour: "numeric",
                          minute: "2-digit",
                        })}
                      </time>
                    </div>
                  </div>

                  <span className="activity-relative-time">
                    {formatRelativeDate(item.date)}
                  </span>
                </article>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}