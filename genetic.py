# Main executable blackjack game
from strategy import randomStrat, optStrat, crossOver, ObjectSchema, getStrategiesFromGeneration
from gameSeries import playSeries
import multiprocessing
import random
import time
import json

NUM_STRATEGIES = 400
NUM_GAMES_PER_STRATEGY = 100000
TOURNAMENT_SIZE = 2
GEN_START = 119

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
    # print(str(i)+ "| net loss from " + str(NUM_GAMES_PER_STRATEGY) +" games: " + str(stratFitness))
    return strategy

def genToJSON(gen, strategies, best):
    objectSchema = ObjectSchema()
    data = {'best' : objectSchema.dump(best), 'strategies' : objectSchema.dump(strategies, many=True)}
    with open('generations/gen' + str(gen)+'.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return

def main():
    mainStartTime = time.time()
    _ = playSeries(optStrat, NUM_GAMES_PER_STRATEGY)
    print('optimal Strategy\n' + str(optStrat))
    if GEN_START == 0:
        strategies = [randomStrat() for i in range(NUM_STRATEGIES)]
        gen = 0
        runFirst = True
    else: 
        strategies = getStrategiesFromGeneration(GEN_START)
        gen = GEN_START
        runFirst = False
    print('got first set of strats')
    while not ifTerminate(strategies):
    # while gen <= 1:
        if time.time() - mainStartTime >= 3600.0:
            print('sleeping')
            time.sleep(900)
            mainStartTime = time.time()
            print('done sleeping')
        if runFirst:
            startTime = time.time()
            pool = multiprocessing.Pool(processes = NUM_STRATEGIES)
            strategies = pool.map(runSeries, strategies)
            best = max(strategies, key = lambda strat: strat.fitness)
            genToJSON(gen, strategies, best)
            print(str(gen)+'|Time ran ' + str(time.time() - startTime))
            best = max(strategies, key = lambda strat: strat.fitness)
            print('best Strategy of gen ' + str(gen) + '\n' + str(best))
        runFirst = True
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
        # print(' '.join(map(str, children)))
        strategies.sort(key = lambda strat: strat.fitness)
        strategies = [incrGeneration(strat) if children == set() else children.pop() for strat in strategies]
        gen += 1
    bestStrat = max(strategies, key = lambda strat: strat.fitness)
    _ = playSeries(bestStrat, NUM_GAMES_PER_STRATEGY)
    print('best Strategy\n' + str(bestStrat))
    _ = playSeries(optStrat, NUM_GAMES_PER_STRATEGY)
    print('optimal Strategy\n' + str(optStrat))

if __name__ == '__main__':
    main()