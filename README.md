# Тестовое задание
## Описание текущего решения
Основа моего решения - графы.
Заполняется таблица data
через использование генераторов. Далее для реализации решения создается метод, который, используя 
plpgsql, создает фукнкцию в базе данных для поиска офиса заданного сотрудника, то есть проход
от листа к корню дерева. По этому офису
производится поиск в глубину благодаря колонке parentid. Так мы находим нужных нам сотрудников.
## Перспективы оптимизации и сложность выборки SQL
Добавить индексы, кэширование, изменить sql-запросы.
## P.s.
В коде много мест, где ловится любое исключение.
Мне стоит добавить обработку нужных исключений, добавить logging.
