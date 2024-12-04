--Триггер для автоматического обновления остатков при продажах
-- Когда добавляется запись о продаже, триггер автоматически уменьшает количество товара на складе

-- Функция для уменьшения остатков при продаже

CREATE OR REPLACE FUNCTION update_stock_after_sale()
RETURNS TRIGGER AS $$
BEGIN
    -- Уменьшаем количество товара на складе
    UPDATE stock
    SET quantity = quantity - NEW.quantity
    WHERE product_id = NEW.product_id;

    -- Проверяем, что остаток на складе не стал отрицательным
    IF (SELECT quantity FROM stock WHERE product_id = NEW.product_id) < 0 THEN
        RAISE EXCEPTION 'Остаток на складе не может быть отрицательным!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для уменьшения остатков после продажи

CREATE TRIGGER reduce_stock_on_sale
AFTER INSERT ON sales
FOR EACH ROW
EXECUTE FUNCTION update_stock_after_sale();

--Триггер для автоматического обновления остатков при поставках
--Когда добавляется запись о поставке, триггер автоматически увеличивает количество товара на складе

-- Функция для увеличения остатков при поставке

CREATE OR REPLACE FUNCTION update_stock_after_shipment()
RETURNS TRIGGER AS $$
BEGIN
    -- Увеличиваем количество товара на складе
    UPDATE stock
    SET quantity = quantity + NEW.quantity
    WHERE product_id = NEW.product_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для увеличения остатков после поставки

CREATE TRIGGER increase_stock_on_shipment
AFTER INSERT ON shipments
FOR EACH ROW
EXECUTE FUNCTION update_stock_after_shipment();


-- Транзакция для оформления крупной партии товаров
-- Для одновременного выполнения нескольких операций (например, продажи и списания остатков) используем транзакцию

BEGIN;

-- Добавление новой продажи
INSERT INTO sales (client_id, product_id, quantity, sale_date)
VALUES (1, 1, 15, CURRENT_DATE);

-- Проверяем, что остаток на складе не стал отрицательным
DO $$
BEGIN
        IF (SELECT quantity FROM stock WHERE product_id = 1) < 0 THEN
            RAISE EXCEPTION 'Ошибка: остаток на складе стал отрицательным!';
        END IF;
END $$;

COMMIT;


--Проверка текущего состояния базы данных
--Остатки на складе:

SELECT p.name AS product_name, st.quantity AS current_stock
FROM stock st
JOIN products p ON st.product_id = p.id
ORDER BY p.name
LIMIT 10;

--Продажи за последний месяц:

SELECT p.name AS product_name, SUM(s.quantity) AS total_sold
FROM sales s
JOIN products p ON s.product_id = p.id
WHERE s.sale_date >= NOW()::DATE - INTERVAL '1 month'
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 10;
