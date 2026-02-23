import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ToastController } from '@ionic/angular';
import { ApiService } from '../api.service';
import { HttpClientModule } from '@angular/common/http';

interface Product {
  id: number;
  name: string;
  price: number;
  category_id: number;
  category_name: string;
  image_url: string;
}

interface Order {
  id: number;
  table_code: string;
  customer_name: string;
  product_id: number;
  product_name: string;
  quantity: number;
  status: string;
  created_at: string;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, HttpClientModule]
})
export class HomePage implements OnInit {
  tableCode: string = '';
  customerName: string = '';
  isLoggedIn: boolean = false;
  segment: string = 'menu';
  menu: Product[] = [];
  categories: string[] = [];
  cart: (Product & { quantity: number })[] = [];
  placedOrders: Order[] = [];

  constructor(private api: ApiService, private toastCtrl: ToastController) {}

  ngOnInit() {}

  login() {
    if (this.tableCode && this.customerName) {
      console.log('Tentativo login con:', this.tableCode, this.customerName);
      this.isLoggedIn = true;
      this.loadMenu();
      this.loadTableStatus();
      setInterval(() => {
        if(this.isLoggedIn) this.loadTableStatus();
      }, 5000);
    }
  }

  loadMenu() {
    console.log('Caricamento menu...');
    this.api.getMenu().subscribe({
      next: (data: Product[]) => {
        console.log('Menu caricato con successo:', data);
        this.menu = data;
        this.categories = [...new Set(data.map((item: Product) => item.category_name))];
      },
      error: (error) => {
        console.error('Errore caricamento menu:', error);
      }
    });
  }

  addToCart(product: Product) {
    const existing = this.cart.find(p => p.id === product.id);
    if (existing) {
      existing.quantity++;
    } else {
      this.cart.push({ ...product, quantity: 1 });
    }
    console.log('Carrello:', this.cart);
  }

  removeFromCart(product: Product) {
    const index = this.cart.findIndex(p => p.id === product.id);
    if (index > -1) {
      this.cart.splice(index, 1);
    }
  }

  getTotal() {
    return this.cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
  }

  async sendOrder() {
    if (this.cart.length === 0) return;

    const orderData = {
      table_code: this.tableCode,
      customer_name: this.customerName,
      items: this.cart.map(item => ({ product_id: item.id, quantity: item.quantity }))
    };

    console.log('Invio ordine:', orderData);
    this.api.placeOrder(orderData).subscribe({
      next: async () => {
        console.log('Ordine inviato con successo');
        const toast = await this.toastCtrl.create({
          message: 'Ordine inviato in cucina!',
          duration: 2000,
          color: 'success'
        });
        toast.present();
        this.cart = [];
        this.segment = 'orders';
        this.loadTableStatus();
      },
      error: (error) => {
        console.error('Errore invio ordine:', error);
      }
    });
  }

  loadTableStatus() {
    if (!this.tableCode) return;
    console.log('Caricamento ordini per tavolo:', this.tableCode);
    this.api.getTableOrders(this.tableCode).subscribe({
      next: (data: Order[]) => {
        console.log('Ordini caricati:', data);
        this.placedOrders = data;
      },
      error: (error) => {
        console.error('Errore caricamento ordini:', error);
      }
    });
  }
}
