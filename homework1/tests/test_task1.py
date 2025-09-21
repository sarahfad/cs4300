import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import task1

def test_greeting():
    assert task1.greeting() == "Hello, World!"