#!/usr/bin/python
# -*- coding: utf-8 -*-


def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))


    # value, weight, taken = naive(weights, values, capacity)
    # value, weight, taken = dynamic(weights, values, capacity)
    value, weight, taken = dynamic_optimized(weights, values, capacity)
    verify(taken, value, values, weight, weights)
    
    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData

def verify(taken, objective, values, weight, weights):
    """
    """
    import itertools
    
    taken_value_sum  = sum(itertools.compress(values, taken))
    taken_weight_sum = sum(itertools.compress(weights, taken))
    
    if objective != taken_value_sum:
        print 'objective {} does not match taken_value_sum: {}, taken: {}'.format(objective, taken_value_sum, taken)
    
    if weight != taken_weight_sum:
        print 'weight {} does not match taken_weight_sum: {}, taken: {}'.format(weight, taken_weight_sum, taken)
    
def naive(weights, values, capacity):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full

    items = len(values)

    value = 0
    weight = 0
    taken = []

    for i in range(0, items):
        if weight + weights[i] <= capacity:
            taken.append(1)
            value += values[i]
            weight += weights[i]
        else:
            taken.append(0)

    return (value, weight, taken)

def dynamic(weights, values, capacity):
    table = [[0 for y in range(len(weights))] for x in xrange(0,capacity+1)]
    maxi = maxj = 0
    
    for i in xrange(capacity+1):
        for j in range(len(weights)):
            if j == 0 and i >= weights[j]:
                table[i][j] = values[j]
                continue
                
            if (i >= weights[j]):
                if (table[i-weights[j]][j-1] + values[j] > table[i][j-1]):
                    table[i][j] = table[i-weights[j]][j-1] + values[j]
                else:
                    table[i][j] = table[i][j-1]
            else:
                table[i][j] = table[i][j-1]

    taken = []; weight = 0;
    i = capacity; j = len(weights)-1
    value = table[i][j]
    
    while i > 0 and j >= 0:
        if (table[i][j] != table[i][j-1]):
            taken.insert(0, 1)
            weight += weights[j]
            i -= weights[j]
        else:
            taken.insert(0,0)
        j -= 1

    return (value, weight, taken)

def dynamic_optimized(weights, values, capacity):
    """
    """
    import bitarray
    
    table = [[{'value': 0, 'pre':bitarray.bitarray()} for y in range(2)] for x in xrange(0,capacity+1)]
    for j in range(len(weights)):
        for i in xrange(capacity+1):
            if j == 0 and i >= weights[j]:
                table[i][j&1] = {'value':values[j],'pre':bitarray.bitarray(1)}
                continue
                
            if (i >= weights[j]):
                if (table[i-weights[j]][~j&1]['value'] + values[j] > table[i][~j&1]['value']):
                    table[i][j&1] = {'value':table[i-weights[j]][~j&1]['value'] + values[j], 
                                     'pre': bitarray.bitarray(table[i-weights[j]][~j&1]['pre'])}
                    table[i][j&1]['pre'].append(1)
                else:
                    table[i][j&1] = {'value':table[i][~j&1]['value'], 'pre': bitarray.bitarray(table[i][~j&1]['pre'])}
                    table[i][j&1]['pre'].append(0)
            else:
                table[i][j&1] = {'value':table[i][~j&1]['value'], 'pre': bitarray.bitarray(table[i][~j&1]['pre'])}
                table[i][j&1]['pre'].append(0)

    maxj = max(enumerate(table[capacity]), key=lambda x: x[1]['value'])[0]
    taken = [[0,1][x] for x in table[capacity][maxj]['pre'].tolist()]
    weight = sum([weights[i] if ex else 0 for i,ex in enumerate(taken)])
    value = table[capacity][maxj]['value']

    return (value, weight, taken)
    
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

