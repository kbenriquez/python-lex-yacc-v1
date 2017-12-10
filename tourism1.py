# Kyle Marcus Enriquez
#
# This program takes in as input the following:
#   people(n)
#   locations(m)
#   preferences(o)
#   order(people, location1, location2)
#
#   people(n) - the number of people as input where n is a positive non-zero integer.
#   locations(m) - the number of locations as input where m is a positive non-zero integer.
#   preferences(o) - the total number of preferences from all the people from people(n) where o is a
#       positive non-zero integer.
#   order(person, location1, location2) - the preference of one person of one location over another.
#       person must be an integer 0 < person <= n, location1 must be an integer
#       0 > location1 >= m and location2 must be an integer 0 < location2 <= locations(m) NOT
#       including location1. This input must be repeated m times.

import sys
import math

def CheckIfEmpty(str):
    if not str.strip():
        return True
    else:
        return False

def GetNonEmptyLine(str):
    while True:
        if CheckIfEmpty(str) == False:
            return str[str.index("(") + 1:str.rindex(")")]
        else:
            str = f.readline()

def getPermutations(arr):
    from itertools import permutations
    l = list(permutations(arr))
    p = []
    for m in l:
        p.append(list(m))
    return p

def getLocations(x):
    list = []
    while x > 0:
        list.append(x)
        x = x - 1
    return list

def getPartialRankings(lst):
    ranking = []
    for item in lst:

        #If list has neither elements
        if item[0] not in ranking and item[1] not in ranking:
            ranking.append(item[0])
            ranking.append(item[1])
        else:
            #If second choice is not in list
            if item[1] not in ranking and item[0] in ranking:
                ranking.insert(ranking.index(item[0])+1, item[1])

            #If first choice is not in list
            elif item[0] not in ranking and item[1] in ranking:
                ranking.insert(ranking.index(item[1]), item[0])

            #If both in list
            else:
                ranking.remove(item[1])
                ranking.insert(ranking.index(item[0]) + 1, item[1])
    return ranking

filename = sys.argv[1]

f = open(filename, "r")

people = f.readline()
people = int(GetNonEmptyLine(people))

locations = f.readline()
locations = int(GetNonEmptyLine(locations))

preferences = f.readline()
preferences = int(GetNonEmptyLine(preferences))

# Now for the preferences
i = 1
order = []
prev = 0
j = i
violations = 0
allPrefs = []

# Get all the locations preferred by each person
while i <= preferences:
    temp = f.readline()
    temp = GetNonEmptyLine(temp)
    temp = temp.split(",")
    temp = list(map(int,temp))
    allPrefs.append(temp)
    i = i + 1

# Loop through the list to compare the second and third values of each list
# Compare the first value to know if it is the same person
# Save the previous third value to compare to next second value
places = getLocations(locations)
options = getPermutations(places)
bestCombo = []
allViolations = []
top = 0

#Get the rankings by each person
allPartialRankings = []
prevPerson = 0
temp = []
for pref in allPrefs:
    if prevPerson == 0:
        prevPerson = pref[0]
    if prevPerson != pref[0]:
        allPartialRankings.append(temp)
        prevPerson = pref[0]
        temp = []
    temp.append([pref[1],pref[2]])
allPartialRankings.append(temp)
print(allPartialRankings)

#Get the 'offical' ranking by each person
officialRankings = []
for x in allPartialRankings:
    officialRankings.append(getPartialRankings(x))
print(officialRankings)

#Count violations for each combination in options
for combination in options:
    numViolations = 0
    for ranking in officialRankings:

        #Compare rankings
        for x in ranking:
            for y in ranking:
                #KEEP y IN FRONT OF x
                if ranking.index(y) <= ranking.index(x):
                    continue
                if combination.index(x) < combination.index(y):
                    numViolations = numViolations + 1

    allViolations.append(numViolations)
final = min(allViolations)

print("violations(", final, ")", sep="")
