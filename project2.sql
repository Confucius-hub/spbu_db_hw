-- Создадим временную таблицу для анализа продаж за последний месяц

-- Создание временной таблицы для анализа продаж за последний месяц
CREATE TEMP TABLE monthly_sales_analysis AS
SELECT
    p.id AS product_id,
    p.name AS product_name,
    SUM(s.quantity) AS total_quantity_sold,
    SUM(s.quantity * p.price) AS total_revenue
FROM
    sales s
JOIN
    products p ON s.product_id = p.id
WHERE
    s.sale_date >= NOW()::DATE - INTERVAL '1 month'
GROUP BY
    p.id, p.name
ORDER BY
    total_revenue DESC
LIMIT 10; -- Ограничиваем для анализа топ-10 продуктов

-- Просмотр данных из временной таблицы
SELECT * FROM monthly_sales_analysis;


--Создадим представления для объединения данных о продажах, поставках и остатках
-- Создание представления для объединения продаж, поставок и остатков

CREATE OR REPLACE VIEW warehouse_overview AS
SELECT
    p.id AS product_id,
    p.name AS product_name,
    COALESCE(SUM(s.quantity), 0) AS total_sold,
    COALESCE(SUM(sh.quantity), 0) AS total_supplied,
    st.quantity AS current_stock
FROM
    products p
LEFT JOIN
    sales s ON p.id = s.product_id
LEFT JOIN
    shipments sh ON p.id = sh.product_id
LEFT JOIN
    stock st ON p.id = st.product_id
GROUP BY
    p.id, p.name, st.quantity
ORDER BY
    total_sold DESC;

-- Просмотр данных из представления
SELECT * FROM warehouse_overview LIMIT 10;

--Добавим гораничений для валидации данных

--Ограничение для запрета отрицательных цен:
ALTER TABLE products
ADD CONSTRAINT positive_price CHECK (price >= 0);

--Ограничение для запрета отрицательных остатков на складе:
ALTER TABLE stock
ADD CONSTRAINT non_negative_stock CHECK (quantity >= 0);

--Ограничение для поставок, количество поставленного товара не может быть меньше 1.
ALTER TABLE shipments
ADD CONSTRAINT positive_shipment_quantity CHECK (quantity > 0);

--Ограничение для продаж, Количество проданного товара не может превышать текущий остаток:
-- Создаём функцию для проверки количества проданного товара

CREATE OR REPLACE FUNCTION check_sale_quantity()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, превышает ли количество проданного товара текущий остаток
    IF NEW.quantity > (
        SELECT st.quantity
        FROM stock st
        WHERE st.product_id = NEW.product_id
    ) THEN
        RAISE EXCEPTION 'Количество проданного товара превышает остаток на складе!';
    END IF;

    -- Если проверка пройдена, разрешаем операцию
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаём триггер, который запускает функцию перед вставкой или обновлением

CREATE TRIGGER validate_sale_quantity
BEFORE INSERT OR UPDATE ON sales
FOR EACH ROW
EXECUTE FUNCTION check_sale_quantity();

--Пример запросов с временными струтктурами
-- анализ продаж для топ-5 клиентво по общей сумме покупок за последний месяц:
-- Создание временной таблицы для топ-5 клиентов

CREATE TEMP TABLE top_clients AS
SELECT
    cl.id AS client_id,
    cl.name AS client_name,
    SUM(s.quantity * p.price) AS total_spent
FROM
    sales s
JOIN
    clients cl ON s.client_id = cl.id
JOIN
    products p ON s.product_id = p.id
WHERE
    s.sale_date >= NOW()::DATE - INTERVAL '1 month'
GROUP BY
    cl.id, cl.name
ORDER BY
    total_spent DESC
LIMIT 5;

-- Просмотр временной таблицы
SELECT * FROM top_clients;


--Обновление остатков после продаж:
-- Обновление остатков в таблице stock на основе продаж
UPDATE stock
SET quantity = quantity - (
    SELECT SUM(s.quantity)
    FROM sales s
    WHERE s.product_id = stock.product_id
    GROUP BY s.product_id
)
WHERE product_id IN (
    SELECT DISTINCT product_id FROM sales
);
