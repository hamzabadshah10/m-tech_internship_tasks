def main():
    total = 0
    while True:
        number = int(input("Enter a number (0 to stop): "))
        if number == 0:
            break
        total += number
    print("Sum of all numbers entered:", total)


if __name__ == "__main__":
    main()
