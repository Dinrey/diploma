from copy import deepcopy
from random import randint
import math

number_of_machines = int(input("Please input number of machines:\n").strip())
number_of_jobs = int(input("Please input number of jobs:\n").strip())

order_of_performing = []
for i in range(number_of_jobs):
    order_of_performing.append(None)

load_factor = 1
random_mode = \
    input("Do the program need to use random mode or manual mode?(1-Random mode, 0-Manual mode):\n").strip() == "1"
if random_mode:
    due_dates = []
    for i in range(number_of_jobs):
        due_dates.append(randint(0, math.ceil(10 * load_factor * (number_of_jobs / number_of_machines ))))
    matrix = []
    for i in range(number_of_machines):
        matrix.append([])
        for j in range(number_of_jobs):
            matrix[i].append(randint(1, 10 * (number_of_jobs / number_of_machines)))
    print("Due dates:")
    print(due_dates)
    print("Matrix:")
    for i in matrix:
        print(i)
else:
    due_dates = list(map(int, input("Due dates:\n")[1:-1].strip().split(",")))
    print("Matrix:")
    matrix = []
    for _ in range(number_of_machines):

        matrix.append(list(map(int, input()[1:-1].strip().split(","))))

static_matrix = deepcopy(matrix)
days = []
for _ in range(number_of_machines):
    days.append(0)
sum_Ti = 0

inp = input("Please input job execution order in \"job position\" format (leave line blank to continue):\n")
while inp != "":
    work, position = list(map(int, inp.strip().split()))
    order_of_performing[position] = work
    inp = input()

for i in range(number_of_jobs):
    due_date = due_dates[i]
    for j in range(number_of_machines):
            matrix[j][i] -= due_date

for job in range(number_of_jobs):

    smallest_indexes = []
    for i in range(number_of_jobs):
        smallest_value = 9999999999
        index = 0
        a = order_of_performing[i]
        for j in range(number_of_machines):
            if not (matrix[j][i] is None):
                if not (i in order_of_performing) or (order_of_performing[job] == i):
                    if matrix[j][i] < smallest_value:
                        index = j
                        smallest_value = matrix[j][i]
                else:
                    index = None
        smallest_indexes.append(index)

    index = order_of_performing[job]
    if index is None:
        # Maximum of minimal values
        index = 0
        maximum = -99999999
        for i in range(number_of_jobs):
            if not (smallest_indexes[i] is None):
                if not (matrix[smallest_indexes[i]][i] is None):
                    if matrix[smallest_indexes[i]][i] > maximum:
                        maximum = matrix[smallest_indexes[i]][i]
                        index = i

    job_done = False

    for i in range(number_of_jobs):
        if not(index is None) and not (smallest_indexes[index] is None):
            if not (matrix[smallest_indexes[index]][i] is None):
                matrix[smallest_indexes[index]][i] += static_matrix[smallest_indexes[index]][index]
                job_done = True
    for i in range(number_of_machines):
        if not (index is None) and not (smallest_indexes[index] is None):
            if not (index is None):
                matrix[i][index] = None

    if job_done:

        print("|job index = " + str(index))
        print("|machine index = " + str(smallest_indexes[index]))
        print("|Pij = " + str(static_matrix[smallest_indexes[index]][index]))
        print("|Mi = " + str(days[smallest_indexes[index]]))
        days[smallest_indexes[index]] += static_matrix[smallest_indexes[index]][index]
        print("|Ci = " + str(days[smallest_indexes[index]]))
        print("|di = " + str(due_dates[index]))
        ti = 0 if days[smallest_indexes[index]] - due_dates[index] < 0 else days[smallest_indexes[index]] - due_dates[index]
        print("|Ti = " + str(ti))
        sum_Ti += ti
        print("---------------")

print("\n\n\nsum Ti = " + str(sum_Ti))
