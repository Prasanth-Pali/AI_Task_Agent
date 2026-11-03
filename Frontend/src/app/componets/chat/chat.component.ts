
import {
  Component,
  ElementRef,
  ViewChild,
  OnInit
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MarkdownModule } from 'ngx-markdown';

import { ChatHistoryService } from '../../services/chat-history.service';
import {
  ChatSession,
  ChatMessage
} from '../../models/chat-session.model';
import { TaskService } from '../../services/task.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MarkdownModule
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements OnInit {

  @ViewChild('chatContainer')
  chatContainer!: ElementRef<HTMLDivElement>;

  question = '';
  isLoading = false;

  sessionId = '';

  messages: ChatMessage[] = [];

  // Saved conversations
  chatHistory: ChatSession[] = [];

  // Currently selected conversation
  currentChat: ChatSession | null = null;

  constructor(
    private taskService: TaskService,
    private chatHistoryService: ChatHistoryService
  ) {}

  // Initialize chat history
  ngOnInit(): void {

    this.chatHistory = this.chatHistoryService.getAllChats();

    // Restore the most recent conversation
    if (this.chatHistory.length > 0) {

      this.openChat(this.chatHistory[0].sessionId);

    } else {

      this.newChat();

    }
  }

  // Send message to AI
  sendMessage(): void {

    const userQuestion = this.question.trim();

    if (!userQuestion || this.isLoading) {
      return;
    }

    // Create a new conversation if necessary
    if (!this.currentChat) {
      this.newChat();
    }

    // Display user's message
    this.messages.push({
      role: 'user',
      content: userQuestion
    });

    // Clear input
    this.question = '';

    // Save user message immediately
    this.saveCurrentChat();

    // Show loading
    this.isLoading = true;

    this.scrollToBottom();

    // Call FastAPI chat endpoint
    this.taskService.askAI(
      userQuestion,
      this.sessionId
    ).subscribe({

      next: (response) => {

        // Add AI response
        this.messages.push({
          role: 'assistant',
          content: response.answer,
          summary: response.summary
        });

        // Save AI response
        this.saveCurrentChat();

        this.isLoading = false;

        this.scrollToBottom();
      },

      error: (error) => {

        console.error('Chat API Error:', error);

        this.messages.push({
          role: 'assistant',
          content:
            error.error?.detail ||
            'Something went wrong. Please try again.'
        });

        // Save error message too
        this.saveCurrentChat();

        this.isLoading = false;

        this.scrollToBottom();
      }

    });
  }

  // Create a new conversation
  newChat(): void {

    // Create and save a new session
    this.currentChat = this.chatHistoryService.createChat();

    this.sessionId = this.currentChat.sessionId;

    // Clear previous messages
    this.messages = [];

    this.question = '';

    this.isLoading = false;

    // Refresh sidebar
    this.refreshChatHistory();
  }

  // Open an existing conversation
  openChat(sessionId: string): void {

    const chat = this.chatHistoryService.getChat(sessionId);

    if (!chat) {
      return;
    }

    this.currentChat = chat;

    this.sessionId = chat.sessionId;

    // Restore previous messages
    this.messages = [...chat.messages];

    this.question = '';

    this.isLoading = false;

    this.scrollToBottom();
  }

  // Save current conversation
  saveCurrentChat(): void {

    if (!this.currentChat) {
      return;
    }

    this.currentChat.messages = [...this.messages];

    // Generate title from first user message
    const firstMessage = this.messages.find(
      message => message.role === 'user'
    );

    if (firstMessage) {

      this.currentChat.title =
        firstMessage.content.length > 35
          ? firstMessage.content.substring(0, 35) + '...'
          : firstMessage.content;

    }

    this.chatHistoryService.updateChat(this.currentChat);

    this.refreshChatHistory();
  }

  // Refresh sidebar history
  refreshChatHistory(): void {

    this.chatHistory = this.chatHistoryService.getAllChats();

  }

  // Delete a conversation
  deleteChat(sessionId: string, event: Event): void {

    event.stopPropagation();

    this.chatHistoryService.deleteChat(sessionId);

    this.refreshChatHistory();

    // If the deleted chat is currently open
    if (this.currentChat?.sessionId === sessionId) {

      this.currentChat = null;

      this.sessionId = '';

      this.messages = [];

      this.newChat();

    }
  }

  // Suggested prompts
  askSuggestion(prompt: string): void {

    this.question = prompt;

    this.sendMessage();

  }

  // Send message using Enter key
  handleKeydown(event: KeyboardEvent): void {

    if (
      event.key === 'Enter' &&
      !event.shiftKey
    ) {

      event.preventDefault();

      this.sendMessage();

    }
  }

  // Scroll to latest message
  private scrollToBottom(): void {

    setTimeout(() => {

      if (this.chatContainer) {

        const element = this.chatContainer.nativeElement;

        element.scrollTop = element.scrollHeight;

      }

    }, 100);
  }

}
