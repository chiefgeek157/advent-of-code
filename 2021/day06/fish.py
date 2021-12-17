import colorama
from colorama import Fore
from colorama import Back
from colorama import Style

#filename = "test.txt"
filename = "input.txt"

#days = 80
days = 256

colorama.init()

# Fish can only be up to 9 days old (0-8)
ages = [0, 0, 0, 0, 0, 0, 0, 0, 0]
with open(filename, "r") as f:
    values = f.readline().strip().split(",")
    for value in values:
        age = int(value)
        ages[age] += 1

print(f"Starting ages {ages}")

for day in range(1, days + 1):
    new_ages = []
    age0 = ages[0]
    for age in range(8):
        ages[age] = ages[age + 1]
    ages[6] += age0
    ages[8] = age0
    print(f"Day {day:2} total {sum(ages)} ages {ages}")

print(f"Anser: {sum(ages)}")