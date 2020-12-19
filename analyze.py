from strategy import bestStrategyFromNormalGeneration, randomStrat, optStrat, bestStrategyFromLowParamGeneration, bestStrategyFromGeneration100_100000, bestStrategyFromGeneraation400_10000
from gameSeries import playSeries
from common import percentDifference

NUM_GAMES_PER_STRATEGY = 500000
# whatGA = 'Normal', 'lowParams'
def analyze():
    normalGA = bestStrategyFromNormalGeneration(656) 
    lowGA = bestStrategyFromLowParamGeneration()
    ga100_100000 = bestStrategyFromGeneration100_100000()
    ga400_10000 = bestStrategyFromGeneraation400_10000() 
    random = randomStrat()
    playSeries(random, NUM_GAMES_PER_STRATEGY)
    playSeries(normalGA, NUM_GAMES_PER_STRATEGY)
    playSeries(optStrat, NUM_GAMES_PER_STRATEGY)
    playSeries(lowGA, NUM_GAMES_PER_STRATEGY)
    playSeries(ga100_100000, NUM_GAMES_PER_STRATEGY)
    playSeries(ga400_10000, NUM_GAMES_PER_STRATEGY)
    print('random Strategy\n' + str(random) +'\n')
    print('best Strategy from normal GA\n' + str(normalGA) +'\n')
    print('best Strategy from low GA\n' + str(lowGA) +'\n')
    print('best Strategy from GA with 400 and 10000\n' + str(ga400_10000) +'\n')
    print('best Strategy from GA with 100 and 100000\n' + str(ga100_100000) +'\n')
    print('optimal Strategy\n' + str(optStrat))
    bestFitness = max(normalGA.fitness, optStrat.fitness)
    if bestFitness == optStrat.fitness:
        print('optStrat is the best Strategy')
    elif bestFitness == normalGA.fitness:
        print('the normal GA has the best strategy')
    print('percent difference with normal and Opt: ' + str(percentDifference(normalGA.fitness, optStrat.fitness)))
    print('percent difference with low and Opt: ' + str(percentDifference(lowGA.fitness, optStrat.fitness)))
    print('percent diff with ga400-10000 and Opt: ' + str(percentDifference(ga400_10000.fitness, optStrat.fitness)))
    print('percent diff with ga100-100000 and Opt: ' + str(percentDifference(ga100_100000.fitness, optStrat.fitness)))
if __name__ == '__main__':
    analyze()