#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script demonstrates different ways to create lists with numbers in Python.
"""

def create_basic_number_list():
    """Create a basic list with numbers."""
    # Method 1: Direct list creation
    numbers = [1, 2, 3, 4, 5]
    print("Basic list:", numbers)
    
    # Method 2: Using list() constructor
    numbers_list = list([1, 2, 3, 4, 5])
    print("Using list() constructor:", numbers_list)
    
    return numbers

def create_range_list():
    """Create a list using range()."""
    # Create a list from 0 to 9
    range_list = list(range(10))
    print("List from range(10):", range_list)
    
    # Create a list from 1 to 10
    range_list_1_to_10 = list(range(1, 11))
    print("List from range(1, 11):", range_list_1_to_10)
    
    # Create a list with step (even numbers from 0 to 20)
    even_numbers = list(range(0, 21, 2))
    print("Even numbers from 0 to 20:", even_numbers)
    
    return range_list

def create_list_comprehension():
    """Create lists using list comprehension."""
    # Create a list of squares from 0 to 9
    squares = [x**2 for x in range(10)]
    print("Squares of numbers 0-9:", squares)
    
    # Create a list of even numbers from 0 to 20
    even_nums = [x for x in range(21) if x % 2 == 0]
    print("Even numbers from 0 to 20:", even_nums)
    
    # Create a list of numbers divisible by 3 or 5 from 1 to 30
    divisible_by_3_or_5 = [x for x in range(1, 31) if x % 3 == 0 or x % 5 == 0]
    print("Numbers divisible by 3 or 5 from 1 to 30:", divisible_by_3_or_5)
    
    return squares

def create_random_number_list():
    """Create a list with random numbers."""
    import random
    
    # Create a list of 10 random integers between 1 and 100
    random_ints = [random.randint(1, 100) for _ in range(10)]
    print("10 random integers between 1 and 100:", random_ints)
    
    # Create a list of 5 random floats between 0 and 1
    random_floats = [random.random() for _ in range(5)]
    print("5 random floats between 0 and 1:", random_floats)
    
    # Create a list of 5 random floats between 10 and 20
    random_floats_range = [random.uniform(10, 20) for _ in range(5)]
    print("5 random floats between 10 and 20:", random_floats_range)
    
    return random_ints

def create_arithmetic_sequence():
    """Create arithmetic sequences."""
    # Create a list with arithmetic sequence: start=1, step=2, length=10
    arithmetic_seq = [1 + i*2 for i in range(10)]
    print("Arithmetic sequence (start=1, step=2):", arithmetic_seq)
    
    # Create a list with arithmetic sequence: start=5, step=3, length=8
    arithmetic_seq2 = [5 + i*3 for i in range(8)]
    print("Arithmetic sequence (start=5, step=3):", arithmetic_seq2)
    
    return arithmetic_seq

def create_geometric_sequence():
    """Create geometric sequences."""
    # Create a list with geometric sequence: start=1, ratio=2, length=8
    geometric_seq = [1 * (2**i) for i in range(8)]
    print("Geometric sequence (start=1, ratio=2):", geometric_seq)
    
    # Create a list with geometric sequence: start=3, ratio=1.5, length=6
    geometric_seq2 = [3 * (1.5**i) for i in range(6)]
    print("Geometric sequence (start=3, ratio=1.5):", geometric_seq2)
    
    return geometric_seq

def main():
    """Main function to demonstrate all list creation methods."""
    print("=== Creating Lists with Numbers in Python ===\n")
    
    print("1. Basic Number Lists:")
    create_basic_number_list()
    print()
    
    print("2. Lists Using range():")
    create_range_list()
    print()
    
    print("3. Lists Using List Comprehension:")
    create_list_comprehension()
    print()
    
    print("4. Lists with Random Numbers:")
    create_random_number_list()
    print()
    
    print("5. Arithmetic Sequences:")
    create_arithmetic_sequence()
    print()
    
    print("6. Geometric Sequences:")
    create_geometric_sequence()
    print()
    
    print("=== End of Demonstration ===")

if __name__ == "__main__":
    main() 