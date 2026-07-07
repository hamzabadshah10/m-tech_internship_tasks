from collections import Counter


def main():
    text = "I love Python because Python is easy"
    words = text.lower().split()
    freq = Counter(words)
    print(freq)


if __name__ == "__main__":
    main()
