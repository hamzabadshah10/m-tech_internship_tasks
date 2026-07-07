def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def main():
    number = int(input("Enter a number: "))
    if is_prime(number):
        print(f"{number} is prime.")
    else:
        print(f"{number} is not prime.")


if __name__ == "__main__":
    main()
