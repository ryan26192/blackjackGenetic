from strategy import randomStrat 
from gameSeries import playSeries
import copy

numGames = 10000

def search():
    strat = randomStrat()
    perf = playSeries(strat, numGames)
    # noNeighbor = True # true if we never find a better neighbor
    while True:
        # Iterate through all neighbor strategies
        # - iterate through hard neighbors (p is player number, d is dealer number)
        for d in range(2,12):
            for p in range(5,21):
                # c corresponds to change
                for c in range(0,3):
                    # amend strat with one change
                    value = 'D'
                    if c == 1: 
                        value = 'H'
                    elif c == 2:
                        value = 'S' 
                    if value == strat.hard[p][d]: #ignore no-change value
                        continue
                    temp = strat.hard[p][d]
                    strat.hard[p][d] = value

                    # compare performance of new strat to old and replace if better
                    newPerf = playSeries(strat, numGames)
                    if(newPerf > perf):
                        perf = newPerf
                        # noNeighbor = False

        # - iterate through soft neighbors (p is player number, d is dealer number)
        for d in range(2,12):
            for p in range(2,10):
                # c corresponds to change
                for c in range(0,3):
                    # amend strat with one change
                    value = 'D'
                    if c == 1: 
                        value = 'H'
                    elif c == 2:
                        value = 'S' 
                    if value == strat.soft[p][d]: #ignore no-change value
                        continue
                    temp = strat.soft[p][d]
                    strat.soft[p][d] = value

                    # compare performance of new strat to old and replace if better
                    newPerf = playSeries(strat, numGames)
                    if(newPerf > perf):
                        perf = newPerf
                        # noNeighbor = False
        
        # - iterate through pair neighbors (p is player number, d is dealer number)
        for d in range(2,12):
            for p in range(2,12):
                # c corresponds to change
                for c in range(0,4):
                    # amend strat with one change
                    value = 'P'
                    if c == 1: 
                        value = 'D'
                    elif c == 2:
                        value = 'H' 
                    elif c == 3:
                        value = 'S' 
                    if value == strat.pair[p][d]: #ignore no-change value
                        continue
                    strat.pair[p][d] = value

                    # compare performance of new strat to old and replace if better
                    newPerf = playSeries(strat, numGames)
                    if(newPerf > perf):
                        perf = newPerf
                        # noNeighbor = False

