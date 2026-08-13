import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NUMBERS_FILE_PATH = os.path.join(SCRIPT_DIR, "Even_Odd_Numbers_OOP_Practice.xlsx")
ACCIDENT_CSV_PATH = os.path.join(SCRIPT_DIR, "road_accident_data_OOP_Practice.csv")


# Part 1
class Student:
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    def result(self):
        if self.mark >= 50:
            return "Pass"
        return "Fail"


s1 = Student("Ana", 78)
s2 = Student("Ben", 42)

print(s1.name, s1.result())
print(s2.name, s2.result())


# Part 2
print("Student 1 name:", s1.name)
print("Student 1 mark:", s1.mark)
print("Student 1 result:", s1.result())


# Part 3
numbers_df = pd.read_excel(NUMBERS_FILE_PATH)

print("Data loaded from Excel file:")
print(numbers_df)


# Part 4
class NumberRecord:
    def __init__(self, number):
        self.number = number

    def is_even(self):
        return self.number % 2 == 0

    def number_type(self):
        if self.is_even():
            return "Even"
        return "Odd"

    def show(self):
        return f"{self.number} is {self.number_type()}"


# Part 5
number_objects = []
for number in numbers_df["Number"]:
    obj = NumberRecord(number)
    number_objects.append(obj)

print("Number of objects created:", len(number_objects))
if number_objects:
    print(number_objects[0].show())


# Part 6
for obj in number_objects:
    print(obj.show())


# Part 7
print("Even numbers:")
for obj in number_objects:
    if obj.is_even():
        print(obj.number)


# Part 8
accident_df = pd.read_csv(ACCIDENT_CSV_PATH)

print("Road accident data loaded:")
print(accident_df)


# Part 9
class AccidentReport:
    def __init__(self, row):
        self.road = row["road"]
        self.weather = row["weather"]
        self.speed = row["speed"]
        self.helmet = row["helmet"]
        self.signal = row["signal"]
        self.severity = row["severity"]

    def show(self):
        return f"{self.road} | {self.weather} | {self.speed} km/h | {self.severity}"

    def is_high_risk(self):
        return self.severity == "High"

    def is_fast(self):
        return self.speed > 60

    # Part 13 challenge task, sublist element 1
    def is_rainy(self):
        return self.weather == "Rainy"

    # Part 13 challenge task, sublist element 3
    def safe_summary(self):
        return self.road, self.speed, self.helmet


# Part 10
accident_objects = []
for _, row in accident_df.iterrows():
    report = AccidentReport(row)
    accident_objects.append(report)

print("Number of accident objects:", len(accident_objects))
print("First accident object:")
if accident_objects:
    print(accident_objects[0].show())

# Part 11
print("High risk reports:")

high_risk_count = 0 # for Part 13, sublist element 4
for report in accident_objects:
    if report.is_high_risk():
        print(report.show())
        high_risk_count += 1 # for Part 13, sublist element 4
"""
OUTPUT (Which accident reports are high risk?)

(venv) ➜  BIT246 git:(main) ✗ /home/mp/BIT246/venv/bin/python /home/mp/BIT246/Week_04_Lab/questions-and-challenge-tasks.py

# output for parts before 11...

High risk reports:
MG Road | Sunny | 77 km/h | High
NH 44 | Rainy | 77 km/h | High
Park Street | Sunny | 67 km/h | High
Park Street | Foggy | 44 km/h | High
Ring Road | Sunny | 35 km/h | High
Ring Road | Cloudy | 68 km/h | High
MG Road | Rainy | 85 km/h | High
Ring Road | Foggy | 70 km/h | High
Ring Road | Cloudy | 43 km/h | High
MG Road | Rainy | 64 km/h | High
"""


# Part 12
print("Fast accident reports:")

for report in accident_objects:
    if report.is_fast():
        print(report.show())
"""
OUTPUT (Which accident reports have speed greater than 60?)

(venv) ➜  BIT246 git:(main) ✗ /home/mp/BIT246/venv/bin/python /home/mp/BIT246/Week_04_Lab/questions-and-challenge-tasks.py

# output for parts before 12...

Fast accident reports:
MG Road | Sunny | 77 km/h | High
NH 44 | Rainy | 77 km/h | High
Park Street | Sunny | 67 km/h | High
Park Street | Sunny | 65 km/h | Medium
Ring Road | Sunny | 78 km/h | Medium
Ring Road | Cloudy | 68 km/h | High
Ring Road | Cloudy | 66 km/h | Medium
MG Road | Sunny | 72 km/h | Medium
MG Road | Rainy | 85 km/h | High
Ring Road | Foggy | 70 km/h | High
MG Road | Rainy | 64 km/h | High
"""

# Part 13, sublist item 1 (is_rainy method defined in class AccidentReport on line 108)
print("Rainy accident reports:")

for report in accident_objects:
    if report.is_rainy():
        print(report.show())

# Part 13, sublist item 4 (high_risk_count defined on line 130, and incremented on line 134)
print(f"Count of high-risk reports: {high_risk_count}")