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

Для получения или создания постов:
```
GET POST api/v1/posts/
{
"text": "string",
"image": "string",
"group": 0
}
```

Для получения или редактирования поста:
```
GET PATCH api/v1/posts/{id}/
{
"text": "string",
"image": "string",
"group": 0
}
```

Для получения и создания комментариев:
```
GET POST posts/{post_id}/comments/
{
"text": "string",
"image": "string",
"group": 0
}
```



