import {
    AlertCircle,
    CheckCircle2,
    Clock3,
    File,
    FileSpreadsheet,
    FileText,
    MoreHorizontal,
    Trash2,
  } from "lucide-react";
  
  import type { DocumentRecord } from "../../types";
  import { formatDate, formatFileSize, getFileExtension } from "../../utils/formatters";
  
  interface DocumentCardProps {
    document: DocumentRecord;
    onDelete: (document: DocumentRecord) => void;
    onView?: (document: DocumentRecord) => void;
  }
  
  function DocumentIcon({ filename }: { filename: string }) {
    const extension = getFileExtension(filename);
  
    if (extension === "CSV") {
      return <FileSpreadsheet size={22} />;
    }
  
    if (["PDF", "DOCX", "TXT", "MD"].includes(extension)) {
      return <FileText size={22} />;
    }
  
    return <File size={22} />;
  }
  
  function StatusIndicator({ status }: { status: string }) {
    if (status === "ready") {
      return (
        <span className="status-badge status-ready">
          <CheckCircle2 size={13} /> Ready
        </span>
      );
    }
  
    if (status === "failed") {
      return (
        <span className="status-badge status-failed">
          <AlertCircle size={13} /> Failed
        </span>
      );
    }
  
    return (
      <span className="status-badge status-processing">
        <Clock3 size={13} /> Processing
      </span>
    );
  }
  
  export default function DocumentCard({
    document,
    onDelete,
    onView,
  }: DocumentCardProps) {
    return (
      <article className="document-card">
        <div className="document-card-top">
          <div className="file-type-icon">
            <DocumentIcon filename={document.original_filename} />
          </div>
  
          <div className="document-card-menu">
            <button
              type="button"
              className="icon-button"
              aria-label={`Delete ${document.original_filename}`}
              title="Delete document"
              onClick={() => onDelete(document)}
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>
  
        <button
          type="button"
          className="document-card-title"
          onClick={() => onView?.(document)}
          title={document.original_filename}
        >
          {document.original_filename}
        </button>
  
        <div className="document-card-meta">
          <span>{formatFileSize(document.file_size)}</span>
          <span className="meta-dot">·</span>
          <span>{formatDate(document.created_at)}</span>
        </div>
  
        <div className="document-card-footer">
          <StatusIndicator status={document.status} />
          <span className="chunk-count">
            {document.chunk_count} chunks
          </span>
        </div>
  
        {document.status === "failed" && document.error_message && (
          <p className="document-error-text">
            {document.error_message}
          </p>
        )}
      </article>
    );
  }