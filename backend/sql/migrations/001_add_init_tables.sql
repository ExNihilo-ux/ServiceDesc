-- 001_add_init_tables.sql
-- Created: 2026-10-06 15:21:38
-- Description: Инициализация базовой схемы БД аэропорта (таблицы, типы, индексы)

BEGIN;

-- 1. Расширение для векторного поиска (pgvector)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. ENUM для статусов заявок
CREATE TYPE request_status AS ENUM (
    'new',
    'in_progress',
    'resolved',
    'cancelled'
);

-- 2b. ENUM для ролей пользователей
CREATE TYPE user_role AS ENUM (
    'admin',      
    'executor',   
    'viewer'      
);

-- 3. Таблица категорий заявок
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);  

-- 4. Таблица пользователей (исполнители, администраторы)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'executor',  -- Используем новый ENUM
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Основная таблица заявок
CREATE TABLE requests (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status request_status DEFAULT 'new',
    category_id INT REFERENCES categories(id),
    assignee_id INT REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Геолокация заявки (терминал, гейт, координаты)
CREATE TABLE request_locations (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) UNIQUE NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
    terminal VARCHAR(50),
    gate VARCHAR(20),
    floor INT,
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Контакты заявителя (маскированные PII-данные)
CREATE TABLE request_contacts (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) UNIQUE NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
    phone_hash VARCHAR(255),
    phone_masked VARCHAR(50),
    email_masked VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. AI-анализ заявки (векторное представление)
CREATE TABLE request_ai_analyses (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(50) UNIQUE NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
    summary TEXT,
    predicted_category VARCHAR(255),
    urgency_score FLOAT,
    embedding VECTOR(1536), -- Размерность эмбеддинга OpenAI/text-embedding-3-small
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Индексы для производительности
CREATE INDEX idx_requests_status ON requests(status);
CREATE INDEX idx_requests_category ON requests(category_id);
CREATE INDEX idx_requests_assignee ON requests(assignee_id);
CREATE INDEX idx_ai_embedding ON request_ai_analyses USING hnsw (embedding vector_cosine_ops);

COMMIT;