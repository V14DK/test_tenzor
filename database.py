import psycopg2


class Db:
    def __init__(self, user, password, dbname, host='localhost', port='5432'):
        try:
            self._conn = psycopg2.connect(user=user,
                                          password=password,
                                          dbname=dbname,
                                          host=host,
                                          port=port)
            self._cursor = self._conn.cursor()
        except Exception as error:
            raise error

    def _close(self):
        """
        Закрывает соединение с бд
        """
        self._cursor.close()
        self._conn.close()
        print('Соединение закрыто')
