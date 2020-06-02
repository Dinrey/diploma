import random
import math
random.seed()

MAX_LEAD_TIME = 10


def out_matrix(m):
    for row in m:
        print(row)


def out_matrix_result(matrix, due_dates, result):
    index = 0
    T_i_summ = 0
    for i in result:
        for j in i:
            print("---------------------")
            print("|job index = {}".format(j[0]))
            print("|machine index = {}".format(index))
            print("|Pij = {}".format(matrix[index][j[0]]))
            print("|Mi = {}".format(j[1]))
            due_date = j[1] + matrix[index][j[0]] - due_dates[j[0]]
            if due_date < 0:
                due_date = 0
            T_i_summ = T_i_summ + due_date
            print("|Ci = {}".format(j[1] + matrix[index][j[0]]))
            print("|di = {}".format(due_dates[j[0]]))
            print("|Ti = {}".format(due_date))
        index = index + 1
    print("---------------------")
    print("\n")
    print("sum Ti = {}".format(T_i_summ))


def init_matrix(number_machines, number_jobs, load_factor):
    due_dates = []

    for i in range(number_jobs):
        due_dates.append(random.randint(1, math.ceil(MAX_LEAD_TIME * load_factor * (number_jobs / number_machines))))
    matrix = []
    for i in range(number_machines):
        matrix.append([])
        for j in range(number_jobs):
            matrix[i].append(random.randint(1, MAX_LEAD_TIME))

    for j in range(number_jobs):
        min_val = matrix[0][j]
        for i in range(number_machines):
            if min_val > matrix[i][j]:
                min_val = matrix[i][j]
        if due_dates[j] < min_val:
            due_dates[j] = min_val

    return matrix, due_dates
