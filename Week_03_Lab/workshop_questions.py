# Workshop Questions
""""
1. Identify and explain the error in the code. Fix the error.
    fruits = ["apple", "banana", "cherry"]
    print(fruit[1])

2. The following code is meant to print even numbers, but it's not working. Identify and
explain the error in the code. Fix the error.
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    for num in numbers
    if num % 2 = 0:
    print(num)

3. Given a string, count how many vowels and consonants it contains using a for loop.
Explain how you would handle punctuation and spaces?

4. Here is a program on a two-dimensional array
    
    # Define a two-dimensional array (5x3)
    matrix = [
    [5, 8, 2],
    [3, 9, 1],
    [7, 6, 4],
    [2, 4, 9],
    [1, 5, 6]
    ]

    values = []
    
    # Iterate over each column
    for col in range(len(matrix[0])):
        val = matrix[0][col]
    
        for row in range(1, len(matrix)):
            # Update max_val if the current element is greater
            if matrix[row][col] > val:
                val = matrix[row][col]

        values.append(val)
    
    for i, val in enumerate(values):
        print(f"Column {i+1}: {val}")

    a. Predict without executing the code, what will be the output of the above code?
    b. Briefly explain how you would modify the code to find the minimum value of each row.
    Modify the code.
    c. Can you modify the code to handle a matrix of any size (m x n), where m and n are user
    inputs? (Hint: Use nested loops with input() to get the dimensions of the matrix
    dynamically)

5. Create a Python script to:
    a. Ask the user for their name and age
    b. Store it in a file called user_data.txt
    c. Append if file already exists

6. Write a program that reads a file data.txt and prints only lines that contain the word
"Python".

7. Create a script that opens an image file in binary mode, copies it to another file, and
verifies that the two files are the same size using os.path.getsize()
"""
# Q1)
fruits = ["apple", "banana", "cherry"]
print(fruits[1])

# Q2)
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
for num in numbers:
    if num % 2 == 0:
        print(num)

# Q3)
# Returns vowel and consonants counts as a tuple, e.g. (vowels_count, consonant_count)
def count_vowels_and_consonants(str):
    lowercase_string = str.lower()

    vowels_count = 0
    consonant_count = 0

    vowels = {'a', 'e', 'i', 'o', 'u'}

    for char in lowercase_string:
        if char.isalpha():
            if char in vowels:
                vowels_count += 1
            else:
                consonant_count += 1

    return vowels_count, consonant_count

# Q4)
# a) (explain given code with comments, what will be output?)
matrix = [
[5, 8, 2],
[3, 9, 1],
[7, 6, 4],
[2, 4, 9],
[1, 5, 6]
]

values = []
# for [new variable col] in range(length of "matrix[0]"). matrix[0] == [5, 8, 2], so len(matrix[0]) == 3
# eqivalent in this case to "for col in range(3):". for loop runs for 3 iterations
for col in range(len(matrix[0])):
    # first iteration assigns matrix[0][0] to the variable val. second iteration matrix[0][1], third iteration matrix[0][2]
    val = matrix[0][col]

    # iterates through the rows in the inner loop
    for row in range(1, len(matrix)):
        # checks if new value is greater than val
        if matrix[row][col] > val:
            # replaces val if greater
            val = matrix[row][col]

    # writes greatest value of row to the list values
    values.append(val)

    # prints the list values
for i, val in enumerate(values):
    print(f"Column {i+1}: {val}")

# therefore, the output will be the maximum value from each column in a list of length col

# b)
# to find minimum values instead, change this line:
# if matrix[row][col] > val:
# to:
# if matrix[row][col] < val:

# or, rewrite the function more pythonically:
matrix = [
[5, 8, 2],
[3, 9, 1],
[7, 6, 4],
[2, 4, 9],
[1, 5, 6]
]

def max_and_min_of_cols_in_matrix(matrix):
    maximums = []
    minimums = []

    for col in zip(*matrix):
        maximums.append(max(col))
        minimums.append(min(col))

    return maximums, minimums

print(max_and_min_of_cols_in_matrix(matrix))

# c) max_and_min_of_cols_in_matrix(matrix) already handles arbitrary sizes of matrix

# Q5)
from pathlib import Path
script_dir = Path(__file__).resolve().parent


def store_name_and_age_in_text_file():
    file_path = script_dir / "user_data.txt"

    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    
    with open(file_path, "a") as file:
        file.write(f"Name: {name}\nAge: {age}\n\n")

store_name_and_age_in_text_file()

# Q6)
def print_python_lines():
    file_path = script_dir / "data.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if "Python" in line:
                    print(line, end="")
    except FileNotFoundError:
        print(f"Error: {file_path.name} was not found in {script_dir}")

print_python_lines()

# Q7)
import os
from pathlib import Path

script_dir = Path(__file__).resolve().parent

file_path = script_dir / "example.jpg"
output_path = script_dir / "output.jpg"
with open(file_path, "rb") as file:
    binary_data = file.read()

with open(output_path, "wb") as file:
    file.write(binary_data)

original_size = os.path.getsize(file_path)
output_size = os.path.getsize(output_path)

if original_size == output_size:
    print(f"Both files are {original_size} bytes.")
else:
    raise ValueError(f"Original is {original_size} bytes, output is {output_size} bytes.")