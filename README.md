# Website Foodgram
### Service description:

In this service users can authorize, publishe recipes, subscribe to publication of ahother users, create list of favorite, form shopping list and download this list. After registration users get authorization token. For add recipes, users should choose ingredients from base and tags(for example: Breakfast), amount, add image, text and cooking time, all fields are required.

In repository exist next directories:frontend, backend,infra(configuration file nginx and docker-compose.yml), data(ingredients file) и docs.

### Technologies
- Python 3.8
- Django 4.1
- Django Rest Framework
- Djoser + TokenAuthentication
- PostreSQL
- Nginx
- Gunicorn
- Docker

### Run project in Docker

Clone project from:
```
git@github.com:lanazzk/foodgram-project-react.git
```
Install and activate virtual environment. Then go to:
```
cd /infra
```
Start up projet by running :
```
docker-compose up
```
Need to create file .env in directory /foodgram/foodgram
Sample of env-file located in /foodgram/foodgram .env.example

Run next commands in rotation:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py loaddata fixtures.json
```

### Request/response examples:
#### New User Registration:
```
POST /api/users/
{
"email": "vpupkin@yandex.ru",
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин",
"password": "Qwerty123"
}
```
#### Request samples to get authorization token:
```
POST auth/token/
{
  "password": "string",
  "email": "string"
}
```
#### Response samples:

```json
{
"auth_token": "string"
}
```
Update recipe
```
Access permission: Only author or administrator.
PATH http://localhost/api/recipes/{id}/

json
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Get all recipes
```
Access permission: Any. Available without registration
GET /api/recipes

{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
Add recipe in "Favorite"
```
Access permission: Authenticated users
POST /api/recipes/{id}/favorite/

{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}

```
}

Download shopping list"

Access permission: Authenticated users

GET /api/recipes/download_shopping_cart/


A complete list can be found in the documentation.
`/api/docs/redoc.html/`
