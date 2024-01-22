# Task App

## Zawartość
* [Wstep](#Wstep)
* [Setup](#setup)
* [Przykładowe komendy CURL](#Przykładowe-komendy-CURL)
* [Końcówki HTTP API Endpoints](#Końcówki-HTTP-API-Endpoints)
* [Wideo](#Video)
* [Zastosowane technologie i biblioteki](#zastosowane-technologie-i-biblioteki)
* [Licencja](#licencja)

## Wstep

Api stworzone do zarządzania zadaniami, które umożliwia rejestrację użytkowników, logowanie, dodawanie, przeglądanie, aktualizację i usuwanie zadań, a także zarządzanie nimi. 
To API zostało stworzone przy użyciu technologii PostgreSQL do przechowywania danych, Docker do konteneryzacji, Gunicorn jako serwera HTTP do obsługi aplikacji Python oraz Nginx jako serwera HTTP i proxy odwrotnego, zapewniającego bezpieczne i efektywne przetwarzanie żądań.

## Setup

Uruchomienie projeku:
```
Tworzymy build kontenera
```
docker-compose -f docker-compose.prod.yml up -d --build
```

Tworzymy migracje danych

```docker-compose exec web python manage.py migrate --noinput```


Kopiujemy pliki statyczne
```
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

Aplikacja uruchamia nam się na http://localhost:1337/api/tasks/

Zatrzymanie kontenerów
```
docker compose -f docker-compose.prod.yml down -v
```

Uruchomienie terminalu bash:
```docker compose exec -it PIERWSZE TRZY LITERY CONTAINER ID bash```

Uruchomienie testów w terminalu bash:

```pytest```

Logowanie się do bazy danych
```
docker-compose exec db psql --username=admin --dbname=admin
```


## Przykładowe komendy CURL

Logowanie użytkownika:
```curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:8000/api/login/```

Pobieranie zadań:
```curl -X GET -H "Authorization: Token {token}" http://localhost:1337/api/tasks/```

Dodowania zadania:
```curl -X POST -H "Content-Type: application/json" -H "Authorization: Token {token}" -d '{"name": "Przykładowe zadanie", "description": "opis zadania", "executing_user": 1}' http://localhost:8000/api/tasks/


## Końcówki HTTP API Endpoints

* http://localhost:1337/admin
    * Pozwala nam na zalogowanie się do panelu administracyjnego, możemy tam zarządzać całą bazą dancyh w naszej aplikacji oraz przyspiywać uprawnienia grupom i użytkownikom.

* http://localhost:1337/register/
    * Metoda: POST
        * Tworzy nowego użytkownika.
        * Parametry żądania:
            * username - Nazwa użytkownika
            * password - Hasło użytkownika
            * email - Mail użytkownika, pole niewymagane
            * first_name - Imię użytkownika, pole niewymagane
            * last_name - Nazwisko użytkownika, pole niewymagane
            * phone_number - Numer telefonu użytkownika, pole niewymagane

* http://localhost:1337/login/
    * Metoda: POST
        * Loguję użytkownika
        * Parametry żądania:
            * username - Nazwa użytkownika
            * password - Hasło użytkownika

* http://localhost:1337/logout/
    * Metoda: POST
        * Wylogowuje użytkownika   

* http://localhost:1337/api/tasks/
    * Metoda: POST
        * Dodaje zadanie
        * Parametry żądania:
            * name - krótki opis zadania
            * description - dłuższy opis zadania, pole niewymagane
            * status - status zadania, automatycznie przypisywany status - New
            * executing_user - użytkownik przypisany do zadania, który jest zarejstrowany w bazie
    * Metoda: GET
        * Wyświetla wszystkie zadania
    * Parametry
        * Wyszukiwanie zadań dla przypisanego użytkownika o danym id
            * /?executing_user=ID_USERA
        * Wyszukiwanie zadań o danym statusie
            * /?status=New
        * Wyszukiwanie zadań o podanej frazie
            */?keyword=task

* http://localhost:1337/api/tasks/ID_ZADANIA
    * Metoda: GET
        * Wyświetla dane zadanie
    * Metoda: PATCH
        * Aktualizacja danych zadania
    * Metoda: DELETE
        * Usuwanie zadania

* http://localhost:1337/api/tasks/ID_ZADANIA/history/
    * Metoda: GET
            * Wyświetla historie zmian danego zadania
    * Parametry
        * Wyszukiwanie histori zmian po dacie
            * /?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
        * Wyszukiwanie zadań dla przypisanego użytkownika o danym id
            * /?executing_user=ID_USERA

* http://localhost:1337/api/tasks/ID_ZADANIA/history/ID_HISTORII_ZADANIA
    * Metoda: GET
                * Wyświetla konkretną historie zmian danego zadania
        
## Wideo

## Zastosowane technologie i biblioteki

* Environment
    * Pyhton 3.11.4
    * Visual Studio Code 1.79
    * Docker 24.0.7
    * Postgres 16.1
    * Ngnix 1.25.3

* Libraries
    * Django 5.0.1
    * django-simple-history 3.4.0
    * djangorestframework 3.14.0
    * pytest 7.4.3
    * gunicorn 21.2.0
    * psycopg2 2.9.9
    * pytest-django 4.7.0

## Licencja

Ten projekt ma charakter open source i jest dostępny na licencji MIT.
