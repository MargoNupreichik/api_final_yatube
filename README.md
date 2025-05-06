# api_final
api final

### Описание

Финальный проект спринта №9 "Настройка API-сервиса"

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов

** Получение публикаций **

Запрос: GET [Link Text](http://127.0.0.1:8000/api/v1/posts/)

Результат:

```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

Создание публикации
Запрос: POST [Link Text](http://127.0.0.1:8000/api/v1/posts/)

```
{
"text": "string",
"image": "string",
"group": 0
}
```

Результат:

```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```