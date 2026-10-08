# ServiceDesc — Airport Maintenance System

Полноценная экосистема для автоматизированной обработки заявок на техническое обслуживание инфраструктуры аэропорта. Включает бэкенд с ИИ-маршрутизацией, мобильное приложение для фиксации неисправностей и веб-панель администратора.

## 🎯 Бизнес-задача

Сократить время реакции на неисправности за счёт:
1.  **Мгновенной фиксации:** Мобильное приложение позволяет создать заявку с фото и геолокацией за секунды.
2.  **ИИ-классификации:** Бэкенд анализирует контент, определяет тип неисправности и формирует эмбеддинг.
3.  **Поиска прецедентов:** Векторный поиск находит исторические заявки («такая же проблема была в марте, помогла замена X»).
4.  **Автоматической маршрутизации:** Заявка направляется в нужный отдел без диспетчера.
5.  **Контроля исполнения:** Администратор корректирует маршрут; сотрудник решает проблему → заявка закрывается.

## 🏗️ Полная структура проекта

```text
ServiceDesc/
── .env                    # Конфигурация окружения (не коммитить!)
├── .env.example            # Шаблон конфигурации
├── alembic.ini             # Конфиг Alembic для миграций БД
├── docker-compose.yml      # Оркестрация всех сервисов
├── pyproject.toml          # Зависимости бэкенда, конфиг pytest
├── README.md               # Этот файл
│
├── backend/                # Python-бэкенд (FastAPI + asyncpg)
│   ├── app/
│   │   ├── api/v1/         # Роутеры FastAPI, Dependency Injection
│   │   ├── core/           # Инфраструктура (database.py, утилиты)
│   │   ├── repositories/   # Слой данных (Raw SQL, request_repository.py)
│   │   ├── schemas/        # Доменные DTO (requests/, types.py)
│   │   ├── services/       # Бизнес-логика (маршрутизация, ИИ)
│   │   ── settings/       # Типизированная конфигурация (database.py, app.py)
│   ├── scripts/            # Утилиты (new_migration.py, seed data)
│   ├── sql/                # Сырые SQL-скрипты, функции, триггеры
│   └── tests/              # TDD по слоям
│       ├── conftest.py     # Глобальные фикстуры (conn для интеграции)
│       ├── e2e/            # HTTP API тесты (dependency_overrides)
│       ├── integration/    # Тесты репозиториев (транзакции ROLLBACK)
│       └── unit/           # Unit-тесты (валидаторы, бизнес-правила)
│
├── mobile/                 # Flutter-приложение для сотрудников
│   ├── android/            # Нативная конфигурация Android
│   ├── ios/                # Нативная конфигурация iOS
│   ├── lib/                # Dart-код приложения
│   │   ├── core/           # Ядро (DI, routing, network)
│   │   ├── features/       # Фичи (auth, requests, profile)
│   │   └── shared/         # Общие виджеты, утилиты, темы
│   ├── assets/             # Ресурсы (иконки, шрифты, изображения)
│   └── pubspec.yaml        # Зависимости Flutter
│
── web_admin/              # Веб-панель администратора
│   ├── app/                # Next.js / React приложение
│   ├── components/         # UI-компоненты
│   ├── services/           # API-клиенты, хуки
│   ├── styles/             # Глобальные стили, Tailwind config
│   └── package.json        # Зависимости Node.js
│
├── docker/                 # Инфраструктура контейнеров
│   ├── monitoring/         # Prometheus + Grafana стек
│   │   ├── dashboards/     # JSON-дашборды Grafana
│   │   └── prometheus.yaml # Конфигурация сбора метрик
│   ├── nginx/              # Reverse proxy
│   │   └── default.conf    # Конфигурация проксирования
│   └── postgres/           # База данных
│       └── initdb.d/       # Скрипты инициализации БД
│
├── docs/                   # Документация проекта
│   ├── api/                # OpenAPI спецификации
│   ├── architecture/       # ADR (Architecture Decision Records)
│   │   └── decisions/      # Записи архитектурных решений
│   └── mobile/             # Документация мобильного приложения
│
└── shared/                 # Общие ресурсы
    └── openapi/            # Единая спецификация API
        ├── spec.yaml       # OpenAPI 3.0 спецификация
        └── types/          # Общие типы данных

        
## 📚 Документация по модулям

Каждый крупный компонент имеет собственный README с детальным описанием архитектуры, запуска и разработки:

-   **[Backend](backend/README.md)** — FastAPI, asyncpg, TDD, миграции Alembic, векторный поиск.
-   **[Mobile App](mobile/README.md)** — Flutter, архитектура Clean Architecture, работа с камерой/GPS.
-   **[Web Admin](web_admin/README.md)** — Next.js, административная панель, управление заявками.
-   **[Docker Infrastructure](docker/README.md)** — Prometheus, Grafana, Nginx, инициализация БД.
-   **[Shared OpenAPI](shared/openapi/README.md)** — Контракт API, генерация типов, версионирование.
-   **[Architecture Decisions](docs/architecture/decisions/README.md)** — ADR, история технических решений.