import {
    useMutation,
    useQuery,
    useQueryClient,
  } from "@tanstack/react-query";
  
  import {
    deleteCollection,
    deleteDocument,
    listCollections,
    listDocuments,
    uploadDocuments,
  } from "../api/documents";
  
  import { getAPIErrorMessage } from "../api/client";
  import { useAppStore } from "../store/appStore";
  import type {
    CollectionCreatePayload,
    CollectionUpdatePayload,
    DocumentRecord,
  } from "../types";
  import {
    createCollection,
    updateCollection,
  } from "../api/documents";
  
  export const documentKeys = {
    all: ["documents"] as const,
    lists: () => [...documentKeys.all, "list"] as const,
    list: (params: Record<string, unknown>) =>
      [...documentKeys.lists(), params] as const,
    detail: (id: string) => [...documentKeys.all, "detail", id] as const,
    chunks: (id: string) => [...documentKeys.all, "chunks", id] as const,
  };
  
  export const collectionKeys = {
    all: ["collections"] as const,
    lists: () => [...collectionKeys.all, "list"] as const,
    list: (params: Record<string, unknown>) =>
      [...collectionKeys.lists(), params] as const,
  };
  
  export function useDocuments(
    page = 1,
    pageSize = 20,
    collectionId?: string | null,
    status?: string,
  ) {
    return useQuery({
      queryKey: documentKeys.list({
        page,
        pageSize,
        collectionId,
        status,
      }),
      queryFn: () =>
        listDocuments({
          page,
          page_size: pageSize,
          collection_id: collectionId || undefined,
          status: status || undefined,
        }),
      staleTime: 10_000,
    });
  }
  
  export function useCollections() {
    const setCollections = useAppStore(
      (state) => state.setCollections,
    );
  
    return useQuery({
      queryKey: collectionKeys.list({ page: 1, pageSize: 100 }),
      queryFn: async () => {
        const result = await listCollections({
          page: 1,
          page_size: 100,
        });
  
        setCollections(result.items);
        return result;
      },
      staleTime: 30_000,
    });
  }
  
  export function useUploadDocuments() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: ({
        files,
        collectionId,
      }: {
        files: File[];
        collectionId?: string | null;
      }) => uploadDocuments(files, collectionId),
  
      onSuccess: async () => {
        await Promise.all([
          queryClient.invalidateQueries({
            queryKey: documentKeys.all,
          }),
          queryClient.invalidateQueries({
            queryKey: collectionKeys.all,
          }),
        ]);
      },
  
      onError: (error) => {
        console.error(getAPIErrorMessage(error));
      },
    });
  }
  
  export function useDeleteDocument() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: (documentId: string) =>
        deleteDocument(documentId),
  
      onSuccess: async (_, documentId) => {
        queryClient.removeQueries({
          queryKey: documentKeys.detail(documentId),
        });
  
        queryClient.removeQueries({
          queryKey: documentKeys.chunks(documentId),
        });
  
        await Promise.all([
          queryClient.invalidateQueries({
            queryKey: documentKeys.all,
          }),
          queryClient.invalidateQueries({
            queryKey: collectionKeys.all,
          }),
        ]);
      },
    });
  }
  
  export function useCreateCollection() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: (payload: CollectionCreatePayload) =>
        createCollection(payload),
  
      onSuccess: async () => {
        await queryClient.invalidateQueries({
          queryKey: collectionKeys.all,
        });
      },
    });
  }
  
  export function useUpdateCollection() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: ({
        id,
        payload,
      }: {
        id: string;
        payload: CollectionUpdatePayload;
      }) => updateCollection(id, payload),
  
      onSuccess: async () => {
        await queryClient.invalidateQueries({
          queryKey: collectionKeys.all,
        });
      },
    });
  }
  
  export function useDeleteCollection() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: (id: string) => deleteCollection(id),
  
      onSuccess: async () => {
        useAppStore.getState().setSelectedCollectionId(null);
  
        await Promise.all([
          queryClient.invalidateQueries({
            queryKey: collectionKeys.all,
          }),
          queryClient.invalidateQueries({
            queryKey: documentKeys.all,
          }),
        ]);
      },
    });
  }
  
  export function useDocumentStatusCounts(
    documents: DocumentRecord[],
  ) {
    return {
      total: documents.length,
      ready: documents.filter((doc) => doc.status === "ready").length,
      processing: documents.filter(
        (doc) => doc.status === "processing",
      ).length,
      failed: documents.filter((doc) => doc.status === "failed").length,
    };
  }