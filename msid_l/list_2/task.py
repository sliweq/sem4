"""Homework for lab_2."""

from typing import List

import pytest


def is_matrix_square(mat: List[List[int]]) -> bool:
    """
    Check if given matrix is a square one.

    :param mat: given matrix

    :return: true if matrix is square one, otherwise false
    """
    matrix_rows = len(mat)
    # if matrix_rows == 0: return False
    
    for row in mat:
        if len(row) != matrix_rows:
            return False

    return True

def get_minor_matrix(mat: List[List[int]], i: int, j: int) -> List[List[int]]:
    """
    Generate a minor matrix of M for row 'i' and column 'j'.

    :param mat: matrix to obtain a minor one by crossing out the row 'i' and
        the column 'j'
    :param i: index of row
    :param j: index of column

    :return: minor matrix
    """
    new_mat = []
    for row in range(len(mat)):
        new_col = []
        if row == i: 
            continue
        for col in range(len(mat[row])):
            if col == j:
                continue
            new_col.append(mat[row][col])
        new_mat.append(new_col)
        print(new_mat)
    return new_mat
    
    # return [row[:j] + row[j+1:] for row_index, row in enumerate(mat) if row_index != i]
    


def matrix_determinant(mat: List[List[int]]) -> int:
    """
    Compute matrix determinant using Laplace method.

    :param mat: matrix to compute determinant for

    :return: determinant
    """
    matrix_rows = len(mat)
    if matrix_rows <= 0:
        raise ValueError("Matrix is empty!")
    if not is_matrix_square(mat):
        raise ValueError("Matrix is not square!")
    if matrix_rows == 1:
        return mat[0][0]

    sign = 1
    result = 0
    for column in range(matrix_rows):
        result += sign*mat[0][column]*matrix_determinant(get_minor_matrix(mat,0,column))
        sign *= -1
    return result
        

@pytest.mark.parametrize(
    "input_matrix, expected_result",
    [
        ([[2, 4, 2], [3, 1, 1], [1, 2, 0]], True),
        ([[5]], True),
        ([[2, 4], [1, 8], [2, 5]], False),
    ],
)
def test_is_matrix_square(input_matrix, expected_result):
    assert expected_result == is_matrix_square(input_matrix)


@pytest.mark.parametrize(
    "input_matrix, row, col, expected_result",
    [
        ([[3, 0, -1], [-1, -1, 0], [1, -1, 2]], 0, 0, [[-1, 0], [-1, 2]]),
        ([[3, 0, -1], [-1, -1, 0], [1, -1, 2]], 1, 1, [[3, -1], [1, 2]]),
        (
            [
                [2, 5, 3, 6, 3],
                [17, 5, 7, 4, 2],
                [7, 8, 5, 3, 2],
                [9, 4, -6, 8, 3],
                [2, -5, 7, 4, 2],
            ],
            2,
            3,
            [[2, 5, 3, 3], [17, 5, 7, 2], [9, 4, -6, 3], [2, -5, 7, 2]],
        ),
    ],
)
def test_get_minor_matrix(input_matrix, row, col, expected_result):
    assert expected_result == get_minor_matrix(input_matrix, row, col)


@pytest.mark.parametrize(
    "matrix, expected_determinant",
    [
        ([[5]], 5),
        ([[4, 6], [3, 8]], 14),
        ([[2, 4, 2], [3, 1, 1], [1, 2, 0]], 10),
        ([[6, 1, 1], [4, -2, 5], [2, 8, 7]], -306),
        ([[2, 4, -3], [1, 8, 7], [2, 3, 5]], 113),
        ([[1, 2, 3, 4], [5, 0, 2, 8], [3, 5, 6, 7], [2, 5, 3, 1]], 24),
        (
            [
                [2, 5, 3, 6, 3],
                [17, 5, 7, 4, 2],
                [7, 8, 5, 3, 2],
                [9, 4, -6, 8, 3],
                [2, -5, 7, 4, 2],
            ],
            2060,
        ),
        (
            [
                [1, 2, 4, 0, 9],
                [2, 3, 4, 1, 1],
                [6, 7, 3, 9, 3],
                [2, 0, 3, 0, 2],
                [4, 5, 2, 3, 1],
            ],
            1328,
        ),
        (
            [
                [2, 4, 5, 3, 1, 2],
                [2, 4, 7, 5, 3, 2],
                [1, 1, 0, 2, 3, 1],
                [1, 3, 9, 0, 3, 2],
                [1, 1, 2, 2, 4, 1],
                [0, 0, 4, 1, 2, 3],
            ],
            88,
        ),
        (
            [
                [3, 2, 1, 4, 0, 1],
                [1, 2, 3, 1, 9, 1],
                [0, 2, 1, 1, 9, 0],
                [8, 2, 1, 0, 2, 3],
                [2, 3, 4, 0, 1, 2],
                [2, 1, 0, 0, 1, 1],
            ],
            -536,
        ),
    ],
)
def test_matrix_determinant_correct(matrix, expected_determinant):
    assert expected_determinant == matrix_determinant(matrix), "Incorrect result!"


@pytest.mark.parametrize(
    "incorrect_matrix",
    [
        ([[]]),
        ([[4, 6]]),
        ([[2, 4, -3], [1, 8, 7], [2, 5]]),
        ([[1, 2, 3, 4], [0, 2, 8], [3, 5, 6, 7], [2, 3, 1]]),
        (
            [
                [2, 5, 3, 6, 3],
                [17, 5, 7, 4, 2],
                [7, 8, 5, 3, 2],
                [9, 4, -6, 8, 3],
                [2, -5, 7, 4, 2],
                [2, -5, 7, 4, 2],
            ]
        ),
        ([[1, 2, 4, 0, 9], [2, 3, 4, 1], [6, 7, 3], [2, 0], [4]]),
    ],
)
def test_matrix_determinant_incorrect(incorrect_matrix):
    with pytest.raises(ValueError) as excinfo:
        matrix_determinant(incorrect_matrix)
    assert "Matrix is not square!" in str(excinfo.value)
