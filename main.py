from parse import Parser
from database import Db
from executor import Executor
from tuner import Tuner


def main():
    db = Db(*Parser._parse_config('config.json'))
    tuner = Tuner(db)
    tuner._start_tuning('data.json')
    executor = Executor(db)
    workers = executor.get_workers()
    print(workers)
    db._close()

if __name__ == '__main__':
    main()
