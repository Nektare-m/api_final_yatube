### Описание:

Простая социальная сеть "Yatube"

Есть возможность создавать посты и комментарии.

Взаимодействие происходит через API.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Nektare-m/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Примеры запросов:

POST "Создание публикации"
```
api/v1/posts/
```
Payload
```
{
"text": "string",            
"image": "string",
"group": 0
}
```
Response
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
GET "Получение комментариев"
```
api/v1/posts/{post_id}/comments/
```
Response
```
{
"id": 0,
"author": "string",
"text": "string",
"created": "2019-08-24T14:15:22Z",
"post": 0
}
```

## Автор - Nektare-m студент Я.Практикум
