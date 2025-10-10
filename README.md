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
- `slug` (SlugField, unique)
- `user` (ForeignKey to User)
#### Task
- `id` (PK)
- `name` (CharField)
- `slug` (SlugField, unique)
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
- `slug` (SlugField, unique)
- `color` (CharField)
- `user` (ForeignKey to User)

4. **SUBTASKS** - приложение для управления подзадачами. Модель:
#### Subtask
- `id` (PK)
- `name` (CharField)
- `slug` (SlugField, unique)
- `is_completed` (BooleanField)
- `task` (ForeignKey to Task)
- `user` (ForeignKey to User)

5. **TASK_CALENDAR** - приложение для отображения вкладки с календарем и отображения задач на 
определенную дату.

В приложении использована иконка
<a target="_blank" href="https://icons8.com/icon/21322/done">
    <img src="{% static 'favicon.ico' %}" alt="Check mark">
</a> icon from <a target="_blank" href="https://icons8.com">Icons8</a>