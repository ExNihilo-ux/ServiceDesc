-- 003_fix_auto_ids_and_refactor_functions.sql
-- Created: 2026-10-07
-- Description: Автогенерация UUID для заявок + оптимизация функций для API

BEGIN;

-- ============================================================================
-- 1. СХЕМА: Добавляем автогенерацию UUID для заявок
-- ============================================================================
ALTER TABLE requests 
ALTER COLUMN id SET DEFAULT gen_random_uuid();

-- ============================================================================
-- 2. ФУНКЦИЯ: upsert_request (API-friendly, возвращает объект заявки)
-- ============================================================================

DROP FUNCTION IF EXISTS upsert_request(
    p_title VARCHAR,
    p_description TEXT,
    p_status request_status,
    p_category_id INT,
    p_assignee_id INT,
    p_id VARCHAR
);

CREATE OR REPLACE FUNCTION upsert_request(
    p_title VARCHAR,
    p_description TEXT,
    p_status request_status,
    p_category_id INT,
    p_assignee_id INT,
    p_id VARCHAR DEFAULT NULL
) RETURNS TABLE(
    out_id VARCHAR,
    out_title VARCHAR,
    out_status request_status,
    out_created_at TIMESTAMPTZ
) AS $$
DECLARE
    v_new_id VARCHAR;
BEGIN
    v_new_id := COALESCE(p_id, gen_random_uuid()::text);
    
    INSERT INTO requests (id, title, description, status, category_id, assignee_id)
    VALUES (v_new_id, p_title, p_description, p_status, p_category_id, p_assignee_id)
    ON CONFLICT (id) DO UPDATE SET
        title = EXCLUDED.title,
        description = EXCLUDED.description,
        status = EXCLUDED.status,
        updated_at = NOW()
    RETURNING id, title, status, created_at 
    INTO out_id, out_title, out_status, out_created_at;  -- Заполняем выходные параметры
    
    RETURN NEXT;  -- Возвращаем заполненную строку
END;
$$ LANGUAGE plpgsql;
-- ============================================================================
-- 3. ФУНКЦИЯ: find_similar_requests (защита от NULL + строгий порог >=)
-- ============================================================================
CREATE OR REPLACE FUNCTION find_similar_requests(
    p_embedding vector, 
    p_threshold double precision DEFAULT 0.7, 
    p_limit integer DEFAULT 5
) RETURNS TABLE(request_id varchar, title varchar, similarity double precision) AS $$
BEGIN
    -- Защита от передачи NULL-вектора
    IF p_embedding IS NULL THEN
        RETURN QUERY SELECT NULL::varchar, NULL::varchar, 0.0::double precision LIMIT 0;
        RETURN;
    END IF;

    RETURN QUERY
    SELECT 
        r.id,
        r.title,
        1 - (ai.embedding <-> p_embedding) AS similarity
    FROM requests r
    JOIN request_ai_analyses ai ON r.id = ai.request_id
    WHERE 1 - (ai.embedding <-> p_embedding) >= p_threshold  -- >= вместо > для точного порога
    ORDER BY ai.embedding <-> p_embedding
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

COMMIT;