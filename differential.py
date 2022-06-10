import random


class DE_0_1_Knapsack:
    capacity = 50
    max_pop = 100
    items_count = 20  # number of items in a collection
    CR = 0.7  # crossover rate
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

    def crossover(self, parents_list, n):
        new_parents = []
        for i in range(len(parents_list)):
            v = self.mutation(parents_list, n, parents_list[i], i)
            ind_fit = self.fitness(parents_list[i])
            v_fit = self.fitness(v)
            if v_fit[0] > ind_fit[0]:
                new_parents.append(v_fit[2])
            else:
                new_parents.append(ind_fit[2])

        return new_parents

    def mutation(self, population, n, ind, index):
        F = random.randint(0, 1)
        selected = [ind]

        canidates = list(range(0, len(population)))
        canidates.remove(index)
        random_index = random.sample(canidates, 3)

        selected.append(population[random_index[0]])
        selected.append(population[random_index[1]])
        selected.append(population[random_index[2]])

        vector = []
        for i in range(n):
            xor = selected[2][i] ^ selected[3][i]  # x2 xoring x3
            aand = F & xor  # F anding xor
            oor = selected[1][i] | aand  # x1 oring aand
            vector.append(oor)

        v_trial = []
        for i in range(len(vector)):
            if random.random() <= self.CR:
                v_trial.append(vector[i])
            else:
                v_trial.append(ind[i])

        return v_trial

    def execute(self):
        next_pop = self.initial_pop(self.items_count)
        next_pop = self.grade_and_sort(next_pop)
        for j in range(800):
            temp = next_pop[:]
            next_pop = []
            for p in temp:
                next_pop.append(p[2])

            children = self.crossover(next_pop, self.items_count)
            next_pop = self.grade_and_sort(children)
            # print("gen", j, next_pop)

        return next_pop[0]


class DE_UnboundedKnapsack:
    capacity = 50
    max_pop = 100
    items_count = 20  # number of items in a collection
    CR = 0.7  # crossover rate
    weights = []
    values = []

    def __init__(self, weights, values, n, capacity):
        self.weights = weights
        self.values = values
        self.items_count = n
        self.capacity = capacity

    def initial_pop(self, n):
        pop = [[random.randint(0, self.max_pop // min(self.weights)) for i in range(n)] for i in range(self.max_pop)]
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

    def crossover(self, parents_list, n):
        new_parents = []
        for i in range(len(parents_list)):
            v = self.mutation(parents_list, n, parents_list[i], i)
            ind_fit = self.fitness(parents_list[i])
            v_fit = self.fitness(v)
            if v_fit[0] > ind_fit[0]:
                new_parents.append(v_fit[2])
            else:
                new_parents.append(ind_fit[2])

        return new_parents

    def mutation(self, population, n, ind, index):
        F = 0.5  # mutation factor
        selected = [ind]  # x4

        canidates = list(range(0, len(population)))
        canidates.remove(index)
        random_index = random.sample(canidates, 3)

        selected.append(population[random_index[0]])  # x1
        selected.append(population[random_index[1]])  # x2
        selected.append(population[random_index[2]])  # x3

        vector = []
        for i in range(n):
            res = round(selected[1][i] + F * (selected[2][i] - selected[3][i]))  # x1 + F*(x2-x3)
            vector.append(abs(res))

        v_trial = []
        for i in range(len(vector)):
            if random.random() <= self.CR:
                v_trial.append(vector[i])
            else:
                v_trial.append(ind[i])

        return v_trial

    def execute(self):
        next_pop = self.initial_pop(self.items_count)
        next_pop = self.grade_and_sort(next_pop)
        for j in range(800):
            temp = next_pop[:]
            next_pop = []
            for p in temp:
                next_pop.append(p[2])

            children = self.crossover(next_pop, self.items_count)
            next_pop = self.grade_and_sort(children)
            # print("gen", j, next_pop)

        return next_pop[0]
