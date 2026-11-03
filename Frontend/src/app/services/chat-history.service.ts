import { Injectable } from '@angular/core';
import { ChatSession } from '../models/chat-session.model';

@Injectable({
  providedIn: 'root'
})
export class ChatHistoryService {

  private storageKey = 'ai_task_chat_history';

  // Get all saved conversations
  getAllChats(): ChatSession[] {
    const data = localStorage.getItem(this.storageKey);

    return data ? JSON.parse(data) : [];
  }

  // Save all conversations
  private saveChats(chats: ChatSession[]): void {
    localStorage.setItem(
      this.storageKey,
      JSON.stringify(chats)
    );
  }

  // Create a new conversation
  createChat(): ChatSession {
    const chat: ChatSession = {
      sessionId: crypto.randomUUID(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    const chats = this.getAllChats();

    chats.unshift(chat);

    this.saveChats(chats);

    return chat;
  }

  // Save messages in an existing conversation
  updateChat(chat: ChatSession): void {
    const chats = this.getAllChats();

    const index = chats.findIndex(
      item => item.sessionId === chat.sessionId
    );

    if (index !== -1) {
      chats[index] = {
        ...chat,
        updatedAt: new Date().toISOString()
      };

      this.saveChats(chats);
    }
  }

  // Delete a conversation
  deleteChat(sessionId: string): void {
    const chats = this.getAllChats().filter(
      chat => chat.sessionId !== sessionId
    );

    this.saveChats(chats);
  }

  // Get a specific conversation
  getChat(sessionId: string): ChatSession | undefined {
    return this.getAllChats().find(
      chat => chat.sessionId === sessionId
    );
  }
}