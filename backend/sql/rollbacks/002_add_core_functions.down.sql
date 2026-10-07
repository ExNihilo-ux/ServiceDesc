-- ============================================================================
-- Rollback: 002_add_core_functions
-- Created:   2026-10-07 by Daniil
-- 
-- Description:
--   Полное удаление хранимых процедур, триггеров и таблицы аудита статусов.
--   Порядок удаления критически важен из-за зависимостей между объектами.
--
-- WARNING:
--   После выполнения этого скрипта векторный поиск и аудит статусов перестанут работать.
--   Убедись, что приложение не вызывает эти функции во время отката.
-- ============================================================================

BEGIN;

-- 1. Сначала удаляем триггер (зависит от функции log_status_change)
DROP TRIGGER IF EXISTS trg_request_status_change ON requests;

-- 2. Удаляем таблицу аудита (создана в UP-миграции)
DROP TABLE IF EXISTS request_status_history CASCADE;

-- 3. Удаляем хранимые процедуры в обратном порядке создания
DROP FUNCTION IF EXISTS cleanup_old_requests(INTEGER);
DROP FUNCTION IF EXISTS find_similar_requests(VECTOR(1536), FLOAT, INTEGER);
DROP FUNCTION IF EXISTS upsert_request(VARCHAR, VARCHAR, TEXT, request_status, INTEGER, INTEGER);
DROP FUNCTION IF EXISTS log_status_change();

COMMIT;