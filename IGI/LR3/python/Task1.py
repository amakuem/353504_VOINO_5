import math
import tabulate

def taylor_exp(x, eps):
    """
    Calculate the exponential function e^x using Taylor series expansion.

    Parameters:
    x (float): The value at which to evaluate the exponential function.
    eps (float): The precision of the approximation. The series continues adding terms until the absolute value of the next term is less than eps.

    Returns:
    tuple: A tuple containing the approximated value of e^x (float) and the number of terms used in the approximation (int).
    """
    sum = 0        
    term = 1       
    i = 0          
    
    while abs(term) > eps and i < 500:
        sum += term    
        i += 1         
        term = term * x / i  
    
    return sum, i 

def Task1_func():
    """Compute the exponential function using Taylor series and compare it with the math library.

    This function prompts the user to enter values for x and eps, computes the approximation using taylor_exp,
    and prints a table comparing the approximated value with the value from math.exp."""
    while True:
        try:

            x = float(input("Enter x: "))
            break
        except ValueError:
            print("Please enter the correct numbers.")
    while True:    
        try:
            eps = float(input("Enter eps: "))
            break
        except ValueError:
            print("Please enter the correct numbers.")

    computed_value, n = taylor_exp(x, eps)
    math_value = math.exp(x)  

    table_data = [
        [x, n, computed_value, math_value, eps]
    ]

    table_headers = ["x", "n", "F(x)", "Math F(x)", "eps"]

    table = tabulate.tabulate(table_data, headers=table_headers, floatfmt=".8f")
    print(table)