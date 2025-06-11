import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class MessageService {
  private apiUrl = '/abc';

  constructor(private http: HttpClient) {}

  sendMessageToApi(message: string): Observable<string> {
    const payload = { message };
    return this.http.post(this.apiUrl, payload, { responseType: 'text' });
  }
}
