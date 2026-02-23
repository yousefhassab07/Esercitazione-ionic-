import pymysql

class DatabaseWrapper:
    def __init__(self):
        # Configurazione standard per Codespaces/Localhost
        # Se il DB ha password diversa, la cambieremo dopo.
        self.host = "localhost"
        self.user = "root"
        self.password = "root" 
        self.db_name = "sushi_db"
        self.cursor_class = pymysql.cursors.DictCursor

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name,
            cursorclass=self.cursor_class,
            autocommit=True
        )

    # --- CATEGORIE E PRODOTTI (MENU) ---
    def get_all_categories(self):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM categories")
            result = cursor.fetchall()
        conn.close()
        return result

    def get_menu_items(self):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            # Uniamo prodotti e categorie per il frontend
            query = """
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id
            """
            cursor.execute(query)
            result = cursor.fetchall()
        conn.close()
        return result

    def add_product(self, name, price, category_id, image_url):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO products (name, price, category_id, image_url) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, price, category_id, image_url))
        conn.close()

    def delete_product(self, product_id):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM products WHERE id = %s"
            cursor.execute(sql, (product_id,))
        conn.close()

    # --- TAVOLI ---
    def get_tables(self):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tables")
            result = cursor.fetchall()
        conn.close()
        return result

    def create_table_session(self, table_code, customer_name):
        # Verifica se il tavolo esiste, se no lo crea o aggiorna lo stato
        conn = self.get_connection()
        with conn.cursor() as cursor:
            # Semplificazione: Inseriamo l'utente in una tabella sessioni o ordini,
            # ma per ora ci assicuriamo che il tavolo esista nel DB.
            # L'esercizio chiede "codice tavolo".
            sql = "INSERT INTO tables (code) VALUES (%s) ON DUPLICATE KEY UPDATE code=code"
            cursor.execute(sql, (table_code,))
        conn.close()

    # --- ORDINI ---
    def add_order(self, table_code, customer_name, product_id, quantity=1):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            # Stato iniziale standard: 'in attesa'
            sql = """
                INSERT INTO orders (table_code, customer_name, product_id, quantity, status, created_at)
                VALUES (%s, %s, %s, %s, 'in attesa', NOW())
            """
            cursor.execute(sql, (table_code, customer_name, product_id, quantity))
        conn.close()

    def get_orders_by_table(self, table_code):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            sql = """
                SELECT o.*, p.name as product_name, p.price 
                FROM orders o
                JOIN products p ON o.product_id = p.id
                WHERE o.table_code = %s
                ORDER BY o.created_at DESC
            """
            cursor.execute(sql, (table_code,))
            result = cursor.fetchall()
        conn.close()
        return result

    def get_all_orders_staff(self):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            sql = """
                SELECT o.*, p.name as product_name 
                FROM orders o
                JOIN products p ON o.product_id = p.id
                ORDER BY o.created_at DESC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
        conn.close()
        return result

    def update_order_status(self, order_id, new_status):
        conn = self.get_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE orders SET status = %s WHERE id = %s"
            cursor.execute(sql, (new_status, order_id))
        conn.close()
