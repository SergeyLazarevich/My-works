# Flask_project

Стек:

ML: sklearn, pandas, numpy, catboost

API: Flask

Данные: с kaggle - https://www.kaggle.com/competitions/titanic/overview

Задача: предсказать по описанию какие пассажиры пережили кораблекрушение Титаника.

Используемые признаки:

- survival: выживший -1 или -0
- pclass: Класс билетов 1 = 1st, 2 = 2nd, 3 = 3rd
- sex: Пол
- Age: Возраст в годах
- sibsp: братьев и сестер/супругов на борту "Титаника"
- parch: родителей/детей на борту "Титаника"
- ticket: Номер билета
- fare: Пассажирский тариф
- cabin: Номер каюты
- embarked: Порт отправления C = Шербур, Q = Квинстаун, S = Саутгемптон

Модель: model

### Запуск сервера
~~~
python app\server.py
~~~

### Запуск клиента
~~~
python app\client.py
~~~
