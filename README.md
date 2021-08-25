# Тестовое задание
## Описание текущего решения
Основа моего решения - графы. Создаются две таблицы: data и parents.
В data хранится информация об объекте, а в parents - id родителя данного объекта.
Под создание таблиц выделен отдельный метод. Заполняются таблицы
через использование генераторов. Далее для реализации решения создается метод, который, используя 
plpgsql, создает фукнкцию в базе данных для поиска офиса заданного сотрудника, то есть проход
от листа к корню дерева. По этому офису
производится поиск в глубину благодаря таблице parents. Так мы находим нужных нам сотрудников.
## Перспективы оптимизации и сложность выборки SQL
Добавить индексы, кэширование.
Сложность выборки офиса для сотрудника равна O(n*logn), а сложность выборки сотрудников офиса  равна 
O(n + m).
## P.s.
В коде много мест, где ловится любое исключение.
Мне стоит добавить обработку нужных исключений, добавить logging.
Еще можно сделать отдельный конфиг для общей инфы, по которой будет происходить подключение к бд.
Можно создать отдельный класс Parser, в который перенести метод для парсинга json-файла, а также 
добавить метод для создания json-файла по базе данных.
