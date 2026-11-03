export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  summary?: string;
}

export interface ChatSession {
  sessionId: string;
  title: string;
  messages: ChatMessage[];
  createdAt: string;
  updatedAt: string;
}