# Tic-tac-toe with REST API

Сервер для игры в «крестики-нолики» на поле 3х3 клетки с одного компьютера.

Как установить:

- Клонируем репозиторий

  cd /path/to/your/work/directory

  git clone https://github.com/Freezedr/lamoda_test.git

- Создаем окружение для проекта и устанавливаем зависимости

  virtualenv env

  pip install -r requirements.txt

- Создаем файл с локальными настройками для django-environ и экспортируем необходимые переменные окружения (смотри файл env.example)



Запуск тестов:
python manage.py test
