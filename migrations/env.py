import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context
import sys
import os

# Добавляем путь к приложению, чтобы Alembic видел наш код
sys.path.append(os.getcwd())

# Импортируем наше приложение и базу данных
from orders_service.app import app, db

# Конфигурация логгера
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ссылка на модель (чтобы Alembic видел изменения в классе Order)
target_metadata = db.metadata


def run_migrations_online():
    """Запуск миграций в режиме 'Online' (с подключением к БД)"""

    # Используем контекст приложения Flask, чтобы достать URL подключения
    with app.app_context():
        # Берем URL, который мы настроили в app.py
        db_url = current_app.config['SQLALCHEMY_DATABASE_URI']

        # Подключаемся и запускаем миграции
        connectable = db.engine
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()


run_migrations_online()
