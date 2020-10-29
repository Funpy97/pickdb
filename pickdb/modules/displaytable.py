"""
DISPLAY OBJECT
def __init__(self, columns, rows, align=DEFAULT_ALIGN):

- 'columns' allowed types: list or tuple, example: ['column 1', 'column 2', ...] or ('column 1', 'column 2', ...)
- 'rows' allowed types: List[list], List[tuple], Tuple[list], Tuple[tuple]
- align allowed chars: '<', '>', '^' or Table.DEFAULT_ALIGN, Table.REVERSE_ALIGN, Table.CENTER_ALIGN

"""
from typing import Sequence


class DisplayTable:

    # TEXT ALIGN MODE
    DEFAULT_ALIGN = '<'
    REVERSE_ALIGN = '>'
    CENTER_ALIGN = '^'

    def __init__(self, columns, rows, align=DEFAULT_ALIGN):

        # TABLE CHARS
        self.NodeBar = '┼'
        self.VerticalBar = '│'
        self.HorizontalBar = '─'

        # SET ALIGN MODE
        self.Align = align

        # TABLE ELEMENTS
        self.Columns = columns
        self.Rows = rows


    def show(self) -> None:

        ColumnWidth = []                    # [max width for column 0, max width for column 1, ...]
        HorizontalSeparator = self.NodeBar  # Starts with a NodeBar

        # MAX WIDTH FOR EACH COLUMN
        for column in self.Columns:
            ColumnWidth.append(len(str(column)))
        for row in self.Rows:
            column_index = 0
            for element in row:
                try:
                    if len(str(element)) > ColumnWidth[column_index]:
                        ColumnWidth[column_index] = len(str(element))
                    column_index += 1
                except IndexError:
                    break

        # HORIZONTAL SEPARATOR
        for width in ColumnWidth:
            HorizontalSeparator += self.HorizontalBar * width + self.NodeBar

        # PRINT COLUMN NAMES ROW
        print(HorizontalSeparator)
        print(self.VerticalBar, end='')
        for i in range(len(self.Columns)):
            print(f'{str(self.Columns[i]):{self.Align}{ColumnWidth[i]}}{self.VerticalBar}', end='')
        print('\n' + HorizontalSeparator)

        # PRINT EACH ROWS
        for row in self.Rows:
            for i in range(len(ColumnWidth)):
                print(self.VerticalBar, end='')
                try:
                    print(f'{str(row[i]):{self.Align}{ColumnWidth[i]}}', end='')
                except IndexError:
                    print(f'{"":{self.Align}{ColumnWidth[i]}}', end='')
            print(self.VerticalBar)
            print(HorizontalSeparator)


def tabulate(columns: Sequence, rows: Sequence[Sequence]):
    table = DisplayTable(columns=columns, rows=rows)
    table.show()