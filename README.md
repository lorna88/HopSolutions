### *Проект Hop Solutions*
Веб-приложение - планировщик задач. Подходит для личного пользования. Основные возможности:
- Создание списков задач для организации повседневных дел, покупок и 
семейных мероприятий.
- Возможность работы в контексте категорий - группировка задач по доскам, и в контексте 
нужной даты.
- Маркировка задач по приоритету и другим критериям.
- Создание подзадач.

### *Используемые технологии*
1. Django - фреймворк для разработки веб-приложения
2. Poetry — менеджер для управления зависимостями и пакетами
3. Docker Compose - платформа для контейнеризации и развёртывания приложения в изолированных
средах

### *Настройка переменных окружения*
Сконфигурируйте файл `.env`, содержащий переменные окружения для корректной работы Django.
Используйте файл настроек `.env.example` в качестве примера. Файл конфигурации должен 
обязательно содержать:
1. Секретный ключ Django
2. Настройки доступа к базе данных:
- *POSTGRES_DB* - имя базы данных Postgres
- *POSTGRES_USER* - имя пользователя Postgres
- *POSTGRES_PASSWORD* - пароль пользователя Postgres
- *POSTGRES_HOST* - имя хоста/адрес сервера (указать `db`)
- *POSTGRES_PORT* - порт (указать `5432`)
3. Настройки для отправки сообщений по EMail:
- *EMAIL_HOST* - адрес хоста SMTP-сервера
- *EMAIL_PORT* - порт SMTP-сервера
- *EMAIL_USE_TLS* - логическое значение, определяющее, использовать ли безопасное 
соединение TLS
- *EMAIL_USE_SSL* - логическое значение, определяющее, использовать ли безопасное 
соединение SSL
- *EMAIL_HOST_USER* - имя пользователя (адрес электронной почты) для входа на SMTP-сервер
- *EMAIL_HOST_PASSWORD* - пароль для SMTP-аккаунта (пароль приложения)

### *Запуск и настройка*
1. Выполнить команду запуска сервисов Docker Compose:
```bash
docker compose up --build
```
В результате выполнения команды будут запущены два сервиса:
- backend - содержит контейнер сервера Django-приложения
- db - содержит контейнер с базой данных PostgreSQL
2. Выполнить миграции базы данных с помощью команды:
```bash
docker compose run backend python manage.py migrate
```
3. Создать суперпользователя Django с помощью команды:
```bash
docker compose run backend python manage.py createsuperuser
```
### Приложение будет доступно по адресу
### `http://localhost:8000/home`

### *Структура Django проекта*
1. **USERS** - приложение для работы с пользователями. Обеспечивает регистрацию и аутентификацию
пользователей в системе, возможности смены пароля, отображение страницы профиля. Модель 
наследуется от AbstractUser:
#### User
- `id` (PK)
- `email` (EmailField, unique)
- `username` (CharField, unique)
- `first_name`, `last_name` (CharField, nullable)
- `phone` (CharField, nullable)

2. **TASKS** - приложение для создания, отображения, редактирования и удаления списков категорий
и задач. Модели:
#### Category
- `id` (PK)
- `name` (CharField)
- `slug` (SlugField)
- `user` (ForeignKey to User)
#### Task
- `id` (PK)
- `name` (CharField)
- `slug` (SlugField)
- `description` (TextField, nullable)
- `date` (DateField, nullable)
- `category` (ForeignKey to Category)
- `is_completed` (BooleanField)
- `tags` (ManyToManyField to Tag)
- `user` (ForeignKey to User)

3. **TAGS** - приложение для управления тегами (метками) задач. Модель:
#### Tag
- `id` (PK)
- `name` (CharField)
- `color` (CharField)
- `user` (ForeignKey to User)

4. **SUBTASKS** - приложение для управления подзадачами. Модель:
#### Subtask
- `id` (PK)
- `name` (CharField)
- `is_completed` (BooleanField)
- `task` (ForeignKey to Task)
- `user` (ForeignKey to User)

5. **TASK_CALENDAR** - приложение для отображения вкладки с календарем и отображения задач на 
определенную дату.

### *Описание запросов REST API*
1. **JWT аутентификация**

Для доступа к основному API приложения необходимо пройти процедуру аутентификации
и получить JWT токены для дальнейшего их использования в запросах. Для этого нужно:
- войти в аккаунт, указав адрес почты email и пароль
- в ответ получить два токена JWT
- access токен необходимо указывать при каждом запросе к API ресурсам в заголовке авторизации:
```
Authorization: Bearer secret.access.token
```
- по истечении срока действия access токена необходимо получить новый (новую пару токенов), 
передав в запрос полученный ранее refresh токен
- если пользователь не зарегистрирован в системе, вначале нужно пройти регистрацию

2. **Эндпоинты, не требующие аутентификации**
### `POST` `/api/users/register` 
Зарегистрировать нового пользователя.

Пример запроса:
```
{                                          
    'email': 'email@example.com',          
    'username': 'your_name',
    'password': 'secret_password'
}
```
Пример ответа:
```
{                                          
    'email': 'email@example.com',          
    'username': 'your_name'
}
```
### `POST` `/api/users/login`
Выполнить вход в аккаунт и получить access/refresh токены.

Пример запроса:
```
{
    'email': 'email@example.com',
    'password': 'secret_password'
}
```
Пример ответа:
```
{
    'access': 'secret.access.token',
    'refresh': 'secret.refresh.token'
}
```
### `POST` `/api/users/login/refresh`
Получить новый access токен по refresh токену.
<br>Пример запроса:
```
{
    'refresh': 'secret.refresh.token'
}
```
Пример ответа:
```
{
    'access': 'secret.access.token',
    'refresh': 'secret.refresh.token'
}
```
3. **Эндпоинты, доступные только по JWT**
### `GET` `/api/tasks/`
Получить список созданных задач. Маршрут использует пагинацию, 10 объектов на странице 
по умолчанию.

Также доступны следующие варианты запроса с параметрами:

`/api/tasks/?page=3` - запрос нужной страницы

`/api/tasks/?page=3&size=5` - запрос нужной страницы с изменением количества объектов на странице
(максимальное равно 20)

`/api/tasks/?date=2025-10-24` - фильтр по дате

`/api/tasks/?date_before=2025-10-24` - фильтр до указанной даты

`/api/tasks/?date_after=2025-10-24` - фильтр после указанной даты

`/api/tasks/?is_completed=false` - только активные (незавершённые) задачи

`/api/tasks/?category=today` - фильтр по имени категории

`/api/tasks/?tag=important` - фильтр по имени тега

`/api/tasks/?search=go to` - поиск в имени и описании задачи

`/api/tasks/?ordering=date` - сортировка по дате, также возможна по полю slug категории и
активным/завершённым задачам, по умолчанию - slug категории

Пример ответа:
```
{
    "count": 26,
    "next": "http://127.0.0.1:8000/api/tasks/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "category": "today",
            "name": "Go to market",
            "slug": "go-to-market",
            "description": null,
            "date": 2025-10-24,
            "is_completed": false,
            "user": "admin",
            "tags": [
                "Important",
                "Family"
            ],
            "subtasks": [
                {
                    "name": "Buy a fish",
                    "is_completed": false
                },
                {
                    "name": "Buy fruits",
                    "is_completed": false
                }
            ]
        },
        ...
    ]
}
```
### `POST` `/api/tasks/`
Создать новую задачу.

Пример запроса:
```
    {
        "category": "today",
        "name": "Complete the project",
        "date": 2025-10-24,
        "tags": [
            "Deadline"
        ],
        "subtasks": [
            {
                "name": "Create docs"
            },
            {
                "name": "Write tests"
            }
        ]
    }
```
### `GET` `PUT` `PATCH` `DELETE` `/api/tasks/<id>/`
Посмотреть, обновить или удалить задачу с заданным id.

### `GET` `POST` `/api/categories/`
Получить список категорий либо создать новую.

### `GET` `PUT` `PATCH` `DELETE` `/api/categories/<id>/`
Посмотреть, обновить или удалить категорию с заданным id.

### `GET` `PUT` `PATCH` `DELETE` `/api/tags/`
Получить список тегов либо создать новый.

### `GET` `PUT` `PATCH` `DELETE` `/api/tags/<id>/`
Просмотреть, обновить или удалить тег с заданным id.

В приложении использована иконка
<a target="_blank" href="https://icons8.com/icon/21322/done">
    <img src="{% static 'favicon.ico' %}" alt="Check mark">
</a> icon from <a target="_blank" href="https://icons8.com">Icons8</a>