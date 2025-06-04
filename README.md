# api_yamdb
api_yamdb

## Описание
Данный проект позволяет с помощью API оставлять отзывы на произведения, а также писать комментарии к отзывам.

## Авторы
1. 

## Установка
1. Клонировать репозиторий и перейти в него в командной строке:

    ```bash
    git clone <ссылка на репозиторий>

    cd api_yamdb/
    ```

2. Cоздать и активировать виртуальное окружение:

    ```bash
    python3 -m venv env

    source env/bin/activate
    ```

    Если у вас Windows, то процесс будет таким:

    ```bash
    python -m venv env
    source env/Scripts/activate
    ```

3. Обновить pip. Далее установить зависимости из файла requirements.txt:

    ```bash
    python3 -m pip install --upgrade pip

    pip install -r requirements.txt
    ```

    Для Windows:

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Перейти в папку с проектом и выполнить миграции:

    ```bash
    cd api_yamdb/

    python3 manage.py migrate
    ```

    Для Windows:

    ```bash
    cd api_yamdb/

    python manage.py migrate
    ```

5. Запустить сервер:

    ```bash
    python3 manage.py runserver
    ```

    Для Windows:

    ```bash
    python manage.py runserver
    ```

### Документация
Для просмотра документации API перейдите на:

    http://127.0.0.1:8000/redoc/