from typing import List
from sympy import Number
from functools import reduce

def solve_simplex_table(table):
    print(matrix_to_str(table))
    print('_____________\n')
    
    if min(table[0][:-1]) >= 0 :
        return table
    
    rowIndex, columnIndex = find_pivot_item(table)
    new_table = pivot_on_pivot_item(table, rowIndex, columnIndex)

    return solve_simplex_table(new_table)


def pivot_on_pivot_item(table, rowIndex, columnIndex):
    pivot_row = rowMultiplication(
        table[rowIndex],
        Number('1') / table[rowIndex][columnIndex])

    f = lambda r: rowAddition(r, pivot_row, -r[columnIndex])
    
    return [f(table[i]) if i != rowIndex else pivot_row for i in range(len(table))]


def find_pivot_item(table):
    columnIndex = find_smallest_item_index(table[0][:-1])
    
    theta = map(lambda x: x[0] / x[1] if x[1] != 0 else None,
        zip([items[-1] for items in table[1:]],
            [items[columnIndex] for items in table[1:]]))

    rowIndex = find_smallest_non_negative_item_index(list(theta)) + 1

    return (rowIndex, columnIndex)


def find_smallest_item_index(l):
    index = 0

    for i in range(len(l)) :
        if l[i] < l[index] :
            index = i

    return index


def find_smallest_non_negative_item_index(l):
    index = 0

    for i in range(len(l)) :
        if l[i] == None:
            continue

        if l[index] == None :
            index = i

        if l[index] < 0 and l[i] > 0:
            index = i

        if l[i] > 0 and l[i] < l[index] :
            index = i

    return index

def make_simplex_table(z, a, b):
    first_row = [-i for i in z] + make_zero_list(len(a)) + [0]
    other_rows = [a[i] + [b[i]] for i in range(len(a))]

    return [first_row] + other_rows


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


def main():
    vars_num = int(input('Enter number of variables : '))
    const_num = int(input('Enter number of constraints : '))
    get_input = lambda n, m: to_symbols(get_input_matrix(n, m))

    print('Enter z matrix: ')
    z = get_input(1, vars_num)
    
    print('Enter A matrix: ')
    a = get_input(const_num, vars_num)
    
    print('Enter b matrix: ')
    b = get_input(const_num, 1)
    
    table = make_simplex_table(z, add_slack_vars(a), b)
    print(matrix_to_str(table))
    print('_________________\n')
    
    result = solve_simplex_table(table)
    print(matrix_to_str(result))


if __name__ == "__main__":
    main()