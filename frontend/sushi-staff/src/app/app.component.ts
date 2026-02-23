import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './api.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'sushi-staff';
  orders: any[] = [];
  menu: any[] = [];
  categories: any[] = [];

  // Modello per il nuovo piatto
  newProduct = {
    name: '',
    price: 0,
    category_id: 1,
    image_url: ''
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.refreshData();
    // Aggiorna gli ordini ogni 5 secondi (polling semplice)
    setInterval(() => {
      this.loadOrders();
    }, 5000);
  }

  refreshData() {
    this.loadOrders();
    this.loadMenu();
    this.loadCategories();
  }

  loadOrders() {
    this.api.getOrders().subscribe(data => {
      this.orders = data;
    });
  }

  loadMenu() {
    this.api.getMenu().subscribe(data => {
      this.menu = data;
    });
  }

  loadCategories() {
    this.api.getCategories().subscribe(data => {
      this.categories = data;
    });
  }

  changeStatus(orderId: number, status: string) {
    this.api.updateOrderStatus(orderId, status).subscribe(() => {
      this.loadOrders(); // Ricarica la lista
    });
  }

  addProduct() {
    this.api.addProduct(this.newProduct).subscribe(() => {
      this.loadMenu(); // Ricarica il menu
      // Reset form
      this.newProduct = { name: '', price: 0, category_id: 1, image_url: '' };
    });
  }

  deleteProduct(id: number) {
    if(confirm('Sei sicuro di voler eliminare questo piatto?')) {
      this.api.deleteProduct(id).subscribe(() => {
        this.loadMenu();
      });
    }
  }
}
