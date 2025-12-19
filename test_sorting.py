import re

# Test sorting
question_numbers = ["1.1", "1.3", "2.1", "2.2", "3.1", "3.2", "4.1", "4.2", "4.3", 
                   "4.5", "4.6", "4.7", "4.8", "4.9", "5.1", "5.2", "5.3", "5.5",
                   "6.1", "6.3", "7.1", "7.2", "8.1", "8.2", "8.4", "8.5", "8.7"]

print("Default sorting (string):")
print(sorted(question_numbers))
print()

# Custom sorting by converting to tuple of ints
def sort_key(q):
    parts = q.split('.')
    return (int(parts[0]), int(parts[1]))

print("Custom sorting (by numeric value):")
print(sorted(question_numbers, key=sort_key))
