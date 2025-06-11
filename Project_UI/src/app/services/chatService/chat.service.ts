import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatApiResponse {
  output: string;
}

export interface ChatApiRequest {
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'https://dnndjh-3000.csb.app/api/n8n-chat'; // Replace with your actual API URL

  constructor(private http: HttpClient) { }

  sendMessage(message: string): Observable<ChatApiResponse> {
    const payload: ChatApiRequest = {
      message: message
    };

    return this.http.post<ChatApiResponse>(this.apiUrl, payload);
  }
}