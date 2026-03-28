-- 1. Поиск по паттерну
CREATE OR REPLACE FUNCTION search_contacts(p text)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.phone
    FROM phonebook pb
    WHERE pb.first_name ILIKE '%' || p || '%'
       OR pb.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Пагинация
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.first_name, pb.phone
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;