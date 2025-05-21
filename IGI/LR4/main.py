import Task1
import Task2
import Task3
import Task4
import Task5

while True:
    while True:
                try:
                    n = int(input("Enter the number of Task(1 - 5): "))
                    if n <= 0 or n > 5:
                        print("Wrong number of task.")
                        continue
                    break
                except ValueError:
                    print("Please enter a correct number.")

    if(n == 1):
        Task1.Task1_func()
    elif (n == 2):
        Task2.Task2_func()
    elif (n == 3):
        Task3.Task3_func()  
    elif (n == 4): 
        Task4.Task4_func()
    elif (n == 5):
        Task5.Task5_func()   