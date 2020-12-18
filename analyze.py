from strategy import bestStrategyFromNormalGeneration, randomStrat, optStrat, bestStrategyFromLowParamGeneration
from gameSeries import playSeries
from common import percentDifference

NUM_GAMES_PER_STRATEGY = 500000
# whatGA = 'Normal', 'lowParams'
def analyze():
    normalGA = bestStrategyFromNormalGeneration(656) 
    lowGA = bestStrategyFromLowParamGeneration()
    random = randomStrat()
    playSeries(random, NUM_GAMES_PER_STRATEGY)
    playSeries(normalGA, NUM_GAMES_PER_STRATEGY)
    playSeries(optStrat, NUM_GAMES_PER_STRATEGY)
    playSeries(lowGA, NUM_GAMES_PER_STRATEGY)
    print('random Strategy from my GA\n' + str(random) +'\n')
    print('best Strategy from normal GA\n' + str(normalGA) +'\n')
    print('best Strategy from low GA\n' + str(lowGA) +'\n')
    print('optimal Strategy\n' + str(optStrat))
    bestFitness = max(normalGA.fitness, optStrat.fitness, lowGA.fitness)
    if bestFitness == optStrat.fitness:
        print('optStrat is the best Strategy')
    elif bestFitness == normalGA.fitness:
        print('the normal GA has the best strategy')
    else:
        print('the GA with low params has the best strategy')
    print('percent difference with normal and Opt: ' + str(percentDifference(normalGA.fitness, optStrat.fitness)))
    print('percent differenct with low and Opt: ' + str(percentDifference(lowGA.fitness, optStrat.fitness)))
if __name__ == '__main__':
    analyze()