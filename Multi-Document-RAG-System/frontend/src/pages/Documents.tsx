import { useMemo, useState } from "react";
import {
  AlertCircle,
  FileText,
  LayoutGrid,
  List,
  Plus,
  Search,
  Trash2,
  UploadCloud,
  X,
} from "lucide-react";

import { useQueryClient } from "@tanstack/react-query";

import Button from "../components/common/Button";
import Loader from "../components/common/Loader";
import EmptyState from "../components/common/EmptyState";
import Modal from "../components/common/Modal";
import UploadDocument from "../components/documents/UploadDocument";
import DocumentCard from "../components/documents/DocumentCard";
import DocumentList from "../components/documents/DocumentList";

import {
  documentKeys,
  useDeleteDocument,
  useDocuments,
} from "../hooks/useDocuments";

import { getAPIErrorMessage } from "../api/client";
import type { DocumentRecord } from "../types";
import { formatFileSize, formatDate } from "../utils/formatters";

type ViewMode = "grid" | "list";
type StatusFilter = "all" | "ready" | "processing" | "failed";

export default function Documents() {
  const [viewMode, setViewMode] = useState<ViewMode>("grid");
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [uploadOpen, setUploadOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<DocumentRecord | null>(null);
  const [selectedDocument, setSelectedDocument] = useState<DocumentRecord | null>(null);
  const [actionError, setActionError] = useState("");

  const queryClient = useQueryClient();
  const documentsQuery = useDocuments(1, 100);
  const deleteMutation = useDeleteDocument();

  const documents = documentsQuery.data?.items ?? [];

  const filteredDocuments = useMemo(() => {
    const normalizedSearch = search.toLowerCase().trim();

    return documents.filter((document) => {
      const matchesSearch =
        !normalizedSearch ||
        document.original_filename.toLowerCase().includes(normalizedSearch);

      const matchesStatus =
        statusFilter === "all" || document.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [documents, search, statusFilter]);

  async function handleDelete() {
    if (!deleteTarget) return;

    setActionError("");

    try {
      await deleteMutation.mutateAsync(deleteTarget.id);
      setDeleteTarget(null);

      if (selectedDocument?.id === deleteTarget.id) {
        setSelectedDocument(null);
      }
    } catch (error) {
      setActionError(getAPIErrorMessage(error));
    }
  }

  if (documentsQuery.isLoading) {
    return <Loader label="Loading document library..." fullPage />;
  }

  return (
    <div className="documents-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">KNOWLEDGE MANAGEMENT</span>
          <h1>Documents</h1>
          <p>
            Upload, organize, and manage the files your AI assistant
            uses to answer questions.
          </p>
        </div>

        <Button
          icon={<UploadCloud size={17} />}
          onClick={() => setUploadOpen(true)}
        >
          Upload documents
        </Button>
      </div>

      {documentsQuery.isError && (
        <div className="inline-alert alert-error">
          <AlertCircle size={17} />
          <span>
            {getAPIErrorMessage(documentsQuery.error)}
          </span>
          <Button
            variant="secondary"
            onClick={() => documentsQuery.refetch()}
          >
            Retry
          </Button>
        </div>
      )}

      {actionError && (
        <div className="inline-alert alert-error" role="alert">
          <AlertCircle size={17} />
          <span>{actionError}</span>
          <button
            type="button"
            className="icon-button"
            onClick={() => setActionError("")}
            aria-label="Dismiss error"
          >
            <X size={15} />
          </button>
        </div>
      )}

      <div className="document-summary-strip">
        <div>
          <span className="summary-strip-label">All documents</span>
          <strong>{documents.length}</strong>
        </div>
        <div>
          <span className="summary-strip-label">Indexed</span>
          <strong>
            {documents.filter((doc) => doc.status === "ready").length}
          </strong>
        </div>
        <div>
          <span className="summary-strip-label">Processing</span>
          <strong>
            {documents.filter((doc) => doc.status === "processing").length}
          </strong>
        </div>
        <div>
          <span className="summary-strip-label">Failed</span>
          <strong>
            {documents.filter((doc) => doc.status === "failed").length}
          </strong>
        </div>
      </div>

      <section className="panel documents-library-panel">
        <div className="documents-toolbar">
          <div className="documents-toolbar-heading">
            <h2>Document library</h2>
            <span>{filteredDocuments.length} files</span>
          </div>

          <div className="documents-toolbar-actions">
            <label className="document-search">
              <Search size={16} />
              <input
                type="search"
                placeholder="Search documents..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                aria-label="Search documents"
              />
              {search && (
                <button
                  type="button"
                  aria-label="Clear search"
                  onClick={() => setSearch("")}
                >
                  <X size={14} />
                </button>
              )}
            </label>

            <select
              className="filter-select"
              value={statusFilter}
              onChange={(event) =>
                setStatusFilter(event.target.value as StatusFilter)
              }
              aria-label="Filter by processing status"
            >
              <option value="all">All statuses</option>
              <option value="ready">Ready</option>
              <option value="processing">Processing</option>
              <option value="failed">Failed</option>
            </select>

            <div className="view-toggle" aria-label="Document layout">
              <button
                type="button"
                className={viewMode === "grid" ? "view-toggle-active" : ""}
                onClick={() => setViewMode("grid")}
                aria-label="Grid view"
                aria-pressed={viewMode === "grid"}
              >
                <LayoutGrid size={17} />
              </button>
              <button
                type="button"
                className={viewMode === "list" ? "view-toggle-active" : ""}
                onClick={() => setViewMode("list")}
                aria-label="List view"
                aria-pressed={viewMode === "list"}
              >
                <List size={17} />
              </button>
            </div>
          </div>
        </div>

        {filteredDocuments.length === 0 ? (
          <EmptyState
            icon={<FileText size={25} />}
            title={
              documents.length === 0
                ? "No documents uploaded yet"
                : "No matching documents"
            }
            description={
              documents.length === 0
                ? "Upload your first files to create a searchable knowledge base."
                : "Try a different search term or change the status filter."
            }
            action={
              documents.length === 0 ? (
                <Button
                  icon={<Plus size={16} />}
                  onClick={() => setUploadOpen(true)}
                >
                  Add your first document
                </Button>
              ) : (
                <Button
                  variant="secondary"
                  onClick={() => {
                    setSearch("");
                    setStatusFilter("all");
                  }}
                >
                  Clear filters
                </Button>
              )
            }
          />
        ) : viewMode === "grid" ? (
          <div className="document-card-grid">
            {filteredDocuments.map((document) => (
              <DocumentCard
                key={document.id}
                document={document}
                onDelete={setDeleteTarget}
                onView={setSelectedDocument}
              />
            ))}
          </div>
        ) : (
          <DocumentList
            documents={filteredDocuments}
            onDelete={setDeleteTarget}
            onView={setSelectedDocument}
          />
        )}
      </section>

      <Modal
        open={uploadOpen}
        title="Upload documents"
        description="Add files to your searchable document library."
        onClose={() => setUploadOpen(false)}
        width="680px"
      >
        <UploadDocument
          onComplete={() => {
            setUploadOpen(false);
            void queryClient.invalidateQueries({
              queryKey: documentKeys.all,
            });
          }}
        />
      </Modal>

      <Modal
        open={Boolean(deleteTarget)}
        title="Delete document"
        description="This action removes the document and its indexed passages."
        onClose={() => setDeleteTarget(null)}
        width="460px"
      >
        {deleteTarget && (
          <div className="delete-confirm-content">
            <div className="delete-warning-icon">
              <Trash2 size={22} />
            </div>

            <p>
              Are you sure you want to delete{" "}
              <strong>{deleteTarget.original_filename}</strong>?
              This cannot be undone.
            </p>

            {actionError && (
              <div className="inline-alert alert-error">
                {actionError}
              </div>
            )}

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
                onClick={handleDelete}
              >
                Delete document
              </Button>
            </div>
          </div>
        )}
      </Modal>

      <Modal
        open={Boolean(selectedDocument)}
        title="Document details"
        description="Metadata for the selected document."
        onClose={() => setSelectedDocument(null)}
      >
        {selectedDocument && (
          <div className="document-detail-panel">
            <div className="detail-file-icon">
              <FileText size={27} />
            </div>

            <h3>{selectedDocument.original_filename}</h3>

            <div className="detail-metadata-list">
              <div>
                <span>Status</span>
                <strong>{selectedDocument.status}</strong>
              </div>
              <div>
                <span>File size</span>
                <strong>{formatFileSize(selectedDocument.file_size)}</strong>
              </div>
              <div>
                <span>Indexed chunks</span>
                <strong>{selectedDocument.chunk_count}</strong>
              </div>
              <div>
                <span>Uploaded</span>
                <strong>{formatDate(selectedDocument.created_at)}</strong>
              </div>
              <div>
                <span>Document ID</span>
                <code>{selectedDocument.id}</code>
              </div>
            </div>

            {selectedDocument.error_message && (
              <div className="inline-alert alert-error">
                {selectedDocument.error_message}
              </div>
            )}

            <Button
              variant="secondary"
              fullWidth
              onClick={() => setSelectedDocument(null)}
            >
              Close
            </Button>
          </div>
        )}
      </Modal>
    </div>
  );
}