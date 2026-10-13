export type DocumentStatus =
  | "processing"
  | "ready"
  | "failed"
  | "pending";

export interface DocumentMetadata {
  [key: string]: unknown;
}

export interface DocumentRecord {
  id: string;
  filename: string;
  original_filename: string;
  content_type: string;
  file_size: number;
  status: DocumentStatus | string;
  error_message: string | null;
  chunk_count: number;
  metadata_json: DocumentMetadata;
  collection_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  chunk_index: number;
  text: string;
  metadata_json: DocumentMetadata;
}

export interface DocumentListResponse {
  items: DocumentRecord[];
  total: number;
  page: number;
  page_size: number;
}

export interface DocumentUploadResponse {
  items: DocumentRecord[];
  accepted: number;
  failed: number;
}

export interface DocumentUpdatePayload {
  filename?: string;
  collection_id?: string | null;
  metadata_json?: DocumentMetadata;
}

export interface CollectionRecord {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  document_count: number;
}

export interface CollectionListResponse {
  items: CollectionRecord[];
  total: number;
}

export interface CollectionCreatePayload {
  name: string;
  description?: string | null;
}

export interface CollectionUpdatePayload {
  name?: string;
  description?: string | null;
}