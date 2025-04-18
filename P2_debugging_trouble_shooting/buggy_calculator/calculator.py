"""
A simple calculator module with a bug to be fixed during debugging.
"""

def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """Divide a by b and return the result.
    
    The bug is that this function incorrectly handles division when a is negative.
    """
    # Bug: incorrect handling of negative numbers
    if b == 0:
        raise ValueError("Cannot divide by zero")
    
    # The bug is here: subtly incorrect for negative numbers
    if a < 0:
        return -(-a / b)  # This is incorrect for certain values (Removed the integer division operator // and repalced it with / to fix the bug. The original code was using integer division which is not correct for negative numbers.)
    
    return a / b  # This is the correct implementation 