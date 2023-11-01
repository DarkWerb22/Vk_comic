## Публикация комиксов вконтакте


Чтобы использовать этот код, вам необходимо:
### Окружение

- Создать файл `.env` в корневой директории проекта и добавить туда следующие переменные:

    * `CLIENT_ID`: ваш идентификатор приложения ВКонтакте.
    * `VK_TOKEN`: ваш токен доступа к API ВКонтакте.
    * `VK_GROUP_ID`: идентификатор группы ВКонтакте, в которой вы хотите публиковать комиксы.
   
### Зависимости 

- Установить пакеты зависимостей:
    ```
    pip install -r requirements.txt
    ```

### Запуск

- Запустить скрипт:
    ```
    python main.py
    ```
### Получение переменных окружения 
- Перед использованием скрипта нужно создать сообщество ВКонтакте и получить токен доступа к Вк Api
Скрипт будет загружать случайный комикс XKCD, загружать его на сервер ВКонтакте и публиковать в группе, указанной в переменной `GROUP_ID`.


### Примечания
- Этот скрипт не проверяет, существует ли комикс с заданным номером. Если такого комикса нет, скрипт выйдет с ошибкой.
