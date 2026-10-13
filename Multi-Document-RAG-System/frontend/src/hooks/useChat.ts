import {
    useMutation,
    useQuery,
    useQueryClient,
  } from "@tanstack/react-query";
  
  import {
    deleteConversation,
    getConversation,
    listConversations,
    renameConversation,
    sendChatMessage,
  } from "../api/chat";
  
  import type {
    ChatMessage,
    ChatRequest,
    Conversation,
  } from "../types";
  
  export const chatKeys = {
    all: ["chat"] as const,
    conversations: () => [...chatKeys.all, "conversations"] as const,
    conversation: (id: string) =>
      [...chatKeys.all, "conversation", id] as const,
  };
  
  export function useConversations() {
    return useQuery({
      queryKey: chatKeys.conversations(),
      queryFn: async () => {
        const result = await listConversations({
          page: 1,
          page_size: 100,
        });
  
        return result.items;
      },
    });
  }
  
  export function useConversation(
    conversationId: string | null,
  ) {
    return useQuery({
      queryKey: chatKeys.conversation(conversationId ?? ""),
      queryFn: () => getConversation(conversationId!),
      enabled: Boolean(conversationId),
      staleTime: 0,
    });
  }
  
  export function useSendMessage() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: (payload: ChatRequest) =>
        sendChatMessage(payload),
  
      onSuccess: async (result) => {
        await Promise.all([
          queryClient.invalidateQueries({
            queryKey: chatKeys.conversations(),
          }),
          queryClient.invalidateQueries({
            queryKey: chatKeys.conversation(
              result.conversation_id,
            ),
          }),
        ]);
      },
    });
  }
  
  export function useDeleteConversation() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: (id: string) => deleteConversation(id),
  
      onSuccess: async (_, id) => {
        queryClient.removeQueries({
          queryKey: chatKeys.conversation(id),
        });
  
        await queryClient.invalidateQueries({
          queryKey: chatKeys.conversations(),
        });
      },
    });
  }
  
  export function useRenameConversation() {
    const queryClient = useQueryClient();
  
    return useMutation({
      mutationFn: ({
        id,
        title,
      }: {
        id: string;
        title: string;
      }) => renameConversation(id, title),
  
      onSuccess: async (conversation) => {
        await Promise.all([
          queryClient.invalidateQueries({
            queryKey: chatKeys.conversations(),
          }),
          queryClient.invalidateQueries({
            queryKey: chatKeys.conversation(conversation.id),
          }),
        ]);
      },
    });
  }
  
  export function createOptimisticMessage(
    content: string,
    role: "user" | "assistant",
    conversationId = "",
  ): ChatMessage {
    return {
      id: `optimistic-${crypto.randomUUID()}`,
      conversation_id: conversationId,
      role,
      content,
      citations: [],
      created_at: new Date().toISOString(),
    };
  }
  
  export function appendMessages(
    conversation: Conversation | undefined,
    messages: ChatMessage[],
  ): ChatMessage[] {
    return [...(conversation?.messages ?? []), ...messages];
  }