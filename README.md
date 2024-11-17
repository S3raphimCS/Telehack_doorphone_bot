# [Hackathon_telehack](https://telehack.ru/services/) 

## Репозиторий команды <u>Via Dolorosa</u>

### Состав команды:
1) <a href="https://github.com/S3raphimCS">Задонский Сергей Сергеевич (капитан)</a>
2) <a href="https://github.com/Merkucios">Медведев Андрей Владимирович</a>
3) <a href="https://github.com/Dissonanccee">Коваль Илья Валерьевич</a>
4) <a href="https://github.com/ogenwp">Гагарин Егор Кириллович</a>
5) <a href="https://github.com/B1a4c">Оришака Владислав Александрович</a>

### Стек используемых технологий:  
- Python 3.11 ![Python](https://img.shields.io/badge/Python-3.11.0-yellow?logo=python)
- Redis  ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
- Aiogram 3.12 ![Aiogram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
- PostgreSQL ![Static Badge](https://img.shields.io/badge/Postgres-latest-lightgrey?logo=postgresql)
- Docker ![Static Badge](https://img.shields.io/badge/Docker-3.9-blue?logo=docker)


## Настройки проекта
Проект настраивается через переменные окружения, указанные в файле .env
Пример .env файла указан в .env.example:

| Ключ                             | Значение                            | По умолчанию               |
|----------------------------------|-------------------------------------|----------------------------|
| `TG_BOT_SECRET_KEY`              | Секретный ключ бота                 | `the-most-secret-key`      |
| `REDIS_URL`                      | Путь до Redis                       | `redis://localhost:6379/0` |
| `POSTGRES_DB`                    | Имя БД                              | `doorphone_bot`            |
| `POSTGRES_USER`                  | Пользователь БД                     | `postgres`                 |
| `POSTGRES_PASSWORD`              | Пароль пользователя БД              | `postgres`                 |
| `POSTGRES_HOST`                  | Адрес СУБД                          | `db`/`localhost`           |
| `HOST`                           | Адрес запуска бота                  | `0.0.0.0`                  |
| `PORT`                           | Порт запуска бота                   | `8000`                     |
| `API_KEY_TYPE`                   | Формат API-ключа domo-dev.profintel | `x-api-key`                |
| `API_TOKEN`                      | Значение API-ключа                  | `SomeToken`                |
| `ADMINS`                         | ID админ-пользователей бота         | `your_id`                  |
| `BASE_URL`                       | URL-адрес для хука бота             | `https://*some_url*`       |

**Локальный разворот проекта**:
1) В директории проекта создать виртуальное окружение python3.10:
   `python3.11 -m venv venv`
2) Активировать виртуальное окружение:
   `. venv/bin/activate` для Linux или `.\venv\Scripts\activate` для Windows
3) Установить зависимости для проекта `pip install -r requirements.txt`

4) Заполнить содержимое файла .env по примеру в .env.example
5) Развернуть базу данных, redis и бота `sudo docker-compose -f docker-compose.yml up` или подключить локально службы, параллельно запустив `aiogram_run.py`

Проверка на линтеры, перейти в папку bot:

1) `flake8`
2) `isort .`
