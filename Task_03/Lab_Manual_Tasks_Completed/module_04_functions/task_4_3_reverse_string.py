def reverse_string(text: str) -> str:
    result = ""
    for char in text:
        result = char + result
    return result


def main():
    text = input("Enter a string: ")
    print("Reversed string:", reverse_string(text))


if __name__ == "__main__":
    main()
