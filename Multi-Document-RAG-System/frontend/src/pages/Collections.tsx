import { useState } from "react";
import { Link } from "react-router-dom";
import {
  AlertCircle,
  ArrowRight,
  BookOpen,
  FileText,
  FolderOpen,
  FolderPlus,
  MoreHorizontal,
  Pencil,
  Plus,
  Search,
  Trash2,
  X,
} from "lucide-react";

import Button from "../components/common/Button";
import EmptyState from "../components/common/EmptyState";
import Loader from "../components/common/Loader";
import Modal from "../components/common/Modal";

import {
  useCollections,
  useCreateCollection,
  useDeleteCollection,
  useUpdateCollection,
} from "../hooks/useDocuments";

import { getAPIErrorMessage } from "../api/client";
import type { CollectionRecord } from "../types";
import { formatDate } from "../utils/formatters";

export default function Collections() {
  const [createOpen, setCreateOpen] = useState(false);
  const [editing, setEditing] = useState<CollectionRecord | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<CollectionRecord | null>(null);
  const [search, setSearch] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  const collectionsQuery = useCollections();
  const createMutation = useCreateCollection();
  const updateMutation = useUpdateCollection();
  const deleteMutation = useDeleteCollection();

  const collections = collectionsQuery.data?.items ?? [];

  const filteredCollections = collections.filter((collection) =>
    `${collection.name} ${collection.description ?? ""}`
      .toLowerCase()
      .includes(search.toLowerCase().trim()),
  );

  function resetForm() {
    setName("");
    setDescription("");
    setError("");
    setCreateOpen(false);
    setEditing(null);
  }

  function beginEdit(collection: CollectionRecord) {
    setEditing(collection);
    setName(collection.name);
    setDescription(collection.description ?? "");
    setError("");
  }

  async function handleSave(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const normalizedName = name.trim();

    if (!normalizedName) {
      setError("Enter a name for this knowledge base.");
      return;
    }

    setError("");

    try {
      if (editing) {
        await updateMutation.mutateAsync({
          id: editing.id,
          payload: {
            name: normalizedName,
            description: description.trim() || null,
          },
        });
      } else {
        await createMutation.mutateAsync({
          name: normalizedName,
          description: description.trim() || null,
        });
      }

      resetForm();
    } catch (mutationError) {
      setError(getAPIErrorMessage(mutationError));
    }
  }

  async function handleDelete() {
    if (!deleteTarget) return;

    setError("");

    try {
      await deleteMutation.mutateAsync(deleteTarget.id);
      setDeleteTarget(null);
    } catch (mutationError) {
      setError(getAPIErrorMessage(mutationError));
    }
  }

  if (collectionsQuery.isLoading) {
    return <Loader label="Loading knowledge bases..." fullPage />;
  }

  return (
    <div className="collections-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">KNOWLEDGE ORGANIZATION</span>
          <h1>Knowledge bases</h1>
          <p>
            Organize related files into focused workspaces for document-grounded
            research and question answering.
          </p>
        </div>

        <Button
          icon={<FolderPlus size={17} />}
          onClick={() => {
            setError("");
            setName("");
            setDescription("");
            setCreateOpen(true);
          }}
        >
          Create knowledge base
        </Button>
      </div>

      {error && !createOpen && !editing && !deleteTarget && (
        <div className="inline-alert alert-error">
          <AlertCircle size={16} />
          <span>{error}</span>
          <button
            type="button"
            className="icon-button"
            onClick={() => setError("")}
            aria-label="Dismiss error"
          >
            <X size={15} />
          </button>
        </div>
      )}

      <div className="collection-overview-strip">
        <div className="collection-overview-icon">
          <FolderOpen size={22} />
        </div>
        <div>
          <strong>{collections.length} knowledge bases</strong>
          <p>
            {collections.reduce(
              (total, collection) => total + collection.document_count,
              0,
            )}{" "}
            documents organized across your collections
          </p>
        </div>
      </div>

      <section className="panel collections-panel">
        <div className="collections-toolbar">
          <div>
            <h2>Your knowledge bases</h2>
            <p>Manage and explore your document collections.</p>
          </div>

          <label className="document-search">
            <Search size={16} />
            <input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search collections..."
              aria-label="Search knowledge bases"
            />
          </label>
        </div>

        {collectionsQuery.isError && (
          <div className="inline-alert alert-error">
            {getAPIErrorMessage(collectionsQuery.error)}
            <Button
              variant="secondary"
              onClick={() => collectionsQuery.refetch()}
            >
              Retry
            </Button>
          </div>
        )}

        {filteredCollections.length === 0 ? (
          <EmptyState
            icon={<FolderOpen size={25} />}
            title={
              collections.length === 0
                ? "Create your first knowledge base"
                : "No matching knowledge bases"
            }
            description={
              collections.length === 0
                ? "Group related documents together so you can organize your research."
                : "Try a different search or create a new knowledge base."
            }
            action={
              <Button
                icon={<Plus size={16} />}
                onClick={() => {
                  setName("");
                  setDescription("");
                  setCreateOpen(true);
                }}
              >
                Create knowledge base
              </Button>
            }
          />
        ) : (
          <div className="collection-card-grid">
            {filteredCollections.map((collection, index) => (
              <article
                className="collection-card"
                key={collection.id}
              >
                <div className="collection-card-top">
                  <div
                    className={`collection-card-icon collection-icon-${index % 4}`}
                  >
                    <FolderOpen size={23} />
                  </div>

                  <div className="collection-card-actions">
                    <button
                      type="button"
                      className="icon-button"
                      title="Edit collection"
                      aria-label={`Edit ${collection.name}`}
                      onClick={() => beginEdit(collection)}
                    >
                      <Pencil size={15} />
                    </button>

                    <button
                      type="button"
                      className="icon-button"
                      title="Delete collection"
                      aria-label={`Delete ${collection.name}`}
                      onClick={() => {
                        setError("");
                        setDeleteTarget(collection);
                      }}
                    >
                      <Trash2 size={15} />
                    </button>
                  </div>
                </div>

                <h3>{collection.name}</h3>

                <p className="collection-description">
                  {collection.description || "No description added."}
                </p>

                <div className="collection-card-meta">
                  <span>
                    <FileText size={15} />
                    {collection.document_count} documents
                  </span>
                  <span>Created {formatDate(collection.created_at)}</span>
                </div>

                <div className="collection-card-footer">
                  <span className="collection-availability">
                    <span />
                    Collection available
                  </span>

                  <Link
                    to={`/chat?collection=${encodeURIComponent(collection.id)}`}
                    className="collection-open-link"
                    onClick={(event) => {
                      event.preventDefault();
                      window.location.assign(
                        `/chat?collection=${encodeURIComponent(collection.id)}`,
                      );
                    }}
                  >
                    Research <ArrowRight size={14} />
                  </Link>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      <div className="collection-note">
        <BookOpen size={17} />
        <p>
          Documents uploaded into a knowledge base are indexed for retrieval.
          Select the corresponding collection in chat to narrow your research.
        </p>
      </div>

      <Modal
        open={createOpen || Boolean(editing)}
        title={editing ? "Edit knowledge base" : "Create knowledge base"}
        description={
          editing
            ? "Update the collection name and description."
            : "Create a dedicated space for related documents."
        }
        onClose={resetForm}
      >
        <form className="collection-form" onSubmit={handleSave}>
          <div className="form-field">
            <label htmlFor="collection-name">Name</label>
            <input
              id="collection-name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="e.g. Engineering research"
              maxLength={160}
              required
              autoFocus
            />
          </div>

          <div className="form-field">
            <label htmlFor="collection-description">
              Description <span>Optional</span>
            </label>
            <textarea
              id="collection-description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Describe the documents this collection will contain..."
              maxLength={2000}
              rows={4}
            />
          </div>

          {error && (
            <div className="inline-alert alert-error" role="alert">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          <div className="modal-actions">
            <Button variant="secondary" onClick={resetForm}>
              Cancel
            </Button>

            <Button
              type="submit"
              loading={createMutation.isPending || updateMutation.isPending}
            >
              {editing ? "Save changes" : "Create collection"}
            </Button>
          </div>
        </form>
      </Modal>

      <Modal
        open={Boolean(deleteTarget)}
        title="Delete knowledge base"
        description="This removes the collection and its associated documents."
        onClose={() => setDeleteTarget(null)}
      >
        {deleteTarget && (
          <>
            <p className="delete-confirm-description">
              Delete <strong>{deleteTarget.name}</strong> and{" "}
              {deleteTarget.document_count} associated document(s)?
              This action cannot be undone.
            </p>

            {error && (
              <div className="inline-alert alert-error">
                {error}
              </div>
            )}

            <div className="modal-actions">
              <Button
                variant="secondary"
                onClick={() => setDeleteTarget(null)}
              >
                Cancel
              </Button>

              <Button
                variant="danger"
                loading={deleteMutation.isPending}
                onClick={handleDelete}
              >
                Delete collection
              </Button>
            </div>
          </>
        )}
      </Modal>
    </div>
  );
}