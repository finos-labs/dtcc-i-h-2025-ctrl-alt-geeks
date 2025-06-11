import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Interface for the expected portfolio data
export interface ExpectedPortfolioData {
  model_name: string;
  model_large_cap_percentage: number;
  model_large_cap_list: string[];
  model_mid_cap_percentage: number;
  model_mid_cap_list: string[];
  model_small_cap_percentage: number;
  model_small_cap_list: string[];
  model_fixed_income_cap_percentage: number;
  model_fixed_income_list: string[] | null;
  model_cash_percentage: number;
}

@Injectable({
  providedIn: 'root'
})
export class ExpectedPortfolioService {
  private apiUrl = 'https://api.example.com/expected-portfolio'; // Placeholder URL

  constructor(private http: HttpClient) { }

  getExpectedPortfolio(): Observable<ExpectedPortfolioData[]> {
    return this.http.get<ExpectedPortfolioData[]>(this.apiUrl);
  }
}