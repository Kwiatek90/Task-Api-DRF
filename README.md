# Task App

## Wstęp

Api stworzone do zarządzania zadaniami, które umożliwia rejestrację użytkowników, logowanie, dodawanie, przeglądanie, aktualizację i usuwanie zadań, a także zarządzanie nimi. To API zostało stworzone przy użyciu technologii PostgreSQL do przechowywania danych, Docker do konteneryzacji, Gunicorn jako serwera HTTP do obsługi aplikacji Python oraz Nginx jako serwera HTTP i proxy odwrotnego, zapewniającego bezpieczne i efektywne przetwarzanie żądań.

## Setup

Uruchomienie projektu:

1. Tworzymy build kontenera

    ```bash
    docker-compose -f docker-compose.prod.yml up -d --build
    ```

2. Tworzymy migracje danych

    ```bash
    docker-compose exec web python manage.py migrate --noinput
    ```

3. Kopiujemy pliki statyczne

    ```bash
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
    ```

4. Aplikacja uruchamia nam się na [http://localhost:1337/api/tasks/](http://localhost:1337/api/tasks/)

5. Zatrzymujemy kontenery

    ```bash
    docker compose -f docker-compose.prod.yml down -v
    ```

6. Uruchamiamy terminal bash:

    ```bash
    docker compose exec -it PIERWSZE TRZY LITERY CONTAINER ID bash
    ```

7. Uruchamiamy testy w terminalu bash:

    ```bash
    pytest
    ```

8. Logujemy się do bazy danych

    ```bash
    docker-compose exec db psql --username=admin --dbname=admin
    ```

## Przykładowe komendy CURL

- Logowanie użytkownika:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:8000/api/login/
    ```

- Pobieranie zadań:

    ```bash
    curl -X GET -H "Authorization: Token {token}" http://localhost:1337/api/tasks/
    ```

- Dodawanie zadania:

    ```bash
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Token {token}" -d '{"name": "Przykładowe zadanie", "description": "opis zadania", "executing_user": 1}' http://localhost:8000/api/tasks/
    ```

## Końcówki HTTP API Endpoints

- [http://localhost:1337/admin](http://localhost:1337/admin)
    - Pozwala na zalogowanie się do panelu administracyjnego, gdzie można zarządzać bazą danych i przyznawać uprawnienia grupom i użytkownikom.

- [http://localhost:1337/register/](http://localhost:1337/register/)
    - Metoda: POST
        - Tworzy nowego użytkownika.
        - Parametry żądania:
            - username - Nazwa użytkownika
            - password - Hasło użytkownika
            - email - Mail użytkownika, pole niewymagane
            - first_name - Imię użytkownika, pole niewymagane
            - last_name - Nazwisko użytkownika, pole niewymagane
            - phone_number - Numer telefonu użytkownika, pole niewymagane

- [http://localhost:1337/login/](http://localhost:1337/login/)
    - Metoda: POST
        - Loguje użytkownika
        - Parametry żądania:
            - username - Nazwa użytkownika
            - password - Hasło użytkownika

- [http://localhost:1337/logout/](http://localhost:1337/logout/)
    - Metoda: POST
        - Wylogowuje użytkownika

- [http://localhost:1337/api/tasks/](http://localhost:1337/api/tasks/)
    - Metoda: POST
        - Dodaje zadanie
        - Parametry żądania:
            - name - krótki opis zadania
            - description - dłuższy opis zadania, pole niewymagane
            - status - status zadania, automatycznie przypisywany status - New
            - executing_user - użytkownik przypisany do zadania, który jest zarejestrowany w bazie
    - Metoda: GET
        - Wyświetla wszystkie zadania
    - Parametry
        - Wyszukiwanie zadań dla przypisanego użytkownika o danym id
            - /?executing_user=ID_USERA
        - Wyszukiwanie zadań o danym statusie
            - /?status=New
        - Wyszukiwanie zadań o podanej frazie
            - /?keyword=task

- [http://localhost:1337/api/tasks/ID_ZADANIA](http://localhost:1337/api/tasks/ID_ZADANIA)
    - Metoda: GET
        - Wyświetla dane zadanie
    - Metoda: PATCH
        - Aktualizacja danych zadania
    - Metoda: DELETE
        - Usuwanie zadania

- [http://localhost:1337/api/tasks/ID_ZADANIA/history/](http://localhost:1337/api/tasks/ID_ZADANIA/history/)
    - Metoda: GET
        - Wyświetla historię zmian danego zadania
    - Parametry
        - Wyszukiwanie historii zmian po dacie
            - /?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
        - Wyszukiwanie zadań dla przypisanego użytkownika o danym id
            - /?executing_user=ID_USERA

- [http://localhost:1337/api/tasks/ID_ZADANIA/history/ID_HISTORII_ZADANIA](http://localhost:1337/api/tasks/ID_ZADANIA/history/ID_HISTORII_ZADANIA)
    - Metoda: GET
        - Wyświetla konkretną historię zmian danego zadania

## Wideo

[Link do wideo]

## Zastosowane technologie i biblioteki

### Environment
- Python 3.11.4
- Visual Studio Code 1.79
- Docker 24.0.7
- PostgreSQL 16.1
- Nginx 1.25.3

### Libraries
- Django 5.0.1
- django-simple-history 3.4.0
- djangorestframework 3.14.0
- pytest 7.4.3
- gunicorn 21.2.0
- psycopg2 2.9.9
- pytest-django 4.7.0

## Licencja

Ten projekt jest dostępny na licencji MIT.
