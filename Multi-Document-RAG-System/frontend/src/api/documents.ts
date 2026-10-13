import { apiClient } from "./client";
import type {
  CollectionCreatePayload,
  CollectionListResponse,
  CollectionRecord,
  CollectionUpdatePayload,
  DocumentChunk,
  DocumentListResponse,
  DocumentRecord,
  DocumentUpdatePayload,
  DocumentUploadResponse,
} from "../types";

export interface ListDocumentsParams {
  page?: number;
  page_size?: number;
  collection_id?: string;
  status?: string;
}

export interface ListCollectionsParams {
  page?: number;
  page_size?: number;
}

export async function uploadDocuments(
  files: File[],
  collectionId?: string | null,
): Promise<DocumentUploadResponse> {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await apiClient.post<DocumentUploadResponse>(
    "/documents/upload",
    formData,
    {
      params: collectionId ? { collection_id: collectionId } : undefined,
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 180_000,
    },
  );

  return response.data;
}

export async function listDocuments(
  params: ListDocumentsParams = {},
): Promise<DocumentListResponse> {
  const response = await apiClient.get<DocumentListResponse>(
    "/documents",
    { params },
  );

  return response.data;
}

export async function getDocument(
  documentId: string,
): Promise<DocumentRecord> {
  const response = await apiClient.get<DocumentRecord>(
    `/documents/${encodeURIComponent(documentId)}`,
  );

  return response.data;
}

export async function getDocumentChunks(
  documentId: string,
): Promise<DocumentChunk[]> {
  const response = await apiClient.get<DocumentChunk[]>(
    `/documents/${encodeURIComponent(documentId)}/chunks`,
  );

  return response.data;
}

export async function updateDocument(
  documentId: string,
  payload: DocumentUpdatePayload,
): Promise<DocumentRecord> {
  const response = await apiClient.patch<DocumentRecord>(
    `/documents/${encodeURIComponent(documentId)}`,
    payload,
  );

  return response.data;
}

export async function deleteDocument(
  documentId: string,
): Promise<void> {
  await apiClient.delete(
    `/documents/${encodeURIComponent(documentId)}`,
  );
}

export async function listCollections(
  params: ListCollectionsParams = {},
): Promise<CollectionListResponse> {
  const response = await apiClient.get<CollectionListResponse>(
    "/collections",
    { params },
  );

  return response.data;
}

export async function getCollection(
  collectionId: string,
): Promise<CollectionRecord> {
  const response = await apiClient.get<CollectionRecord>(
    `/collections/${encodeURIComponent(collectionId)}`,
  );

  return response.data;
}

export async function createCollection(
  payload: CollectionCreatePayload,
): Promise<CollectionRecord> {
  const response = await apiClient.post<CollectionRecord>(
    "/collections",
    payload,
  );

  return response.data;
}

export async function updateCollection(
  collectionId: string,
  payload: CollectionUpdatePayload,
): Promise<CollectionRecord> {
  const response = await apiClient.patch<CollectionRecord>(
    `/collections/${encodeURIComponent(collectionId)}`,
    payload,
  );

  return response.data;
}

export async function deleteCollection(
  collectionId: string,
): Promise<void> {
  await apiClient.delete(
    `/collections/${encodeURIComponent(collectionId)}`,
  );
}