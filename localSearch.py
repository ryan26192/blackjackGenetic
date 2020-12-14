from strategy import randomStrat 
from gameSeries import playSeries
import copy

numGames = 10000

def search():
    strat = randomStrat() # current strategy
    perf = playSeries(strat, numGames) # performance of current strategy
    # noNeighbor = True # true if we never find a better neighbor
    while True:
        # Iterate through all neighbor strategies
        # A) Check hard table
        if(test_hard(strat, perf)):
            continue

        # B) Check soft table
        if(test_soft(strat, perf)):
            continue

        # C) Check pair table
        if(test_pair(strat, perf)):
            continue
        
        # if we reach this line, that means no improvements were found in any neighbors and we are done
        return strat

# Tests hard table cells for improvements
# Returns true if strat has been updated with improvement
def test_hard(strat, perf):
    # A) iterate through hard neighbors (p is player index, d is dealer index)
    for d in range(0,10): # dealer index range (really cards 2 through 12 minus 2)
        for p in range(5,21): # player inedx range 5-20
            temp = strat.hard[p][d]
            # If current cell is stay, test hit
            if(temp == 'S'): 
                strat.hard[p][d] = 'H'
            # If current cell is hit, test double down
            elif(temp == 'H'):
                strat.hard[p][d] = 'D'

            # compare performance of new strat to old and replace if better
            newPerf = playSeries(strat, numGames)
            if(newPerf > perf):
                return True
            else:
                strat.hard[p][d] = temp #revert change and continue
    return False

# Tests soft table cells for improvements
# Returns true if strat has been updated with improvement
def test_soft(strat, perf):
    # B) iterate through soft neighbors (p is player index, d is dealer index)
    for d in range(0,10): # dealer index range (really cards 2 through 12 minus 2)
        for p in range(2,10): # player index range 2-9
            temp = strat.soft[p][d]
            # If current cell is stay, test hit
            if(temp == 'S'): 
                strat.soft[p][d] = 'H'
            # If current cell is hit, test double down
            elif(temp == 'H'):
                strat.soft[p][d] = 'D'

            # compare performance of new strat to old and replace if better
            newPerf = playSeries(strat, numGames)
            if(newPerf > perf):
                return True
            else:
                strat.soft[p][d] = temp #revert change and continue
    return False

# Tests pair table cells for improvements
# Returns true if strat has been updated with improvement
def test_pair(strat, perf):
    # C) iterate through pair neighbors (p is player index, d is dealer index)
    for d in range(0,10): # dealer index range (really cards 2 through 12 minus 2)
        for p in range(2,12): # player index 2-11
            temp = strat.pair[p][d]

            # If current cell is stay, test hit AND pair
            if(temp == 'S'): 
                strat.pair[p][d] = 'H'
                # compare performance of new strat to old and replace if better
                newPerf = playSeries(strat, numGames)
                if(newPerf > perf):
                    return True

                strat.pair[p][d] = 'H'
                # compare performance of new strat to old and replace if better
                newPerf = playSeries(strat, numGames)
                if(newPerf > perf):
                    return True

            # If current cell is hit, test double down
            elif(temp == 'H'):
                strat.pair[p][d] = 'D'
                # compare performance of new strat to old and replace if better
                newPerf = playSeries(strat, numGames)
                if(newPerf > perf):
                    return True

            strat.soft[p][d] = temp #revert change and continue
    return False