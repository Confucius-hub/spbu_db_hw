-- Создадим структуру базы данных:
--1) suppliers — поставщики мебели:
    --Поля: id, name, contact_info.
--2) clients — магазины-клиенты:
   --Поля: id, name, contact_info.
--3) products — мебель на складе:
   --Поля: id, name, type, size, price.
--4) stock — учёт текущих остатков на складе:
   --Поля: product_id, quantity.
--5) shipments — поступления товара от поставщиков:
   --Поля: id, supplier_id, product_id, quantity, shipment_date.
--6) sales — отгрузки товара клиентам:
   --Поля: id, client_id, product_id, quantity, sale_date.

-- Таблица поставщиков
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,              -- Уникальный идентификатор поставщика
    name VARCHAR(255) NOT NULL,         -- Название поставщика
    contact_info TEXT                   -- Контактная информация
);

-- Таблица клиентов
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,              -- Уникальный идентификатор клиента
    name VARCHAR(255) NOT NULL,         -- Название клиента
    contact_info TEXT                   -- Контактная информация
);

-- Таблица товаров
CREATE TABLE products (
    id SERIAL PRIMARY KEY,              -- Уникальный идентификатор товара
    name VARCHAR(255) NOT NULL,         -- Название товара
    type VARCHAR(50) NOT NULL,          -- Тип товара (корпусная, мягкая)
    size VARCHAR(50) NOT NULL,          -- Размер товара (крупногабаритная, мелкогабаритная)
    price NUMERIC(10, 2) NOT NULL       -- Цена товара
);

-- Таблица остатков на складе
CREATE TABLE stock (
    product_id INT REFERENCES products(id) ON DELETE CASCADE, -- Ссылка на таблицу товаров
    quantity INT NOT NULL CHECK (quantity >= 0),              -- Количество товара на складе
    PRIMARY KEY (product_id)                                  -- Уникальный идентификатор по товару
);

-- Таблица поставок
CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,              -- Уникальный идентификатор поставки
    supplier_id INT REFERENCES suppliers(id) ON DELETE CASCADE, -- Ссылка на таблицу поставщиков
    product_id INT REFERENCES products(id) ON DELETE CASCADE,   -- Ссылка на таблицу товаров
    quantity INT NOT NULL CHECK (quantity > 0),                 -- Количество поставленного товара
    shipment_date DATE NOT NULL                                  -- Дата поставки
);

-- Таблица продаж
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,              -- Уникальный идентификатор продажи
    client_id INT REFERENCES clients(id) ON DELETE CASCADE,     -- Ссылка на таблицу клиентов
    product_id INT REFERENCES products(id) ON DELETE CASCADE,   -- Ссылка на таблицу товаров
    quantity INT NOT NULL CHECK (quantity > 0),                 -- Количество проданного товара
    sale_date DATE NOT NULL                                      -- Дата продажи
);


--Добавим тестовые записи

--Поставщики:
INSERT INTO suppliers (name, contact_info)
VALUES ('ООО МебельПлюс', 'info@mebelplus.ru'),
('ИП МягкийКомфорт', 'softcomfort@example.com'),
('МебельОптТрейд', 'contact@opttrade.com');

--Клиенты:
INSERT INTO clients (name, contact_info)
VALUES ('Мебельный Магазин №1', 'client1@example.com'),
('Супермаркет Мебели', 'client2@example.com'),
('ЭкономМебель', 'client3@example.com');

--Товары:
INSERT INTO products (name, type, size, price)
VALUES ('Стол деревянный', 'Корпусная', 'Крупногабаритная', 5000),
('Стул пластиковый', 'Корпусная', 'Мелкогабаритная', 1500),
('Диван кожаный', 'Мягкая', 'Крупногабаритная', 25000);

--Остатки:
INSERT INTO stock (product_id, quantity)
VALUES (1, 100), (2, 200), (3, 50);

--Поставки:
INSERT INTO shipments (supplier_id, product_id, quantity, shipment_date)
VALUES (1, 1, 50, CURRENT_DATE - INTERVAL '5 days'),
(2, 2, 100, CURRENT_DATE - INTERVAL '10 days'),
(3, 3, 20, CURRENT_DATE - INTERVAL '2 days');

--Продажи:
INSERT INTO sales (client_id, product_id, quantity, sale_date)
VALUES (1, 1, 10, CURRENT_DATE - INTERVAL '3 days'),
(2, 2, 50, CURRENT_DATE - INTERVAL '7 days'),
(3, 3, 5, CURRENT_DATE - INTERVAL '1 day');

-- Запросы + Агрегации

--Список всех товаров с указанием типа, размера и цен
SELECT id AS product_id, name AS product_name, type AS product_type, size, price
FROM products
ORDER BY price DESC
LIMIT 10; -- Ограничиваем результат, чтобы не перегружать оперативную память

--Остатки товаров на складе
SELECT p.name AS product_name, s.quantity AS stock_quantity
FROM stock s
         JOIN products p ON s.product_id = p.id
ORDER BY s.quantity DESC
LIMIT 10; -- Ограничиваем результат

--Общая стоимость товаров на складе
SELECT SUM(p.price * s.quantity) AS total_stock_value
FROM stock s
JOIN products p ON s.product_id = p.id;

--Топ-5 самых продаваемых товаров за последний месяц
SELECT p.name AS product_name, SUM(s.quantity) AS total_sold
FROM sales s
JOIN products p ON s.product_id = p.id
WHERE s.sale_date >= NOW()::DATE - INTERVAL '1 month'
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 5; -- Ограничиваем результат до топ-5

--Среднее количество товара в поставках
SELECT AVG(sh.quantity) AS average_shipment_quantity
FROM shipments sh;

--Список поставщиков с количеством поставленного товара
SELECT sp.name AS supplier_name, SUM(sh.quantity) AS total_supplied
FROM suppliers sp
JOIN shipments sh ON sp.id = sh.supplier_id
GROUP BY sp.name
ORDER BY total_supplied DESC
LIMIT 10; -- Ограничиваем результат

--Список клиентов с общей суммой их покупок
SELECT cl.name AS client_name, SUM(s.quantity * p.price) AS total_spent
FROM clients cl
JOIN sales s ON cl.id = s.client_id
JOIN products p ON s.product_id = p.id
GROUP BY cl.name
ORDER BY total_spent DESC
LIMIT 10; -- Ограничиваем результат

--Выручка по каждому дню за последний месяц
SELECT s.sale_date, SUM(s.quantity * p.price) AS daily_revenue
FROM sales s
JOIN products p ON s.product_id = p.id
WHERE s.sale_date >= NOW()::DATE - INTERVAL '1 month'
GROUP BY s.sale_date
ORDER BY s.sale_date DESC
LIMIT 10; -- Ограничиваем результат
