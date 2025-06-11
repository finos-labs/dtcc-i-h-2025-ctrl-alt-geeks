import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ClientsService {

  constructor(private readonly http: HttpClient) {}

  getClientsData() {
    const url = 'https://dnndjh-3000.csb.app/api/cors-proxy/clients';
    return this.http.get(url).pipe(
      catchError((error) => {
        console.error('Error fetching clients data:', error);
        return throwError(() => new Error('Failed to fetch clients data'));
      })
    );
  }
}
