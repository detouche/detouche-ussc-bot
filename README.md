![image](https://github.com/detouche/detouche-ussc-bot/assets/91479557/b66e81be-3499-4df7-b935-647d685481c7)


<h1 align="center">Interview Bot by detouche</h1>

### Чат-бот для экспресс-оценки управленческих компетенций на собеседовании в компании ООО “УЦСБ”. ###

![image](https://github.com/detouche/detouche-ussc-bot/assets/91479557/0823a9e3-8fa2-4769-9949-1c70645ba633)


<h2 align="center">Оглавление</h2>


1. [Описание](https://github.com/detouche/detouche-ussc-bot#общие-сведения-о-проекте)
2. [Роли пользователей и их  функциональные возможности](https://github.com/detouche/detouche-ussc-bot#роли-пользователей-и-их-функциональные-возможности)
 	- Главный администратор
	- Администратор сессии
	- Оценивающий
3. [Технологии используемые в проекте](https://github.com/detouche/detouche-ussc-bot#технологии-используемые-в-проекте)
	- Библиотеки и их версии
	- Для чего используется и какую проблему решает
4. [Техническое описание проекта](https://github.com/detouche/detouche-ussc-bot#техническое-описание-проекта)
	- [Структура проекта](https://github.com/detouche/detouche-ussc-bot#структура-проекта)
	- [Установка и настройка](https://github.com/detouche/detouche-ussc-bot#установка-и-настройка)
	- Добавление `Администратора сессии`

---



<h2 align="center">Общие сведения о проекте</h2>


Чат-бот должен сократить время анализа оценок, выставленных кандидату группой сотрудников, после проведения собеседования, соединить все выставленные оценки, вывести аналитику по результатам оценивания и сохранить полученную сводку результатов для дальнейшего рассмотрения. Болью заказчика являются затраты времени на обсуждение оценок персонала и отсутствие записи мнений. Отсутствие сохраненной сводки результатов затрудняет возможность вернуться к анализу прошедшего собеседования через некоторое время. 

![Видео 22-05-2023 20_46_01](https://github.com/detouche/detouche-ussc-bot/assets/91479557/51a33dad-8a9d-4b14-be25-d5c0df84d723)





<h2 align="center">Роли пользователей и их функциональные возможности</h2>



**Пользователей чат-бота можно разделить на 3 типа в соответствии с необходимым функционалом использования:**
- Главный администратор 
- Администратор
- Пользователь (оценивающий)

`Главный администратор` может добавлять и удалять администраторов, также имеет все возможности `Администратора`

`Администратор` имеет доступ к созданию, управлению, завершению сессии оценивания, изменению списка компетенций и их описания, а также к добавлению сотрудников (пользователей чат-бота) к начатой сессии посредством отправки им кода подключения. При завершении сессии администратор может скачать PDF файл, содержащий все выставленные оценки пользователей.

`Пользователь` имеет доступ к присоединению к сессии оценивания по коду, высланному ему организатором сессии (администратором), оцениванию компетенций кандидата и изменению своей оценки.


<h2 align="center">Технологии используемые в проекте</h2>



**Основная библиотека для написания бота:**
- python 3.8
- [aiogram 3.0.0b7](https://docs.aiogram.dev/en/dev-3.x/)


**База данных:**
- sqlite3


**Вспомогательные бибилиотеки:**
- imgkit 1.2.3
- pdfkit 1.0.0
- qrcode 7.4.2
- jinja2 3.1.2
- python-dotenv 1.0.0

При использовании бота было необходимо выводить большие объемы данных (Созданные компетенции и их описание, а также Профили компетенций). При помощи данных библиотек автоматически генерируется картинка со всей необходимой полной информацией, а в сопровождающем сообщении - лишь минимальный список.

![image](https://github.com/detouche/detouche-ussc-bot/assets/91479557/205d27d2-3340-4970-ba86-c7add47f8ede)
![image](https://github.com/detouche/detouche-ussc-bot/assets/91479557/30248ece-7617-4bb7-90a3-736b83e1d634)




<h2 align="center">Техническое описание проекта</h2>

### Структура проекта ###

`config_data` - Загрузка файла конфигурации бота.

`database` - Обращения к базе данных.

`handlers` - Функции вывода и обработки команд, поступающих боту.

`html` - html-шаблоны для генерации файлов с информацией.

`keyboards` - Клавиатуры, выводимые ботом при определнных запросах в нему.

`states` - Структура различных состояний бота.

`loader.py` и `main.py` - Инициализация и запуск бота.


### Установка и настройка ###

1. Клонируйте репозиторий с GitHub

`$ git clone https://github.com/detouche/detouche-ussc-bot.git`

2. Создайте виртуальное окружение.

`python -m venv /path/to/new/virtual/environment`

3. Установите зависимости

`pip install -r requirements.txt`

4. Установите [wkhtmltopdf](https://wkhtmltopdf.org/)

5. Настройте переменные окружения в файле `.env.ex` 

```
BOT_TOKEN = "ТОКЕН бота, взятый из BotFather"

MAIN_ADMINS = "ID_Первого_Администратора ID_Второго_Администратора"
```

Изменить название файла `.env.ex` на `.env`

В поле `BOT_TOKEN` укажите токен, который был получен в BotFather. Как получить токен?

1. В Telegram зайдите в бот [BotFather](https://t.me/BotFather)
2. Введите команду `/start`
3. Введите команду `/new_bot`
4. Введите название для своего бота.
5. Введите ТЕГ для своего бота, который будет содержать `Bot` в своем названии. (Пример: TetrisBot or tetris_bot)
6. После п.5 бот отправит вам сообщение, в котором будет содержаться ТОКЕН Вашего бота.

В поле `MAIN_ADMINS` введите через ПРОБЕЛ ID главных администраторов.


6. Запустите бота.

`python main.py` или `python3 main.py`


### Добавление администратора ###

Чтобы добавить `Администратора сессии` необходимо.

1. Человеку, которого нужно сделать администратором, зайти в бот и зарегестрироваться (Ввести свои ФИО).
2. `Главному администратору` зайти во вкладку `Администраторы`
3. Из предложенного списка выбрать нужного человека и подтвердить действие.



<h2 align="center">detouche Team</h2>

:star: `Тимлид` Ворсин Алексей 

:star: `Аналитик` Иванов Никита

:star: `Разработчик - Тестировщик` Валиуллин Антон

:star: `Дизайнер` Голубев Игорь 

:star: `Разработчик` Пичугин Михаил

**Наши соц. сети:**

:newspaper: VK: [detouche](https://vk.com/detouche)

![image](https://github.com/detouche/detouche-ussc-bot/assets/91479557/8dd1bc03-8b64-46ff-93ad-156d1fa4d5e8)
