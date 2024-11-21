API приложение для поиска, продажи и покупки товаров.

Имеет следующий функционал:

* Регистрация пользователя с подтверждением почты.
* Авторизация и аутентификация пользователей.
* Изменение пароля через электронную почту.
* CRUD для объявлений на сайте (админ может удалять или редактировать все объявления, а пользователи только свои).
* Под каждым объявлением пользователи могут оставлять отзывы.
* CRUD для отзывов (админ может удалять или редактировать все отзывы, а пользователи только свои).
* В заголовке сайта можно осуществлять поиск объявлений по названию, а также отзывов.
* Добавление товара в корзину и удаление из нее.
* Создание заказа всего содержимого в корзине и оплата его на сайте STRIPE
* Проверка дней рождений у пользователей и автоматическая отправка сообщений с поздравлениями на email
* Автоматическая рассылка пользователям раз в неделю сообщений с акциями
* REDOC для взаимодействия с другими сервисами

В проекте используются следующие зависимости:

* django
* djangorestframework
* djangorestframework-simplejwt
* django-cors-headers
* drf-yasg
* psycopg2-binary
* python-dotenv
* pillow
* django-filter
* docker
* pytest
* pytest-django
* pytest-cov
* stripe
* celery
* django-celery-beat
* redis

Для разработки дополнительно:
* flake8
* ipython
* black
* isort

Для начала работы:

1. Скачать репозиторий.
2. Применить все зависимости с файла [requirements.txt](requirements.txt) 
   
    (**команда: pip install -r requirements.txt**).
3. Создать файл _.env_ и внести все чувствительные параметры указанные в файле [.env.sample](.env.sample)
4. Для заполнения базы данных применить подготовленные фикстуры [announcements.json](announcements/fixtures/announcements.json), [baskets.json](baskets/fixtures/baskets.json), [orders.json](orders/fixtures/orders.json), [users.json](users/fixtures/users.json) 

    (**команда: python3 manage.py loaddata users.json announcements.json baskets.json orders.json**)

    Если нужна пустая база данных с суперпользователем, то выполните команду csu 

    (**команда: python3 manage.py csu**) 
5. Для работы celery запустите redis сервер 

    (**команда: redis-server**) и далее (**команда: celery -A config worker --beat --scheduler django --loglevel=info**)
6. Если есть надобность задеплоить проект на Docker 

    (**команда: docker-compose up -d --build**)

Имеются тесты на весь функционал проекта с покрытием в 96%

Приятного использования. GromovAS.
