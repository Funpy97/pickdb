# pickdb v0.0.4a
A simple and easy database manager based on pickle that provides to:
- Create database
- Create the tables in the database
- Manage the tables in the database


*Example code*
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
*Output*
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

# Some other example
```
"""
Create a table called 'test' in a database called 'db' and
insert in the table 10 fake users using the random module.
"""

from pickdb import *
import random

if __name__ == '__main__':
    db_name = 'db'
    table_name = 'test'
    columns = ('Name', 'Email', 'Age')

    try:
        db = PickleDB(db_name, is_new=True)

    except DatabaseExistsError:
        db = PickleDB(db_name)

    try:
        table = db.add(table_name, columns=columns)

    except TableExistsError:
        db.delete(table_name)
        table = db.add(table_name, columns = ('Name', 'Email', 'Age'))

    names = ['Carl', 'Mark', 'Anna', 'Nicole', 'David']
    age = range(20, 30)

    records = 10

    for _ in range(records):
        table.insert({'Name': random.choice(names), 'Email': 'example@test.com', 'Age': random.choice(age)},
                     syncsave=False)

```

*Print the table*
```
    print(table)
```
*Output*
```
┼──┼──────┼────────────────┼───┼
│id│Name  │Email           │Age│
┼──┼──────┼────────────────┼───┼
│0 │Carl  │example@test.com│22 │
┼──┼──────┼────────────────┼───┼
│1 │Nicole│example@test.com│24 │
┼──┼──────┼────────────────┼───┼
│2 │Anna  │example@test.com│26 │
┼──┼──────┼────────────────┼───┼
│3 │Anna  │example@test.com│20 │
┼──┼──────┼────────────────┼───┼
│4 │Mark  │example@test.com│23 │
┼──┼──────┼────────────────┼───┼
│5 │David │example@test.com│26 │
┼──┼──────┼────────────────┼───┼
│6 │Carl  │example@test.com│21 │
┼──┼──────┼────────────────┼───┼
│7 │Mark  │example@test.com│23 │
┼──┼──────┼────────────────┼───┼
│8 │Carl  │example@test.com│23 │
┼──┼──────┼────────────────┼───┼
│9 │Mark  │example@test.com│21 │
┼──┼──────┼────────────────┼───┼
```

*Delete records*
```
    """ Delete records where 'Age' is 23 or 'Age' is 24 """
    table.del_records([{'Age': 23}, {'Age': 24}])

    """ Delete records where 'Age' is 27 and 'Name' is 'Mark' """
    table.del_records([{'Age': 27, 'Name': 'Mark'}])

    """ Print the table """
    print(table)
```
*Output*
```
┼──┼─────┼────────────────┼───┼
│id│Name │Email           │Age│
┼──┼─────┼────────────────┼───┼
│0 │Carl │example@test.com│22 │
┼──┼─────┼────────────────┼───┼
│2 │Anna │example@test.com│26 │
┼──┼─────┼────────────────┼───┼
│3 │Anna │example@test.com│20 │
┼──┼─────┼────────────────┼───┼
│5 │David│example@test.com│26 │
┼──┼─────┼────────────────┼───┼
│6 │Carl │example@test.com│21 │
┼──┼─────┼────────────────┼───┼
│9 │Mark │example@test.com│21 │
┼──┼─────┼────────────────┼───┼
```


*Update records*
```
    """ Get the list of the id where 'Name' is 'David' """
    id_list = table.records_id({'Name': 'David'})

    """ Update the 'Email' to 'example2@test.com' for each id in the list_id """
    for _id in id_list:
        table.update(_id, {'Email': 'example2@test.com'}, syncsave=False)

    """ Print the table """
    print(table)
```
*Output*
```
┼──┼─────┼─────────────────┼───┼
│id│Name │Email            │Age│
┼──┼─────┼─────────────────┼───┼
│0 │Carl │example@test.com │22 │
┼──┼─────┼─────────────────┼───┼
│2 │Anna │example@test.com │26 │
┼──┼─────┼─────────────────┼───┼
│3 │Anna │example@test.com │20 │
┼──┼─────┼─────────────────┼───┼
│5 │David│example2@test.com│26 │
┼──┼─────┼─────────────────┼───┼
│6 │Carl │example@test.com │21 │
┼──┼─────┼─────────────────┼───┼
│9 │Mark │example@test.com │21 │
┼──┼─────┼─────────────────┼───┼
```


*Print records*
```
    """ Print the records where 'Name' is 'Mark' """
    print(table.get_records(table.records_id({'Name': 'Mark'})))
```
*Output*
```
[{'Name': 'Mark', 'Email': 'example@test.com', 'Age': 21}]
```

*Chek if a record is matched*
```
    """ Print if there are 2 records with age 27 """
    print(table.is_matched_n({'Age': 27}, n=2))
```
*Output*
```
False
```



