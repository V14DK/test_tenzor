import json
import psycopg2


class Db:
    def __init__(self, user, password, dbname, path, host='localhost', port='5432'):
        try:
            self.__conn = psycopg2.connect(user=user,
                                           password=password,
                                           dbname=dbname,
                                           host=host,
                                           port=port)
            self.__cursor = self.__conn.cursor()
            if self.__conn:
                self.connection = True
            else:
                self.connection = False
            print('Соединение открыто')
            self.start_settings(path)
        except Exception as error:
            raise error

    def _close(self):
        """
        Закрывает соединение с бд
        """
        self.__cursor.close()
        self.__conn.close()
        print('Соединение закрыто')

    def start_settings(self, file):
        """
        Запускает создание и заполнение таблиц по json-файлу,
        создание функции в бд
        """
        self.__create_tables()
        self.__fill_tables(file)
        self.__create_function()

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

    def __create_tables(self):
        """
        Создает таблицы в существующей бд
        """
        query = f"""
                create table if not exists parents
                (
                    Id integer primary key,
                    ParentId integer
                );
                create table if not exists data
                (
                    Id integer primary key references parents (Id),
                    Name character varying(100) not null,
                    Type integer not null
                );
                """
        try:
            self.__cursor.execute(query)
            self.__conn.commit()
            print('Таблицы созданы')
        except Exception as error:
            raise error

    def __fill_tables(self, file):
        """
        Заполняет таблицы значениями из json-файла
        """
        queries = self.__parse_json(file)
        try:
            for query in queries:
                self.__cursor.execute(query)
            self.__conn.commit()
            print('Таблицы заполнены')
        except Exception as error:
            raise error

    def __parse_json(self, file):
        """
        Парсит json-файл для заполнения таблиц
        """
        with open(file, 'r', encoding='utf-8') as db:
            data = json.load(db)

        for row in data:
            id = row.get('id')
            parentid = row.get('ParentId')
            parentid = parentid if parentid is not None else 'NULL'
            name = row.get('Name')
            type = row.get('Type')
            query = f'insert into parents (Id, ParentId) values ({id}, {parentid}) ' \
                    f'on conflict (Id) do update set ParentId = {parentid}'
            yield query
            query = f"insert into data (Id, Name, Type) values ({id}, '{name}', {type}) " \
                    f"on conflict (Id) do update set Name = '{name}', Type = {type}"
            yield query

    def __create_function(self):
        """
        Создает фунцию в бд для поиска корня графа
        :return:
        """
        query = f"""
                create or replace function getroot(identificator integer) returns integer 
                    language plpgsql as $$
                declare
                    parent int := identificator;
                    type int := (select data.type from data where data.id = identificator);
                    root int;
                begin
                    if type = 3 then
                        while parent is not null loop
                            select parents.parentid, parents.id from parents where parents.id = parent
                                into parent, root;
                        end loop;
                        return root;
                    else
                        return -1;
                    end if;
                end; $$;
                """
        try:
            self.__cursor.execute(query)
            self.__conn.commit()
            print('Функция создана')
        except Exception as error:
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

    def __get_workers(self, id):
        """
        Выполняет поиск в глубину для нахождения всех сотрудников офиса
        по ID офиса

        :param id: ID офиса
        """
        if id == -1:
            raise KeyError
        query = f"""
                WITH RECURSIVE tree(id, parentid, path) AS (
                SELECT id, parentid, array[id]::integer[]
                FROM parents WHERE parentid = {id}
                UNION ALL
                SELECT parents.*, path || array[parents.id]::integer[]
                FROM parents INNER JOIN tree on tree.id = parents.parentid)

                select data.name from data
                where data.id in
                    (select parents.id from parents
                    where parents.id not in (select parentid from tree) 
                        and parents.parentid in (select id from tree))
                """
        try:
            self.__cursor.execute(query)
            return self.__cursor.fetchall()
        except Exception as error:
            raise error
