-- ============================================================================
-- Migration: 002_add_core_functions
-- Created:   2026-10-07 by Daniil
-- Type:      FUNCTIONS & TRIGGERS
-- 
-- Description:
--   Добавляет хранимые процедуры для безопасного upsert заявок, векторного поиска,
--   автоматического аудита статусов и очистки устаревших данных.
--
-- Dependencies:
--   - Требуется расширение vector (из миграции 001)
--   - Таблицы requests, categories, users, request_ai_analyses должны существовать
--
-- Rollback:
--   См. sql/rollbacks/002_add_core_functions.down.sql
-- ============================================================================

BEGIN;

-- 1. Таблица истории изменений статусов
CREATE TABLE IF NOT EXISTS request_status_history (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
    old_status request_status,
    new_status request_status NOT NULL,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    changed_by INT REFERENCES users(id)
);

COMMENT ON TABLE request_status_history IS 'Аудит переходов статусов заявок';

-- 2. Функция логирования изменения статуса (для триггера)
CREATE OR REPLACE FUNCTION log_status_change() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO request_status_history (request_id, old_status, new_status, changed_by)
        VALUES (NEW.id, OLD.status, NEW.status, NEW.assignee_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION log_status_change() IS 'Триггерная функция для записи в request_status_history';

-- Привязка триггера к таблице заявок
DROP TRIGGER IF EXISTS trg_request_status_change ON requests;
CREATE TRIGGER trg_request_status_change
AFTER UPDATE ON requests
FOR EACH ROW EXECUTE FUNCTION log_status_change();

-- 3. Безопасный upsert заявки (INSERT или UPDATE)
CREATE OR REPLACE FUNCTION upsert_request(
    p_id VARCHAR(50),
    p_title VARCHAR(500),
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
        category_id = EXCLUDED.category_id,
        assignee_id = EXCLUDED.assignee_id,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION upsert_request(VARCHAR, VARCHAR, TEXT, request_status, INT, INT) 
IS 'Атомарное создание или обновление заявки по ID';

-- 4. Векторный поиск похожих заявок через pgvector
CREATE OR REPLACE FUNCTION find_similar_requests(
    p_embedding VECTOR(1536),
    p_threshold FLOAT DEFAULT 0.7,
    p_limit INT DEFAULT 5
) RETURNS TABLE (
    request_id VARCHAR(50),
    title VARCHAR(500),
    similarity FLOAT
) AS $$
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

COMMENT ON FUNCTION find_similar_requests(VECTOR(1536), FLOAT, INT) 
IS 'Поиск семантически похожих заявок по вектору эмбеддинга';

-- 5. Очистка отмененных заявок старше N дней
CREATE OR REPLACE FUNCTION cleanup_old_requests(p_days INT DEFAULT 90) RETURNS INT AS $$
DECLARE
    deleted_count INT;
BEGIN
    DELETE FROM requests 
    WHERE created_at < NOW() - (p_days || ' days')::INTERVAL
      AND status = 'cancelled';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION cleanup_old_requests(INT) 
IS 'Удаление отмененных заявок старше указанного количества дней';

COMMIT;