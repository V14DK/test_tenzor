from database import Db


def main():
    try:
        db = Db(user='postgres', password='12Qwaszx04', dbname='test', path='data.json')
        workers = db.get_workers()
        print(workers)
    except:
        print("Ошибка при работе с PostgreSQL")
    finally:
        if db.connection:
            db._close()


if __name__ == '__main__':
    main()
