""" This module contain the 2 main classes of the package: Table, PickleDB. """

import pickle
import os
from typing import List, Sequence, Iterable
from pickdb.modules.displaytable import tabulate
from pickdb.modules.exceptions import *


class Table:
    def __init__(self, db_path: str, name: str, columns: Sequence):
        """ Table object.\n
         It provides the manipulation of the stored data. """

        self.db_path = db_path
        self.name = name
        self.columns = ['id'] + list(str(data) for data in columns)
        self.__record_id = 0
        self.__data = {cname: [] for cname in self.columns}

    def reset(self):
        """ Reset each column in the table.\n
        Note: it will not reset the id list. """

        self.__data = {cname: [] for cname in self.columns}

        self.save()

    def last_id(self) -> int:
        """ Return the last id of the table. """

        return self.__record_id

    def reset_id_list(self):
        """ Reset the id list, id will reset to 0.\n
        Note: table must be empty or a IdError will be raised.
        """

        if len(self.__data['id']) != 0:
            raise IdError('Table must be empty to call reset_id_list(self)')

        else:
            self.__record_id = 0

    def data(self) -> dict:
        """ Return a dictionary of the data stored in the table. """

        return self.__data

    def id_list(self) -> list:
        """ Return a list object of the id of each record stored. """

        return self.__data['id']

    def copy(self):
        """ Return itself.\n
         Note: must call self.rename() after self.copy() to save the copied table in the PickleDB path.\n\n
         Example code:\n
         db = PickleDB('MyDb')\n
         t1 = db.add('MyTable')\n
         t2 = t1.copy()  # copied but not saved\n
         t2.rename('MyTableCopy')  # now t2 is saved
         """

        return self

    def rename(self, new_name: str):
        """ Rename the current table name with new_name. """

        if os.path.exists(os.path.join(self.db_path, new_name)):
            raise TableExistsError('Cannot rename the table if a table called new_name already exists')

        os.rename(os.path.join(self.db_path, self.name), os.path.join(self.db_path, new_name))
        self.name = new_name
        self.save()

    def add_column(self, column_name: str):
        """ Add a column called column_name in the table. """

        if column_name in self.columns:
            raise ColumnExistsError(f'Column {column_name} already exists')

        data = list(None for _ in range(len(self.__data['id'])))

        self.__data[column_name] = data
        self.columns.append(column_name)

        self.save()

    def del_column(self, column_name: str):
        """ Delete the column where name is column_name. """

        if column_name not in self.columns:
            raise ColumnNotFoundError(f'Column {column_name} not exists')

        self.__data.pop(column_name, None)

        self.save()

    def insert(self, record: dict, **kwargs):
        """ Insert a record in the table.\n
        The record is a dict like {'ColumnName': value}.\n
        If value is a Sequence or an Iterable, except a str, a RecordError will be raised. """

        if len(record.keys()) > len(self.columns) - 1:
            raise RecordError(f'Too many columns, {self.name} has {len(self.columns) - 1} columns')

        for key in record.keys():
            if key not in self.columns[1:]:
                raise RecordError(f'Table {self.name} not has column {key}')

            if isinstance(record[key], (Sequence, Iterable)) and type(record[key]) is not str:
                raise RecordError(f'Record values cannot contain Sequence or Iterable except of str: {record[key]}')

        data_to_load = [self.__record_id] + list(record[key] if str(key) in record.keys() else None
                                                 for key in self.columns[1:])
        self.__record_id += 1

        data_index = 0
        for key, value in self.__data.items():
            self.__data[key].append(data_to_load[data_index])
            data_index += 1

        if kwargs.get('syncsave', True):
            self.save()

    def update(self, record_id: int, new_record: dict, **kwargs):
        """ Update a record where id is record_id. """

        if record_id not in self.__data['id']:
            raise IdError(f'No id found with value {record_id}')

        if len(new_record.keys()) > len(self.columns) - 1:
            raise RecordError(f'Too many columns, {self.name} has {len(self.columns) - 1} columns')

        for key in new_record.keys():
            if key not in self.columns[1:]:
                raise RecordError(f'{new_record}\nKey not valid: "{key}"')

            if isinstance(new_record[key], (Sequence, Iterable)) and type(new_record[key]) is not str:
                raise RecordError(
                    f'Record values cannot contain Sequence or Iterable except of str: {new_record[key]}')

        data_index = self.__data['id'].index(record_id)

        for key in self.columns[1:]:
            if key in new_record.keys():
                self.__data[key][data_index] = new_record[key]

        if kwargs.get('syncsave', True):
            self.save()

    def count(self, record: dict) -> int:
        """ Return the number of rows where the record is matched. """

        if len(record.keys()) > len(self.columns) - 1:
            raise RecordError(f'Too many columns, {self.name} has {len(self.columns) - 1} columns')

        for key in record.keys():
            if key not in self.columns[1:]:
                raise RecordError(f'{record}\nKey not valid: "{key}"')

            if isinstance(record[key], (Sequence, Iterable)) and type(record[key]) is not str:
                raise RecordError(f'Record values cannot contain Sequence or Iterable except of str: {record[key]}')

        counter = 0

        for i in range(len(self.id_list())):
            if {key: self.__data[key][i] for key in record.keys()} == record:
                counter += 1

        return counter

    def is_matched_n(self, record: dict, n=1) -> bool:
        """ Check if a record is matched n time in the table. """

        counter = self.count(record)

        if counter == n:
            return True

        else:
            return False

    def records_id(self, record: dict) -> List[int]:
        """ Return a list object that contains the id of each row where the record is matched. """

        if len(record.keys()) > len(self.columns) - 1:
            raise RecordError(f'Too many columns, {self.name} has {len(self.columns) - 1} columns')

        for key in record.keys():
            if key not in self.columns[1:]:
                raise RecordError(f'{record}\nKey not valid: "{key}"')

            if isinstance(record[key], (Sequence, Iterable)) and type(record[key]) is not str:
                raise RecordError(f'Record values cannot contain Sequence or Iterable except of str: {record[key]}')

        id_list = []

        for i in range(len(self.id_list())):
            if {key: self.__data[key][i] for key in record.keys()} == record:
                id_list.append(self.__data['id'][i])

        return id_list

    def column(self, column_name: str) -> list:
        """ Return a list object that contain the values of the column column_name. """

        if column_name not in self.columns:
            raise ColumnNotFoundError(f'Column {column_name} not exists')

        return self.__data[column_name]

    def get_records(self, id_list: Sequence[int]) -> List[dict]:
        """ Return a list object that contains the dictionary of the record where id is in id_list. """

        records = []
        for _id in id_list:
            if _id not in self.__data['id']:
                raise IdError(f'No id found with value {_id}')

            data_index = self.__data['id'].index(_id)
            records.append({key: value[data_index] for key, value in self.__data.items() if key != 'id'})

        return records

    def del_records(self, records: Sequence[dict]):
        """ Delete all records from the table that matches with a record in records sequence. """

        if not isinstance(records, Sequence) or type(records) is str:
            raise RecordError('Records must be a sequence of dictionaries')

        id_list = []

        for record in records:
            for record_id in self.records_id(record):
                id_list.append(record_id)

        self.del_records_by_id(id_list)

    def del_records_by_id(self, id_list: Sequence[int]):
        """ Delete the records from the table where id is in id_list. """

        for _id in id_list:
            if _id not in self.__data['id']:
                raise IdError(f'No id found with value {_id}')

            data_index = self.__data['id'].index(_id)

            for key in self.__data.keys():
                self.__data[key].pop(data_index)

        self.save()

    def save(self):
        """ Save the current table. """

        with open(os.path.join(self.db_path, self.name), 'wb') as tablefile:
            pickle.dump(self, tablefile, pickle.HIGHEST_PROTOCOL)

    def __str__(self):
        """ Print the table. """

        raw_rows = list(value for value in self.__data.values())

        rows = []

        for i in range(len(raw_rows[0])):
            rows.append([row[i] for row in raw_rows])

        tabulate(self.columns, rows)

        return ''

    def __getitem__(self, item) -> list:
        """ Return a list object that contain the values of the column passed between [] """

        if item not in self.columns:
            raise ColumnNotFoundError(f'Column {item} not exists')

        return self.__data[item]


class PickleDB:
    def __init__(self, db_name: str, is_new=False):
        """ PickleDB object\n
        It provides the tables manipulation in the DB. """

        self.name = db_name
        self.path = os.path.join(os.getcwd(), self.name)

        if is_new:
            if os.path.exists(self.path):
                raise DatabaseExistsError('This database already exists in this directory')

            else:
                os.mkdir(self.path)

        else:
            if not os.path.exists(self.path):
                raise DatabaseNotFoundError(f'Database {self.name} not exists')

    def add(self, table_name: str, **kwargs) -> Table:
        """ Add a table called table_name in the DB. """

        if os.path.exists(os.path.join(self.path, table_name)):
            raise TableExistsError(f'A table called {table_name} already exists in this database')

        columns = kwargs.get('columns', ())
        if not isinstance(columns, Sequence):
            raise ValueError("Columns must be a Sequence like object")

        with open(os.path.join(self.path, table_name), 'wb') as tablefile:
            pickle.dump(Table(self.path, table_name, columns), tablefile, pickle.HIGHEST_PROTOCOL)

        return self.load(table_name)

    def load(self, table_name: str) -> Table:
        """ Load a table called table_name from the DB. """

        if not os.path.exists(os.path.join(self.path, table_name)):
            raise TableNotFoundError(f'Table {table_name} not exist')

        with open(os.path.join(self.path, table_name), 'rb') as tablefile:
            table = pickle.load(tablefile)

        return table

    def delete(self, table_name: str):
        """ Delete the table from the DB called table_name. """

        try:
            os.remove(os.path.join(self.path, table_name))

        except FileNotFoundError:
            pass

    def tables(self) -> List[Table]:
        """ Return a list of all Table objects stored in the DB. """

        names = os.listdir(self.path)

        tables = []
        for name in names:
            tables.append(self.load(name))

        return tables