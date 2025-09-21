def count_words(filename):
    """Opens a file and counts how many words are in the file"""
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    return len(text.split())

if __name__ == "__main__":
    print(count_words("src/task6_read_me.txt"))