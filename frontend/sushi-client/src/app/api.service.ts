import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // Usa l'URL pubblico HTTPS del backend
  private baseUrl = 'https://refactored-waffle-r49qjg9jqwp5cwp57-5000.app.github.dev/api';

  constructor(private http: HttpClient) { }

  getMenu(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/products`);
  }

  placeOrder(orderData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/orders`, orderData);
  }

  getTableOrders(tableCode: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/orders/${tableCode}`);
  }
}
