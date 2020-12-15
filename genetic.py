# Main executable blackjack game
from strategy import randomStrat, printClean, optStrat, crossOver, ObjectSchema, getStrategiesFromGeneration, bestStrategyFromGeneration
from gameSeries import playSeries
import multiprocessing
import random
import time
import json

NUM_STRATEGIES = 400 #Number of strategies each gen to run the genetic algorithm
NUM_GAMES_PER_STRATEGY = 500000 # Number of games each strategy plays through to get fitness score
TOURNAMENT_SIZE = 2 # Tournament Size for Tournament Select
GEN_START = 143 # If GEN_START = 0, starts GA from scratch, or you can start from a specific saved generation


#[tournamentSelect tournamentSize strategySet] returns the winner of a tournament through
#tournament selection
def tournamentSelect(tournamentSize, strategySet):
    tourneyEntrants = random.sample(strategySet, k=tournamentSize)
    parent = max(tourneyEntrants, key = lambda strat: strat.fitness)
    return parent

# [ifTerminate strategies] determines whether the GA algorithm should terminate
# by checking whether the best strategy has been leading for 20 generations
def ifTerminate(strategies):
    bestStrat = max(strategies, key = lambda strat: strat.fitness)
    return bestStrat.numGenerations >= 20

# [incrGeneration strat] increments the generation of strategy and returns it
def incrGeneration(strategy):
    strategy.incrGen()
    return strategy
# runSeries(strategy) runs a blackjack series for NUM_GAMES_PER_STRATEGY then updates the fitness score
def runSeries(strategy):
    stratFitness = playSeries(strategy, NUM_GAMES_PER_STRATEGY)
    strategy.setFitness(stratFitness)
    # print(str(i)+ "| net loss from " + str(NUM_GAMES_PER_STRATEGY) +" games: " + str(stratFitness))
    return strategy

# converts a generation to a JSON and writes it to a file
def genToJSON(gen, strategies, best):
    objectSchema = ObjectSchema()
    data = {'best' : objectSchema.dump(best), 'strategies' : objectSchema.dump(strategies, many=True)}
    with open('generations/gen' + str(gen)+'.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return

# main executable for GA algorithm
def main():
    mainStartTime = time.time() #starts up a timer for the algorithm
    #checks if we are starting from a saved generation or a new beginning
    if GEN_START == 0:
        strategies = [randomStrat() for i in range(NUM_STRATEGIES)]
        gen = 0
        runFirst = True
    else: 
        strategies = getStrategiesFromGeneration(GEN_START)
        gen = GEN_START
        runFirst = False
    print('got first set of strats')
    # main while loop each loop is a generation, and runs until it reaches a terminating state
    while not ifTerminate(strategies):
    # while gen <= 1:
        # conditional for every hour of running the program, sleep for 15 minutes to avoid pushing
        # the computer too much
        if time.time() - mainStartTime >= 3600.0:
            print('sleeping')
            time.sleep(900)
            mainStartTime = time.time()
            print('done sleeping')

        # runs the set of strategies through blackjack games to find their fitness scores
        # uses multiprocessing to run through blackjack games faster
        # once it has ran writes the generation to a json
        # increments numGenerations for the best strategy
        if runFirst:
            startTime = time.time()
            pool = multiprocessing.Pool(processes = NUM_STRATEGIES)
            strategies = pool.map(runSeries, strategies)
            best = max(strategies, key = lambda strat: strat.fitness)
            genToJSON(gen, strategies, best)
            print(str(gen)+'|Time ran ' + str(time.time() - startTime))
            best = max(strategies, key = lambda strat: strat.fitness)
            strategies = [incrGeneration(strat) if strat.fitness == best.fitness else strat for strat in strategies]
            print('best Strategy of gen ' + str(gen) + '\n' + str(best))
        runFirst = True

        ## Tournament Selection
        # Runs tournament selection to find a set of suitable parents
        worstStrategy = min(strategies, key = lambda strat: strat.fitness)
        parents = []
        numParents = int(NUM_STRATEGIES/2 if (NUM_STRATEGIES/2) % 2 == 0 else (NUM_STRATEGIES - 1)/2)
        for i in range(numParents):
            parents.append(tournamentSelect(TOURNAMENT_SIZE, strategies))
        
        ## Crossover
        # Iterates through 2 parents to make a new child strategy
        children = set()
        for i in range(0, len(parents), 2):
            children.add(crossOver(parents[i], parents[i+1], worstStrategy.fitness))
        
        ## Deletion
        # Replaces all of the worst strategies with children
        strategies.sort(key = lambda strat: strat.fitness)
        strategies = [strat if children == set() else children.pop() for strat in strategies]

        gen += 1

    ## GA HAS FINISHED
    # Finds the best strategy and prints it, and compares it to the baseline optimal strat     
    bestStrat = max(strategies, key = lambda strat: strat.fitness)
    _ = playSeries(bestStrat, NUM_GAMES_PER_STRATEGY)
    print('best Strategy\n' + str(bestStrat))
    _ = playSeries(optStrat, NUM_GAMES_PER_STRATEGY)
    print('optimal Strategy\n' + str(optStrat))

if __name__ == '__main__':
    # main()
    bestStrat = bestStrategyFromGeneration(154)
    randomStrat = randomStrat()
    playSeries(randomStrat, NUM_GAMES_PER_STRATEGY)
    playSeries(bestStrat, NUM_GAMES_PER_STRATEGY)
    playSeries(optStrat, NUM_GAMES_PER_STRATEGY)
    print('random Strategy from my GA\n' + str(randomStrat) +'\n')
    printClean(randomStrat)
    print('best Strategy from my GA\n' + str(bestStrat) +'\n')
    printClean(bestStrat)
    print('optimal Strategy\n' + str(optStrat))
    printClean(optStrat)