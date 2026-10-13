import {
    AlertCircle,
    CheckCircle2,
    Clock3,
    FileText,
    MoreHorizontal,
    Trash2,
  } from "lucide-react";
  
  import type { DocumentRecord } from "../../types";
  import {
    formatDate,
    formatFileSize,
    getFileExtension,
  } from "../../utils/formatters";
  
  interface DocumentListProps {
    documents: DocumentRecord[];
    onDelete: (document: DocumentRecord) => void;
    onView?: (document: DocumentRecord) => void;
  }
  
  function StatusBadge({ status }: { status: string }) {
    const config =
      status === "ready"
        ? {
            label: "Ready",
            icon: CheckCircle2,
            className: "status-ready",
          }
        : status === "failed"
          ? {
              label: "Failed",
              icon: AlertCircle,
              className: "status-failed",
            }
          : {
              label: "Processing",
              icon: Clock3,
              className: "status-processing",
            };
  
    const Icon = config.icon;
  
    return (
      <span className={`status-badge ${config.className}`}>
        <Icon size={13} />
        {config.label}
      </span>
    );
  }
  
  export default function DocumentList({
    documents,
    onDelete,
    onView,
  }: DocumentListProps) {
    return (
      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              <th>Document</th>
              <th>Status</th>
              <th>Size</th>
              <th>Chunks</th>
              <th>Added</th>
              <th aria-label="Actions" />
            </tr>
          </thead>
  
          <tbody>
            {documents.map((document) => (
              <tr key={document.id}>
                <td>
                  <button
                    type="button"
                    className="table-document-name"
                    onClick={() => onView?.(document)}
                  >
                    <span className="table-file-icon">
                      <FileText size={19} />
                    </span>
  
                    <span className="table-document-info">
                      <strong>{document.original_filename}</strong>
                      <small>
                        {getFileExtension(document.original_filename)}
                      </small>
                    </span>
                  </button>
                </td>
  
                <td>
                  <StatusBadge status={document.status} />
                </td>
  
                <td className="table-muted">
                  {formatFileSize(document.file_size)}
                </td>
  
                <td className="table-muted">
                  {document.chunk_count}
                </td>
  
                <td className="table-muted">
                  {formatDate(document.created_at)}
                </td>
  
                <td>
                  <button
                    type="button"
                    className="icon-button table-action"
                    onClick={() => onDelete(document)}
                    aria-label={`Delete ${document.original_filename}`}
                    title="Delete document"
                  >
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }