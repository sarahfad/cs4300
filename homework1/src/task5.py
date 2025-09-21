def favorite_books():
    """Returns a list of book titles and their authors"""
    return [
        ("The Hunger Games", "Suzanne Collins"),
        ("The Summer I Turned Pretty", "Jenny Han"),
        ("Divergent", "Veronica Roth"),
        ("Percy Jackson and the Lightning Thief", "Rick Riordan"),
    ]

def first_three_books():
    """Returns the first three books in a list"""
    return favorite_books()[:3]


def student_database():
    """Returns a dictionary with student's names and id numbers"""
    return {
        "James": 1102,
        "Laura": 1103,
        "Beth": 1104,
        "Alexandar": 1105,

    }

if __name__ == "__main__":
    print(favorite_books())
    print(first_three_books())
    print(student_database())