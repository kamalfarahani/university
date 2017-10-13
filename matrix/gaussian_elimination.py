from copy import deepcopy


def getFirstNonZeroIndex(row):
    for i in range(len(row)):
        if row[i] != 0:
            return i

    return len(row)


def findSmallestNonZeroElement(matrix, rowIndex):
    firsNonZeroIndexes = list(map(
        getFirstNonZeroIndex, matrix[rowIndex:]))

    elementColumn = min(firsNonZeroIndexes)
    elementRow = firsNonZeroIndexes.index(elementColumn) + rowIndex
    return elementRow, elementColumn


def rowMultiplication(row, multiplier):
    return list(map(
        lambda elm: elm * multiplier,
        row))


def rowAddition(addedRow, addingRow, multiplier):
    return list(map(
        lambda elm: elm[0] + multiplier * elm[1],
        list(zip(addedRow, addingRow))))


def toReducedRowEchelonForm(matrix):
    rowCount = len(matrix)
    columnCount = len(matrix[0])
    resultMatrix = deepcopy(matrix)

    for row in range(rowCount):
        tmpRow, tmpColumn = findSmallestNonZeroElement(resultMatrix, row)
        if tmpColumn >= columnCount:
            return resultMatrix

        resultMatrix[row], resultMatrix[
            tmpRow] = resultMatrix[tmpRow], resultMatrix[row]

        resultMatrix[row] = rowMultiplication(
            resultMatrix[row], float(1 / resultMatrix[row][tmpColumn]))

        for i in range(rowCount):
            if i == row:
                continue
            resultMatrix[i] = rowAddition(
                resultMatrix[i], resultMatrix[row], -resultMatrix[i][tmpColumn])

    return resultMatrix


def inputMatrix():
    rowsNum = int(input("Enter number of rows: "))
    columnsNum = int(input("Enter number of columns: "))

    matrix = [[0 for c in range(columnsNum)] for r in range(rowsNum)]
    for rowIndex in range(rowsNum):
        for columnIndex in range(columnsNum):
            matrix[rowIndex][columnIndex] = int(input(
                "Enter element {}-{} :".format(rowIndex, columnIndex)))

    return matrix


def printMatrix(matrix):
    for row in matrix:
        print (", ".join((map(str, row))))


def main():
    resultMtx = toReducedRowEchelonForm(inputMatrix())
    printMatrix(resultMtx)


if __name__ == "__main__":
    main()
