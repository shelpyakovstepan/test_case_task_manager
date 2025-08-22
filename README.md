# test_case_task_manager
Тестовое задание  "Менеджер задач" с тестами


Стек проекта:

FastAPI\
Postgres\
Pytest\
Poetry\
Ruff, Pyright, isort\
Docker и Docker-compose\
Gitlab CI

Структура проекта:

```
├── app
    ├── config.py
    ├── dao
    │   └── base.py
    ├── database.py
    ├── exceptions.py
    ├── logger.py
    ├── main.py
    ├── tasks
    │   ├── dao.py
    │   ├── models.py
    │   ├── router.py
    │   └── schemas.py
    └── users
    │   ├── auth.py
    │   ├── dao.py
    │   ├── dependencies.py
    │   ├── models.py
    │   ├── router.py
    │   └── schemas.py
├── tests
    ├── api_tests
        ├── tests_tasks_api.py
        └── tests_users_api.py
    ├── conftest.py
    └── unit_tests
        ├── tests_tasks_dao.py
        └── tests_users_dao.py
├── docker
    └── app.sh
├── migrations
    ├── README
    ├── env.py
    ├── script.py.mako
    └── versions
    │   ├── 0d4e51a51829_initial_migration.py
    │   └── 2bfeff22d049_поменял_тип_у_колонки_user_id_в_tasks.py
├── .gitignore
├── .gitlab-ci.yml
├── .isort.cfg
├── Dockerfile
├── LICENSE
├── README.md
├── alembic.ini
├── docker-compose-local.yml
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── pyrightconfig.json
├── pytest.ini
└── ruff.toml
```

Реализована работа с пользователями через JWT токены, пользователи могут создавать, просматривать задачи по отдельности и все вместе, изменять статусы и удалять задачи.
Для эндпоинта по поиску всех задач сделана пагинация.

CRUD методы для работы с задачами (Tasks):

create - add,\
get - find_by_id // find_one_or_none,\
get_list - find_all_users_tasks,\
update,\
delete

Статусы задач реализованы через Enum (StatusEnum):

создано - CREATED\
в работе - WORKING\
заверешено - COMPLETED

```
class StatusEnum(enum.Enum):
    CREATED = "CREATED"
    WORKING = "WORKING"
    COMPLETED = "COMPLETED"
```

Тесты сделаны через Pytest, работают в любой бд (не нужна тестовая) (покрытие по pytest-cov 85%):
сделаны API и DAO тесты
```
tests
    ├── api_tests
        ├── tests_tasks_api.py
        └── tests_users_api.py
    ├── conftest.py
    └── unit_tests
        ├── tests_tasks_dao.py
        └── tests_users_dao.py
```
Для всех функций и эндпоинтов сделана документация в стиле Google
(Пример)
```
"""
Добавляет задачу.

Args:
    session: DbSession(AsyncSession) - Асинхронная сессия базы данных.
    new_task_data: Pydantic модель SAddTasks, содержащая данные для добавления новой задачи.
    user: Экземпляр модели Users, представляющий текущего пользователя, полученный через зависимость get_current_user().

Returns:
    new_task: Экземпляр Pydantic модели STasks, представляющий созданную задачу.
"""
```
Есть Docker и Docker compose, реализовано Gitlab CI

```
├── docker-compose-local.yml
├── docker-compose.yml
```
docker-compose-local.yml - docker compose файл для локального запуска с локальными енв данными\
docker-compose.yml - docker compose файл для запуска с gitlab ci, env данные прокидываются из gitlab variables

