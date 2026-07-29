import pandas as pd
print("Pandas is ready.")

data = pd.read_excel("Week_02_Lab/Even_Odd_Numbers.xlsx", sheet_name="Numbers")

def isEven(input_num):
    return input_num % 2 == 0

evens = set()
odds = set()

for number in data["Number"]:
    if pd.notna(number):
        if isEven(number):
            evens.add(number)
            print(f"{number} is even.")
        else:
            odds.add(number)
            print(f"{number} is odd.")

print("The largest even number is", max(evens))
print("The smallest odd number is", min(odds))