class Executor:
    def __init__(self, db):
        self.__conn = db._conn
        self.__cursor = db._cursor

    def get_workers(self):
        """
        Возвращает список сотрудников из одного офиса
        """
        print('Введите идентификатор сотрудника')
        try:
            id = int(input())
            result = self.__get_workers(self.__get_root(id))
            workers = []
            for tup in result:
                for worker in tup:
                    workers.append(worker)
            return workers
        except:
            print('Некорректный ID')

    def __get_workers(self, id):
        """
        Выполняет поиск в глубину для нахождения всех сотрудников офиса
        по ID офиса

        :param id: ID офиса
        """
        if id == -1:
            raise KeyError
        query = f"""
                WITH RECURSIVE tree(id, parentid, name, type, path) AS (
                SELECT id, parentid, name, type, array[id]::integer[]
                FROM data WHERE parentid = {id}
                UNION ALL
                SELECT data.*, path || array[data.id]::integer[]
                FROM data INNER JOIN tree on tree.id = data.parentid)
                
                select data.name from data
                where data.id in
                    (select data.id from data
                    where data.id not in (select parentid from tree) 
                        and data.parentid in (select id from tree))
                """
        try:
            self.__cursor.execute(query)
            return self.__cursor.fetchall()
        except Exception as error:
            print('Ошибка в поиске сотрудников')
            raise error

    def __get_root(self, id):
        """
        Запускает поиск корня графа по указанному ID

        :param id: ID сотрудника
        """
        query = f'select getroot({id})'
        try:
            self.__cursor.execute(query)
            return self.__cursor.fetchone()[0]
        except Exception as error:
            raise error
