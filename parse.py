import json


class Parser:
    @staticmethod
    def open_json(file: json):
        with open(file, 'r', encoding='utf-8') as data:
            return json.load(data)

    @staticmethod
    def _parse_config(file: json):
        data = Parser.open_json(file)
        user = data.get('user')
        password = data.get('password')
        dbname = data.get('dbname')
        host = data.get('host')
        port = data.get('port')
        return user, password, dbname, host, port

    @staticmethod
    def _parse_data(file: json):
        """
        Парсит json-файл для заполнения таблиц
        """
        data = Parser.open_json(file)
        for row in data:
            id = row.get('id')
            parentid = row.get('ParentId')
            parentid = parentid if parentid is not None else 'NULL'
            name = row.get('Name')
            type = row.get('Type')
            query = f"""
                    insert into data (Id, ParentId, Name, Type) values ({id}, {parentid}, '{name}', {type})
                    on conflict (Id) do update set ParentId = {parentid}, Name = '{name}', Type = {type}
                    """
            yield query
