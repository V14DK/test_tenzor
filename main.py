from database import Db


def main():
    db = Db(user='postgres', password='12Qwaszx04', dbname='test2', path='data.json')
    workers = db.get_workers()
    print(workers)
    db._close()


if __name__ == '__main__':
    main()
