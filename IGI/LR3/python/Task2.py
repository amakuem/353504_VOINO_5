import random
def user_input():
    """
    Collect numbers from the user until a number less than -100 is entered, and count how many positive numbers were entered.

    The function repeatedly prompts the user for input, increments a counter for each positive number,
    and stops when a number less than -100 is entered. Invalid inputs are handled with an error message.

    Returns:
    int: The count of positive numbers entered before a number less than -100 was entered.
    """
    count = 0
    while True:
            try:
                num = int(input("Enter a number:"))
                if num > 0:
                    count += 1
                if num < -100:
                    break
            except ValueError:
                print("Please enter a real number.")
    return count

def number_generator():
     """
    Generate random numbers between -200 and 100 until a number less than -100 is generated.

    This is a generator function that yields random integers and prints each generated number.

    Yields:
    int: A random number between -200 and 100 (inclusive).
    """
     count = 0
     while True:
        num = random.randint(-200, 100)  # Случайное число от -200 до 100
        print(f"Сгенерированное число: {num}")
        yield num

def Task2__func():
    """
    Count positive numbers entered by the user or generated randomly until a number less than -100 is encountered.

    The function prompts the user to choose between manual input (option 1) or random generation (option 2).
    It then counts positive numbers based on the chosen method and prints the result.
    """
    print("Select the initialization method:")
    print("1. User Input")
    print("2. Generating a random list")
    
    while True:
            try:
                choice = int(input("Enter 1 or 2: "))
                if choice != 1 and choice != 2:
                    print("PLease enter a correct number.")
                    continue
                
                break
            except ValueError:
                print("Please enter a real number.")
    
    if choice == 1:
        result = user_input()
        print(f"Counter of positive numbers: {result}")
    elif choice == 2:
        count = 0
        generator = number_generator()
        for num in generator:
            if num > 0:
                count += 1
            if num < -100:
                break
        print(f"Counter of positive numbers: {count}")

    