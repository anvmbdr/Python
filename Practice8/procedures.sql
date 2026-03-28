-- 1. Upsert (вставить или обновить)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Массовая вставка с валидацией телефона
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_data TEXT[][])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    p_name VARCHAR;
    p_phone VARCHAR;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts(
        first_name VARCHAR,
        phone VARCHAR
    ) ON COMMIT DELETE ROWS;

    FOR i IN 1 .. array_length(p_data, 1) LOOP
        p_name := p_data[i][1];
        p_phone := p_data[i][2];

        -- Валидация: телефон должен начинаться с + и содержать только цифры после
        IF p_phone ~ '^\+[0-9]{10,15}$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
                UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
            ELSE
                INSERT INTO phonebook(first_name, phone) VALUES(p_name, p_phone);
            END IF;
        ELSE
            INSERT INTO invalid_contacts VALUES(p_name, p_phone);
        END IF;
    END LOOP;

    -- Показать неверные данные
    RAISE NOTICE 'Некорректные контакты:';
    FOR p_name, p_phone IN SELECT * FROM invalid_contacts LOOP
        RAISE NOTICE 'Имя: %, Телефон: %', p_name, p_phone;
    END LOOP;
END;
$$;

-- 3. Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_type = 'name' THEN
        DELETE FROM phonebook WHERE first_name = p_value;
    ELSIF p_type = 'phone' THEN
        DELETE FROM phonebook WHERE phone = p_value;
    END IF;
END;
$$;