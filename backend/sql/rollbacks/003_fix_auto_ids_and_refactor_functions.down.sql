-- 003_fix_auto_ids_and_refactor_functions.down.sql
-- Rollback: Откат автогенерации ID и возврат старых версий функций

BEGIN;

-- ============================================================================
-- 1. СХЕМА: Убираем автогенерацию UUID
-- ============================================================================
ALTER TABLE requests ALTER COLUMN id DROP DEFAULT;

-- ============================================================================
-- 2. ФУНКЦИЯ: upsert_request (возврат к старой сигнатуре RETURNS VOID/VARCHAR)
-- ============================================================================
CREATE OR REPLACE FUNCTION upsert_request(
    p_id VARCHAR,
    p_title VARCHAR,
    p_description TEXT,
    p_status request_status,
    p_category_id INT,
    p_assignee_id INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO requests (id, title, description, status, category_id, assignee_id)
    VALUES (p_id, p_title, p_description, p_status, p_category_id, p_assignee_id)
    ON CONFLICT (id) DO UPDATE SET
        title = EXCLUDED.title,
        description = EXCLUDED.description,
        status = EXCLUDED.status,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 3. ФУНКЦИЯ: find_similar_requests (возврат к строгому > без защиты от NULL)
-- ============================================================================
CREATE OR REPLACE FUNCTION find_similar_requests(
    p_embedding vector, 
    p_threshold double precision DEFAULT 0.7, 
    p_limit integer DEFAULT 5
) RETURNS TABLE(request_id varchar, title varchar, similarity double precision) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id,
        r.title,
        1 - (ai.embedding <-> p_embedding) AS similarity
    FROM requests r
    JOIN request_ai_analyses ai ON r.id = ai.request_id
    WHERE 1 - (ai.embedding <-> p_embedding) > p_threshold
    ORDER BY ai.embedding <-> p_embedding
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

COMMIT;