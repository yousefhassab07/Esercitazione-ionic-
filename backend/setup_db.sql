USE wrapper;

-- Tabella Categorie
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Tabella Prodotti
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(5,2) NOT NULL,
    category_id INT,
    image_url TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Tabella Tavoli
CREATE TABLE IF NOT EXISTS tables (
    code VARCHAR(10) PRIMARY KEY,
    active BOOLEAN DEFAULT TRUE
);

-- Tabella Ordini
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_code VARCHAR(10),
    customer_name VARCHAR(50),
    product_id INT,
    quantity INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'in attesa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Inserimento Dati di Prova
INSERT IGNORE INTO categories (id, name) VALUES 
(1, 'Nigiri'),
(2, 'Uramaki'),
(3, 'Sashimi');

INSERT IGNORE INTO products (name, price, category_id, image_url) VALUES 
('Sake Nigiri', 3.50, 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Salmon_nigiri.jpg/800px-Salmon_nigiri.jpg'),
('Maguro Nigiri', 4.00, 1, 'https://upload.wikimedia.org/wikipedia/commons/9/9f/Tuna_nigiri.jpg'),
('California Roll', 8.00, 2, 'https://upload.wikimedia.org/wikipedia/commons/1/1a/California_roll.jpg'),
('Salmon Sashimi', 12.00, 3, 'https://upload.wikimedia.org/wikipedia/commons/f/f6/Sashimi_salmon.jpg');

-- Crea un tavolo di prova
INSERT IGNORE INTO tables (code) VALUES ('T1'), ('T2');
