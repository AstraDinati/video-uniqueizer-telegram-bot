# Бот Уникализатор Видео

#### Это инструкция по установке бота на системе Linux, как и сам код, она немного отличается от аналогичной инструкции для Windows, так что, если вы используете Windows, перейдите в ветку с названием windows-version

## Описание проекта

Этот проект представляет из себя телеграм бота, написанного с использованием библиотеки **[Telethon](https://docs.telethon.dev/en/stable/#)**. Его функционал на данный момент ограничивается изменением видео при помощи мультимедийного фреймворка **[FFmpeg](https://ffmpeg.org/)**. 

##### Бот умеет:
>
> - Изменять битрейт видео
> - Отзеркаливать изображение видео по горизонтали
> - Накладывать на видео .png изображение
> - Удалять с видео метаданные

## Установка

> *Установка бота будет рассматриваться исходя из предположения о том, что у пользователя, который хочет установить бота уже есть телеграм аккаунт и он может зарегистрировать на нём бота.* 

Перед установкой нам необходимо будет пойти к **[@BotFather](https://t.me/botfather)** и зарегистрировать у него своего бота, получив BOT_TOKEN. Затем мы проходим по **[ссылке](https://my.telegram.org/)**, вводим свой номер телефона и в появившемся списке выбираем 

- API development tools

Из открывшегося окна нам потребуется сохранить значения полей

- App api_id
- App api_hash

В оставшихся полях App title и Short name мы можем назвать своё приложение. Имея эти данные можно приступать в установке.

1. Клонируем репозиторий:

    ```git clone https://github.com/AstraDinati/video-uniqueizer-telegram-bot.git```

2. Переходим в директорию проекта:

    ```cd video-uniqueizer-telegram-bot```

3. Создаём виртуальное окружение (venv) для изоляции зависимостей.

    - Linux/macOS:

        ```python3 -m venv venv```

4. Активируем виртуальное окружение:

    - Linux/macOS:

        ```source venv/bin/activate```

5. Устанавливаем зависимости из файла requirements.txt:

    ```pip install -r requirements.txt```

6. Создаём в корневой дирректории проекта файл с названием .env и заполняем его следующим образом:

```
API_ID=ваш API_ID
API_HASH=ваш API_HASH
BOT_TOKEN=ваш BOT_TOKEN (который вы получали у BotFather)
```

7. Запускаем наше приложение:

    ```python bot.py```

Готово теперь бот должен работать и корректно обрабатывать видео в зависимости от ваших команд. 

В проекте так же присутствуют файлы Procfile, .buildpacks и runtime.txt, необходимые для того, чтобы задеплоить бота на хост [Heroku](https://id.heroku.com/), если вам вдруг это понадобится.
Их содержимое:
- Procfile - команда для запуска бота на сервере
- .buildpacks - билдпаки для установки python и ffmpeg на сервере
- runtime.txt - файл необходимый heroku для определения рабочей версии python
