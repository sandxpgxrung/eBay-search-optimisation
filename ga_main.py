from ebay_api import search_items
from collections import namedtuple
from typing import Callable, List, Tuple
from random import choices, randint, randrange, random
from functools import partial

item_dict = search_items(keyword="PS5")  # uses API service to retrieve specified products
# set_price = int(input("Enter a price limit: "))
[*item_list] = item_dict  # stores API response dictionary in a packed list
item_structure = namedtuple('item', ['id', 'title', 'price'])


def get_item(items):  # elicits the desired API response elements from dictionary
    final_list = []
    for i, j in enumerate(items):
        [list_id] = items[i].itemid
        [list_title] = items[i].title
        [list_price] = map(float, items[i].currentprice)
        [item_tuple] = [
            item_structure(list_id, list_title, list_price)
        ]
        final_list.append(item_tuple)
    return final_list


search_list = get_item(item_list)  # stores get_items()'s return value (tuple) in variable search_list
Genome = List[int]  # a list for storing Genomes of binary 0's and 1's
Population = List[Genome]
_fitness = Callable[[Genome], int]
_populate = Callable[[], Population]
_selection = Callable[[_populate, _fitness], Tuple[Genome, Genome]]
_crossover = Callable[[Genome, Genome], Tuple[Genome, Genome]]
_mutate = Callable[[Genome], Genome]


def generate_genome(length: int) -> Genome:  # length refers to the quantity of items in the list
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def fitness(genome: Genome, items: [item_structure], price_limit: float) -> int:
    if len(genome) != len(items):  # pre-condition to assume that genome and items are of same length for validity
        raise ValueError("genome and items must be of same length")

    value: float = 0

    for i, item in enumerate(items):
        if genome[i] == 1:
            value += item.price

            if value >= price_limit:
                return 0
    return round(value)


def selection_pair(_population: Population, fitness_function: _fitness) -> Population:  # separation of concerns
    return choices(
        population=_population,
        weights=[fitness_function(genome) for genome in _population],  # set probability for elements to choose from
        k=2  # draw twice from population to select a pair
    )


def n_p_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:  # single point crossover
    if len(a) != len(b):
        raise ValueError("genomes a and b must of same length")

    length = len(a)
    if length < 2:
        return a, b

    cp = randint(1, length - 1)  # cp = acronym for cutting point
    return a[0:cp] + b[cp:], b[0:cp] + a[cp:]


def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome


def evolution(
        populate: _populate, fitness_function: _fitness, fitness_limit: int, selection: _selection = selection_pair,
        crossover: _crossover = n_p_crossover, mutation_function: _mutate = mutation, gen_limit: int = 100
) -> Tuple[Population, int]:
    ev_population = populate()

    for i in range(gen_limit):
        ev_population = sorted(ev_population, key=lambda genome: fitness_function(genome), reverse=True)

        if fitness_function(ev_population[0]) >= fitness_limit:
            break

        new_gen = ev_population[0:2]  # elitism to keep a copy of top 2 solutions for next generation

        for j in range(int(len(ev_population) / 2) - 1):
            parents = selection(ev_population, fitness_function)
            offspring_a, offspring_b = crossover(parents[0], parents[1])
            offspring_a = mutation_function(offspring_a)  # apply mutation probability to each offspring
            offspring_b = mutation_function(offspring_b)
            new_gen += [offspring_a, offspring_b]

        ev_population = new_gen

    ev_population = sorted(ev_population, key=lambda genome: fitness_function(genome), reverse=True)

    return ev_population, i


population, generation = evolution(
    populate=partial(generate_population, size=len(search_list), genome_length=len(search_list)),
    fitness_function=partial(fitness, items=search_list, price_limit=10000),
    fitness_limit=1000, gen_limit=10000)


def genome_to_items(genome: Genome, items: [item_structure]) -> [item_structure]:
    result = []
    for i, item in enumerate(items):
        if genome[i] == 1:
            result += [items]
        #if genome[i] == 0:
        #    result += [items]
    return result


print(f"number of generations: {generation}")
print(f"textual solution (Best): {genome_to_items(population[1], search_list)}")
