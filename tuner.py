import json
from parse import Parser


class Tuner:
    def __init__(self, db):
        self.__conn = db._conn
        self.__cursor = db._cursor

    def _start_tuning(self, file: json):
        """
        Запускает создание и заполнение таблиц по json-файлу,
        создание функции в бд
        """
        self.__create_table()
        self.__fill_table(file)
        self.__create_function()

    def __create_table(self):
        """
        Создает таблицы в существующей бд
        """
        query = f"""
                create table if not exists data
                (
                    Id integer primary key,
                    ParentId integer,
                    Name character varying(100) not null,
                    Type integer not null
                );
                """
        try:
            self.__cursor.execute(query)
            self.__conn.commit()
            print('Таблица создана')
        except Exception as error:
            raise error

    def __fill_table(self, file):
        """
        Заполняет таблицы значениями из json-файла
        """
        queries = Parser._parse_data(file)
        try:
            for query in queries:
                self.__cursor.execute(query)
            self.__conn.commit()
            print('Таблицы заполнены')
        except Exception as error:
            raise error

    def __create_function(self):
        """
        Создает фунцию в бд для поиска корня графа
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
                            select data.parentid, data.id from data where data.id = parent
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
