"""
Task 4 – Text-based Arithmetic Analyzer
--------------------------------------
Create a text-based analyzer that:
1. Counts non-space characters.
2. Counts words.
3. Extracts numbers and computes their sum and average.
Use helper functions:
- count_characters(text)
- count_words(text)
- extract_numbers(text)
- analyze_text(text)
Print formatted summary in main.
"""


def count_characters(text):
    """Count non-space characters in a string."""
    # TODO: implement
    count = 0
    for char in text:
        if char != " ":
            count += 1
    return count


def count_words(text):
    """Count number of words in a string."""
    # TODO: implement
    words = text.split()
    return len(words)


def extract_numbers(text):
    """Return list of integers found in text."""
    # TODO: implement
    numbers = []
    words = text.split()
    for word in words:
        if word.isdigit():
            numbers.append(int(word))
    return numbers


def analyze_text(text):
    """Perform text-based arithmetic analysis."""
    # TODO: call helper functions and compute total, average, etc.
    char_count = count_characters(text)
    word_count = count_words(text)
    numbers = extract_numbers(text)

    total = sum(numbers)
    average = total / len(numbers) if numbers else 0

    return {
        "char_count": char_count,
        "word_count": word_count,
        "numbers": numbers,
        "total": total,
        "average": average,
    }


if __name__ == "__main__":
    # TODO: read input, call analyze_text(), and print results
    text = input("Enter a text with some numbers: ")
    results = analyze_text(text)

    print(f"\nText Analysis Summary:")
    print(f"Non-space characters: {results['char_count']}")
    print(f"Word count: {results['word_count']}")
    print(f"Numbers found: {results['numbers']}")
    print(f"Sum of numbers: {results['total']}")
    print(f"Average of numbers: {results['average']:.2f}")
