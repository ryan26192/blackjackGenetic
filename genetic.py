# Main executable blackjack game
from strategy import randomStrat, optStrat, crossOver
from gameSeries import playSeries
import multiprocessing
import random
import time

NUM_STRATEGIES = 400
NUM_GAMES_PER_STRATEGY = 100000
TOURNAMENT_SIZE = 2
# print(round(NUM_STRATEGIES/2, ndigits=None ))
def tournamentSelect(tournamentSize, strategySet):
    tourneyEntrants = random.sample(strategySet, k=tournamentSize)
    parent = max(tourneyEntrants, key = lambda strat: strat.fitness)
    return parent

def ifTerminate(strategies):
    bestStrat = max(strategies, key = lambda strat: strat.fitness)
    return bestStrat.numGenerations >= 20

def incrGeneration(strategy):
    strategy.incrGen()
    return strategy

def runSeries(strategy):
    stratFitness = playSeries(strategy, NUM_GAMES_PER_STRATEGY)
    strategy.setFitness(stratFitness)
    return strategy
    # print(str(i)+ "| net loss from " + str(NUM_GAMES_PER_STRATEGY) +" games: " + str(strategyFitness))

# def runGenerationWithProcessing(strategies, genNum):
#     startTime = time.time()
#     # strategies = [randomStrat() for i in range(NUM_STRATEGIES)]
#     i = 0
#     jobs = []
#     for strat in strategies:
#         p = multiprocessing.Process(target=runSeries, args=(strat, i))
#         i += 1
#         jobs.append(p)
#     for job in jobs: job.start()
#     for job in jobs: job.join()
#     print(str(genNum)+'|Time ran ' + str(time.time() - startTime))

# def runGeneration(strategies):
#     # strategies = [randomStrat() for i in range(NUM_STRATEGIES)]
#     i = 0
#     for strat in strategies:
#         runSeries(strat, i)
#         print(strat.fitness)
#         i += 1
#     return

    
def main():
    strategies = [randomStrat() for i in range(NUM_STRATEGIES)]
    gen = 0
    print('got first set of strats')
    while not ifTerminate(strategies):
    # while gen < 3:
        startTime = time.time()
        # strategies = [randomStrat() for i in range(NUM_STRATEGIES)]
        i = 0
        # jobs = []
        pool = multiprocessing.Pool(processes = NUM_STRATEGIES)
        strategies = pool.map(runSeries, strategies)
        # for strat in strategies:
        #     p = multiprocessing.Process(target=runSeries, args=(strat, i, fitness))
        #     i += 1
        #     jobs.append(p)
        # for job in jobs: job.start()
        # for job in jobs: job.join()
        print(str(gen)+'|Time ran ' + str(time.time() - startTime))
        # runGenerationWithProcessing(strategies, gen)
        # runGeneration(strategies)
        # print(' '.join(map(str, strategies)))
        best = max(strategies, key = lambda strat: strat.fitness)
        print('best Strategy of gen ' + str(gen) + '\n' + str(best))
        # print(' '.join(map(str, strategies)))
        ## Tournament Selection
        worstStrategy = min(strategies, key = lambda strat: strat.fitness)
        parents = []
        numParents = int(NUM_STRATEGIES/2 if (NUM_STRATEGIES/2) % 2 == 0 else (NUM_STRATEGIES - 1)/2)
        for i in range(numParents):
            parents.append(tournamentSelect(TOURNAMENT_SIZE, strategies))
        # print(' '.join(map(str, parents)))  
        children = set()
        for i in range(0, len(parents), 2):
            children.add(crossOver(parents[i], parents[i+1], worstStrategy.fitness))
        # print("children")
        # print(' '.join(map(str, children)))
        strategies.sort(key = lambda strat: strat.fitness)
        strategies = [incrGeneration(strat) if children == set() else children.pop() for strat in strategies]
        # print('next generation')
        gen += 1
    bestStrat = max(strategies, key = lambda strat: strat.fitness)
    _ = playSeries(bestStrat, NUM_GAMES_PER_STRATEGY)
    print('best Strategy\n' + str(bestStrat))
    _ = playSeries(optStrat, NUM_GAMES_PER_STRATEGY)
    print('optimal Strategy\n' + str(optStrat))

if __name__ == '__main__':
    main()
    # print('Processing: ' + str(timeit.timeit(runGenerationWithProcessing)))
    # print('normal: ' + str(timeit.timeit(runGeneration)))