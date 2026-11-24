print("Program Started")

try:

    number = 10

    result = number / 0

    print(result)

except ZeroDivisionError:

    print("Cannot divide by zero.")

print("Program Finished")