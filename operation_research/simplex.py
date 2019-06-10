import json
from typing import List
from sympy import Number, symbols
from functools import reduce


FILE_PATH = './input.json'

def solve_simplex_table(table, basic_vars):
    print_table(table, basic_vars)

    if min(table[0][:-1]) >= 0:
        if has_other_answer(table[0], basic_vars):
            print('We have another answer!')

        return table, basic_vars
    
    rowIndex, columnIndex = find_pivot_item(table)
    if has_no_answer(table, columnIndex):
        raise Exception('Problem has no unique answer!')

    new_table = pivot_on_pivot_item(table, rowIndex, columnIndex)
    new_basic_vars = make_basic_vars(basic_vars, rowIndex -1 , columnIndex)

    return solve_simplex_table(new_table, new_basic_vars)


def print_table(table, basic_vars):
    print(matrix_to_str(table), '\n')
    print('basic_vars: {}'.format(basic_vars))
    print('_____________\n')


def has_no_answer(table, column_index):
    column_items = [row[column_index] for row in table]
    positive_items = list(filter(
        lambda x: x > 0,
        column_items))
    
    return len(positive_items) == 0


def has_other_answer(first_row, basic_vars):
    basic_vars_columns = list(map(
        lambda x: sym_to_number(x[0]), basic_vars))
    
    for index, var in enumerate(first_row[:-1]):
        if (index not in basic_vars_columns) and var == 0:
            return True

    return False


def pivot_on_pivot_item(table, rowIndex, columnIndex):
    pivot_row = rowMultiplication(
        table[rowIndex],
        Number('1') / table[rowIndex][columnIndex])

    f = lambda r: rowAddition(r, pivot_row, -r[columnIndex])
    
    return [f(table[i]) if i != rowIndex else pivot_row for i in range(len(table))]


def find_pivot_item(table):
    columnIndex = find_smallest_item_index(table[0][:-1])
    
    theta = map(lambda x: safe_div(x[0], x[1]) if x is not None else None,
        map(lambda x: None if x[0] == 0 and x[1] < 0 else x,
            zip([items[-1] for items in table[1:]],
                [items[columnIndex] for items in table[1:]])))

    rowIndex = find_smallest_non_negative_item_index(list(theta)) + 1

    return (rowIndex, columnIndex)


def make_basic_vars(basic_vars, rowIndex, columnIndex):
    return [
        item if item[1] != rowIndex else (make_x_sym(columnIndex), item[1]) for item in basic_vars
    ]


def find_smallest_item_index(l):
    index = 0

    for i in range(len(l)) :
        if l[i] < l[index] :
            index = i

    return index


def find_smallest_non_negative_item_index(l):
    result_and_index = min(
        filter(
            lambda i: (i[0] is not None) and i[0] >= 0,
            zip(l, range(len(l)))),
            key = lambda i: i[0])
    
    return result_and_index[1]


def make_simplex_table(z, a, b):
    first_row = [-i for i in z] + make_zero_list(len(a[0]) - len(z)) + [0]
    other_rows = [a[i] + [b[i]] for i in range(len(a))]
    
    basic_vars = find_basic_vars(a)

    return ([first_row] + other_rows, basic_vars)


def find_basic_vars(a):
    size = len(a)
    id_mat = make_identity_matrix(size)

    basic_vars = []
    for i in range(size):
        col_index = find_column_index(get_column(i, id_mat), a)
        basic_var = (make_x_sym(col_index), i)
        basic_vars.append(basic_var)

    return basic_vars


def make_identity_matrix(size):
    return [
        [0 if j != i else 1 for j in range(size)] for i in range(size)
    ]


def get_columns(mat):
    return [get_column(i, mat) for i in range(len(mat[0]))]


def get_column(index, mat):
    return [row[index] for row in mat]


def find_column_index(column, mat):
    return get_columns(mat).index(column)


def add_slack_vars(a):
    length = len(a)
    tmp = zip(a, range(len(a)))
    f = lambda row : row[0] + make_zero_list(row[1]) + [1] + make_zero_list(length - row[1] - 1)
    
    return list(map(f , tmp))


def make_zero_list(length: int):
    return [Number('0') for _ in range(length)]


def rowMultiplication(row, multiplier):
    return list(map(
        lambda elm: elm * multiplier,
        row))


def rowAddition(addedRow, addingRow, multiplier):
    return list(map(
        lambda elm: elm[0] + multiplier * elm[1],
        list(zip(addedRow, addingRow))))


def make_x_sym(index):
    return symbols('x' + str(index))


def sym_to_number(sym):
    return int(str(sym)[1:])


def list_to_symbols(l):
    return list(map(lambda x: Number(str(x)), l))


def matrix_to_symbols(mat):
    return map(list_to_symbols, mat)


def matrix_to_str(mat):
    f = lambda row: reduce(lambda x, y: str(x) + '\t' + str(y), row)
    return reduce(lambda r1, r2: r1 + '\n' + r2, map(f, mat))


def to_symbols(x):
    if type(x) != type([]):
        return Number(str(x)) 
    
    return list(map(to_symbols, x))


def get_input_matrix(n, m):
    mat = [([0] * m) for _ in range(n)]

    for i in range(n):
        for j in range(m):
            mat[i][j] = input(
                'Please enter element {} {} :'.format(i + 1, j + 1))
    
    if n == 1 :
        mat = mat[0]
    
    if m == 1 :
        mat = [i[0] for i in mat]

    return mat


def safe_div(x1, x2):
    if x1 is None or x2 is None:
        return None
    
    if x2 == 0:
        return None
    
    return x1 / x2

def read_from_file():
    file = open(FILE_PATH)
    file_str = reduce(
        lambda acc, line: acc + line,
        file.readlines())
    
    file.close()

    data = json.loads(file_str)
    z = to_symbols(data['z'])
    a = to_symbols(data['a'])
    b = to_symbols(data['b'])
    kind = data['kind']

    return (z, a, b, kind)
 

def main():
    z, a, b, kind = read_from_file()

    if kind != '=':
        a = add_slack_vars(a)
    
    table, basic_vars = make_simplex_table(z, a, b)
    print(matrix_to_str(table))
    print('_________________\n')
    
    try:
        solve_simplex_table(table, basic_vars)
    except:
        print('Problem has no unique answer!')


if __name__ == "__main__":
    main()