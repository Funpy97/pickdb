# pickdb v0.1a
A simple and easy database manager based on pickle that provide to:
- Create database
- Create tables in the database
- Manager tables in the database


Example code

```
from pickdb import *
import random
import time


if __name__ == '__main__':
    db_name = 'db'
    table_name = 'test'

    try:
        db = PickleDB(db_name, is_new=True)

    except DatabaseExistsError:
        db = PickleDB(db_name)

    try:
        table = db.add(table_name)

    except TableExistsError:
        db.delete(table_name)
        table = db.add(table_name)

    columns = ('Name', 'Email', 'Age')

    for column in columns:
        table.add_column(column)

    names = ['Carl', 'Mark', 'Anna', 'Nicole', 'David']
    age = range(18, 60)

    records = 10000

    t_start = time.time()
    for _ in range(records):
        table.insert({'Name': random.choice(names), 'Email': 'example@test.com', 'Age': random.choice(age)},
                     syncsave=False)
    print(f'insert time (on {records}): {int((time.time() - t_start) * 1000)}ms')

    t_start = time.time()
    ct = table.count({'Age': 23})
    print(f'count time (on {records})({str("{Age : 23}")}): {int((time.time() - t_start) * 1000)}ms')

    t_start = time.time()
    table.del_records([{'Age': 23}])
    print(f'del_records time (on {records})({ct}): {int((time.time() - t_start) * 1000)}ms')

    records -= ct

    t_start = time.time()
    id_list = table.records_id({'Age': 30})
    print(f'records_id time (on {records})({len(id_list)}): {int((time.time() - t_start) * 1000)}ms')

    t_start = time.time()
    table.del_records_by_id(id_list)
    print(f'del_records_by_id time (on {records})({len(id_list)}): {int((time.time() - t_start) * 1000)}ms')

    records -= len(id_list)

    rid = table.records_id({'Age': 22})

    t_start = time.time()
    for index in rid:
        table.update(index, {'Age': 23}, syncsave=False)
    print(f'update time (on {records})({len(rid)}): {int((time.time() - t_start) * 1000)}ms')

    t_start = time.time()
    table.is_matched_n({'Age': 40})
    print(f'is_matched_n time (on {records}): {int((time.time() - t_start) * 1000)}ms')
    
```

Output

```
insert time (on 10000): 82ms
count time (on 10000)({Age : 23}): 3ms
del_records time (on 10000)(232): 30ms
records_id time (on 9768)(256): 2ms
del_records_by_id time (on 9768)(256): 30ms
update time (on 9512)(219): 21ms
is_matched_n time (on 9512): 3ms

Process finished with exit code 0
```
