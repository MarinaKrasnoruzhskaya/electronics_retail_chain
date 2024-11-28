# Cеть по продаже электроники

Создано веб-приложение с API-интерфейсом и админ-панелью. Сеть по продаже электроники представляет собой
иерархическую структуру из трех уровней:

- завод;
- розничная сеть;
- индивидуальный предприниматель.
  Каждое звено сети ссылается только на одного поставщика оборудования (не обязательно предыдущего по иерархии). Уровень
  иерархии определяется не названием звена, а отношением к остальным элементам сети, т. е. завод всегда находится на
  уровне 0, а если розничная сеть относится напрямую к заводу, минуя остальные звенья, ее уровень — 1.

## Инструкции по развертыванию проекта с Docker

1. Убедиться, что установлен Docker, Docker-compose
2. Клонировать репозиторий
   ```sh
   git clone git@github.com:MarinaKrasnoruzhskaya/electronics_retail_chain.git
   ```
3. Заполнить файл ```.env.sample``` и переименовать его в файл с именем ```.env```
4. Собрать образ
   ```sh
   docker-compose build
   ```
5. Запустить контейнеры
   ```sh
   docker-compose up
   ```
6. Запустить тестирование
   ```sh
   docker-compose exec app coverage run --source='.' manage.py test
   docker-compose exec app coverage report -m
   ```

## Инструкции по развертыванию проекта без Docker

1. Клонировать репозиторий
   ```sh
   git clone git@github.com:MarinaKrasnoruzhskaya/electronics_retail_chain.git
   ```
2. Перейти в директорию
   ```sh
   cd electronics_retail_chain
   ```
3. Установить виртуальное окружение
   ```sh
   python -m venv env
   ```
4. Активировать виртуальное окружение
   ```sh
   source env/bin/activate
   ```
5. Установить зависимости
   ```sh
   pip install -r requirements.txt
   ```
6. Заполнить файл ```.env.sample``` и переименовать его в файл с именем ```.env```
7. Создать БД ```uds```
   ```
   psql -U postgres
   create database electronics_retail_chain;  
   \q
   ```
8. Применить миграции
    ```sh
   python manage.py migrate
    ```
9. Создать суперпользователя
    ```sh
   python manage.py csu
   ```
10. Запустить тестирование
   ```sh
   coverage run --source='.' manage.py test
   coverage report -m
   ```

## Документация проекта:

1. http://127.0.0.1:8000/swagger-ui/
2. http://127.0.0.1:8000/redoc/


## Возможные действия в Django Admin:

- 

## Эндпоинты проекта:

- 

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)
