import random


class GA_0_1_Knapsack:
    capacity = 50
    max_pop = 100
    items_count = 20
    mutation_rate = 0.01
    weights = []
    values = []

    def __init__(self, weights, values, n, capacity):
        self.weights = weights
        self.values = values
        self.items_count = n
        self.capacity = capacity

    def initial_pop(self, n):
        pop = [[random.randint(0, 1) for i in range(n)] for i in range(self.max_pop)]
        return pop

    def fitness(self, individual):
        indiv_weight = 0
        indiv_value = 0
        for i in range(len(individual)):
            indiv_weight += individual[i] * self.weights[i]
            indiv_value += individual[i] * self.values[i]
        if indiv_weight > self.capacity:
            return tuple([self.capacity - indiv_weight, indiv_weight, individual])
        return tuple([indiv_value, indiv_weight, individual])

    def grade_and_sort(self, population):
        graded = []
        for indiv in population:
            graded.append(self.fitness(indiv))
        graded.sort(reverse=True)
        return graded

    def random_selection(self, population):
        rs_rate = 0.2
        selected = []
        for indiv in population:
            if random.random() < rs_rate:
                selected.append(population[random.randint(self.max_pop // 3, self.max_pop - 1)])
        return selected

    def crossover(self, parents_list, n):
        crossover_point = random.randint(0, n - 1)
        children = []
        for i in range(len(parents_list) - 1):
            children.append(parents_list[i][:crossover_point] + parents_list[i + 1][crossover_point:])
        return children

    def mutation(self, population, n):
        for i in range(len(population)):
            if random.random() < self.mutation_rate:
                rand_index = random.randint(0, n - 1)
                population[i][rand_index] = int(not population[i][rand_index])

    def execute(self):
        next_pop = self.initial_pop(self.items_count)
        next_pop = self.grade_and_sort(next_pop)
        for j in range(800):
            temp = next_pop[:]
            next_pop = []
            for p in temp:
                next_pop.append(p[2])

            parents = next_pop[:2] + self.random_selection(next_pop)
            children = self.crossover(parents, self.items_count)
            selected = self.random_selection(next_pop)
            temp = children + selected
            for i in range(self.max_pop - (len(children) + len(selected))):
                temp.append(next_pop[i])
            next_pop = temp[:]
            self.mutation(next_pop, self.items_count)
            next_pop = self.grade_and_sort(next_pop)
            # print("gen", j, next_pop)
            if j >= 100 and self.mutation_rate < 0.1:
                self.mutation_rate += 0.01

        return next_pop[0]


class GA_UnboundedKnapsack:
    capacity = 50
    max_pop = 100
    items_count = 20
    mutation_rate = 0.01
    weights = []
    values = []

    def __init__(self, weights, values, n, capacity):
        self.weights = weights
        self.values = values
        self.items_count = n
        self.capacity = capacity

    def initial_pop(self, n):
        pop = [[random.randint(0, self.capacity // min(self.weights)) for i in range(n)] for i in range(self.max_pop)]
        return pop

    def fitness(self, individual):
        indiv_weight = 0
        indiv_value = 0
        for i in range(len(individual)):
            indiv_weight += individual[i] * self.weights[i]
            indiv_value += individual[i] * self.values[i]
        if indiv_weight > self.capacity:
            return tuple([self.capacity - indiv_weight, indiv_weight, individual])
        return tuple([indiv_value, indiv_weight, individual])

    def grade_and_sort(self, population):
        graded = []
        for indiv in population:
            graded.append(self.fitness(indiv))
        graded.sort(reverse=True)
        return graded

    def random_selection(self, population):
        rs_rate = 0.2
        selected = []
        for indiv in population:
            if random.random() < rs_rate:
                selected.append(population[random.randint(self.max_pop // 3, self.max_pop - 1)])
        return selected

    def crossover(self, parents_list, n):
        crossover_point = random.randint(0, n - 1)
        children = []
        for i in range(len(parents_list) - 1):
            children.append(parents_list[i][:crossover_point] + parents_list[i + 1][crossover_point:])
        return children

    def mutation(self, population, n):
        for i in range(len(population)):
            if random.random() < self.mutation_rate:
                rand_index1 = random.randint(0, n - 1)
                rand_index2 = random.randint(0, n - 1)
                temp = population[i][rand_index1]
                population[i][rand_index1] = population[i][rand_index2]
                population[i][rand_index2] = temp

    def execute(self):
        next_pop = self.initial_pop(self.items_count)
        next_pop = self.grade_and_sort(next_pop)
        for j in range(800):
            temp = next_pop[:]
            next_pop = []
            for p in temp:
                next_pop.append(p[2])

            parents = next_pop[:2] + self.random_selection(next_pop)
            children = self.crossover(parents, self.items_count)
            selected = self.random_selection(next_pop)
            temp = children + selected
            for i in range(self.max_pop - (len(children) + len(selected))):
                temp.append(next_pop[i])
            next_pop = temp[:]
            self.mutation(next_pop, self.items_count)
            next_pop = self.grade_and_sort(next_pop)
            # print("gen", j, next_pop)
            if j >= 100 and self.mutation_rate < 0.1:
                self.mutation_rate += 0.01

        return next_pop[0]
