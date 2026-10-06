-- 001_add_init_tables.down.sql
-- Rollback for 001_add_init_tables

BEGIN;

DROP INDEX IF EXISTS idx_ai_embedding;
DROP INDEX IF EXISTS idx_requests_assignee;
DROP INDEX IF EXISTS idx_requests_category;
DROP INDEX IF EXISTS idx_requests_status;

DROP TABLE IF EXISTS request_ai_analyses CASCADE;
DROP TABLE IF EXISTS request_contacts CASCADE;
DROP TABLE IF EXISTS request_locations CASCADE;
DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

DROP TYPE IF EXISTS request_status;
DROP TYPE IF EXISTS user_role;
DROP EXTENSION IF EXISTS vector;

COMMIT;