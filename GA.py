from Chromossome import *
from copy import *


class GA():
    def __init__(self, num_gen=100, pop_size=50, cross_tax=0.5,
                         mut_chance=0.1, chrom_size=5, tourn_size=3, selection=1):
        self.num_generation = num_gen
        self.pop_size = pop_size
        self.crossover_tax = cross_tax
        self.mutation_chance = mut_chance
        self.chromossome_size = chrom_size
        self.tournament_size = tourn_size
        self.cities = {}
        self.population = []
        self.selection = selection
        self.error = 0.01

    def get_cities(self, filename):
        f = open(filename, "r")
        key = 1
        for line in f:
            self.cities[key] = map(int, line.split())
            key += 1
        f.close()    

    def init_pop(self):
        for i in range(self.pop_size):
            chromossome = Chromossome(self.chromossome_size, self.crossover_tax, self.mutation_chance)
            self.verify_valid_son(chromossome)
            self.population.append(chromossome)    

    def fitness(self, population):
        index = 0
        for chromossome in population:
            chromossome.absolute_fitness = 0
            chromossome.relative_fitness = 0
            for i in range(self.chromossome_size):
                chromossome.absolute_fitness += self.cities[int(chromossome.value[i])][int(chromossome.value[i + 1]) - 1]
            chromossome.relative_fitness = 1.0/chromossome.absolute_fitness

    def verify_valid_son(self, chromossome):
        generate_new_son = False
        for i in range(len(chromossome.value) - 1):
            if (self.cities[int(chromossome.value[i])][int(chromossome.value[i + 1]) - 1] == -1):
                generate_new_son = True
        if(chromossome.value[0] != chromossome.value[-1]):
            generate_new_son = True
        for i in range(1, self.chromossome_size - 1):
            for j in range(i + 1, self.chromossome_size):
                if chromossome.value[i] == chromossome.value[j]:
                    generate_new_son = True
        if generate_new_son == True:
            chromossome.value = sample(xrange(1, self.chromossome_size + 1),  self.chromossome_size)
            chromossome.value.append(chromossome.value[0])
            self.verify_valid_son(chromossome)
                    
    def tournament(self):
        fathers = []
        best_index = 0
        best_fitness = 0
        for i in range(self.tournament_size):
            fathers.append(self.population[int(random() * self.pop_size)])
            if fathers[i].relative_fitness > best_fitness:
                best_index = i
                best_fitness = fathers[i].relative_fitness
        return fathers[best_index]

    def sum_all_fitness(self):
        sum_fitness = 0
        for chromossome in self.population:
            sum_fitness += chromossome.relative_fitness
        return sum_fitness
        
    def roulette(self):
        index = 0
        aux_sum = 0
        upper_boundary = random()*self.sum_all_fitness()
        i = 0
        while(aux_sum < upper_boundary) and (i < self.pop_size):
            aux_sum += self.population[i].relative_fitness
            i += 1
        index = i - 1
        return self.population[index]

    def get_best(self, population):
        index_best = 0
        fitness_best = 0
        for i in range(len(population)):
            if population[i].relative_fitness > fitness_best:
                index_best = i
                fitness_best = population[i].relative_fitness
        return index_best
    
    def generation(self):
        new_population = []
        index_fathers = 1
        index_sons = 1
        if self.selection == 0:
            print "Selection Mode: Roulette"
        else:
            print "Selection Mode: Tournament"
        while(len(new_population) < self.pop_size):
            if self.selection == 0:
                father1 = self.roulette()
                father2 = self.roulette()
                print "Selected Fathers:\n\n#{0}: {1}\n#{2}: {3}\n".format(index_fathers, father1, index_fathers + 1, father2)
                sons = father1.crossover(father2)
                index_fathers += 2
            else:
                father1 = self.tournament()
                father2 = self.tournament()
                print "Selected Fathers:\n\n#{0}: {1}\n#{2}: {3}\n".format(index_fathers, father1, index_fathers + 1, father2)
                sons = father1.crossover(father2)
                index_fathers += 2
            for son in sons:
                son.mutation()
                self.verify_valid_son(son)
                print "Adding son #{0}:{1} to the population.\n".format(index_sons, son)
                index_sons += 1
                new_population.append(son)
        self.population = deepcopy(new_population)
        self.fitness(self.population)

    def calc_media(self, population):
        media = 0.0
        for chromossome in population:
            media += chromossome.relative_fitness
        media = media / len(population)
        return media

    def verify_convergence(self):
        convergence = False
        index_best = self.get_best(self.population)
        if (self.population[index_best].relative_fitness - self.calc_media(self.population)) < self.error:
            convergence = True
        return convergence
    
    def process(self):
        self.get_cities("cidades.txt")
        self.init_pop()
        self.fitness(self.population)
        generation_index = 1
        while (not self.verify_convergence()) and (generation_index < self.num_generation):
            print "\n\n\t\t\tGENERATION {0}\n".format(generation_index)
            generation_index += 1
            self.generation()
        print "\n\n\t\tBEST SOLUTION FOUND AT GENERATION {0}.\nBest is : {1}".format(generation_index, self.population[self.get_best(self.population)])
        print "Number of Generations: {0}.\n".format(generation_index)
        print "Population Converged.\n"
            
if __name__ == "__main__":
    test = GA(10, 10, 0.5, 0.1, 5, 3, 1)
    test.process()
