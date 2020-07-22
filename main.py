from random import randint, choice, seed
from math import sqrt
import sys
from datetime import datetime

# TARGET = [0, 0, 1, 2, 3, 5, 5, 5, 6, 3, 1]
TARGET = [0, 5, 10, 15, 15, 20, 15, 15, 10, 10, 25, 30, 20, 10, 20, 25, 10,
          10, 0]

MAX_SHIFT_LENGTH = 8
MIN_SHIFT_LENGTH = 3

MUTATION_RATE = 0.25
POPULATION = 100
GENERATIONS = 100
NEGATIVE_PENALTY_FACTOR = 1


def run():
    seed()
    start = datetime.now()
    schedule = initialize()
    output_current(schedule)
    for i in range(GENERATIONS):
        population = [copy_schedule(schedule) for x in range(POPULATION)]
        mutate_population(population)
        current_rms = get_rms(schedule)

        new_schedule = get_best_schedule(population)
        new_rms = get_rms(new_schedule)
        if new_rms < current_rms:
            schedule = new_schedule
            print(f'Generation {i}')
            output_current(schedule)

    elapsed_seconds = (datetime.now() - start).seconds
    print('-------------------------')
    output_current(schedule)
    print(f'Agents: {len(schedule)}')
    print(f'Seconds elapsed: {elapsed_seconds}')


def get_best_schedule(population):
    best_rms = float(sys.maxsize)
    best_schedule = None
    for schedule in population:
        current_rms = get_rms(schedule)
        if current_rms < best_rms:
            best_rms = current_rms
            best_schedule = schedule

    return best_schedule


def mutate_population(population):
    mutations = max(1, int(MUTATION_RATE*len(population[0])))
    for schedule in population:
        for i in range(mutations):
            mutation = choice(['update', 'add', 'remove'])
            if mutation == 'update':
                schedule[randint(0, len(schedule)-1)] = create_agent_shift()
            elif mutation == 'add':
                schedule.append(create_agent_shift())
            elif mutation == 'remove':
                del schedule[len(schedule)-1]


def schedule_update(schedule, position, value):
    schedule[position] = value


def output_current(schedule):
    print(get_schedule_as_string(schedule))
    print(format_array(get_slot_sum(schedule)))
    print(format_array(TARGET))
    print(f'RMS: {get_rms(schedule)}')
    print()


def copy_schedule(schedule):
    return [shift.copy() for shift in schedule]


def initialize():
    schedule = []
    agents = 1
    # agents = max(TARGET)*2
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
    shift = [
        1 if x >= start and x <= start+length-1 else 0 for x in range(slots)]
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


def get_rms(schedule):
    slot_sum = get_slot_sum(schedule)
    square_diff = []
    for i in range(len(TARGET)):
        if slot_sum[i] < TARGET[i]:
            square_diff.append(
                (NEGATIVE_PENALTY_FACTOR * (slot_sum[i] - TARGET[i]))**2)
        else:
            square_diff.append((slot_sum[i] - TARGET[i])**2)
    # square_diff = [(slot_sum[i] - TARGET[i])**2 for i in range(len(TARGET))]

    mean_square = sum(square_diff) / len(square_diff)
    return sqrt(mean_square)


if __name__ == '__main__':
    run()
