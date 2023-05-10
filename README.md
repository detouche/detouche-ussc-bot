![detouche-logo](https://github.com/detouche/detouche-ussc-bot/assets/91479557/607fb8a7-22d3-4166-88ac-a0c477282f6a)


# Interview Bot by detouche #
### Чат-бот для экспресс-оценки управленческих компетенций на собеседовании в компании ООО “УЦСБ”. ###

![image](https://github.com/detouche/detouche-ussc-bot/assets/91479557/ff6bac98-a751-4d53-8871-e6335a7329fa)



## Общие сведения о проекте


Чат-бот должен сократить время анализа оценок, выставленных кандидату группой сотрудников, 
после проведения собеседования, соединить все выставленные оценки, вывести аналитику по результатам оценивания и сохранить полученную сводку результатов для дальнейшего рассмотрения. Болью заказчика являются затраты времени на обсуждение оценок персонала и отсутствие записи мнений. Отсутствие сохраненной сводки результатов затрудняет возможность вернуться к анализу прошедшего собеседования через некоторое время. 



## Оглавление ##


1. Описание (с использованием слов и изображений)
2. Роли пользователей и их  функциональные возможности
	- Администратор сессии
	- Оценивающий
3. Технологии используемые в проекте
	- Библиотеки и их версии
	- Для чего используется и какую проблему решает
4. Техническое описание проекта
	- Установка
	- Настройка

	


## Роли пользователей и их функциональные возможности ##



Пользователей чат-бота можно разделить на 2 типа в соответствии с необходимым функционалом использования:
- Администратор
- Пользователь (сотрудник)

Администратор имеет доступ к созданию, управлению, завершению сессии оценивания, изменению списка компетенций и их описания, а также к добавлению сотрудников (пользователей чат-бота) к начатой сессии посредством отправки им кода подключения. При завершении сессии администратор может скачать PDF файл, содержащий все выставленные оценки пользователей.

Пользователь имеет доступ к присоединению к сессии оценивания по коду, высланному ему организатором сессии (администратором), оцениванию компетенций кандидата и изменению своей оценки.


## Технологии используемые в проекте



Основная библиотека для написания бота:
- aiogram 3.0.0b7



Вспомогательные бибилиотеки:
- imgkit 1.2.3
- pdfkit 1.0.0
- qrcode 7.4.2

При использовании бота было необходимо выводить большие объемы данных (Созданные компетенции и их описание, а также Профили компетенций). При помощи даныых бибилиотек автоматически генерируется картинка со всей необходимой полной информацией, а в сопровождающемся сообщения лишь минимальный список.
