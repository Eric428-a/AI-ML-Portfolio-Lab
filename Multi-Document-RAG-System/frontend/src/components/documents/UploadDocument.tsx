import {
    useCallback,
    useRef,
    useState,
    type ChangeEvent,
    type DragEvent,
  } from "react";
  
  import {
    AlertCircle,
    CheckCircle2,
    FileText,
    FolderOpen,
    LoaderCircle,
    UploadCloud,
    X,
  } from "lucide-react";
  
  import Button from "../common/Button";
  import { useCollections, useUploadDocuments } from "../../hooks/useDocuments";
  import { getAPIErrorMessage } from "../../api/client";
  
  const ACCEPTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".csv",
  ];
  
  interface UploadDocumentProps {
    onComplete?: () => void;
  }
  
  export default function UploadDocument({
    onComplete,
  }: UploadDocumentProps) {
    const inputRef = useRef<HTMLInputElement>(null);
    const [files, setFiles] = useState<File[]>([]);
    const [collectionId, setCollectionId] = useState("");
    const [dragging, setDragging] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
  
    const { data: collectionData } = useCollections();
    const uploadMutation = useUploadDocuments();
  
    const validateFiles = useCallback((incoming: File[]) => {
      const accepted: File[] = [];
      const rejected: string[] = [];
  
      for (const file of incoming) {
        const extension = `.${file.name.split(".").pop()?.toLowerCase() ?? ""}`;
  
        if (!ACCEPTED_EXTENSIONS.includes(extension)) {
          rejected.push(`${file.name}: unsupported file type`);
          continue;
        }
  
        if (file.size === 0) {
          rejected.push(`${file.name}: file is empty`);
          continue;
        }
  
        if (file.size > 25 * 1024 * 1024) {
          rejected.push(`${file.name}: maximum size is 25 MB`);
          continue;
        }
  
        accepted.push(file);
      }
  
      setError(rejected.join(". "));
      setSuccess("");
  
      if (accepted.length > 0) {
        setFiles((previous) => {
          const existingKeys = new Set(
            previous.map((file) => `${file.name}:${file.size}:${file.lastModified}`),
          );
  
          const unique = accepted.filter(
            (file) =>
              !existingKeys.has(
                `${file.name}:${file.size}:${file.lastModified}`,
              ),
          );
  
          return [...previous, ...unique].slice(0, 20);
        });
      }
    }, []);
  
    function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
      validateFiles(Array.from(event.target.files ?? []));
  
      if (event.target) {
        event.target.value = "";
      }
    }
  
    function handleDrop(event: DragEvent<HTMLDivElement>) {
      event.preventDefault();
      setDragging(false);
      validateFiles(Array.from(event.dataTransfer.files));
    }
  
    async function handleUpload() {
      if (files.length === 0 || uploadMutation.isPending) {
        return;
      }
  
      setError("");
      setSuccess("");
  
      try {
        const result = await uploadMutation.mutateAsync({
          files,
          collectionId: collectionId || null,
        });
  
        setSuccess(
          `${result.accepted} document(s) indexed successfully. ${
            result.failed > 0
              ? `${result.failed} document(s) failed.`
              : ""
          }`,
        );
  
        setFiles([]);
        onComplete?.();
      } catch (uploadError) {
        setError(getAPIErrorMessage(uploadError));
      }
    }
  
    return (
      <div className="upload-panel">
        <div
          className={`upload-dropzone ${dragging ? "upload-dropzone-active" : ""}`}
          onDragOver={(event) => {
            event.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          role="button"
          tabIndex={0}
          aria-label="Select or drop documents to upload"
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              inputRef.current?.click();
            }
          }}
        >
          <div className="upload-cloud-icon">
            <UploadCloud size={29} />
          </div>
  
          <h3>Upload your documents</h3>
  
          <p>
            Drag and drop your files here, or{" "}
            <span className="upload-browse">browse files</span>
          </p>
  
          <div className="upload-file-types">
            {ACCEPTED_EXTENSIONS.map((extension) => (
              <span key={extension}>{extension.slice(1).toUpperCase()}</span>
            ))}
          </div>
  
          <small>Maximum 25 MB per file · Up to 20 files per upload</small>
  
          <input
            ref={inputRef}
            type="file"
            multiple
            accept={ACCEPTED_EXTENSIONS.join(",")}
            onChange={handleFileChange}
            hidden
          />
        </div>
  
        <div className="upload-collection-field">
          <label htmlFor="upload-collection">
            <FolderOpen size={16} />
            Knowledge base
          </label>
  
          <select
            id="upload-collection"
            value={collectionId}
            onChange={(event) => setCollectionId(event.target.value)}
          >
            <option value="">Default workspace</option>
  
            {collectionData?.items.map((collection) => (
              <option key={collection.id} value={collection.id}>
                {collection.name}
              </option>
            ))}
          </select>
        </div>
  
        {files.length > 0 && (
          <div className="upload-queue">
            <div className="upload-queue-header">
              <strong>Selected files</strong>
              <span>{files.length} / 20</span>
            </div>
  
            {files.map((file) => (
              <div
                className="upload-queue-item"
                key={`${file.name}:${file.size}:${file.lastModified}`}
              >
                <span className="queue-file-icon">
                  <FileText size={19} />
                </span>
  
                <div className="queue-file-info">
                  <strong>{file.name}</strong>
                  <small>
                    {(file.size / (1024 * 1024)).toFixed(2)} MB
                  </small>
                </div>
  
                <button
                  type="button"
                  className="icon-button"
                  aria-label={`Remove ${file.name}`}
                  disabled={uploadMutation.isPending}
                  onClick={() =>
                    setFiles((previous) =>
                      previous.filter((item) => item !== file),
                    )
                  }
                >
                  <X size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
  
        {error && (
          <div className="inline-alert alert-error" role="alert">
            <AlertCircle size={17} />
            <span>{error}</span>
          </div>
        )}
  
        {success && (
          <div className="inline-alert alert-success" role="status">
            <CheckCircle2 size={17} />
            <span>{success}</span>
          </div>
        )}
  
        <div className="upload-actions">
          <Button
            variant="secondary"
            onClick={() => setFiles([])}
            disabled={files.length === 0 || uploadMutation.isPending}
          >
            Clear selection
          </Button>
  
          <Button
            onClick={handleUpload}
            disabled={files.length === 0}
            loading={uploadMutation.isPending}
            icon={
              uploadMutation.isPending ? (
                <LoaderCircle size={16} />
              ) : (
                <UploadCloud size={16} />
              )
            }
          >
            {uploadMutation.isPending
              ? "Processing documents..."
              : `Upload ${files.length || ""} ${files.length === 1 ? "document" : "documents"}`}
          </Button>
        </div>
      </div>
    );
  }