export interface Citation {
    document_id: string;
    filename: string;
    chunk_id: string;
    chunk_index: number;
    text: string;
    score: number | null;
    page: number | null;
  }
  
  export interface ChatRequest {
    question: string;
    conversation_id?: string | null;
    collection_id?: string | null;
    document_ids?: string[] | null;
    top_k?: number;
    include_sources?: boolean;
  }
  
  export interface ChatResponse {
    answer: string;
    conversation_id: string;
    message_id: string;
    citations: Citation[];
    retrieved_chunks: number;
    model: string;
    created_at: string;
  }
  
  export interface ChatMessage {
    id: string;
    conversation_id: string;
    role: "user" | "assistant" | string;
    content: string;
    citations: Citation[];
    created_at: string;
  }
  
  export interface Conversation {
    id: string;
    title: string;
    collection_id: string | null;
    created_at: string;
    updated_at: string;
    messages: ChatMessage[];
  }
  
  export interface ConversationListResponse {
    items: Conversation[];
    total: number;
  }
  
  export interface APIError {
    success?: boolean;
    detail?: string;
    error?: {
      code?: string;
      message?: string;
      details?: unknown;
    };
  }