def logging_decorator(func):
    """
    A decorator that logs when the decorated function is called.

    Parameters:
    func (function): The function to be decorated.

    Returns:
    function: The wrapped function that includes logging before execution.
    """
    def wrapper(*args, **kwargs):
        print(f"Log: Function called {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

@logging_decorator
def count_lowercase_words():
    """
    Count how many words in a user-input string start with a lowercase letter.

    The function prompts the user to enter a string, splits it into words, and counts how many words
    start with a lowercase letter. It also logs the input string and the count via the logging_decorator.
    """
    s = input("Enter string: ")
    words = s.split()
    count = 0
    for word in words:
        if word and word[0].islower():
            count += 1
   # print("The number of words starting with a lowercase letter:", count)
    #print(f"Log: Line entered '{s}', found {count} words with a lowercase letter")
    return  (s, count)



def Task3_func():   
    count_lowercase_words()