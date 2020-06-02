from tkinter import *
from tkinter import filedialog
import xlrd as wb
import numpy
import plotly.figure_factory as ff
from datetime import timedelta, datetime
import time as ct
import alg
import sys


class Schedule:
    workers = []

    def __init__(self, w):
        self.workers.clear()
        tmp = []
        for i in range(0, w):
            tmp.append([])
        self.workers = tmp.copy()

    def clear(self):
        self = []


class WorkData:
    workers = 0  # количество исполнителей
    works = 0  # Количество работ
    terms = []  # директивные сроки выполнения для каждой работы
    start_times = []  # времена доступности каждой работы
    duration = []  #


class Task:
    def __init__(self, num, t1, t2):
        self.num = num
        self.time_s = t1
        self.time_e = t2

    time_s = 0  # время начала выполнения задачи
    time_e = 0  # время окончания выполнения задачи
    num = 0  # номер задачи


def list_schedule():
    global schedule
    sum_ti = 0
    try:
        for i in range(0, len(schedule.workers)):
            t = schedule.workers[i]
            for task in t:
                ti = task.time_e - project.terms[task.num]
                if ti < 0:
                    ti = 0
                s = 'job index = ' + str(task.num) + ' machine index = ' + str(i) + ' Pij = ' + str(task.time_e - task.time_s) +\
                    ' Mi = ' + str(task.time_s) + ' Ci =' + str(task.time_e) + ' di = ' + str(project.terms[task.num]) +\
                    ' Ti = ' + str(ti)
                print(s)
                sum_ti += ti
        print('sum Ti = ' + str(sum_ti))
    except:
        print('Расписание не сформировано')


def add_task(schedule, worker, task):
    tmp_worker = schedule.workers[worker - 1].append(task)


def loadxls():
    file_name = filedialog.askopenfilename(filetypes=[("XLS files", "*.xlsx")], defaultextension='.xlsx')
    try:
        book = wb.open_workbook(file_name)
        sheet = book.sheet_by_name('WorkData')

        # ищем количество работ
        count = 0
        while sheet.cell(count, 0).value != 'works':
            count += 1

        count_c = 1
        while (count_c < sheet.ncols) | (sheet.cell(count, count_c).value != ''):
            if count_c < sheet.ncols - 1:
                count_c += 1
            else:
                break
        project.works = count_c

        # вносим нормативы-директивные сроки
        while sheet.cell(count, 0).value != 'norms':
            count += 1

        for i in range(1, project.works + 1):
            if sheet.cell(count, i).value == '':
                project.terms.append(0)
            else:
                project.terms.append(int(sheet.cell(count, i).value))

        project.start_times = numpy.zeros(project.works)

        # вносим времена доступности работ
        while sheet.cell(count, 0).value != 'start_times':
            count += 1

        for i in range(1, project.works + 1):
            project.start_times[i - 1] = int(sheet.cell(count, i).value)

        # читаем массив времен выполнения работ исполнителями
        while sheet.cell(count, 0).value != 'duration':
            count += 1

        count += 1
        project.workers = 0
        while sheet.cell(count, 0).value != 'end':
            current_worker = []
            for i in range(1, project.works + 1):
                if sheet.cell(count, i).value == '':
                    current_worker.append(0)
                else:
                    current_worker.append(int(sheet.cell(count, i).value))

            project.duration.append(current_worker)
            count += 1
            project.workers += 1

        print('Load complete')
    except:
        print('Ошибка ввода-вывода')

# инициализация переменных, подготовка к работе
def init():
    # обнуляем все рабочие массивы
    works = numpy.zeros(project.works)  # массив работ. Длина равна количеству работ. Содержит флаги 0,1 выполнения
    # работы
    freetime = numpy.zeros(project.works)  # одномерный массив сроков доступности исполнителей после окончания работы

    # создаем массив времен доступности исполнителей
    for i in range(1, project.works + 1):
        freetime[i - 1] = 0


def draw_schedule():
    global schedule
    today = datetime.now()
    df = []
    counter = 1
    for worker in schedule.workers:
        for task in worker:
            st_date = today + timedelta(task.time_s)
            end_date = today + timedelta(task.time_e)
            dt = dict(Task='Worker'+str(counter), Start=st_date, Finish=end_date, Resource='Tasks')
            df.append(dt)
        counter += 1

    colors = {'Tasks': 'rgb(200, 200, 200)'}

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=False, showgrid_x=True)
    file_name = filedialog.asksaveasfilename(title="Select file to save", filetypes=[("HTML files", "*.html")],
                                             defaultextension='.html')
    fig.write_html(file_name)


def get_duration(worker, job):
    tmp = project.duration[worker-1]
    return tmp[job]


def generate():
    global schedule
    print("Start processing")
    time = 0
    init()
    # запуск алгоритма
    start = ct.time()
    result = alg.calculate(project.duration, project.terms, project.workers, project.works)
    finish = ct.time()

    #обработка данных, выданных алгоритмом
    print('Время работы алгоритма ' + str((finish - start)*1000) + ' мс')

    #размещение данных в объект вывода
    schedule = Schedule(project.workers)
    wrk_counter = 1;
    for wrkr in result:
        for job in wrkr:
            t = Task(job[0], job[1], get_duration(wrk_counter, job[0])+job[1])
            add_task(schedule, wrk_counter, t)
        wrk_counter += 1


def optimize_schedule():
    global schedule

    if (schedule is None) or (schedule == []):
        print('No schedule to optimize')
        return

    if len(schedule.workers) == 0:
        print('No schedule to optimize')
        return

    #массив окончания работы исполнителей
    t_end = numpy.zeros(len(schedule.workers))
    count = 0
    for worker in schedule.workers:
        for task in worker:
            t_temp = task.time_e
        t_end[count] = t_temp
        count += 1

    worker_number = 0
    task_number = 0
    shifts = []
    for worker in schedule.workers:
        for task in worker:
            current_num = task.num
            current_duration = task.time_e - task.time_s
            minus_duration = t_end[worker_number] - current_duration
            for i in range(0, project.workers):
                if t_end[i] + get_duration(i, current_num) < minus_duration:
                    print('Optimization...')
                    shifts.append((current_num, worker_number, i))
            task_number += 1
        task_number = 0
        worker_number += 1

    s = shifts[0]
    shift_task(s[0], s[1], s[2])


def shift_task(number, old, new):
    global schedule
    print('Optimization method starting...')
    #переместить задачу number с работника old в конец работника new
    sequence_old = schedule.workers[old].copy()
    sequence_new = schedule.workers[new].copy()
    for task in sequence_old:
        if task.num == number:
            t_start_shift = task.time_s
            t_shift = task.time_e - task.time_s

    sequence_old_shift = []
    for task in sequence_old:
        if task.num != number:
            if not(task.num < t_start_shift):
                t = Task(task.num, task.time_s - t_shift, task.time_e - t_shift)
            else:
                t = Task(task.num, task.time_s, task.time_e)
            sequence_old_shift.append(t)

    sequence_new_shift = []
    for task in sequence_new:
        sequence_new_shift.append(task)
        t_append = task.time_e

    t = Task(number, t_append, t_append + get_duration(new, number))
    sequence_new_shift.append(t)

    wrk = len(schedule.workers)
    new_schedule = Schedule(0)
    count = 0
    for wrkr in schedule.workers:
        if count == old:
            new_schedule.workers.append(sequence_old_shift)
        elif count == new:
            new_schedule.workers.append(sequence_new_shift)
        else:
            new_schedule.workers.append(wrkr.copy())
        count += 1
    schedule.workers = new_schedule.workers.copy()
    print(len(schedule.workers))

def quit_program():
    master.destroy()
    sys.exit(0)


# создание основного окна программы
master = Tk()
schedule = []

# установка геометрии окна
master.geometry("190x350")

# виджет кнопки загрузки данных
b = Button(master, text='Load data...', command=loadxls, width=20, height=2)
b.place(x=20, anchor=NW, y=25)

b2 = Button(master, text='Generate schedule', command=generate, width=20, height=2)
b2.place(x=20, y=80, anchor=NW)

b3 = Button(master, text='Optimize schedule', command=optimize_schedule, width=20, height=2)
b3.place(x=20, y=135, anchor=NW)

b4 = Button(master, text='Show schedule', command=draw_schedule, width=20, height=2)
b4.place(x=20, y=190, anchor=NW)

b5 = Button(master, text='List schedule', command=list_schedule, width=20, height=2)
b5.place(x=20, y=245, anchor=NW)

b6 = Button(master, text='Exit', command=quit_program, width=20, height=2)
b6.place(x=20, y=300, anchor=NW)

project = WorkData()
mainloop()
