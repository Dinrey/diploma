# Создание конвертированой матрицы
def convert_matrix(matrix, delays, number_machines, number_jobs):
    cost_matrix = [[] for x in range(number_machines)]
    for i in range(number_machines):
        for j in range(number_jobs):
            cost_matrix[i].append(matrix[i][j] - delays[j])
    return cost_matrix

# Выбор работы с минимальным di
def choice_task(matrix, do_not_used_tasks, number_machines, number_jobs, l):
    min_cost_values = []
    index = 0
    for j in do_not_used_tasks:
        min_cost_values.append(matrix[0][j] + l[0])
        for i in range(number_machines):
            if min_cost_values[index] > matrix[i][j] + l[i]:
                min_cost_values[index] = matrix[i][j] + l[i]
        index = index + 1

    job_index = do_not_used_tasks[0]
    max_min_cost = min_cost_values[0]
    index = 0
    for i in min_cost_values:
        if max_min_cost < i:
            job_index = do_not_used_tasks[index]
            max_min_cost = i
        index = index + 1
    return job_index


# Удалить выполненую работу
def rem_completed_task(do_not_used_tasks, task_i):
    for i in range(len(do_not_used_tasks)):
        if do_not_used_tasks[i] == task_i:
            del do_not_used_tasks[i]
            return


# Выбор исполнителя (который выполнит задачу с минимальным штрафом)
def choice_executor(matrix, number_machines, l, job_index):
    min_pos = None
    min_val = None
    for i in range(number_machines):
        min_current = matrix[i][job_index] + l[i]
        if min_val is None or min_val > min_current:
            min_pos = i
            min_val = min_current
    return min_pos


# l - время завершения выполнения последней работы
# l_indexes - список исполнителя и его работ
def calculate(matrix, delays, number_machines, number_jobs):
    l = [0 for x in range(len(matrix))]
    l_indexes = [[] for x in range(len(matrix))]
    cost_matrix = convert_matrix(matrix, delays, number_machines, number_jobs)

    do_not_used_tasks = [x for x in range(number_jobs)]

    while len(do_not_used_tasks) > 0:

        job_index = choice_task(cost_matrix, do_not_used_tasks, number_machines, number_jobs, l)

        machine_index = choice_executor(matrix, number_machines, l, job_index)

        l_indexes[machine_index].append([job_index, l[machine_index]])
        l[machine_index] += matrix[machine_index][job_index]
        rem_completed_task(do_not_used_tasks, job_index)
        #print('----------------------')

    return l_indexes
