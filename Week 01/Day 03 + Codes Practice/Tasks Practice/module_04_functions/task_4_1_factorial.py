def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def main():
    number = int(input("Enter a number: "))
    print(f"Factorial of {number} is {factorial(number)}")


if __name__ == "__main__":
    main()
