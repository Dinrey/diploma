import alg
import matrix as ma


def main():

    print("Please input number of machines:")
    number_machines = int(input())

    print("Please input number of jobs:")
    number_jobs = int(input())
    load_factor = 2
    matrix, due_dates = ma.init_matrix(number_machines, number_jobs, load_factor)

    print("Due dates:")
    print(due_dates)
    print("Matrix:")
    ma.out_matrix(matrix)
    print('\n')

    result = alg.calculate(matrix, due_dates, number_machines, number_jobs)

    print("\nResult:")
    ma.out_matrix_result(matrix, due_dates, result)


main()
