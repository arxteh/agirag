-- Создание отдельных баз данных для сервисов.
-- Важно: этот файл выполняется через `psql` на этапе инициализации контейнера Postgres.
-- Поэтому можно использовать psql-метакоманду `gexec`.

SELECT 'CREATE DATABASE n8n'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'n8n')\gexec

SELECT 'CREATE DATABASE flowise'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'flowise')\gexec

SELECT 'CREATE DATABASE langfuse'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'langfuse')\gexec

SELECT 'CREATE DATABASE mlflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mlflow')\gexec
