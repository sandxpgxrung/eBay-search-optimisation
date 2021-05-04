from ebay_api import search_items
from collections import namedtuple
from random import choices, randint, random, randrange
from typing import List, Callable, Tuple
from functools import partial
import time

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

item_structure = namedtuple('item', ['id', 'title', 'price'])
item_dictionary = search_items(keyword=input("Enter an item name: "))
price_limit = int(input("Enter a price limit: "))
[*item_list] = item_dictionary


def return_tuple(active_item) -> [item_structure]:
    return_list = []
    for i, j in enumerate(active_item):
        [item_id] = j.itemid
        [item_title] = j.title
        [item_price] = map(float, j.currentprice)
        [item_tuple] = [item_structure(item_id, item_title, item_price)]
        return_list.append(item_tuple)
    return return_list


items = return_tuple(item_list)


def get_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def get_population(size: int, genome_length: int) -> Population:
    return [get_genome(genome_length) for _ in range(size)]


def get_fitness(genome: Genome, items: [item_structure], weight_limit: int) -> int:
    if len(genome) != len(items):
        raise ValueError("genome and items must be of the same length")

    value = 0

    for i, item in enumerate(items):
        if genome[i] == 1:
            value += item.price

            if value > weight_limit:
                return 0
    return value


def get_selection(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(population=population, weights=[fitness_func(genome) for genome in population], k=2)


def get_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    cp = randint(1, length-1)
    return a[0:cp] + b[cp:], b[0:cp] + a[cp:]


def get_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index]-1)
    return genome


start = time.time()


def run_evolution(populate_func: PopulateFunc, fitness_func: FitnessFunc, fitness_limit: int,
                  selection_func: SelectionFunc = get_selection, crossover_func: CrossoverFunc = get_crossover,
                  mutation_func: MutationFunc = get_mutation, generation_limit: int = 100) -> Tuple[Population, int]:
    population = populate_func()
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population)/2)-1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation
    population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
    return population, i


population, generations = run_evolution(populate_func=partial(get_population, size=len(items), genome_length=len(items)),
                                        fitness_func=partial(get_fitness, items=items, weight_limit=price_limit),
                                        fitness_limit=price_limit, generation_limit=1000)
end = time.time()


def genome_to_items(genome: Genome, items: [item_structure]) -> [item_structure]:
    result = []
    for i, item in enumerate(items):
        if genome[i] == 1:
            result += [item.title]
            print(f"gen: {i} binary sol: {population}")
        if genome[i] == 0:
            result += [item.title + str("<EXCLUDED>")]
    return result


print(f"number of generations: {generations}")
print(f"time taken: {end - start}s")
print(f"binary solution: {population}")
print(f"textual solution (Best): {genome_to_items(population[1], items)}")
