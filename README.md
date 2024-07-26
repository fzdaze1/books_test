# Установка и запуск
# Через Docker
1) Клонировать репозиторий
   ```
   git clone https://github.com/fzdaze1/books_test.git
   ```
2) Перейти в директорию проекта
   ```
   cd books_test
   ```
3) .env файл создавать не нужно, все данные базовые
4) Выполнить команду для запуска проекта. Эта команда соберёт и запустит все контейнеры, описанные в файле docker-compose.yml
   ```
   docker compose -f docker-compose.prod.yml up -d --build   
   ```
5) Выполнить команду для миграций в БД(также там заранее заложены велосипеды для примера)
   ```
   docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
   ```
6) Собрать все статические файлы проекта
   ```
   docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   ```
Проект позволяет создавать, редактировать, удалять и искать книги по формам на странице, в проекте использован nginx, gunicorn, memcached, postgresql, htmx, js, также применена локализация на EN/RU
