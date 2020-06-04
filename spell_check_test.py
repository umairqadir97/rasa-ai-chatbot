from fuzzywuzzy import process
from itertools import combinations


b = 'balance'
words_of_balance = ([''.join(l) for i in range(len(b)) for l in combinations(b, i + 1)])
print(words_of_balance)
#print("Number of possible combinations of the word balance:", len(words_of_balance))

Ratios_balance = process.extract(b, words_of_balance, limit=250)
print("PERCENTAGE OF ALL POSSIBLE WORDS OF BALANCE:")
print(Ratios_balance)
# select the string with the highest matching percentage
highest_balance = process.extractOne(b, words_of_balance)
print("PERCENTAGE OF HIGHEST MATCHED FRO THE WORD BALANCE:")
print(highest_balance)
#bests_balance = process.extractBests(b, words_of_balance, limit=10)
#print(bests_balance)

lo = 'load'
words_of_load = ([''.join(l) for i in range(len(lo)) for l in combinations(lo, i + 1)])
#print(words_of_load)
#print("Number of possible combinations of the word load:", len(words_of_load))

Ratios_load = process.extract(lo, words_of_load, limit=250)
print("PERCENTAGE OF ALL POSSIBLE WORDS OF LOAD:")
print(Ratios_load)
# select the string with the highest matching percentage
highest_load = process.extractOne(lo, words_of_load)
print("PERCENTAGE OF HIGHEST MATCHED FOR THE WORD LOAD:")
print(highest_load)
#bests_load = process.extractBests(lo, words_of_load)
#print(bests_load)
