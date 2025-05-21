def user_input_list():
    """ Requests the list items from the user to verify the correctness of the input."""
    while True:
        try:
            n = int(input("Enter the number of items in the list: "))
            if n <= 0:
                print("The number of elements must be a positive number.")
                continue
            break
        except ValueError:
            print("Please enter an integer.")
    
    lst = []
    for i in range(n):
        while True:
            try:
                elem = float(input(f"Enter the element {i+1}: "))
                lst.append(elem)
                break
            except ValueError:
                print("Please enter a real number.")
    return lst

def generate_list(n, min_val, max_val):
    """Generates n random real numbers in the range [min_val, max_val]."""
    import random
    for _ in range(n):
        yield random.uniform(min_val, max_val)


def Task5_func():
    """The main function of the program is to process the list and complete the task."""
    print("Select the initialization method for the list:")
    print("1. User Input")
    print("2. Generating a random list")
    choice = input("Enter 1 or 2: ")
    
    if choice == '1':
        lst = user_input_list()
    elif choice == '2':
        while True:
            try:
                n = int(input("Enter the number of items in the list:"))
                min_val = float(input("Enter the minimum value: "))
                max_val = float(input("Enter the maximum value: "))
                if n <= 0:
                    print("The number of elements must be a positive number.")
                    continue
                if min_val >= max_val:
                    print("The minimum value must be less than the maximum.")
                    continue
                break
            except ValueError:
                print("Please enter the correct numbers.")
        lst = list(generate_list(n, min_val, max_val))
    else:
        print("Wrong choice. The program is completed.")
        return
    
    # Вывод списка на экран
    print("List:", lst)
    
    # Нахождение максимального по модулю элемента
    max_abs_elem = max(lst, key=abs)
    print("The maximum modulo element:", max_abs_elem)
    
    # Нахождение суммы элементов между первым и вторым положительными элементами
    positive_indices = []
    for i in range(len(lst)):
        if lst[i] > 0:
            positive_indices.append(i)
    
    if len(positive_indices) >= 2:
        first_pos = positive_indices[0]
        second_pos = positive_indices[1]
        if second_pos > first_pos + 1:
            sum_between = sum(lst[first_pos + 1:second_pos])
            print("The sum of the elements between the first and second positive elements:", sum_between)
        else:
            print("There are no elements between the first and second positive elements.")
    else:
        print("There are fewer than two positive elements in the list.")
