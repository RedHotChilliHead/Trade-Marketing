# Trade Marketing

## Описание
Trade Marketing — это микросервис для сбора и анализа статистики маркетинговых показателей. 
Сервис предоставляет REST API для работы со статистикой кликов и показов, 
а также для расчета средней стоимости клика (CPC) и средней стоимости 1000 показов (CPM). 
Входные данные всех методов проходят валидацию, чтобы обеспечить корректность и целостность данных.

## Методы API

### Метод сохранения статистики

#### Описание

Метод позволяет сохранять статистику за конкретную дату.

#### Эндпоинт
```http
POST /statistic/
```

#### URL
```
http://127.0.0.1:8000/statistic/
```

#### Параметры запроса
- обязательные параметры:
  - `date` (дата события, формат: `YYYY-MM-DD`)
- не обязательные параметры:
  - `views` (количество показов)
  - `clicks` (количество кликов)
  - `cost` (стоимость кликов)

#### Пример запроса
```http
POST
Content-Type: application/json
{
    "date": "2024-01-01",
    "views": 100,
    "clicks": 10,
    "cost": 20.00
}
```

#### Пример ответа
```
HTTP 201 Created
Allow: GET, POST, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "OK": "Statistics are saved"
}
```

### Метод получения статистики

#### Описание

Метод позволяет получить статистику по указанному диапазону дат.
Статистика агрегируется по дате.

#### Эндпоинт
```http
GET /statistic/
```

#### URL
```
http://127.0.0.1:8000/statistic/
```

#### Параметры запроса

- обязательные параметры:
  - `from` (дата начала периода, включительно, формат: `YYYY-MM-DD`)
  - `to` (дата окончания периода, включительно, формат: `YYYY-MM-DD`)
- не обязательные параметры:
  - `ordering` (сортировка по любому полю по убыванию и возрастанию `(-)field`)

#### Пример запроса

```http
GET http://127.0.0.1:8000/statistic/?from=2024-07-01&to=2024-07-04&ordering=-views
```

#### Пример ответа
```
HTTP 200 OK
Allow: GET, POST, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "date": "2024-08-04",
        "views": 20,
        "clicks": 30,
        "cost": "0.50",
        "cpc": 0.02,
        "cpm": 25.0
    },
    {
        "date": "2024-07-04",
        "views": 10,
        "clicks": 10,
        "cost": "0.10",
        "cpc": 0.01,
        "cpm": 10.0
    }
]
```
Где:
-  cpc = cost/clicks (средняя стоимость клика)
- cpm = cost/views * 1000 (средняя стоимость 1000 показов)

### Метод сброса статистики

#### Описание

Удаляет всю сохраненную статистику.

#### Эндпоинт

```http
DELETE /statistic/
```

#### URL
```
http://127.0.0.1:8000/statistic/
```

#### Пример запроса

```http
DELETE /statistic/
```

### Пример ответа

```
HTTP 204 No Content
Allow: GET, POST, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "OK": "Statistics are deleted"
}
```

### Предварительные требования

- Убедитесь, что у вас установлены Docker и Docker Compose
- Версия Python: 3.11

### Шаги установки

1. Клонируйте репозиторий проекта:

```sh
git clone https://github.com/RedHotChilliHead/Trade-Marketing.git
cd Trade-Marketing
```

2. Установите зависимости:
```sh
pip install -r requirements.txt
```

3. Соберите и запустите Docker-контейнеры:
```sh
docker compose up -d
```

4. Выполните миграции
```sh
docker compose run trade_marketingapp python manage.py migrate
```
После выполнения всех шагов приложение будет доступно по адресу: http://localhost:8000

## Unit-тесты

Для запуска юнит-тестов используйте следующую команду:

```sh
docker compose run trade_marketingapp python manage.py test
```