import pytest
import task5
from task5 import favorite_books, first_three_books, student_database

# favorite books tests

def test_favorite_books_is_list_of_tuples():
    books = favorite_books()
    assert isinstance(books, list)
    assert all(isinstance(b, tuple) and len(b) == 2 for b in books)

def test_favorite_books_contents():
    books = favorite_books()
    expected = [
        ("The Hunger Games", "Suzanne Collins"),
        ("The Summer I Turned Pretty", "Jenny Han"),
        ("Divergent", "Veronica Roth"),
        ("Percy Jackson and the Lightning Thief", "Rick Riordan"),
    ]
    assert books == expected

def test_first_three_books_slicing():
    assert first_three_books() == favorite_books()[:3]
    assert len(first_three_books()) == 3

@pytest.mark.parametrize("title, author", [
    ("The Hunger Games", "Suzanne Collins"),
    ("The Summer I Turned Pretty", "Jenny Han"),
    ("Divergent", "Veronica Roth"),
])
def test_specific_books_in_first_three(title, author):
    assert (title, author) in first_three_books()

# student database tests

def test_student_database_structure():
    db = student_database()
    assert isinstance(db, dict)
    assert all(isinstance(k, str) for k in db.keys())
    assert all(isinstance(v, int) for v in db.values())

def test_student_database_known_entries():
    db = student_database()
    assert db["James"] == 1102
    assert db["Laura"] == 1103
    assert db["Beth"] == 1104
    assert db["Alexandar"] == 1105

@pytest.mark.parametrize("name", ["James", "Laura", "Beth", "Alexandar"])
def test_student_database_contains_names(name):
    db = student_database()
    assert name in db

@pytest.mark.parametrize("bad_name", ["Zoe", "Sam", ""])
def test_student_database_missing_names(bad_name):
    db = student_database()
    assert bad_name not in db
