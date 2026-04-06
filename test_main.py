import pytest
from main import sanitize_filename

def test_sanitize_filename():
    assert sanitize_filename("Normal Title") == "Normal Title"
    assert sanitize_filename("Title / With \\ Slashes") == "Title  With  Slashes"
    assert sanitize_filename("Title <with> : invalid * characters ?") == "Title with  invalid  characters"
    assert sanitize_filename("   Trim me   ") == "Trim me"
    assert sanitize_filename("") == "untitled"
    # Test length limit
    long_title = "a" * 100
    assert len(sanitize_filename(long_title)) == 50

def test_sanitize_filename_non_printable():
    # Test with newline and other non-printables
    assert sanitize_filename("Line 1\nLine 2") == "Line 1Line 2"
