import { Component, ElementRef, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';// Import the chat service
import { ChatService } from '../services/chatService/chat.service';

interface ChatMessage {
  text: string;
  isUser: boolean;
  timestamp: Date;
}

@Component({
  selector: 'app-chat',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
  standalone: true,
})
export class ChatComponent {

  constructor(
    private router: Router,
    private chatService: ChatService // Inject the chat service
  ) { }

  @Output() tabChanged = new EventEmitter<{ tab: string; clientId: string | null }>();

  @ViewChild('chatMessages') private chatMessagesContainer!: ElementRef;

  loading: boolean = false;
  clientId: string = '';

  messages: ChatMessage[] = [
    {
      text: 'Hello! How can I help you today?',
      isUser: false,
      timestamp: new Date(),
    },
  ];

  currentMessage: string = '';
  private shouldScrollToBottom = false;

  // New property to control chat visibility
  isChatOpen: boolean = false;

  sendMessage(): void {
    const message = this.currentMessage.trim();

    if (message && !this.loading) {
      // Add user message
      this.messages.push({
        text: message,
        isUser: true,
        timestamp: new Date(),
      });

      // Clear input
      this.currentMessage = '';
      this.shouldScrollToBottom = true;
      this.loading = true; // Set loading to prevent multiple requests

      // Call the API service
      this.chatService.sendMessage(message).subscribe({
        next: (response) => {
          // Add bot response from API
          this.messages.push({
            text: response?.output,
            isUser: false,
            timestamp: new Date(),
          });
          this.shouldScrollToBottom = true;
          this.loading = false;
        },
        error: (error) => {
          console.error('Error sending message:', error);
          // Add error message
          this.messages.push({
            text: 'Sorry, I encountered an error. Please try again.',
            isUser: false,
            timestamp: new Date(),
          });
          this.shouldScrollToBottom = true;
          this.loading = false;
        }
      });
    }
  }

  handleKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.sendMessage();
    }
  }

  // New method to toggle chat visibility
  toggleChat(): void {
    this.isChatOpen = !this.isChatOpen;
    if (this.isChatOpen) {
      // Scroll to bottom when chat opens
      setTimeout(() => {
        this.shouldScrollToBottom = true;
      }, 100);
    }
  }

  ngAfterViewChecked(): void {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  private scrollToBottom(): void {
    try {
      if (this.chatMessagesContainer) {
        this.chatMessagesContainer.nativeElement.scrollTop =
          this.chatMessagesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.error('Error scrolling to bottom:', err);
    }
  }
}