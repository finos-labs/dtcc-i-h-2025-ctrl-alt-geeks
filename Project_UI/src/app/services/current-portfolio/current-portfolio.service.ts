import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

// Define an interface for your stock data (used for the current portfolio pie chart)
export interface StockData {
  tradingsymbol: string;
  exchange: string;
  instrument_token: number;
  isin: string;
  product: string;
  price: number;
  quantity: number;
  used_quantity: number;
  t1_quantity: number;
  realised_quantity: number;
  authorised_quantity: number;
  authorised_date: string;
  authorisation: {};
  opening_quantity: number;
  short_quantity: number;
  collateral_quantity: number;
  collateral_type: string;
  discrepancy: boolean;
  average_price: number;
  last_price: number;
  close_price: number;
  pnl: number;
  day_change: number;
  day_change_percentage: number;
  mtf: {
    quantity: number;
    used_quantity: number;
    average_price: number;
    value: number;
    initial_margin: number;
  };
}

// Interface for individual position details within 'net' or 'day' arrays (for the positions table)
export interface PositionDetail {
  tradingsymbol: string;
  exchange: string;
  instrument_token: number;
  product: string;
  quantity: number;
  overnight_quantity: number;
  multiplier: number;
  average_price: number;
  close_price: number;
  last_price: number;
  value: number;
  pnl: number;
  m2m: number;
  unrealised: number;
  realised: number;
  buy_quantity: number;
  buy_price: number;
  buy_value: number;
  buy_m2m: number;
  sell_quantity: number;
  sell_price: number;
  sell_value: number;
  sell_m2m: number;
  day_buy_quantity: number;
  day_buy_price: number;
  day_buy_value: number;
  day_sell_quantity: number;
  day_sell_price: number;
  day_sell_value: number;
}

// Interface for the parsed JSON inside the 'output' string for positions
export interface CurrentPositionsResponseContent {
  net: PositionDetail[];
  day: PositionDetail[];
}

// The API response structure for both current portfolio and current positions
interface ApiResponseWrapper {
  output: string; // The string containing "json\n[...]" or "json\n{...}"
}

@Injectable({
  providedIn: 'root'
})
export class CurrentPortfolioService {
  private apiUrl = 'http://54.69.201.106:5678/webhook/zerodha-agent-chat';

  constructor(private http: HttpClient) {}

  getCurrentPortfolio(): Observable<ApiResponseWrapper> {
    const payload = 'what is the portfolio details. give response in json. Use to the get-holdings tool and give the response in same format as given by tool. Do not modify anything in it';
    return this.http.post<ApiResponseWrapper>(this.apiUrl, payload);
  }

  getCurrentPositions(): Observable<ApiResponseWrapper> {
    const payload = 'What are my current positions, give response in json. Use to the get-positions tool and give the response in same format as given by tool. Do not modify anything in it';
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain',
      'Content-Length': payload.length.toString()
    });
    return this.http.post<ApiResponseWrapper>(this.apiUrl, payload, { headers });
  }
}