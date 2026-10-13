import { apiClient } from "./client";
import type {
  ChatRequest,
  ChatResponse,
  Conversation,
  ConversationListResponse,
} from "../types";

export interface ListConversationsParams {
  page?: number;
  page_size?: number;
}

export async function sendChatMessage(
  payload: ChatRequest,
): Promise<ChatResponse> {
  const response = await apiClient.post<ChatResponse>(
    "/chat",
    payload,
  );

  return response.data;
}

export async function listConversations(
  params: ListConversationsParams = {},
): Promise<ConversationListResponse> {
  const response = await apiClient.get<ConversationListResponse>(
    "/chat/conversations",
    { params },
  );

  return response.data;
}

export async function getConversation(
  conversationId: string,
): Promise<Conversation> {
  const response = await apiClient.get<Conversation>(
    `/chat/conversations/${encodeURIComponent(conversationId)}`,
  );

  return response.data;
}

export async function renameConversation(
  conversationId: string,
  title: string,
): Promise<Conversation> {
  const response = await apiClient.patch<Conversation>(
    `/chat/conversations/${encodeURIComponent(conversationId)}`,
    { title },
  );

  return response.data;
}

export async function deleteConversation(
  conversationId: string,
): Promise<void> {
  await apiClient.delete(
    `/chat/conversations/${encodeURIComponent(conversationId)}`,
  );
}