# shbang
# Judah Tanninen
# test suite for libby
# 03/24/23

import lib as libby
import pytest

# Test 1, test valid types, black box
def test_valid_type():
    search = '1234' # Must be 3 characters, will test later
    types = ["author", "title"]
    for type in types:
        assert(libby.handleValidation(type, search) == True)

# Test 2, invalid types (anything that is not "author" or "title"), black box
def test_invalid_type():
    search = '1234' # Must be 3 characters, will test later
    invalid = "randomstringgarble"
    assert(libby.handleValidation(invalid, search) != True)

# Test 3, verify search length must be over 2, black box
def test_search_length():
    search1 = "the way of kings" # Good book, over 2 characters
    assert(libby.handleValidation("title", search1) == True)
    search2 = "12" # Not real. not enough characters
    assert(libby.handleValidation("title", search2) != True)

# Test 4, tests title searching, black box
def test_title_search():
    type = "title"
    search = "the way of kings" # Search should be case sensitive
    res = libby.basicSearch(type, search) # Get results
    assert len(res) > 0 # Should be more than zero results
    # Check the first result
    first = res[0]
    assert "kings" in first['title'].lower()

# Test 5, tests author searching, black box
def test_author_search():
    type = "author"
    search = "brandon sanderson"
    res = libby.basicSearch(type, search)
    assert len(res) > 0 # Should be more than zero results
    # Check the first result
    first = res[0]
    assert "brandon" in first['author'].lower()

# Test 6, tests that result from search is at most 10, black box
def test_search_results_length():
    type = "author"
    search = "brandon sanderson" # Search should be case sensitive
    res = libby.basicSearch(type, search)
    assert len(res) <= 10

# Test 7, tests the resolve download link function, integration
def test_link_getter():
    # Get some books
    res = libby.basicSearch("title", "the way of kings")
    # Get the first element
    first = res[0]
    # Hand the element to the get links function and verify it returns a dict with keys
    res2 = libby.getLinksFor(first)
    resultLen = len(res2)
    assert resultLen > 0

# Test 8, tests the map function, black box
def test_map_function():
    badKeyNames = ['ID', 'Author', 'Title', 'Year', 'Size', 'Extension', 'Mirror_1']
    goodKeyNames = ['id', 'author', 'title', 'year', 'size', 'ext', 'Mirror_1']
    bigd = {}
    for key in badKeyNames:
        bigd[key] = "test"
    newd = libby.clearUneeded(bigd)
    for key in newd:
        assert key in goodKeyNames
        assert newd[key] == "test"

# Test 9, tests the format results function, integration
def test_format_results():
    # Get some books
    res = libby.basicSearch("title", "the way of kings")
    formatted = libby.formatResults(res)
    first = formatted[0]
    assert isinstance(first, str), 'Element should be a string'

# Test 10, tests the format links function, integration
def test_format_links():
    # Get some books
    res = libby.basicSearch("title", "the way of kings")
    # Get the first element
    first = res[0]
    res2 = libby.getLinksFor(first)
    formatted = libby.formatLinks(res2)
    assert len(formatted) > 0
    assert isinstance(formatted[0], str)

# Test 11, tests basic search does not fail when no results occur, black box
def test_no_results():
    type = "title"
    search = "asdfoaofwhfohasdkzmxcvoiadfasf34gsdf"
    res = libby.basicSearch(type, search)
    assert len(res) == 0

# Test 12, testing all functionalities of handle validation, white box
# Below is the code for the function
# def handleValidation(type: str, search: str):
#     valid_types = ["author", "title"]
#     in_string = type.lower()
#     if in_string not in valid_types:
#         print('Bad Type')
#         type_str = ', '.join(valid_types)
#         return "Invalid type, must be one of the following: " + type_str
#     if (len(search) < 3):
#         return "Search string must be at least 3 characters long"
#     return True

def test_all_validation():
    # Test valid types
    validTypes = ["author", "title", "AUTHOR", "TiTLe"]
    for type in validTypes:
        assert libby.handleValidation(type, "test") == True
    invalidTypes = ["bad", "invalid"]
    for type in invalidTypes:
        res = libby.handleValidation(type, "test")
        assert "invalid type" in res.lower()
    validLengths = [3, 5, 20]
    for length in validLengths:
        search = "a" * length
        res = libby.handleValidation("title", search)
        assert res == True
    invalidLengths = [0, 1, 2]
    for length in invalidLengths:
        search = "a" * length
        res = libby.handleValidation("title", search)
        assert "at least" in res.lower()