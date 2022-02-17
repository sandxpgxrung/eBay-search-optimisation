from main import search_items
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
input_limit = int(input("Enter a price limit: "))
[*item_list] = item_dictionary


def return_tuple(active_item) -> [item_structure]:  # get specific item fields and store it in a list
    return_list = []
    for i, j in enumerate(active_item):
        [item_id] = j.itemid
        [item_title] = j.title
        [item_price] = map(float, j.currentprice)
        [item_tuple] = [item_structure(item_id, item_title, item_price)]
        return_list.append(item_tuple)
    return return_list


items = return_tuple(item_list)  # the items are stored in this variable


def get_genome(length: int) -> Genome:  # generate list of genomes to represent the set of items in a given solution
    return choices([0, 1], k=length)


def get_population(size: int, genome_length: int) -> Population:  # stores the the list of genomes in a population set
    return [get_genome(genome_length) for _ in range(size)]


def get_fitness(genome: Genome, items: [item_structure], price_limit: int) -> int:  # define the fitness of a solution set with respect to the current population, price limit is the given constraint
    if len(genome) != len(items):
        raise ValueError("Ensure genome and items have the same solution length")

    value = 0

    for i, item in enumerate(items):
        if genome[i] == 1:
            value += item.price

            if value > price_limit:
                return 0
    return value


def get_selection(population: Population, fitness_func: FitnessFunc) -> Population:  # from the population set, 2 list of solutions are retrieved at random probability
    return choices(population=population, weights=[fitness_func(genome) for genome in population], k=2)


def get_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:  # the selected solution pairs are performed over a crossover operation to retrieve 2 new offsprings
    if len(a) != len(b):
        raise ValueError("Ensure the genomes A and B are given the same solution length")

    length = len(a)
    if length < 2:
        return a, b

    cp = randint(1, length - 1)
    return a[0:cp] + b[cp:], b[0:cp] + a[cp:]


def get_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:  # an offspring is mutated at random probability but with respect to the mutation rate
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)  # if the random probability is more than the mutation probability, then explicitly set the genome to 0
    return genome


start = time.time()

# the evolutionary functions take all the sub-functions of genetic algorithm and composes it together, so it can be iterated for the given evolutionary limit (generation limit)
def run_evolution(populate_func: PopulateFunc, fitness_func: FitnessFunc, fitness_limit: int,
                  selection_func: SelectionFunc = get_selection, crossover_func: CrossoverFunc = get_crossover,
                  mutation_func: MutationFunc = get_mutation, generation_limit: int = 100) -> Tuple[Population, int]:
    population = populate_func()
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation
    population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
    return population, i


population, generations = run_evolution(
    populate_func=partial(get_population, size=len(items), genome_length=len(items)),
    fitness_func=partial(get_fitness, items=items, price_limit=input_limit),
    fitness_limit=input_limit, generation_limit=1000)
end = time.time()


def genome_to_items(genome: Genome, items: [item_structure]) -> [item_structure]:  # this function is not part of the GA, only to output value's of solutions
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
