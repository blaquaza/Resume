   # Importing the math module

import math

# Prompt the user to input 10 floats

print("Please enter 10 numbers (floats or integers):")
numbers = [float(input(f"Number {i+1}: ")) for i in range(10)]

# Calculate the total of all numbers

total = sum(numbers)
print(f"\nTotal of all numbers: {total}")

# Find the index of the maximum number

max_index = numbers.index(max(numbers))
print(f"Index of the maximum number: {max_index}")

# Find the index of the minimum number

min_index = numbers.index(min(numbers))
print(f"Index of the minimum number: {min_index}")

# Calculate the average of the numbers and round to 2 decimal places

average = round(total / len(numbers), 2)
print(f"Average of the numbers: {average}")

# Calculate the median

sorted_numbers = sorted(numbers)
if len(sorted_numbers) % 2 == 0:
    median = (sorted_numbers[len(sorted_numbers)//2 - 1] + sorted_numbers[len(sorted_numbers)//2]) / 2
else:
    median = sorted_numbers[len(sorted_numbers)//2]
print(f"Median of the numbers: {median}")