from random import randint
from math import sqrt
import sys

TARGET = [0, 0, 1, 2, 3, 5, 5, 5, 6, 3, 0]

MAX_SHIFT_LENGTH = 8
MIN_SHIFT_LENGTH = 3

MUTATION_RATE = 0.25
POPULATION = 1000
GENERATIONS = 50


def run():
    print('foo')
    schedule = initialize()
    output_current(schedule)
    for i in range(GENERATIONS):
        population = [copy_schedule(schedule) for x in range(POPULATION-1)]
        mutate_population(population)

        schedule = get_best_schedule(population)
        output_current(schedule)


def get_best_schedule(population):
    best_rms = float(sys.maxsize)
    best_schedule = None
    for schedule in population:
        current_rms = rms(schedule)
        if current_rms < best_rms:
            best_rms = current_rms
            best_schedule = schedule

    return best_schedule


def mutate_population(population):
    is_first = True
    for schedule in population:
        if is_first:
            is_first = False
        else:
            mutate_schedule(schedule)


def mutate_schedule(schedule):
    mutations = int(MUTATION_RATE*len(schedule))
    for i in range(mutations):
        schedule[randint(0, len(schedule)-1)] = create_agent_shift()


def output_current(schedule):
    print(get_schedule_as_string(schedule))
    print(format_array(get_slot_sum(schedule)))
    print(format_array(TARGET))
    print(f'RMS: {rms(schedule)}')
    print()


def copy_schedule(schedule):
    return [shift.copy() for shift in schedule]


def initialize():
    schedule = []
    agents = max(TARGET)
    for i in range(agents):
        shift = create_agent_shift()
        schedule.append(shift)

    return schedule


def get_slot_sum(schedule):
    sum = [0 for x in range(len(TARGET))]
    for shift in schedule:
        for i in range(len(TARGET)):
            sum[i] += shift[i]
    return sum


def create_agent_shift():
    slots = len(TARGET)
    start = randint(0, slots - MIN_SHIFT_LENGTH)
    length = randint(MIN_SHIFT_LENGTH, min(MAX_SHIFT_LENGTH, slots-start))
    shift = [1 if x >= start and x <= start+length-1 else 0 for x in range(slots)]
    return shift


def get_schedule_as_string(schedule):
    schedule_as_string = ''
    for i in range(len(schedule)):
        shift_string = format_array(schedule[i])
        # shift_string = shift_format_string.format(*schedule[i])
        schedule_as_string += f'{shift_string}\n'

    return schedule_as_string


def format_array(array):
    format_string = ''.join('{:4}'*(len(array)))
    return format_string.format(*array)


def rms(schedule):
    slot_sum = get_slot_sum(schedule)
    square_diff = [(slot_sum[i] - TARGET[i])**2 for i in range(len(TARGET))]

    mean_square = sum(square_diff) / len(square_diff)
    return sqrt(mean_square)


if __name__ == '__main__':
    run()
